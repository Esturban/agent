from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.types import Send

from .tools import (
    BRANCH_PROMPT,
    N_BRANCHES,
    SCORE_PROMPT,
    SYNTHESIS_PROMPT,
    BranchState,
    ToTState,
    judge_llm,
    llm,
)


def generate_branches(state: ToTState) -> list[Send]:
    """Fan out N branches using the Send API."""
    return [
        Send(
            "score_branch", {"problem": state["problem"], "branch_id": i, "thought": "", "score": 0}
        )
        for i in range(N_BRANCHES)
    ]


def score_branch(state: BranchState) -> dict:
    """Generate thought for this branch, then score it."""
    # Generate thought
    branch_prompt = BRANCH_PROMPT.format(
        branch_id=state["branch_id"] + 1,
        n_branches=N_BRANCHES,
        problem=state["problem"],
    )
    thought_result = llm.invoke([HumanMessage(content=branch_prompt)])
    thought = thought_result.content.strip()

    # Score thought
    score_prompt = SCORE_PROMPT.format(problem=state["problem"], thought=thought)
    score_result = judge_llm.invoke([HumanMessage(content=score_prompt)])
    try:
        score = int("".join(filter(str.isdigit, score_result.content.strip()))[:2])
        score = min(10, max(0, score))
    except (ValueError, IndexError):
        score = 5
    print(f"  Branch {state['branch_id'] + 1}: score={score}/10 | {thought[:60]}...")
    # Return as a dict to be accumulated by the `branches` reducer
    return {"branches": [{"branch_id": state["branch_id"], "thought": thought, "score": score}]}


def select_best(state: ToTState) -> dict:
    """Pick highest-scoring branch."""
    best = max(state["branches"], key=lambda b: b["score"])
    print(f"  Best branch: {best['branch_id'] + 1} (score={best['score']}/10)")
    return {"best_thought": best["thought"]}


def synthesize(state: ToTState) -> dict:
    """Expand best thought into final answer."""
    prompt = SYNTHESIS_PROMPT.format(
        problem=state["problem"],
        thought=state["best_thought"],
        n=N_BRANCHES,
    )
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"final_answer": result.content}


def create_workflow():
    graph = StateGraph(ToTState)
    graph.add_node("score_branch", score_branch)
    graph.add_node("select_best", select_best)
    graph.add_node("synthesize", synthesize)
    graph.set_conditional_entry_point(generate_branches, {"score_branch": "score_branch"})
    graph.add_edge("score_branch", "select_best")
    graph.add_edge("select_best", "synthesize")
    graph.add_edge("synthesize", END)
    return graph.compile()
