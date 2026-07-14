from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import USER_ID, retrieve_relevant, store_turn

# Vector memory vs list-based memory (example 82 — Redis):
#   Redis LRANGE:     O(N) — loads ALL history on every query.
#   ChromaDB query:   O(k) — loads only the k most RELEVANT turns.
#
# At 10 turns the difference is negligible.
# At 10,000 turns: Redis loads 10,000 messages; Chroma loads 3.

_llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)


class VectorMemoryState(TypedDict):
    user_id: str
    query: str
    memories: list[str]   # retrieved relevant turns
    answer: str


def retrieve(state: VectorMemoryState) -> dict:
    """Embed the query and retrieve the k most semantically relevant memory turns."""
    memories = retrieve_relevant(state["query"], user_id=state["user_id"], k=3)
    return {"memories": memories}


def respond(state: VectorMemoryState) -> dict:
    """Generate an answer conditioned on the retrieved memories."""
    mem_block = "\n".join(f"- {m}" for m in state["memories"])
    msgs = [
        SystemMessage(content=(
            f"Relevant memories about this user:\n"
            f"{mem_block or '(no memories retrieved)'}\n\n"
            "Use these to personalise your response."
        )),
        HumanMessage(content=state["query"]),
    ]
    answer = _llm.invoke(msgs).content
    return {"answer": answer}


def save(state: VectorMemoryState) -> dict:
    """Embed and store the current turn so future queries can retrieve it."""
    turn = f"User asked: {state['query']} | Agent replied: {state['answer']}"
    store_turn(turn, user_id=state["user_id"])
    return {}


def create_workflow():
    builder = StateGraph(VectorMemoryState)
    builder.add_node("retrieve", retrieve)
    builder.add_node("respond",  respond)
    builder.add_node("save",     save)
    builder.add_edge(START,      "retrieve")
    builder.add_edge("retrieve", "respond")
    builder.add_edge("respond",  "save")
    builder.add_edge("save",     END)
    return builder.compile()
