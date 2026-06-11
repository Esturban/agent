#!/usr/bin/env python3
# main.py - CLI entry point for the idea generation agent

import argparse
import json
import os
from datetime import datetime

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Import from local modules
from src.models import AgentState
from src.tools import create_tools
from src.workflow import create_workflow

load_dotenv()


def idea_generation_agent():
    """Main function to run the idea generation agent"""

    # Set up API keys
    brave_key = os.getenv("BRAVE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not brave_key or not openai_key:
        raise ValueError("Missing required API keys: BRAVE_API_KEY and OPENAI_API_KEY")

    # Set up LLMs
    parser_llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY", openai_key),
        model="meta-llama/llama-3.1-8b-instruct:free",
        temperature=0,
    )
    idea_llm = ChatOpenAI(model="gpt-5-mini")

    # Create tools and workflow
    tools = create_tools()
    graph = create_workflow(parser_llm, idea_llm, tools)

    # Initialize state
    initial_state = AgentState(parsed_content=None, ideas=None)

    # Run the workflow
    print("🚀 Starting idea generation agent...")
    print("📋 Will parse free-for-dev list and generate high-value, low-effort agentic solutions")

    try:
        result = graph.invoke(initial_state)

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return

        ideas = result.get("ideas", [])
        parsed_content = result.get("parsed_content")

        if not ideas:
            print("❌ No ideas generated")
            return

        print(f"\n🎉 Generated {len(ideas)} simple product ideas!\n")

        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/ideas/free_dev_ideas_{timestamp}.json"

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Format ideas for output with parsed tools included
        output_data = {
            "timestamp": timestamp,
            "total_ideas": len(ideas),
            "parsed_tools_summary": parsed_content.summary
            if parsed_content
            else "No summary available",
            "available_tools_count": len(parsed_content.tools) if parsed_content else 0,
            "available_categories": parsed_content.categories if parsed_content else [],
            "sample_tools": [
                {"name": tool.name, "category": tool.category, "description": tool.description}
                for tool in (
                    parsed_content.tools[:10] if parsed_content else []
                )  # Include first 10 tools as sample
            ],
            "ideas": [
                {
                    "title": idea.idea_concept.title,
                    "description": idea.idea_concept.description,
                    "target_tools": idea.idea_concept.target_tools,
                    "value_proposition": idea.idea_concept.value_proposition,
                    "effort_level": idea.idea_concept.effort_level,
                    "implementation_complexity": idea.idea_concept.implementation_complexity,
                    "confidence": idea.confidence,
                    "reasoning": idea.reasoning,
                    "next_steps": idea.next_steps,
                }
                for idea in ideas
            ],
        }

        # Save to file
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=2)

        # print(f"💾 Ideas saved to: {output_file}")

        # Display ideas
        # for i, idea in enumerate(ideas, 1):
        #     print(f"\n{i}. {idea.idea_concept.title}")
        #     print(f"   Description: {idea.idea_concept.description}")
        #     print(f"   Tools: {', '.join(idea.idea_concept.target_tools)}")
        #     print(f"   Value: {idea.idea_concept.value_proposition}")
        #     print(f"   Effort: {idea.idea_concept.effort_level} | Complexity: {idea.idea_concept.implementation_complexity}")
        #     print(f"   Confidence: {idea.confidence:.2f}")
        #     print(f"   Next steps: {', '.join(idea.next_steps)}")

        print("✅ Simple idea generation completed!")
        print(f"📊 Total: {len(ideas)} ideas generated")
        return output_file
    except Exception as e:
        print(f"❌ Error running agent: {str(e)}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Idea Generation Agent CLI")
    parser.add_argument(
        "--output", "-o", default="data/ideas/free_dev_ideas", help="Output file prefix"
    )
    args = parser.parse_args()

    result_file = idea_generation_agent()
    if result_file:
        print(f"\n📄 Results saved to: {result_file}")
