from langgraph.graph import StateGraph, END
from typing import TypedDict
from .tools import SemanticCache, embed, ask_llm


class SemanticCacheState(TypedDict):
    queries: list[str]
    threshold: float
    responses: list[dict]
    cache_stats: dict


def process_queries(state: SemanticCacheState, config: dict) -> SemanticCacheState:
    client = config["configurable"]["client"]
    cache = SemanticCache(threshold=state.get("threshold", 0.92))
    responses = []
    for query in state["queries"]:
        vec = embed(query, client)
        cached = cache.get(vec)
        if cached:
            responses.append({"query": query, "response": cached, "source": "cache", "latency_ms": 0})
        else:
            answer, latency = ask_llm(query, client)
            cache.set(vec, answer)
            responses.append({"query": query, "response": answer, "source": "llm", "latency_ms": latency})
    return {**state, "responses": responses, "cache_stats": cache.stats()}


def create_workflow():
    graph = StateGraph(SemanticCacheState)
    graph.add_node("process", process_queries)
    graph.set_entry_point("process")
    graph.add_edge("process", END)
    return graph.compile()
