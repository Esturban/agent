# agent.py - Core agent logic and processing functions

import json
import os
import time

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser

# Configuration: judge thresholds and rerun limits for research relevance checks
from .models import AgentState, OutputSchema, ResearchOutput

QUERY_TOKEN_LIMIT = 20
LOOKBACK_MONTHS = 3
MAX_QUERIES = 3


# Minimal retry helper: retry on rate-limit / connection errors, re-raise other errors
def retry_on_rate_limit(llm, messages, max_retries: int = 5, backoff: float = 1.0):
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            return llm.invoke(messages)
        except Exception as e:
            last_exc = e
            s = str(e).lower()
            # retry heuristics: HTTP 429, rate limit, connection errors
            if (
                "429" in s
                or "too many requests" in s
                or "rate limit" in s
                or "connection error" in s
            ):
                sleep_time = backoff * (2 ** (attempt - 1))
                print(
                    f"Rate/connection error on attempt {attempt}: {e}. Backing off {sleep_time}s..."
                )
                time.sleep(sleep_time)
                continue
            # non-retriable error — re-raise immediately so issues are visible
            raise
    # exhausted retries — raise the last exception
    raise last_exc


def _strip_code_block(text: str) -> str:
    """Remove surrounding markdown code fences (``` or ```json) and leading/trailing whitespace."""
    if not isinstance(text, str):
        return text
    t = text.strip()
    # remove leading/trailing triple backticks blocks
    if t.startswith("```") and t.endswith("```"):
        # find first newline after opening fence
        # allow ```json or ```json\n
        # remove the opening fence and optional language tag
        first_newline = t.find("\n")
        if first_newline != -1:
            inner = t[first_newline + 1 : -3]
            return inner.strip()
        return t[3:-3].strip()
    return t


# NOTE: judge/rerun logic removed to keep researcher single-pass and focused on strict 3-month facts


def researcher_agent(state: AgentState, researcher_llm, search_tool) -> dict:
    """Phase 1: Research the prospect.

    Improvements made while preserving compatibility with existing `main.py`:
    - Generate multiple candidate queries (3) with short rationales
    - Run the web search tool for each query and aggregate results
    - Ask the LLM to produce a compact JSON summary with facts, confidence, and 5 curiosity questions
    - Return `ResearchOutput.search_results` as a single string (aggregated) so downstream code remains unchanged
    """
    prospect = state["prospect"]

    # Build prospect JSON
    prospect_payload = {
        "first_name": prospect.first_name,
        "last_name": prospect.last_name,
        "company": prospect.company,
        "position": prospect.position,
    }

    # 1) Generate 2-3 targeted queries with engine selection (structured JSON)
    query_gen_instruction = SystemMessage(
        f"Generate 2-3 search queries for company/industry research."
        f" Return JSON array: [{{'query': '...', 'engines': 'reuters,bing'}}, ...]"
        "\n\nFOCUS ON:"
        "\n1. Company news, funding, acquisitions, product launches"
        "\n2. Industry trends affecting their sector"
        "\n3. Company role context (what {prospect.position}s do at {prospect.company})"
        "\n\nQUERY FORMAT:"
        f"\n- {prospect.company} news 2024"
        f"\n- {prospect.company} funding OR acquisition OR partnership"
        f"\n- {prospect.company} industry trends challenges"
        "\n\nENGINES:"
        "\n- Company/industry news: reuters,bing"
        "\n- Tech companies: google,bing"
        "\n\nReturn ONLY valid JSON."
    )

    query_resp = retry_on_rate_limit(
        researcher_llm, [SystemMessage(json.dumps(prospect_payload)), query_gen_instruction]
    )
    raw_queries = getattr(query_resp, "content", str(query_resp))
    raw_queries_strip = _strip_code_block(raw_queries)
    try:
        candidate_queries = json.loads(raw_queries_strip)
        if not isinstance(candidate_queries, list):
            raise ValueError("queries not a list")
    except Exception:
        print("Failed to parse query generator output. Raw response below:")
        print(raw_queries)
        raise

    # 2) Execute search for each candidate query with selected engines and collect structured results
    aggregated_results = []
    for q in candidate_queries[:3]:
        qtext = q.get("query") if isinstance(q, dict) else str(q)
        engines = q.get("engines", "google,bing") if isinstance(q, dict) else "google,bing"

        # Invoke search tool with both query and engines
        raw = search_tool.invoke({"query": qtext, "engines": engines})

        # Expect the tool to return a list of structured results
        if isinstance(raw, list):
            aggregated_results.append({"query": qtext, "engines": engines, "results": raw})
        else:
            aggregated_results.append(
                {
                    "query": qtext,
                    "engines": engines,
                    "results": [
                        {"title": str(raw), "snippet": "", "url": "", "date": "", "source": ""}
                    ],
                }
            )

    # 3) Ask LLM to summarize aggregated results into strict plain-text facts (last 3 months only)

    # DEBUG: Log what we're sending to the LLM
    debug_mode = os.getenv("SEARXNG_DEBUG", "false").lower() == "true"
    if debug_mode:
        print("\n[DEBUG] ===== AGGREGATED RESULTS FOR SUMMARIZER =====")
        print(f"  Number of queries: {len(aggregated_results)}")
        for i, agg in enumerate(aggregated_results):
            print(f"\n  Query {i + 1}: {agg.get('query', 'N/A')}")
            print(f"    Engines: {agg.get('engines', 'N/A')}")
            print(f"    Results count: {len(agg.get('results', []))}")
            if agg.get("results"):
                for j, result in enumerate(agg["results"][:2]):  # Show first 2 results
                    print(f"    Result {j + 1}:")
                    print(f"      Title: {result.get('title', 'N/A')[:80]}")
                    print(f"      URL: {result.get('url', 'MISSING URL!')}")
                    print(f"      Snippet: {result.get('snippet', 'N/A')[:100]}")

    summarizer_instruction = SystemMessage(
        """Extract recent facts about the COMPANY and INDUSTRY from search results.

INPUT: JSON array of search results.

OUTPUT (plain text, one fact per line):
Company: [Recent company news/development] (Source: FULL_URL)
Industry: [Industry trend/challenge] (Source: FULL_URL)

WHAT TO EXTRACT:
- Company: Funding, acquisitions, product launches, partnerships, growth, challenges
- Industry: Market trends, regulations, technology shifts, competitive landscape

RULES:
1. MUST include full http/https URL for each fact
2. Recent news only (2024-2025)
3. Skip: LinkedIn, social media, job postings
4. If nothing relevant: "No recent information found for this prospect."

GOOD EXAMPLES:
Company: Visier raised $120M Series E to expand workforce analytics (Source: https://techcrunch.com/2024/...)
Industry: HR tech market growing 12% annually due to AI adoption (Source: https://reuters.com/...)

BAD (no URL, too vague):
Company: Visier is growing
Industry: HR tech is important"""
    )

    summarizer_resp = retry_on_rate_limit(
        researcher_llm, [SystemMessage(json.dumps(aggregated_results)), summarizer_instruction]
    )
    raw_summary = getattr(summarizer_resp, "content", str(summarizer_resp))
    summary_text = _strip_code_block(raw_summary).strip()

    # DEBUG: Log what the summarizer returned
    if debug_mode:
        print("\n[DEBUG] ===== SUMMARIZER RAW RESPONSE =====")
        print(f"  Raw length: {len(raw_summary)}")
        print(f"  Full summary:\n{summary_text}")
        print("  ===== END SUMMARIZER RESPONSE =====")

    # Post-LLM validation: require at least one line containing a full URL (http/https)
    lines = [l.strip() for l in summary_text.splitlines() if l.strip()]
    valid_lines = [l for l in lines if "http" in l]

    # DEBUG: Log validation results
    debug_mode = os.getenv("SEARXNG_DEBUG", "false").lower() == "true"
    if debug_mode:
        print("\n[DEBUG] ===== VALIDATION RESULTS =====")
        print(f"  Total lines from LLM: {len(lines)}")
        print(f"  Lines with URLs (valid): {len(valid_lines)}")
        if lines:
            print("\n  All lines from LLM:")
            for idx, line in enumerate(lines[:5]):  # Show first 5
                has_url = "✓ HAS URL" if "http" in line else "✗ NO URL"
                print(f"    {idx + 1}. [{has_url}] {line[:120]}")
        if not valid_lines and lines:
            print(f"\n  ⚠️  WARNING: LLM returned {len(lines)} lines but NONE contain URLs!")
            print("  This means all research will be discarded.")

    if not valid_lines:
        final_text = "No recent information found for this prospect."
    else:
        final_text = "\n".join(valid_lines)

    # 4) Return ResearchOutput with strict plain-text search_results
    debug_mode = os.getenv("SEARXNG_DEBUG", "false").lower() == "true"
    if debug_mode:
        print("\n[DEBUG] Researcher Final Output:")
        print(
            f"  Query: {', '.join([str(q.get('query') if isinstance(q, dict) else q) for q in candidate_queries])}"
        )
        print(f"  Results length: {len(final_text)}")
        print(f"  Results preview: {final_text[:150]}...")

    return {
        "research": ResearchOutput(
            search_query=", ".join(
                [str(q.get("query") if isinstance(q, dict) else q) for q in candidate_queries]
            ),
            search_results=final_text,
        )
    }


def copywriter_agent(state: AgentState, copywriter_llm) -> dict:
    """Phase 2: Draft personalized outreach message"""
    prospect = state["prospect"]
    research = state["research"]

    system_prompt = """You are an expert copy writer producing highly personalized outreach messages. You will be given
    prospect metadata and web search results; produce a concise, personalized outreach message no longer than 40 words.
    The goal isn't to push our services, but to make an open ended inquiry about how new developments in the industry
    are developing, especially if there's a relevant point about the prospect's industry being impacted by AI. This isn't
    a point to push our product, but rather to develop a relationship with the prospect. You never mention the services
    we offer unless they ask. It is so important to establish credibility by being specific and well informed about them
    or their industry. This is vital since our goal is to get a response from them. In fact, sometimes focusing on
    troubling things, without insulting them, their industry or their company is what is important. Recent developments
    are valuable here. Additionally, consider being friendly using simple language. This is the first message, don't be overwhelming N
    ote, if the research agent provides you with a link that acts as a piece of evidence for relevant information
    that helps in the first draft, you will be able to include it in the message AT THE END OF THE MESSAGE."""

    assistant_input = """Use the web search output to produce a JSON object with keys: generated_message (string, <=300 chars),
    confidence (float 0-1), source_summary (string). Return only valid JSON matching that schema."""

    draft_user = HumanMessage(
        f"""Draft the outreach message for {prospect.first_name} {prospect.last_name} at {prospect.company}."""
    )
    tool_msg = SystemMessage(f"[web_search_tool output]\n{research.search_results}")
    draft_messages = [
        SystemMessage(system_prompt),
        AIMessage(assistant_input),
        draft_user,
        tool_msg,
    ]

    # Use structured output parser
    parser = JsonOutputParser(pydantic_object=OutputSchema)
    draft_resp = retry_on_rate_limit(copywriter_llm, draft_messages)
    raw = getattr(draft_resp, "content", str(draft_resp)).strip()
    # Try to strip common markdown code fences before parsing the copywriter's JSON
    raw_stripped = _strip_code_block(raw)
    try:
        parsed = parser.parse(raw_stripped)
    except Exception:
        print("Failed to parse copywriter output. Raw response below:")
        print(raw)
        raise

    # Override copywriter `source_summary` with top 2-3 http(s) URLs from researcher output
    import re

    raw_research = (state.get("research").search_results) if state.get("research") else ""
    urls = re.findall(r"https?://[^\s)]+", raw_research or "")
    top_links = urls[:3]
    print(f"Top links: {top_links}")
    source_summary_links = (
        "; ".join(top_links) if top_links else "No recent information found for this prospect."
    )

    return {
        "output": OutputSchema(
            generated_message=parsed["generated_message"],
            confidence=parsed["confidence"],
            source_summary=source_summary_links,
        )
    }
