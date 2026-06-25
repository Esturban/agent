from langgraph.graph import StateGraph, END
from typing import TypedDict
from .tools import ask_vision


class VisionState(TypedDict):
    image_source: str
    question: str
    answer: str


def answer_node(state: VisionState, config: dict) -> VisionState:
    client = config["configurable"]["client"]
    model = config["configurable"].get("model", "gpt-4o-mini")
    answer = ask_vision(state["image_source"], state["question"], client, model)
    return {**state, "answer": answer}


def create_workflow():
    graph = StateGraph(VisionState)
    graph.add_node("answer", answer_node)
    graph.set_entry_point("answer")
    graph.add_edge("answer", END)
    return graph.compile()
