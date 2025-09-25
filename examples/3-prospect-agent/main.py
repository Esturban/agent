import os
import json
from typing import Annotated, TypedDict, Literal
from dotenv import load_dotenv
from time import time
from langchain.tools import tool
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import HuggingFaceDatasetLoader
from langchain_community.tools import BraveSearch
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import pandas as pd
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


load_dotenv()
brave_key = os.getenv("BRAVE_API_KEY")
class State(TypedDict):
    messages: Annotated[list, add_messages]

class OutputSchema(BaseModel):
    generated_message: str = Field(..., description="Personalized outreach message")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    source_summary: str = Field(..., description="Concise summary of sources used")

def prospect_agent(prospect_path: str, output_path: str):
    # minimal CSV handling: read and ensure not empty
    prospects = pd.read_csv(prospect_path)[:2]
    if prospects.empty:
        raise ValueError(f"Prospects CSV is empty or unreadable: {prospect_path}")
    
    @tool("web_search_tool")
    def search_tool(query):
        """
        Search the web for the most relevant information about the query.
        """
        search = BraveSearch.from_api_key(api_key=brave_key, search_kwargs={"count": 3})
        raw = search.run(query)
        if isinstance(raw, str):
            return raw
        if isinstance(raw, dict):
            results = raw.get("results") or raw.get("organic") or []
        elif isinstance(raw, list):
            results = raw
        else:
            results = []
        lines = []
        for r in results[:3]:
            title = r.get("title") or r.get("name") or r.get("headline") if isinstance(r, dict) else str(r)
            snippet = r.get("snippet") or r.get("snippet_text") or r.get("description") if isinstance(r, dict) else ""
            lines.append(f"- {title}: {snippet}" if snippet else f"- {title}")
        return "\n".join(lines) if lines else json.dumps(raw)

    tools = [search_tool]
    tool_node = ToolNode(tools=tools)
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

    # Function to decide whether to continue or stop the workflow
    def route(state: MessagesState) -> Literal["tools", END]:
        messages = state["messages"]
        last_message = messages[-1]
        # If the LLM makes a tool call, go to the "tools" node
        if last_message.tool_calls:
            return "tools"
        # Otherwise, finish the workflow
        return END

    workflow = StateGraph(MessagesState)


    def call_model(state: MessagesState):
        messages = state["messages"]
        response = llm.invoke(messages)
        # Debug: print tool calls and content emitted by the LLM
        # If the LLM did not emit tool_calls, call the single web_search_tool directly
        tc = getattr(response, "tool_calls", None)
        if tc:
            return {"messages": [response]}

        # If no tool_calls, ask the LLM (as a separate step) to build a concise search query
        prospect_meta = None
        for m in messages:
            if isinstance(m, SystemMessage) and isinstance(getattr(m, "content", ""), str) and m.content.startswith("__prospect__:"):
                prospect_meta = m
                break

        if prospect_meta:
            # instruct the LLM to produce a short search query (<= 50 tokens) targeting LinkedIn/profile/news
            query_instruction = SystemMessage(
                "You are a concise search-query generator. Given a prospect metadata SystemMessage prefixed with '__prospect__:', produce a single-line search query (<=50 tokens) that will find the prospect's LinkedIn/profile, short bio, or recent news. Return only the query string."
            )
            # build messages for the query builder LLM call
            builder_messages = [query_instruction, prospect_meta]
            query_resp = llm.invoke(builder_messages)
            query = getattr(query_resp, "content", str(query_resp)).strip()
            # run the tool with the generated query and append its output for the agent
            tool_out = search_tool.invoke(query)
            tool_msg = SystemMessage(f"[web_search_tool output]\n{tool_out}")
            return {"messages": [response, tool_msg]}

        # fallback: return original response if no prospect metadata present
        return {"messages": [response]}


    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    # Conditional routing from agent should return the specific tool node name (e.g. 'hf')
    workflow.add_conditional_edges("agent", route)
    # Route each tool node back to the agent so the workflow can continue
    workflow.add_edge("tools", "agent")

    graph = workflow.compile(checkpointer=MemorySaver())


    def run_agent(prospect_data):
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
        print(parsed)
        # parsed is an instance of OutputSchema
        return parsed["generated_message"], parsed["confidence"], parsed["source_summary"]
    
    # run_agent now returns (generated_message, confidence, source_summary)
    cols = prospects.apply(lambda row: pd.Series(run_agent(row)), axis=1)
    cols.columns = ["generated_message", "confidence", "source_summary"]
    prospects = pd.concat([prospects, cols], axis=1)

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    prospects.to_csv(output_path, index=False)
    

if __name__ == "__main__":
    prospect_agent(prospect_path="data/sample_connections.csv", output_path="data/aug/sample_connections_aug.csv")
