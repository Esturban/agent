# tools.py - Simple tool to parse free-for-dev list

import json
import re
import requests
from langchain.tools import tool
from .models import FreeTool, ParsedContent

def create_tools():
    """Create simple tools for parsing free dev tools"""

    @tool("parse_free_dev_list")
    def parse_free_dev_list(url: str) -> str:
        """
        Simple parser for the free-for-dev list. Just extracts tools and categories.
        Returns clean JSON with tools organized by category.
        """
        response = requests.get(url)
        response.raise_for_status()
        content = response.text

        # Find all sections (lines starting with ##)
        sections = re.findall(r'##\s*(.*?)\s*\n(.*?)(?=\n##|$)', content, re.DOTALL)

        tools_by_category = {}
        all_categories = []

        for section_title, section_content in sections:
            section_title = section_title.strip()
            if section_title and not section_title.startswith('Table of Contents'):
                all_categories.append(section_title)
                tools_by_category[section_title] = []

                # Find tools in this section (lines like "* [Tool Name](url) - description")
                tool_lines = re.findall(r'[\*\-]\s*\[([^\]]+)\]\(([^)]+)\)\s*-\s*(.*?)(?=\n|$)', section_content)

                for tool_name, url, description in tool_lines:
                    # Clean up the description
                    description = re.sub(r'\s+', ' ', description.strip())

                    tools_by_category[section_title].append({
                        "name": tool_name.strip(),
                        "description": description,
                        "category": section_title,
                        "url": url.strip() if url else None
                    })

        # Convert to our model format
        all_tools = []
        for category_tools in tools_by_category.values():
            for tool in category_tools:
                all_tools.append(FreeTool(
                    name=tool["name"],
                    category=tool["category"],
                    description=tool["description"],
                    url=tool.get("url"),
                    free_tier="Free tier available"
                ))

        parsed_content = ParsedContent(
            tools=all_tools,
            categories=all_categories,
            summary=f"Found {len(all_tools)} free tools in {len(all_categories)} categories"
        )

        return json.dumps(parsed_content.dict(), indent=2)

    return [parse_free_dev_list]
