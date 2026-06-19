from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from .tools import attacker_call, target_call, judge_call, MAX_ITER, THRESHOLD


class PAIRState(TypedDict):
    iteration: int
    attack_history: list[dict]
    current_prompt: str
    current_strategy: str
    target_response: str
    judge_score: int
    judge_explanation: str
    scores: list[int]
    converged: bool


def attacker_node(state: PAIRState) -> PAIRState:
    history = state["attack_history"]
    result = attacker_call(history)
    return {
        **state,
        "current_prompt": result.get("prompt", ""),
        "current_strategy": result.get("strategy", ""),
    }


def target_node(state: PAIRState) -> PAIRState:
    response = target_call(state["current_prompt"])
    return {**state, "target_response": response}


def judge_node(state: PAIRState) -> PAIRState:
    verdict = judge_call(state["current_prompt"], state["target_response"])
    score = verdict.get("score", 1)
    explanation = verdict.get("explanation", "")
    what_worked = verdict.get("what_worked", "")

    new_history = state["attack_history"] + [
        {"role": "user", "content": f"Iteration {state['iteration']} feedback:\nScore: {score}/10\n{explanation}\nWhat worked: {what_worked}\n\nRefine your attack prompt."}
    ]

    converged = score >= THRESHOLD or state["iteration"] >= MAX_ITER
    return {
        **state,
        "iteration": state["iteration"] + 1,
        "attack_history": new_history,
        "judge_score": score,
        "judge_explanation": explanation,
        "scores": state["scores"] + [score],
        "converged": converged,
    }


def should_continue(state: PAIRState) -> str:
    return END if state["converged"] else "attacker"


def create_workflow():
    graph = StateGraph(PAIRState)
    graph.add_node("attacker", attacker_node)
    graph.add_node("target", target_node)
    graph.add_node("judge", judge_node)
    graph.set_entry_point("attacker")
    graph.add_edge("attacker", "target")
    graph.add_edge("target", "judge")
    graph.add_conditional_edges("judge", should_continue)
    return graph.compile()
