from typing import Any, TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from mem0 import Memory

_mem = Memory()
_llm = ChatOpenAI(model="gpt-5-nano", temperature=0)


class MemState(TypedDict):
    user_id: str
    query: str
    recalled: list[dict]
    answer: str
    messages: list[dict]


def recall_memories(state: MemState) -> dict:
    results = _mem.search(state["query"], user_id=state["user_id"], limit=5)
    memories = results.get("results", results) if isinstance(results, dict) else results
    return {"recalled": memories}


def respond(state: MemState) -> dict:
    context = "\n".join(
        f"- {m.get('memory', m.get('text', ''))}" for m in state["recalled"]
    )
    prompt = (
        f"Memories about the user:\n{context or '(none)'}\n\n"
        f"User: {state['query']}\n"
        "Answer based on the memories if relevant, otherwise say you don't know."
    )
    response = _llm.invoke([HumanMessage(content=prompt)])
    return {"answer": response.content}


def store_memories(state: MemState) -> dict[str, Any]:
    if state.get("messages"):
        _mem.add(state["messages"], user_id=state["user_id"])
    return {}


def create_workflow():
    builder = StateGraph(MemState)
    builder.add_node("recall", recall_memories)
    builder.add_node("respond", respond)
    builder.add_node("store", store_memories)
    builder.add_edge(START, "recall")
    builder.add_edge("recall", "respond")
    builder.add_edge("respond", "store")
    builder.add_edge("store", END)
    return builder.compile()
