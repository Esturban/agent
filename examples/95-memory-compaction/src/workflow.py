from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from .tools import HOT_TIER_MAX, WARM_TIER_MAX, importance_score, build_context

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class MemState(TypedDict):
    query: str
    response: str
    # hot: verbatim recent turns — always injected into context
    hot_tier: list[dict]
    # warm: LLM-generated summaries of compacted hot turns
    warm_tier: list[dict]
    # cold: oldest summaries archived when warm overflows; never auto-loaded
    cold_tier: list[dict]
    context: str


def load_context(state: MemState) -> dict:
    """Assemble system context: warm summaries first, then verbatim hot turns."""
    return {"context": build_context(state["hot_tier"], state["warm_tier"])}


def respond(state: MemState) -> dict:
    """Answer the query using assembled memory context as the system prompt."""
    system = "You are a helpful assistant with access to the conversation history below.\n\n" + state["context"]
    reply = _llm.invoke([
        {"role": "system", "content": system},
        {"role": "user", "content": state["query"]},
    ])
    return {"response": reply.content}


def save_turn(state: MemState) -> dict:
    """Append current exchange; decay recency of existing hot turns by 10% each step."""
    decayed = [{**t, "recency": t.get("recency", 1.0) * 0.9} for t in state["hot_tier"]]
    decayed.append({"role": "user",      "content": state["query"],    "recency": 1.0})
    decayed.append({"role": "assistant", "content": state["response"], "recency": 0.9})
    return {"hot_tier": decayed}


def compact(state: MemState) -> dict:
    """Move hot → warm when hot overflows; move warm → cold when warm overflows.

    Importance = recency × boost. Lowest-importance turns are summarized first,
    so high-signal turns ('remember that…') stay verbatim in hot longer.
    """
    hot  = list(state["hot_tier"])
    warm = list(state["warm_tier"])
    cold = list(state["cold_tier"])

    if len(hot) <= HOT_TIER_MAX:
        return {}  # nothing to do

    # Identify the n least-important turns to compact.
    n_to_compact = len(hot) - HOT_TIER_MAX // 2
    order = sorted(range(len(hot)), key=lambda i: importance_score(hot[i]))
    compact_set = set(order[:n_to_compact])
    to_compact = [hot[i] for i in sorted(compact_set)]
    hot        = [t for i, t in enumerate(hot) if i not in compact_set]

    # Summarize the compacted turns into a single warm block.
    text = "\n".join(f"{t['role']}: {t['content']}" for t in to_compact)
    summary = _llm.invoke([
        {"role": "system", "content": "Summarize this conversation excerpt in 2-3 sentences, preserving every key fact mentioned by the user."},
        {"role": "user",   "content": text},
    ]).content
    warm.append({"summary": summary})

    # When warm overflows, archive the oldest blocks to cold.
    if len(warm) > WARM_TIER_MAX:
        overflow = len(warm) - WARM_TIER_MAX
        cold.extend(warm[:overflow])
        warm = warm[overflow:]

    return {"hot_tier": hot, "warm_tier": warm, "cold_tier": cold}


def create_workflow():
    g = StateGraph(MemState)
    g.add_node("load_context", load_context)
    g.add_node("respond",      respond)
    g.add_node("save_turn",    save_turn)
    g.add_node("compact",      compact)
    g.add_edge(START,          "load_context")
    g.add_edge("load_context", "respond")
    g.add_edge("respond",      "save_turn")
    g.add_edge("save_turn",    "compact")
    g.add_edge("compact",      END)
    return g.compile()
