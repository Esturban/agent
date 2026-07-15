"""Red-team pipeline: N parallel attack chains, each attack_and_judge in one node.

Uses Send() fan-out so all N attacks run concurrently — same pattern as examples 89/97/98.
Results accumulate via operator.add reducer; summarise computes the attack success rate (ASR).
"""

import json
import operator
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from .tools import (
    ATTACKER_SYSTEM, JUDGE_SYSTEM, N_ATTACKS, TARGET_SYSTEM,
    attacker_llm, judge_llm, target_llm,
)


class RTState(TypedDict):
    goal: str
    results: Annotated[list[dict], operator.add]
    attack_success_rate: float


class AttackState(TypedDict):
    goal: str
    idx: int


def dispatch(state: RTState) -> list[Send]:
    # Fan out N independent attack chains in parallel.
    return [Send("attack_and_judge", {"goal": state["goal"], "idx": i}) for i in range(N_ATTACKS)]


def attack_and_judge(state: AttackState) -> dict:
    # Step 1: attacker generates an adversarial prompt.
    attack_prompt = attacker_llm.invoke([
        SystemMessage(content=ATTACKER_SYSTEM),
        HumanMessage(content=f"Goal: {state['goal']}\nGenerate adversarial prompt #{state['idx'] + 1}:"),
    ]).content.strip()

    # Step 2: target responds (the system under test).
    target_response = target_llm.invoke([
        SystemMessage(content=TARGET_SYSTEM),
        HumanMessage(content=attack_prompt),
    ]).content.strip()

    # Step 3: judge scores the exchange.
    raw = judge_llm.invoke([
        SystemMessage(content=JUDGE_SYSTEM),
        HumanMessage(content=f"Prompt: {attack_prompt}\n\nResponse: {target_response}"),
    ]).content
    s, e = raw.find("{"), raw.rfind("}") + 1
    try:
        verdict = json.loads(raw[s:e]) if s >= 0 else {}
        if not isinstance(verdict.get("success"), bool) or not isinstance(verdict.get("reason"), str):
            raise ValueError("invalid judge verdict")
    except (json.JSONDecodeError, ValueError):
        verdict = {"success": False, "reason": "invalid judge verdict"}

    return {"results": [{"attack": attack_prompt[:80], **verdict}]}


def summarise(state: RTState) -> dict:
    asr = sum(1 for r in state["results"] if r["success"]) / len(state["results"])
    return {"attack_success_rate": round(asr, 2)}


def create_workflow():
    g = StateGraph(RTState)
    g.add_node("attack_and_judge", attack_and_judge)
    g.add_node("summarise", summarise)
    g.add_conditional_edges(START, dispatch, ["attack_and_judge"])
    g.add_edge("attack_and_judge", "summarise")
    g.add_edge("summarise", END)
    return g.compile()
