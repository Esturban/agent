import os
from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

# Zep Cloud Memory (getzep.com) — production memory layer for LLM agents
#
# What Zep handles automatically (vs. DIY Redis from example 82):
#   - Auto-summarizes old turns when history exceeds a threshold
#   - Extracts named entities (people, places, facts) into a searchable graph
#   - Applies temporal decay so stale facts score lower in retrieval
#   - Returns a ready-to-inject `context` string for the system prompt
#
# Tradeoff vs. Redis:
#   Redis (ex 82): full control, manual compaction, ~10 lines of plumbing
#   Zep:           batteries-included, managed auto-summary, less raw control
#
# Setup: pip install zep-cloud
#        Set ZEP_API_KEY in .env (free tier at getzep.com)
#
# Pattern: load_memory → respond → save_memory
# Same three-node structure as Redis (example 82) — swap the store, keep the graph.

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def _get_zep_client():
    """Lazy-load the Zep client to avoid import errors when dep is missing."""
    from zep_cloud.client import Zep  # pip install zep-cloud
    return Zep(api_key=os.environ["ZEP_API_KEY"])


class ZepState(TypedDict):
    user_id: str
    session_id: str
    query: str
    context: str   # compressed memory context from Zep (auto-summary + facts)
    response: str


def load_memory(state: ZepState) -> dict:
    """Retrieve memory context from Zep for this session.

    memory.context is a string that Zep assembles from:
      - Auto-generated summary of older turns
      - Extracted entity facts (e.g. 'User's name is Alex')
    Inject it into the system prompt so the model has full context without
    needing raw history — Zep has already done the compression for you.
    """
    zep = _get_zep_client()
    try:
        memory = zep.memory.get(session_id=state["session_id"])
        context = memory.context or ""
    except Exception:
        context = ""  # new session has no memory yet
    return {"context": context}


def respond(state: ZepState) -> dict:
    """Generate a response using the compressed Zep memory as system context."""
    messages = []
    if state["context"]:
        messages.append(SystemMessage(
            content=f"Memory context from prior conversations:\n{state['context']}"
        ))
    messages.append(HumanMessage(content=state["query"]))
    answer = _llm.invoke(messages).content.strip()
    return {"response": answer}


def save_memory(state: ZepState) -> dict:
    """Persist this turn to Zep. Zep auto-summarizes when history grows long.

    Unlike Redis where you manually call RPUSH + EXPIRE, Zep handles:
      - Appending the new turn to the session
      - Triggering summarization in the background when needed
      - Updating the entity graph with any new facts extracted from the turn
    """
    from zep_cloud.types import Message

    zep = _get_zep_client()
    try:
        zep.memory.add(
            session_id=state["session_id"],
            messages=[
                Message(role="user",      role_type="user",      content=state["query"]),
                Message(role="assistant", role_type="assistant",  content=state["response"]),
            ],
        )
    except Exception:
        pass  # session may need to be created first; handled in main.py
    return {}


def create_workflow():
    builder = StateGraph(ZepState)
    builder.add_node("load_memory", load_memory)
    builder.add_node("respond", respond)
    builder.add_node("save_memory", save_memory)
    builder.add_edge(START, "load_memory")
    builder.add_edge("load_memory", "respond")
    builder.add_edge("respond", "save_memory")
    builder.add_edge("save_memory", END)
    return builder.compile()
