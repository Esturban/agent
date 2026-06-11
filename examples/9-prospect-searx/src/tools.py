# tools.py - Tool definitions and setup

import os
import time

from langchain.tools import tool
from langchain_community.utilities import SearxSearchWrapper
from langgraph.prebuilt import ToolNode


def create_tools(wait_seconds: float = 1.0):
    """Create SearXNG search tool."""

    searxng_host = os.getenv("SEARXNG_HOST", "http://localhost:8888")
    debug_mode = os.getenv("SEARXNG_DEBUG", "false").lower() == "true"

    @tool("web_search_tool")
    def search_tool(query: str, engines: str = "google,bing"):
        """Search the web for the most relevant information about the query using SearXNG.

        Args:
            query: The search query string
            engines: Comma-separated list of search engines to use.
                     Available: google, bing, duckduckgo, brave, reuters, github, arxiv, gitlab, pubmed
                     Example: "google,bing" or "reuters,bing" for news

        Sleeps `wait_seconds` before each call to reduce rate pressure.
        """
        # simple rate-spacing
        if wait_seconds and wait_seconds > 0:
            time.sleep(wait_seconds)

        results = []

        # Parse engines parameter
        engine_list = [e.strip() for e in engines.split(",") if e.strip()]

        if debug_mode:
            print("\n[DEBUG] SearXNG Request:")
            print(f"  Host: {searxng_host}")
            print(f"  Query: {query}")
            print(f"  Engines: {engine_list}")

        try:
            # Initialize SearxNG wrapper
            searx = SearxSearchWrapper(searx_host=searxng_host)

            # Test basic connectivity first
            if debug_mode:
                import requests

                test_url = f"{searxng_host}/search?q=test&format=json"
                print(f"  Test URL: {test_url}")
                try:
                    test_resp = requests.get(test_url, timeout=5)
                    print(f"  Test Response Status: {test_resp.status_code}")
                    if test_resp.status_code != 200:
                        print(f"  Test Response Body: {test_resp.text[:500]}")
                except Exception as test_e:
                    print(f"  Test Connection Error: {test_e}")

            # Get results from SearxNG
            raw_results = searx.results(query, num_results=5, engines=engine_list)

            if debug_mode:
                print(f"  Raw Results Count: {len(raw_results) if raw_results else 0}")
                if raw_results:
                    print(
                        f"  First Result Keys: {list(raw_results[0].keys()) if raw_results[0] else 'N/A'}"
                    )
                    # Show ACTUAL content of first result
                    print("\n  FIRST RAW RESULT CONTENT:")
                    import json

                    print(f"  {json.dumps(raw_results[0], indent=4)}")

            # Transform SearxNG output to match agent expectations
            # SearxNG returns: url, snippet, title, category, engines (OR link instead of url)
            # Agent expects: title, snippet, url, date, source
            for idx, r in enumerate(raw_results[:5]):
                if not isinstance(r, dict):
                    if debug_mode:
                        print(f"  [WARNING] Result {idx + 1} is not dict: {type(r)}")
                    results.append(
                        {"title": str(r), "snippet": "", "url": "", "date": "", "source": ""}
                    )
                    continue

                # Check if this is an error/weird result structure
                if "Result" in r and "title" not in r:
                    if debug_mode:
                        print(f"  [WARNING] Result {idx + 1} has error structure - skipping")
                    continue  # Skip error results

                # Get URL from either 'url' or 'link' field
                result_url = r.get("url", "") or r.get("link", "")

                result_obj = {
                    "title": r.get("title", ""),
                    "snippet": r.get("snippet", ""),
                    "url": result_url,
                    "date": "",  # SearxNG doesn't provide dates by default
                    "source": r.get("category", ""),
                }

                if debug_mode and not result_url:
                    print(f"  [WARNING] Result {idx + 1} has NO URL! Keys: {list(r.keys())}")

                results.append(result_obj)

            if debug_mode:
                print(f"  Transformed Results: {len(results)}")
                if results:
                    print(
                        f"  First transformed result URL: {results[0]['url'][:80] if results[0]['url'] else 'NO URL'}"
                    )

        except Exception as e:
            error_msg = str(e)
            print(f"\n[ERROR] SearxNG search failed for query: {query}")
            print(f"  Error: {error_msg}")

            # Provide helpful diagnostic info
            if "403" in error_msg or "Forbidden" in error_msg:
                print("\n[DIAGNOSTIC] 403 Forbidden Error Detected")
                print("  Possible causes:")
                print("  1. JSON API format not enabled in SearXNG settings.yml")
                print("  2. Rate limiting blocking requests")
                print("  3. API access restricted")
                print("\n  Quick fixes:")
                print("  - Check settings.yml has: search.formats = ['html', 'json']")
                print("  - Disable rate limiting: server.limiter = false")
                print("  - Check server.secret_key is set")
                print(f"  - Verify access: curl '{searxng_host}/search?q=test&format=json'")
            elif "Connection" in error_msg or "refused" in error_msg:
                print("\n[DIAGNOSTIC] Connection Error Detected")
                print(f"  - Is SearXNG running? Check: curl {searxng_host}")
                print(f"  - Correct host? Currently using: {searxng_host}")
                print("  - Set SEARXNG_HOST env var if using different port")

            # Return empty results on error
            results = []

        return results

    # Return tools list and tool_node
    tools = [search_tool]
    tool_node = ToolNode(tools=tools)
    return tools, tool_node
