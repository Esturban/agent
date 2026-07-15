from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import HAZARD_CATEGORIES

# Safety Guardrails — LlamaGuard pattern (Inan et al. 2023)
# arxiv.org/abs/2312.06674
#
# LlamaGuard is a fine-tuned Llama model that classifies inputs/outputs as
# SAFE or UNSAFE against a configurable policy (S1-S6 hazard taxonomy).
#
# This example implements the same GRAPH PATTERN using an OpenAI classifier
# prompt so it runs without extra dependencies. Swap in the real LlamaGuard
# (via Groq `llama-guard-3-8b`, Ollama, or Together AI) for production —
# the graph structure and routing logic stay identical.
#
# Key principle: the guard node runs BEFORE the agent node. Unsafe inputs
# never reach the reasoning model — they are refused at the gate.
#
# Graph: START → classify → (safe → respond) | (unsafe → refuse) → END

# Two separate LLM instances for clarity:
# guard uses a system prompt focused on classification only.
# agent answers questions — it never sees unsafe inputs.
_guard_llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
_agent_llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)

_GUARD_SYSTEM = """You are a content safety classifier. Classify the user message as safe or unsafe.

Unsafe categories:
S1: Violent Crimes  S2: Non-Violent Crimes  S3: Sex-Related Crimes
S4: Child Exploitation  S5: Defamation/Privacy  S6: Weapons/Bio/Chem/Nuclear Hazards

Respond with EXACTLY one of:
  safe
  unsafe S<N>

No other text."""


class GuardrailState(TypedDict):
    query: str
    classification: str   # "SAFE" or "UNSAFE"
    hazard_category: str  # e.g. "S6" if unsafe, "" if safe
    response: str


def classify(state: GuardrailState) -> dict:
    """Run the safety classifier before the query reaches the agent.

    This is the guard node — it classifies EVERY input against the policy.
    In production you would use LlamaGuard or NeMo Guardrails here; the
    structure of this node is identical regardless of the underlying model.
    """
    result = _guard_llm.invoke([
        SystemMessage(content=_GUARD_SYSTEM),
        HumanMessage(content=state["query"]),
    ]).content.strip().lower()

    if result.startswith("unsafe"):
        parts = result.split()
        category = parts[1].upper() if len(parts) > 1 else "S0"
        return {"classification": "UNSAFE", "hazard_category": category}
    if result == "safe":
        return {"classification": "SAFE", "hazard_category": ""}
    return {"classification": "UNSAFE", "hazard_category": "S0"}


def route_after_guard(state: GuardrailState) -> str:
    """Conditional router: SAFE inputs go to respond; UNSAFE go to refuse.

    This is the decision point — the graph branches here. The agent node
    ('respond') is only reachable via the SAFE path.
    """
    return "respond" if state["classification"] == "SAFE" else "refuse"


def respond(state: GuardrailState) -> dict:
    """Normal agent response — only reachable for inputs that passed the guard."""
    answer = _agent_llm.invoke([HumanMessage(content=state["query"])]).content.strip()
    return {"response": answer}


def refuse(state: GuardrailState) -> dict:
    """Policy refusal — do not reveal the specific hazard category to the user.

    Exposing the category could help adversaries craft inputs that evade
    detection. Return a generic refusal instead.
    """
    return {"response": "I can't assist with that request as it may violate safety policies."}


def create_workflow():
    builder = StateGraph(GuardrailState)
    builder.add_node("classify", classify)
    builder.add_node("respond", respond)
    builder.add_node("refuse", refuse)

    builder.add_edge(START, "classify")
    # Conditional branch after guard: route_after_guard() returns "respond" or "refuse".
    builder.add_conditional_edges("classify", route_after_guard, ["respond", "refuse"])
    builder.add_edge("respond", END)
    builder.add_edge("refuse", END)
    return builder.compile()
