from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import MemoryStore

# Three-tier memory architecture — Tulving (1972) + MemGPT (Packer et al. 2023)
# arxiv.org/abs/2310.08560
#
# Each tier has a different storage and retrieval strategy:
#   Episodic   → append-only log; retrieve by recency (last N entries)
#   Semantic   → key-value facts; retrieve by key lookup
#   Procedural → always-on rules; prepend ALL to system prompt every turn

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

_CLASSIFIER_PROMPT = """Classify the following user input into ONE memory tier.
Reply with exactly one word: episodic, semantic, or procedural.

- episodic:   a past event or interaction ("we discussed X last time")
- semantic:   a fact about the user or world ("my name is Alex", "Python is fast")
- procedural: a rule about how the agent should behave ("always use bullet points")

Input: {text}
Classification:"""


class AgentState(TypedDict):
    memory: MemoryStore
    query: str
    answer: str


def classify_and_store(state: AgentState) -> dict:
    """LLM classifies the query; if it's a new fact/rule, store it in the right tier."""
    tier = _llm.invoke([
        HumanMessage(content=_CLASSIFIER_PROMPT.format(text=state["query"]))
    ]).content.strip().lower()

    memory = dict(state["memory"])  # shallow copy — don't mutate state in place

    if tier == "episodic":
        memory["episodic"] = list(memory["episodic"]) + [f"User said: {state['query']}"]
    elif tier == "semantic":
        # Simple extraction: treat the query as a fact to remember verbatim.
        # A production version would parse "my name is X" → {"name": "X"}.
        memory["semantic"] = {**memory["semantic"], "last_fact": state["query"]}
    elif tier == "procedural":
        memory["procedural"] = list(memory["procedural"]) + [state["query"]]

    return {"memory": memory}


def respond(state: AgentState) -> dict:
    """Build a system prompt from all three memory tiers and generate an answer."""
    m = state["memory"]
    # Procedural rules always come first — they govern how the agent behaves.
    rules     = "\n".join(f"  • {r}" for r in m["procedural"])
    facts     = "\n".join(f"  {k}: {v}" for k, v in m["semantic"].items())
    # Episodic: only the last 5 events to avoid context bloat.
    recent    = "\n".join(f"  - {e}" for e in m["episodic"][-5:])

    system = (
        f"Behavioural rules (ALWAYS follow these):\n{rules}\n\n"
        f"Known facts about the user:\n{facts}\n\n"
        f"Recent conversation history:\n{recent or '  (none)'}"
    )
    answer = _llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=state["query"]),
    ]).content
    return {"answer": answer}


def create_workflow():
    builder = StateGraph(AgentState)
    builder.add_node("classify_and_store", classify_and_store)
    builder.add_node("respond",            respond)
    builder.add_edge(START,                "classify_and_store")
    builder.add_edge("classify_and_store", "respond")
    builder.add_edge("respond",            END)
    return builder.compile()
