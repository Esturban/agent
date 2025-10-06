# agent.py - Core agent logic and processing functions

import json
import time
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from .models import AgentState, ResearchOutput, OutputSchema


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
            if "429" in s or "too many requests" in s or "rate limit" in s or "connection error" in s:
                sleep_time = backoff * (2 ** (attempt - 1))
                print(f"Rate/connection error on attempt {attempt}: {e}. Backing off {sleep_time}s...")
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
    if t.startswith('```') and t.endswith('```'):
        # find first newline after opening fence
        # allow ```json or ```json\n
        # remove the opening fence and optional language tag
        first_newline = t.find('\n')
        if first_newline != -1:
            inner = t[first_newline+1:-3]
            return inner.strip()
        return t[3:-3].strip()
    return t

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
        "Generate exactly 3 concise search queries (<=50 tokens) as a JSON array of objects:"
        " [{\"query\": \"...\", \"rationale\": \"one-line\"}, ...]."
        " The queries should target the prospect's LinkedIn/profile, short bio, or recent news (last 6 months)."
        " Return only valid JSON."
    )

    query_resp = retry_on_rate_limit(researcher_llm, [SystemMessage(json.dumps(prospect_payload)), query_gen_instruction])
    raw_queries = getattr(query_resp, "content", str(query_resp))
    raw_queries_strip = _strip_code_block(raw_queries)
    try:
        candidate_queries = json.loads(raw_queries_strip)
        if not isinstance(candidate_queries, list):
            raise ValueError("queries not a list")
    except Exception as e:
        print("Failed to parse query generator output. Raw response below:")
        print(raw_queries)
        raise

    # 2) Execute search for each candidate query and collect structured results
    aggregated_results = []
    for q in candidate_queries[:3]:
        qtext = q.get("query") if isinstance(q, dict) else str(q)
        try:
            raw = search_tool.invoke(qtext)
        except Exception:
            raw = [{"title": "search_error", "snippet": "tool failed", "url": "", "date": "", "source": ""}]

        # Expect the tool to return a list of structured results
        if isinstance(raw, list):
            aggregated_results.append({"query": qtext, "results": raw})
        else:
            # fallback: wrap the string
            aggregated_results.append({"query": qtext, "results": [{"title": str(raw), "snippet": "", "url": "", "date": "", "source": ""}]})

    # 3) Ask LLM to summarize aggregated results into JSON with facts, confidences, and curiosity questions
    summarizer_instruction = SystemMessage(
        """
        You are a research summarizer. Input: a JSON array of search result records: [{"query":"...","results":[{title,snippet,url,date,source}, ...]}, ...].
        Output: JSON with keys:
        - facts: list of {text, source_url, date, confidence: "low"|"med"|"high"}
        - curiosity_questions: list of 5 strings tailored to the prospect
        - source_summary: short string (2-3 lines)
        Return only valid JSON. If a claim cannot be sourced, do not invent a URL.
        """
    )
    summarizer_resp = retry_on_rate_limit(researcher_llm, [SystemMessage(json.dumps(aggregated_results)), summarizer_instruction])
    raw_summary = getattr(summarizer_resp, "content", str(summarizer_resp))
    raw_summary_strip = _strip_code_block(raw_summary)
    try:
        summary_obj = json.loads(raw_summary_strip)
    except Exception:
        print("Failed to parse summarizer output. Raw response below:")
        print(raw_summary)
        raise

    # 4) Prepare a compatibility-friendly aggregated string for ResearchOutput.search_results
    try:
        aggregated_str_lines = []
        for r in aggregated_results:
            lines = [f"Query: {r.get('query')}"]
            for item in r.get("results", [])[:5]:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                url = item.get("url", "")
                date = item.get("date", "")
                lines.append(f"- {title}: {snippet} ({url} {date})")
            aggregated_str_lines.append("\n".join(lines))
        aggregated_str = "\n\n".join(aggregated_str_lines)
        # Append LLM-produced source_summary and top facts when available
        if isinstance(summary_obj, dict):
            if summary_obj.get("source_summary"):
                aggregated_str += "\n\nLLM source_summary:\n" + str(summary_obj.get("source_summary"))
            facts = summary_obj.get("facts") or []
            if facts:
                aggregated_str += "\n\nTop facts:\n"
                for f in facts[:5]:
                    txt = f.get("text", "")
                    src = f.get("source_url", "")
                    conf = f.get("confidence", "")
                    aggregated_str += f"- {txt} ({src}) [{conf}]\n"
    except Exception:
        aggregated_str = json.dumps(aggregated_results)

    # 5) Return ResearchOutput while preserving fields expected by downstream code
    return {
        "research": ResearchOutput(
            search_query=", ".join([str(q.get("query") if isinstance(q, dict) else q) for q in candidate_queries]),
            search_results=aggregated_str,
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

    draft_user = HumanMessage(f"""Draft the outreach message for {prospect.first_name} {prospect.last_name} at {prospect.company}.""")
    tool_msg = SystemMessage(f"[web_search_tool output]\n{research.search_results}")
    draft_messages = [SystemMessage(system_prompt), AIMessage(assistant_input), draft_user, tool_msg]

    # Use structured output parser
    parser = JsonOutputParser(pydantic_object=OutputSchema)
    draft_resp = retry_on_rate_limit(copywriter_llm, draft_messages)
    raw = getattr(draft_resp, "content", str(draft_resp)).strip()
    parsed = parser.parse(raw)
    
    # Return output
    return {
        "output": OutputSchema(
            generated_message=parsed["generated_message"],
            confidence=parsed["confidence"],
            source_summary=parsed["source_summary"]
        )
    }
