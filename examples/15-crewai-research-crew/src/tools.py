from crewai.tools import tool


@tool("Web Search")
def web_search(query: str) -> str:
    """Search the web for recent information about a topic."""
    from ddgs import DDGS
    results = list(DDGS().text(query, max_results=5))
    return "\n".join(f"- {r['body']}" for r in results) if results else "No results found."
