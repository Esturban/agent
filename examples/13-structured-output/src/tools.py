from duckduckgo_search import DDGS


def search_web(query: str, max_results: int = 5) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    if not results:
        return "No results found."
    return "\n".join(f"{r['title']}: {r['body']}" for r in results)
