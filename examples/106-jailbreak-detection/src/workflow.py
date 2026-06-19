from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .tools import classify_input

BLOCK_THRESHOLD = 0.6


class DetectionState(TypedDict):
    user_input: str
    category: str
    confidence: float
    reasoning: str
    response: str


def classify_node(state: DetectionState) -> DetectionState:
    result = classify_input(state["user_input"])
    return {
        **state,
        "category": result.get("category", "BENIGN"),
        "confidence": result.get("confidence", 0.0),
        "reasoning": result.get("reasoning", ""),
    }


def route_after_classify(state: DetectionState) -> str:
    if state["category"] != "BENIGN" and state["confidence"] >= BLOCK_THRESHOLD:
        return "block"
    return "respond"


def block_node(state: DetectionState) -> DetectionState:
    return {
        **state,
        "response": f"[BLOCKED] Detected {state['category']} attack (confidence: {state['confidence']:.0%}). {state['reasoning']}",
    }


def respond_node(state: DetectionState) -> DetectionState:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=state["user_input"]),
    ]
    reply = llm.invoke(messages)
    return {**state, "response": reply.content}


def create_workflow():
    graph = StateGraph(DetectionState)
    graph.add_node("classify", classify_node)
    graph.add_node("block", block_node)
    graph.add_node("respond", respond_node)
    graph.set_entry_point("classify")
    graph.add_conditional_edges("classify", route_after_classify, {"block": "block", "respond": "respond"})
    graph.add_edge("block", END)
    graph.add_edge("respond", END)
    return graph.compile()
