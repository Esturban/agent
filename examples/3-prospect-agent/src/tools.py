# tools.py - Tool definitions and setup

import json
from langchain.tools import tool
from langchain_community.tools import BraveSearch
from langgraph.prebuilt import ToolNode

def create_tools(brave_key: str):
    @tool("web_search_tool")
    def search_tool(query):
        """
        Search the web for the most relevant information about the query.
        """
        search = BraveSearch.from_api_key(api_key=brave_key, search_kwargs={"count": 3})
        raw = search.run(query)
        if isinstance(raw, str):
            return raw
        if isinstance(raw, dict):
            results = raw.get("results") or raw.get("organic") or []
        elif isinstance(raw, list):
            results = raw
        else:
            results = []
        lines = []
        for r in results[:3]:
            title = r.get("title") or r.get("name") or r.get("headline") if isinstance(r, dict) else str(r)
            snippet = r.get("snippet") or r.get("snippet_text") or r.get("description") if isinstance(r, dict) else ""
            lines.append(f"- {title}: {snippet}" if snippet else f"- {title}")
        return "\n".join(lines) if lines else json.dumps(raw)

    tools = [search_tool]
    tool_node = ToolNode(tools=tools)
    return tools, tool_node
