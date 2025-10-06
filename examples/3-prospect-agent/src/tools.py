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
        search = BraveSearch.from_api_key(api_key=brave_key, search_kwargs={"count": 5})
        raw = search.run(query)
        # Normalize into structured list of results: {title, snippet, url, date, source}
        results = []
        if isinstance(raw, dict):
            candidates = raw.get("results") or raw.get("organic") or raw.get("items") or []
        elif isinstance(raw, list):
            candidates = raw
        else:
            candidates = []

        for r in candidates[:5]:
            if not isinstance(r, dict):
                results.append({"title": str(r), "snippet": "", "url": "", "date": "", "source": ""})
                continue
            title = r.get("title") or r.get("name") or r.get("headline") or ""
            snippet = r.get("snippet") or r.get("snippet_text") or r.get("description") or ""
            url = r.get("url") or r.get("link") or r.get("displayUrl") or r.get("formattedUrl") or ""
            date = r.get("date") or r.get("published_at") or r.get("pubDate") or ""
            source = r.get("source") or r.get("site") or ""
            results.append({"title": title, "snippet": snippet, "url": url, "date": date, "source": source})

        return results

    tools = [search_tool]
    tool_node = ToolNode(tools=tools)
    return tools, tool_node
