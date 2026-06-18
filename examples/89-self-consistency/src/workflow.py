import operator
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from src.tools import N_PATHS

# Self-Consistency (Wang et al. 2022 — arxiv.org/abs/2203.11171)
#
# Core insight: asking the same question N times at temperature > 0 produces
# different reasoning paths — but CORRECT answers cluster more than wrong ones.
# Majority vote over N paths is more reliable than any single greedy decode.
#
# Accuracy gains from the paper:
#   GSM8K:  56% (CoT greedy) → 74% (self-consistency N=40)
#   MATH:   +15-20 points over single-pass CoT
#
# LangGraph pattern: same Send() fan-out as MoA (example 86) but ALL branches
# receive IDENTICAL input. Difference from MoA: we count answers, not synthesise.

# temperature=0.7 ensures different reasoning traces even with identical prompts.
_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Aggregator uses temp=0 for deterministic majority-vote extraction.
_aggregator = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class SCState(TypedDict):
    question: str
    # Annotated[list, operator.add]: each parallel branch appends its result
    # instead of overwriting — same reducer pattern as MoA (example 86).
    reasoning_paths: Annotated[list[str], operator.add]
    final_answer: str


class PathState(TypedDict):
    question: str  # same question sent to every path


def dispatch(state: SCState) -> list[Send]:
    """Fan out: send the SAME question to N_PATHS independent reason nodes.

    Unlike MoA, every branch gets IDENTICAL input — diversity comes only from
    temperature sampling, not different personas or prompts.
    """
    return [Send("reason", {"question": state["question"]}) for _ in range(N_PATHS)]


def reason(state: PathState) -> dict:
    """Generate one chain-of-thought reasoning path at temperature > 0.

    The step-by-step instruction matters: it forces explicit intermediate work
    before the final answer, making extraction more reliable in aggregation.
    """
    prompt = (
        "Think step by step, then clearly state your final answer on the last line "
        "prefixed with 'Final answer:'.\n\n"
        f"Problem: {state['question']}"
    )
    reply = _llm.invoke([HumanMessage(content=prompt)]).content
    # Wrap in list so operator.add merges it into the parent state's list.
    return {"reasoning_paths": [reply]}


def aggregate(state: SCState) -> dict:
    """Extract final answers from all N paths and return the majority vote.

    An LLM extractor handles paraphrase ('60 mph' vs '60 miles per hour')
    more robustly than regex. Aggregator runs at temp=0 for consistency.
    """
    paths_text = "\n\n---\n\n".join(
        f"Path {i + 1}:\n{p}" for i, p in enumerate(state["reasoning_paths"])
    )
    prompt = (
        f"Here are {len(state['reasoning_paths'])} independent solutions:\n\n"
        f"{paths_text}\n\n"
        "Extract the final answer from each path. "
        "Return ONLY the most common answer (majority vote). No explanation."
    )
    vote = _aggregator.invoke([HumanMessage(content=prompt)]).content.strip()
    return {"final_answer": vote}


def create_workflow():
    builder = StateGraph(SCState)
    builder.add_node("reason", reason)
    builder.add_node("aggregate", aggregate)
    # dispatch() returns a list of Send objects — one per path — that all
    # route to "reason" and execute in parallel.
    builder.add_conditional_edges(START, dispatch, ["reason"])
    builder.add_edge("reason", "aggregate")
    builder.add_edge("aggregate", END)
    return builder.compile()
