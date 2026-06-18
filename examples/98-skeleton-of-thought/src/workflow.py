import operator
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from .tools import SKELETON_PROMPT, EXPAND_PROMPT

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class SoTState(TypedDict):
    question:   str
    skeleton:   list[str]
    # operator.add accumulates one {idx, point, content} dict per parallel expand call.
    # idx is required — parallel execution returns in arbitrary order.
    expansions: Annotated[list[dict], operator.add]
    answer:     str


class PointState(TypedDict):
    question: str
    point:    str
    idx:      int


def make_skeleton(state: SoTState) -> dict:
    """Single LLM call that determines structure — the serial bottleneck before parallelism."""
    reply = _llm.invoke([
        {"role": "user", "content": SKELETON_PROMPT.format(question=state["question"])}
    ])
    points = [l.strip() for l in reply.content.strip().splitlines() if l.strip()]
    return {"skeleton": points}


def dispatch(state: SoTState) -> list[Send]:
    """Fan out one expand call per skeleton point — all fire concurrently."""
    return [
        Send("expand", {"question": state["question"], "point": p, "idx": i})
        for i, p in enumerate(state["skeleton"])
    ]


def expand(state: PointState) -> dict:
    """Expand one point into prose; tag with idx so concatenate can restore order."""
    reply = _llm.invoke([
        {"role": "user", "content": EXPAND_PROMPT.format(
            question=state["question"], point=state["point"]
        )}
    ])
    return {"expansions": [{"idx": state["idx"], "point": state["point"], "content": reply.content.strip()}]}


def concatenate(state: SoTState) -> dict:
    """Sort by idx to undo any out-of-order arrival, then join into the final answer."""
    ordered = sorted(state["expansions"], key=lambda e: e["idx"])
    answer  = "\n\n".join(f"{e['point']}\n{e['content']}" for e in ordered)
    return {"answer": answer}


def create_workflow():
    g = StateGraph(SoTState)
    g.add_node("make_skeleton", make_skeleton)
    g.add_node("expand",        expand)
    g.add_node("concatenate",   concatenate)
    g.add_edge(START, "make_skeleton")
    g.add_conditional_edges("make_skeleton", dispatch, ["expand"])
    g.add_edge("expand",      "concatenate")
    g.add_edge("concatenate", END)
    return g.compile()
