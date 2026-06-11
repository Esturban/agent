# agent.py - Core agent logic and processing functions

import json
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

    # 1) Generate 3 candidate queries (structured JSON)
    query_gen_instruction = SystemMessage(
        f"Generate exactly {MAX_QUERIES} concise search queries (<= {QUERY_TOKEN_LIMIT} tokens)."
        f" Return a JSON array where each item is an object with keys 'query' and 'rationale'."
        f" Each query should target the prospect's LinkedIn/profile, short bio, or recent news (last {LOOKBACK_MONTHS} months)."
        " Prioritize LinkedIn, company domains, and trade publications. Avoid social media and political/opinion sources."
        " Return only valid JSON."
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

    # 2) Execute search for each candidate query and collect structured results
    aggregated_results = []
    for q in candidate_queries[:3]:
        qtext = q.get("query") if isinstance(q, dict) else str(q)
        raw = search_tool.invoke(qtext)

        # Expect the tool to return a list of structured results
        if isinstance(raw, list):
            aggregated_results.append({"query": qtext, "results": raw})
        else:
            aggregated_results.append(
                {
                    "query": qtext,
                    "results": [
                        {"title": str(raw), "snippet": "", "url": "", "date": "", "source": ""}
                    ],
                }
            )

    # 3) Ask LLM to summarize aggregated results into strict plain-text facts (last 3 months only)
    summarizer_instruction = SystemMessage(
        """
        You are a prospect enrichment specialist. Input: a JSON array of search result records: [{"query":"...","results":[{title,snippet,url,date,source}, ...]}, ...].
        Output: Plain text facts ONLY about the Company, Industry, and Prospect from the LAST 6 MONTHS.
        Format EXACTLY as lines like:
        Company: Fact (YYYY-MM-DD) (Source: FULL_URL)
        Industry: Fact (YYYY-MM-DD) (Source: FULL_URL)
        Prospect: Fact (YYYY-MM-DD) (Source: FULL_URL)
        - Only include verifiable facts with FULL URLs (http/https). If a fact lacks a FULL URL or is older than 6 months, exclude it.
        - If no valid recent facts, return exactly: No recent information found for this prospect.
        - Avoid linkedin or social media sources in your output. We have these and these access them in different tools.
        - Return plain text only, no explanation, no JSON.
        """
    )

    summarizer_resp = retry_on_rate_limit(
        researcher_llm, [SystemMessage(json.dumps(aggregated_results)), summarizer_instruction]
    )
    raw_summary = getattr(summarizer_resp, "content", str(summarizer_resp))
    summary_text = _strip_code_block(raw_summary).strip()

    # Post-LLM validation: require at least one line containing a full URL (http/https)
    lines = [l.strip() for l in summary_text.splitlines() if l.strip()]
    valid_lines = [l for l in lines if "http" in l]
    if not valid_lines:
        final_text = "No recent information found for this prospect."
    else:
        final_text = "\n".join(valid_lines)

    # 4) Return ResearchOutput with strict plain-text search_results
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
