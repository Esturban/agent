# ADK reads plain Python docstrings for tool schema — no decorators needed.
# The function signature + docstring is enough for ADK to generate the JSON schema.

KNOWLEDGE_BASE: dict[str, str] = {
    "python":    "Python is a high-level, dynamically typed programming language emphasising readability.",
    "langgraph": "LangGraph builds stateful, graph-based agents with TypedDict state and explicit nodes/edges.",
    "google-adk": "Google ADK (Agent Development Kit) is a framework for building Gemini-powered agents. Tools are plain Python functions; ADK generates the schema from docstrings automatically.",
    "langchain": "LangChain provides chains, memory, and tool abstractions that compose into LLM pipelines.",
    "chromadb":  "ChromaDB is an open-source embedding database for vector similarity search.",
}

SAMPLE_QUERIES = [
    "What is Google ADK and how does it compare to LangGraph?",
    "Explain what LangGraph is in simple terms.",
    "What topics are in your knowledge base?",
]


def search_knowledge(topic: str) -> str:
    """Search the knowledge base for information about a technology topic.

    Args:
        topic: The technology name to look up (e.g. 'python', 'langgraph').

    Returns:
        A description of the topic, or a not-found message.
    """
    key = topic.lower().strip()
    result = KNOWLEDGE_BASE.get(key)
    if result:
        return result
    # Partial match — check if key is a substring of any stored key
    for k, v in KNOWLEDGE_BASE.items():
        if key in k or k in key:
            return v
    return f"No entry found for '{topic}'. Available topics: {list_topics()}"


def list_topics() -> str:
    """List all available topics in the knowledge base.

    Returns:
        Comma-separated list of topic names.
    """
    return ", ".join(KNOWLEDGE_BASE.keys())
