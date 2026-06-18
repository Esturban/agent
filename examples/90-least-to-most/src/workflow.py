from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

# Least-to-Most Prompting (Zhou et al. 2022 — arxiv.org/abs/2205.10625)
#
# Two-stage strategy that outperforms standard CoT on compositional tasks:
#
# Stage 1 — Decompose: break the problem into ordered sub-questions,
#   easiest first. Each sub-question should require only information already
#   known or solved by a prior sub-question.
#
# Stage 2 — Solve sequentially: answer each sub-question in order, appending
#   all prior (question, answer) pairs as context before the next solve call.
#   This accumulation is the key difference from CoT — the model always "sees"
#   what it has already established.
#
# LangGraph loop: decompose → [solve_next → check_done] → finalize
# The state carries `solutions` and `current_idx` to implement the loop.

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class LtMState(TypedDict):
    problem: str
    subproblems: list[str]  # populated by decompose; ordered easy→hard
    solutions: list[str]    # grows with each iteration of solve_next
    current_idx: int        # index of the sub-problem to solve next
    final_answer: str


def decompose(state: LtMState) -> dict:
    """Stage 1: break the problem into 3-4 ordered sub-problems.

    The ordering matters — easier sub-problems establish facts that harder
    ones depend on. If the model skips order, the context chain breaks.
    """
    prompt = (
        "Break this problem into 3-4 sub-problems ordered from simplest to most complex. "
        "Each sub-problem's answer should contribute toward the final answer.\n\n"
        f"Problem: {state['problem']}\n\n"
        "Return a numbered list of sub-problems only. No solutions yet."
    )
    result = _llm.invoke([HumanMessage(content=prompt)]).content
    # Parse "1. sub-problem text" lines into a clean list.
    subproblems = [
        line.split(". ", 1)[1].strip()
        for line in result.strip().split("\n")
        if line.strip() and ". " in line
    ]
    return {"subproblems": subproblems, "solutions": [], "current_idx": 0}


def solve_next(state: LtMState) -> dict:
    """Stage 2: solve one sub-problem, feeding ALL prior solutions as context.

    This is the core of least-to-most: each call sees the full prior work.
    The `prior_context` grows with each iteration — this is how facts chain.
    """
    idx = state["current_idx"]
    prior_context = "\n".join(
        f"Q{i + 1}: {state['subproblems'][i]}\nA{i + 1}: {state['solutions'][i]}"
        for i in range(idx)
    )
    prompt = (
        f"Original problem: {state['problem']}\n\n"
        + (f"Prior solved steps:\n{prior_context}\n\n" if prior_context else "")
        + f"Now solve: {state['subproblems'][idx]}\n"
        "Give a concise, specific answer."
    )
    answer = _llm.invoke([HumanMessage(content=prompt)]).content.strip()
    # Immutable update: append to solutions list, advance index.
    return {
        "solutions": list(state["solutions"]) + [answer],
        "current_idx": idx + 1,
    }


def check_done(state: LtMState) -> str:
    """Router: keep looping through sub-problems or move to finalize."""
    return "solve_next" if state["current_idx"] < len(state["subproblems"]) else "finalize"


def finalize(state: LtMState) -> dict:
    """Synthesize the final answer from all accumulated sub-problem solutions."""
    steps = "\n".join(
        f"Step {i + 1} ({state['subproblems'][i]}): {s}"
        for i, s in enumerate(state["solutions"])
    )
    prompt = (
        f"Problem: {state['problem']}\n\n"
        f"Solved steps:\n{steps}\n\n"
        "State the final answer clearly and concisely."
    )
    answer = _llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return {"final_answer": answer}


def create_workflow():
    builder = StateGraph(LtMState)
    builder.add_node("decompose", decompose)
    builder.add_node("solve_next", solve_next)
    builder.add_node("finalize", finalize)

    builder.add_edge(START, "decompose")
    builder.add_edge("decompose", "solve_next")
    # Conditional loop: solve_next feeds back into itself until all sub-problems
    # are solved, then routes to finalize.
    builder.add_conditional_edges("solve_next", check_done, ["solve_next", "finalize"])
    builder.add_edge("finalize", END)
    return builder.compile()
