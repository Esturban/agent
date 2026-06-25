from langgraph.graph import StateGraph, END
from typing import TypedDict
from .tools import compress, count_tokens


class CompressionState(TypedDict):
    chunks: list[str]
    query: str
    ratio: float
    original_tokens: int
    compressed_context: str
    compressed_tokens: int
    answer: str


def compress_node(state: CompressionState, config: dict) -> CompressionState:
    client = config["configurable"]["client"]
    ratio = state.get("ratio", 0.4)
    original_text = " ".join(state["chunks"])
    original_tokens = count_tokens(original_text)
    compressed = compress(state["chunks"], state["query"], client, ratio)
    return {
        **state,
        "original_tokens": original_tokens,
        "compressed_context": compressed,
        "compressed_tokens": count_tokens(compressed),
    }


def answer_node(state: CompressionState, config: dict) -> CompressionState:
    client = config["configurable"]["client"]
    model = config["configurable"].get("model", "gpt-4o-mini")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Context:\n{state['compressed_context']}"},
            {"role": "user", "content": state["query"]},
        ],
        max_tokens=256,
    )
    return {**state, "answer": resp.choices[0].message.content}


def create_workflow():
    graph = StateGraph(CompressionState)
    graph.add_node("compress", compress_node)
    graph.add_node("answer", answer_node)
    graph.set_entry_point("compress")
    graph.add_edge("compress", "answer")
    graph.add_edge("answer", END)
    return graph.compile()
