from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from .tools import (
    EXECUTOR_SYSTEM,
    PLANNER_SYSTEM,
    SYNTHESIZER_SYSTEM,
    PlanState,
    llm,
    planner_llm,
)


def planner(state: PlanState) -> dict:
    plan = planner_llm.invoke(
        [
            SystemMessage(PLANNER_SYSTEM),
            HumanMessage(state["task"]),
        ]
    )
    return {"steps": [s.step for s in plan.steps], "results": []}


def executor(state: PlanState) -> dict:
    step = state["steps"][0]
    prior = "\n".join(f"Step result: {r}" for r in state["results"])
    prompt = (
        f"Task context: {state['task']}\n\nPrior results:\n{prior}\n\nExecute this step: {step}"
    )
    result = llm.invoke([SystemMessage(EXECUTOR_SYSTEM), HumanMessage(prompt)])
    print(f"  ✓ {step[:60]}...")
    return {"steps": state["steps"][1:], "results": [result.content]}


def synthesizer(state: PlanState) -> dict:
    steps_and_results = "\n".join(f"Step {i + 1}: {r}" for i, r in enumerate(state["results"]))
    prompt = f"Task: {state['task']}\n\nCompleted steps:\n{steps_and_results}"
    answer = llm.invoke([SystemMessage(SYNTHESIZER_SYSTEM), HumanMessage(prompt)])
    return {"final_answer": answer.content}


def should_continue(state: PlanState) -> str:
    return "executor" if state["steps"] else "synthesizer"


def create_workflow():
    graph = StateGraph(PlanState)
    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_node("synthesizer", synthesizer)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_conditional_edges(
        "executor", should_continue, {"executor": "executor", "synthesizer": "synthesizer"}
    )
    graph.add_edge("synthesizer", END)
    return graph.compile()
