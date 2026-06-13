from typing import TypedDict

from langgraph.graph import END, StateGraph

from src.tools import evaluate_answer, run_agent


class EvalState(TypedDict):
    question: str
    expected: str
    actual: str
    result: dict


def evaluate_one(state: EvalState) -> EvalState:
    actual = run_agent(state["question"])
    result = evaluate_answer(state["expected"], actual)
    return {**state, "actual": actual, "result": result}


def create_workflow():
    graph = StateGraph(EvalState)
    graph.add_node("evaluate_one", evaluate_one)
    graph.set_entry_point("evaluate_one")
    graph.add_edge("evaluate_one", END)
    return graph.compile()
