import operator
from typing import Annotated, TypedDict

from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """Search the web for factual information."""
    results = {
        "python release year": "Python was first released in 1991 by Guido van Rossum.",
        "eiffel tower height": "The Eiffel Tower is 330 meters tall.",
        "largest planet": "Jupiter is the largest planet in our solar system.",
    }
    for key, val in results.items():
        if key in query.lower():
            return val
    return f"Search result for: {query} — Found relevant information."


@tool
def calculate(expression: str) -> str:
    """Evaluate a simple mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"


@tool
def lookup_fact(topic: str) -> str:
    """Look up a specific fact from a knowledge base."""
    facts = {
        "python": "Python is a high-level, general-purpose programming language.",
        "langgraph": "LangGraph is a library for building stateful multi-actor LLM applications.",
        "openai": "OpenAI was founded in 2015 and created GPT-4 and ChatGPT.",
    }
    return facts.get(topic.lower(), f"No fact found for: {topic}")


AGENT_TASKS = [
    {
        "input": "Search for Python's release year and calculate 2024 minus that year.",
        "expected_tools": ["search_web", "calculate"],
    },
    {
        "input": "Look up a fact about LangGraph.",
        "expected_tools": ["lookup_fact"],
    },
    {
        "input": "What is the height of the Eiffel Tower? Search for it.",
        "expected_tools": ["search_web"],
    },
]

TOOLS = [search_web, calculate, lookup_fact]


class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    tool_calls_made: list[str]
