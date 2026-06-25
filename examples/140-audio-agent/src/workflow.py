from langgraph.graph import StateGraph, END
from typing import TypedDict
from .tools import transcribe, classify_and_extract, route


class AudioState(TypedDict):
    audio_path: str
    transcript: str
    analysis: dict
    queue: str


def transcribe_node(state: AudioState, config: dict) -> AudioState:
    client = config["configurable"]["client"]
    transcript = transcribe(state["audio_path"], client)
    return {**state, "transcript": transcript}


def analyze_node(state: AudioState, config: dict) -> AudioState:
    client = config["configurable"]["client"]
    model = config["configurable"].get("model", "gpt-4o-mini")
    analysis = classify_and_extract(state["transcript"], client, model)
    return {**state, "analysis": analysis}


def route_node(state: AudioState, config: dict) -> AudioState:
    intent = state["analysis"].get("intent", "general")
    return {**state, "queue": route(intent)}


def create_workflow():
    graph = StateGraph(AudioState)
    graph.add_node("transcribe", transcribe_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("route", route_node)
    graph.set_entry_point("transcribe")
    graph.add_edge("transcribe", "analyze")
    graph.add_edge("analyze", "route")
    graph.add_edge("route", END)
    return graph.compile()
