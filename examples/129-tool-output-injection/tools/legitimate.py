"""
Legitimate tool implementations — clean, no injected content.

These represent what the tools would look like in a production deployment.
Each tool returns typed, structured output. No hidden fields, no instructions.
"""

from langchain_core.tools import tool
import json


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression and return the numeric result."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return json.dumps({"result": result, "expression": expression})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def web_search(query: str) -> str:
    """Search the web and return a list of results with title, url, and snippet."""
    return json.dumps({
        "results": [
            {"title": "LangGraph documentation", "url": "https://example.com/lg", "snippet": "LangGraph is a library for building stateful multi-actor LLM applications."},
            {"title": "LangChain overview", "url": "https://example.com/lc", "snippet": "LangChain provides tools, agents, and chains for LLM applications."},
            {"title": "OpenAI API", "url": "https://example.com/oai", "snippet": "The OpenAI API provides access to GPT-4o and other models."},
        ]
    })


@tool
def weather_api(city: str) -> str:
    """Get current weather for a city. Returns temperature, condition, and advisory."""
    return json.dumps({
        "city": city,
        "temperature": "22°C",
        "condition": "Partly cloudy",
        "humidity": "65%",
        "advisory": "No significant weather alerts.",
    })


@tool
def memory_read(key: str) -> str:
    """Read a stored value from memory by key."""
    store = {
        "user_preference": "dark mode enabled",
        "last_query": "What is LangGraph?",
        "session_id": "abc-123",
    }
    value = store.get(key, f"No value found for key '{key}'")
    return json.dumps({"key": key, "value": value})
