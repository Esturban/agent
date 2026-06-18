# Agno reads function signatures + docstrings to build tool schemas — no decorators needed.
# This is the same pattern as Google ADK: clean Python, no framework boilerplate.

_knowledge: dict[str, str] = {
    "python":    "Python is a high-level, dynamically typed language emphasising readability.",
    "agno":      "Agno is a lightweight, high-performance agent framework with minimal boilerplate.",
    "langgraph": "LangGraph builds stateful agents as explicit graphs with TypedDict state.",
    "fastapi":   "FastAPI is a modern, async Python web framework with automatic OpenAPI docs.",
}

SAMPLE_TASKS = [
    "What do you know about Python and agno?",
    "Add a new entry: 'redis' is an in-memory data structure store used as a cache and message broker.",
    "List all the topics you currently know about.",
    "What is the difference between agno and LangGraph?",
]


def search_knowledge(topic: str) -> str:
    """Search the knowledge base for information about a technology topic.

    Args:
        topic: The topic name to look up.

    Returns:
        Description string or a not-found message.
    """
    key = topic.lower().strip()
    if key in _knowledge:
        return _knowledge[key]
    # Fuzzy: check substring
    for k, v in _knowledge.items():
        if key in k or k in key:
            return v
    return f"No entry for '{topic}'. Known topics: {', '.join(_knowledge)}"


def add_knowledge(topic: str, description: str) -> str:
    """Add a new entry to the knowledge base.

    Args:
        topic: The topic name (key).
        description: The description to store.

    Returns:
        Confirmation message.
    """
    _knowledge[topic.lower().strip()] = description
    return f"Added '{topic}' to knowledge base."


def list_topics() -> str:
    """List all topics currently in the knowledge base.

    Returns:
        Comma-separated list of topic names.
    """
    return ", ".join(_knowledge.keys())
