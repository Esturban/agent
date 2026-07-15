from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from .tools import HOT_TIER_MAX, WARM_TIER_MAX, importance_score, build_context

_llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)


class MemState(TypedDict):
    query: str
    response: str
    hot_tier: list[dict]   # verbatim recent turns — always in context
    warm_tier: list[dict]  # LLM summaries of compacted hot turns
    cold_tier: list[dict]  # oldest summaries; never auto-loaded
    context: str


def load_context(state: MemState) -> dict:
    return {"context": build_context(state["hot_tier"], state["warm_tier"])}


def respond(state: MemState) -> dict:
    system = "You are a helpful assistant with access to the conversation history below.\n\n" + state["context"]
    reply = _llm.invoke([
        {"role": "system", "content": system},
        {"role": "user",   "content": state["query"]},
    ])
    return {"response": reply.content}


def save_turn(state: MemState) -> dict:
    """Append exchange; decay recency of existing hot turns by 10% each step."""
    decayed = [{**t, "recency": t.get("recency", 1.0) * 0.9} for t in state["hot_tier"]]
    decayed.append({"role": "user",      "content": state["query"],    "recency": 1.0})
    decayed.append({"role": "assistant", "content": state["response"], "recency": 0.9})
    return {"hot_tier": decayed}


def compact(state: MemState) -> dict:
    """Lowest-importance hot turns → warm summary; oldest warm blocks → cold archive."""
    hot, warm, cold = list(state["hot_tier"]), list(state["warm_tier"]), list(state["cold_tier"])
    if len(hot) <= HOT_TIER_MAX:
        return {}

    n = len(hot) - HOT_TIER_MAX // 2
    order = sorted(range(len(hot)), key=lambda i: importance_score(hot[i]))
    drop = set(order[:n])
    text = "\n".join(f"{hot[i]['role']}: {hot[i]['content']}" for i in sorted(drop))
    hot  = [t for i, t in enumerate(hot) if i not in drop]

    summary = _llm.invoke([
        {"role": "system", "content": "Summarize in 2-3 sentences, preserving every user fact."},
        {"role": "user",   "content": text},
    ]).content
    warm.append({"summary": summary})

    if len(warm) > WARM_TIER_MAX:
        overflow = len(warm) - WARM_TIER_MAX
        cold.extend(warm[:overflow])
        warm = warm[overflow:]

    return {"hot_tier": hot, "warm_tier": warm, "cold_tier": cold}


def create_workflow():
    g = StateGraph(MemState)
    for name, fn in [("load_context", load_context), ("respond", respond),
                     ("save_turn", save_turn), ("compact", compact)]:
        g.add_node(name, fn)
    g.add_edge(START, "load_context"); g.add_edge("load_context", "respond")
    g.add_edge("respond", "save_turn"); g.add_edge("save_turn", "compact")
    g.add_edge("compact", END)
    return g.compile()
