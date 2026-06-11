from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from .tools import (
    JUDGE_SYSTEM,
    MAX_ROUNDS,
    SOLVER_A_SYSTEM,
    SOLVER_B_SYSTEM,
    DebateState,
    llm,
)


def solve_a(state: DebateState) -> dict:
    if state.get("critique_a"):
        content = (
            f"Topic: {state['topic']}\n\n"
            f"Your current position: {state['position_a']}\n\n"
            f"Opponent's critique of your argument: {state['critique_a']}\n\n"
            "Refine your argument, addressing the critique:"
        )
    else:
        content = f"Topic: {state['topic']}\n\nPresent your opening argument FOR SPECIALIZATION:"
    result = llm.invoke([SystemMessage(SOLVER_A_SYSTEM), HumanMessage(content)])
    return {"position_a": result.content}


def solve_b(state: DebateState) -> dict:
    if state.get("critique_b"):
        content = (
            f"Topic: {state['topic']}\n\n"
            f"Your current position: {state['position_b']}\n\n"
            f"Opponent's critique of your argument: {state['critique_b']}\n\n"
            "Refine your argument, addressing the critique:"
        )
    else:
        content = f"Topic: {state['topic']}\n\nPresent your opening argument FOR GENERALIZATION:"
    result = llm.invoke([SystemMessage(SOLVER_B_SYSTEM), HumanMessage(content)])
    return {"position_b": result.content}


def debate(state: DebateState) -> dict:
    crit_a_content = (
        f"Topic: {state['topic']}\n\n"
        f"Opponent argues: {state['position_b']}\n\n"
        "Write a 2-sentence critique of the opponent's argument:"
    )
    crit_b_content = (
        f"Topic: {state['topic']}\n\n"
        f"Opponent argues: {state['position_a']}\n\n"
        "Write a 2-sentence critique of the opponent's argument:"
    )
    critique_a = llm.invoke([SystemMessage(SOLVER_A_SYSTEM), HumanMessage(crit_a_content)])
    critique_b = llm.invoke([SystemMessage(SOLVER_B_SYSTEM), HumanMessage(crit_b_content)])
    return {
        "critique_a": critique_a.content,
        "critique_b": critique_b.content,
        "round": state.get("round", 0) + 1,
    }


def should_continue(state: DebateState) -> str:
    return "solve_a" if state.get("round", 0) < MAX_ROUNDS else "judge"


def judge(state: DebateState) -> dict:
    content = (
        f"Topic: {state['topic']}\n\n"
        f"POSITION A (Specialization):\n{state['position_a']}\n\n"
        f"POSITION B (Generalization):\n{state['position_b']}"
    )
    result = llm.invoke([SystemMessage(JUDGE_SYSTEM), HumanMessage(content)])
    return {"verdict": result.content}


def create_workflow():
    graph = StateGraph(DebateState)
    graph.add_node("solve_a", solve_a)
    graph.add_node("solve_b", solve_b)
    graph.add_node("debate", debate)
    graph.add_node("judge", judge)

    graph.set_entry_point("solve_a")
    graph.add_edge("solve_a", "solve_b")
    graph.add_edge("solve_b", "debate")
    graph.add_conditional_edges("debate", should_continue, {"solve_a": "solve_a", "judge": "judge"})
    graph.add_edge("judge", END)
    return graph.compile()
