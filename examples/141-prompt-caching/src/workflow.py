from langgraph.graph import StateGraph, END
from typing import TypedDict
from .tools import call_no_cache, call_with_cache, compute_savings


class CacheState(TypedDict):
    system_prompt: str
    questions: list[str]
    uncached_results: list
    cached_results: list
    savings: dict


def run_uncached(state: CacheState, config: dict) -> CacheState:
    client = config["configurable"]["client"]
    results = [call_no_cache(state["system_prompt"], q, client) for q in state["questions"]]
    return {**state, "uncached_results": results}


def run_cached(state: CacheState, config: dict) -> CacheState:
    client = config["configurable"]["client"]
    results = [call_with_cache(state["system_prompt"], q, client) for q in state["questions"]]
    return {**state, "cached_results": results}


def compare_node(state: CacheState, config: dict) -> CacheState:
    savings = compute_savings(state["uncached_results"], state["cached_results"])
    return {**state, "savings": savings}


def create_workflow():
    graph = StateGraph(CacheState)
    graph.add_node("uncached", run_uncached)
    graph.add_node("cached", run_cached)
    graph.add_node("compare", compare_node)
    graph.set_entry_point("uncached")
    graph.add_edge("uncached", "cached")
    graph.add_edge("cached", "compare")
    graph.add_edge("compare", END)
    return graph.compile()
