# agent.py - Core agent logic and processing functions

import json
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from .models import AgentState, ResearchOutput, OutputSchema

def researcher_agent(state: AgentState, researcher_llm, search_tool) -> dict:
    """Phase 1: Research the prospect and generate search query"""
    prospect = state["prospect"]
    
    # Build query via researcher LLM
    prospect_meta = SystemMessage("__prospect__:" + json.dumps({
        "first_name": prospect.first_name,
        "last_name": prospect.last_name,
        "company": prospect.company,
        "position": prospect.position,
    }))
    query_instruction = SystemMessage(
        """You are a concise search-query generator. Given a prospect metadata SystemMessage prefixed with '__prospect__:',
        produce a single-line search query (<=50 tokens) to find the prospect's LinkedIn/profile, short bio, or recent news (within the 
        last 3 months ONLY, anything older is not relevant) about that person or developments with the company in th news. The search should be 
        specific to the prospect and the company. If nothing seems likely to be found, we should be focused a bit on the industry or 
        anything relevant that could help us find anything that gives the impression we have done some research on the company at all. 
        Don't make the query too strict it is useless and gets no results, don't make it too broad that we can't get any information about them.
        Return only the query string."""
    )
    query_resp = researcher_llm.invoke([query_instruction, prospect_meta])
    query = getattr(query_resp, "content", str(query_resp)).strip()

    # Call search tool
    search_results = search_tool.invoke(query)
    
    # Return research output
    return {
        "research": ResearchOutput(
            search_query=query,
            search_results=search_results
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
    are valuable here.  Note, if the research agent provides you with a link that acts as a piece of evidence for relevant information
    that helps in the first draft, you will be able to include it in the message. BUT ONLY INCLUDE THE URL AT THE END OF THE MESSAGE."""

    assistant_input = """Use the web search output to produce a JSON object with keys: generated_message (string, <=300 chars),
    confidence (float 0-1), source_summary (string). Return only valid JSON matching that schema."""

    draft_user = HumanMessage(f"""Draft the outreach message for {prospect.first_name} {prospect.last_name} at {prospect.company}.""")
    tool_msg = SystemMessage(f"[web_search_tool output]\n{research.search_results}")
    draft_messages = [SystemMessage(system_prompt), AIMessage(assistant_input), draft_user, tool_msg]

    # Use structured output parser
    parser = JsonOutputParser(pydantic_object=OutputSchema)
    draft_resp = copywriter_llm.invoke(draft_messages)
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
