# workflow.py - Workflow graph definition and related functions

from typing import Literal
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.checkpoint.memory import MemorySaver
from .models import State

def create_workflow(llm, tools, tool_node):
    # Function to decide whether to continue or stop the workflow
    def route(state: MessagesState) -> Literal["tools", END]:
        messages = state["messages"]
        last_message = messages[-1]
        # If the LLM makes a tool call, go to the "tools" node
        if last_message.tool_calls:
            return "tools"
        # Otherwise, finish the workflow
        return END

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
            tool_out = tools[0].invoke(query)  # Assuming first tool is search_tool
            tool_msg = SystemMessage(f"[web_search_tool output]\n{tool_out}")
            return {"messages": [response, tool_msg]}

        # fallback: return original response if no prospect metadata present
        return {"messages": [response]}

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    # Conditional routing from agent should return the specific tool node name (e.g. 'hf')
    workflow.add_conditional_edges("agent", route)
    # Route each tool node back to the agent so the workflow can continue
    workflow.add_edge("tools", "agent")

    graph = workflow.compile(checkpointer=MemorySaver())
    return graph
