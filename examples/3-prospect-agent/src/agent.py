# agent.py - Core agent logic and processing functions

import json
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from .models import OutputSchema

def run_agent(prospect_data, llm, search_tool):
    # print(prospect_data)
    system_prompt = """You are an expert researcher and copy writer to find information efficiently about a potential
    prospect when given the name, company, and position of the prospect. You will be given prospect metadata and web
    search results; produce a concise, personalized outreach message no longer than 40 words. The goal isn't to push
    our services, but to make an open ended inquiry about how new developments in the industry are developing, especially
    if there's a relevant point about the prospect's industry being impacted by AI. This isn't a point to push our product, but
    rather to develop a relationship with the prospect. You never mention the services we offer unless they ask. It is so important to
    establish credibility by being specific and well informed about them or their industry. This is vital since our goal
    is to get a response from them. In fact, sometimes focusing on troubling things, without insulting them, their
    industry or their company is what is important. Recent developments are valuable here"""

    # 1) Build query via LLM
    prospect_meta = SystemMessage("__prospect__:" + json.dumps({
        "first_name": prospect_data.get("First Name"),
        "last_name": prospect_data.get("Last Name"),
        "company": prospect_data.get("Company"),
        "position": prospect_data.get("Position"),
    }))
    query_instruction = SystemMessage(
        """You are a concise search-query generator. Given a prospect metadata SystemMessage prefixed with '__prospect__:',
        produce a single-line search query (<=50 tokens) to find the prospect's LinkedIn/profile, short bio, or recent news
        about that person or developments with the company. The search should be specific to the prospect and the company. If
        nothing seems likely to be found, we should be focused a bit on the industry or anything relevant that could help us
        find anything that gives the impression we have done some research on the company at all. Don't make the query too strict
        it is useless and gets no results, don't make it too broad that we can't get any information about them.
        Return only the query string."""
    )
    query_resp = llm.invoke([query_instruction, prospect_meta])
    query = getattr(query_resp, "content", str(query_resp)).strip()

    # 2) Call tool
    tool_out = search_tool.invoke(query)

    # 3) Draft message + structured JSON output using JsonOutputParser
    assistant_input = f"""Use the web search output to produce a JSON object with keys: generated_message (string, <=300 chars),
    confidence (float 0-1), source_summary (string). Return only valid JSON matching that schema."""

    draft_user = HumanMessage(f"""Draft the outreach message for {prospect_data.get('First Name')}
                              {prospect_data.get('Last Name')} at {prospect_data.get('Company')}.""")
    tool_msg = SystemMessage(f"[web_search_tool output]\n{tool_out}")
    draft_messages = [SystemMessage(system_prompt), AIMessage(assistant_input), draft_user, tool_msg]

    # Use structured output parser (Pydantic model)
    # structured
    parser = JsonOutputParser(pydantic_object=OutputSchema)
    # Chain: prompt -> llm -> parser (invoke directly for simplicity)
    draft_resp = llm.invoke(draft_messages)
    raw = getattr(draft_resp, "content", str(draft_resp)).strip()
    parsed = parser.parse(raw)
    # print(parsed)
    # parsed is an instance of OutputSchema
    return parsed["generated_message"], parsed["confidence"], parsed["source_summary"]
