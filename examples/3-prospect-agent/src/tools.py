# tools.py - Tool definitions and setup

import time

from langchain.tools import tool
from langchain_community.tools import BraveSearch, DuckDuckGoSearchResults
from langgraph.prebuilt import ToolNode


def create_tools(brave_key: str = None, prefer: str = "ddg", wait_seconds: float = 1.0):
    """Create search tools. Default provider is DuckDuckGo (ddg)."""

    @tool("web_search_tool")
    def search_tool(query: str):
        """Search the web for the most relevant information about the query.

        Sleeps `wait_seconds` before each call to reduce rate pressure.
        """
        # simple rate-spacing
        if wait_seconds and wait_seconds > 0:
            time.sleep(wait_seconds)

        results = []

        if prefer == "brave" and brave_key:
            search = BraveSearch.from_api_key(api_key=brave_key, search_kwargs={"count": 5})
            raw = search.run(query)
        else:
            ddg = DuckDuckGoSearchResults(output_format="list", source="news")
            raw = ddg.invoke(query)

        # Normalize into structured list of results: {title, snippet, url, date, source}
        if isinstance(raw, dict):
            candidates = raw.get("results") or raw.get("organic") or raw.get("items") or []
        elif isinstance(raw, list):
            candidates = raw
        else:
            # DuckDuckGo/Brave sometimes return tuples/lists; try to coerce
            candidates = []

        for r in candidates[:5]:
            # handle simple tuple/list rows like (url, snippet, title)
            if not isinstance(r, dict):
                try:
                    # attempt to parse common tuple/list shapes
                    if isinstance(r, (list, tuple)) and len(r) >= 3:
                        url, snippet, title = r[0], r[1], r[2]
                        results.append(
                            {
                                "title": title or "",
                                "snippet": snippet or "",
                                "url": url or "",
                                "date": "",
                                "source": "",
                            }
                        )
                        continue
                except Exception:
                    pass
                results.append(
                    {"title": str(r), "snippet": "", "url": "", "date": "", "source": ""}
                )
                continue

            title = r.get("title") or r.get("name") or r.get("headline") or r.get("titleText") or ""
            snippet = (
                r.get("snippet")
                or r.get("snippet_text")
                or r.get("description")
                or r.get("summary")
                or ""
            )
            url = (
                r.get("url")
                or r.get("link")
                or r.get("displayUrl")
                or r.get("formattedUrl")
                or r.get("href")
                or ""
            )
            date = r.get("date") or r.get("published_at") or r.get("pubDate") or ""
            source = r.get("source") or r.get("site") or r.get("domain") or ""
            results.append(
                {"title": title, "snippet": snippet, "url": url, "date": date, "source": source}
            )

        tools = [search_tool]
        tool_node = ToolNode(tools=tools)
        return results, tool_node

    # Backwards-compatible return: return tools list and tool_node
    tools = [search_tool]
    tool_node = ToolNode(tools=tools)
    return tools, tool_node
