import operator
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from src.tools import PERSONAS

# Ref: Wang et al. 2024 — "Mixture-of-Agents Enhances Large Language Model Capabilities"
# arxiv.org/abs/2406.04692
#
# Pattern: fan out to N proposers in parallel → aggregate into one final answer.
# Annotated[list[str], operator.add] is the key: each parallel branch *appends*
# to the list instead of overwriting it, so no branch's output is lost.

_proposer_llm   = ChatOpenAI(model="gpt-5.4-nano", temperature=0.7)  # diversity via temp
_aggregator_llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)    # deterministic synthesis


class MoAState(TypedDict):
    question: str
    # operator.add merges proposals from parallel branches: [] + ["A"] + ["B"] = ["A", "B"]
    proposals: Annotated[list[str], operator.add]
    final_answer: str


class ProposerState(TypedDict):
    question: str
    persona: dict  # {"name": str, "system": str}


def dispatch(state: MoAState) -> list[Send]:
    """Fan out: one Send per persona — all proposer nodes run in parallel."""
    return [
        Send("proposer", {"question": state["question"], "persona": p})
        for p in PERSONAS
    ]


def proposer(state: ProposerState) -> dict:
    """One proposer: answer the question from the persona's perspective."""
    msgs = [
        SystemMessage(content=state["persona"]["system"]),
        HumanMessage(content=state["question"]),
    ]
    reply = _proposer_llm.invoke(msgs).content
    # Wrap in list so operator.add can merge it into the parent proposals list.
    return {"proposals": [f"[{state['persona']['name']}]\n{reply}"]}


def aggregate(state: MoAState) -> dict:
    """Synthesise all proposer outputs into one comprehensive final answer."""
    joined = "\n\n---\n\n".join(state["proposals"])
    prompt = (
        f"You received {len(state['proposals'])} independent perspectives on:\n"
        f"'{state['question']}'\n\n{joined}\n\n"
        "Synthesise these into a single, comprehensive, well-structured answer. "
        "Preserve the best insights from each perspective."
    )
    answer = _aggregator_llm.invoke([HumanMessage(content=prompt)]).content
    return {"final_answer": answer}


def create_workflow():
    builder = StateGraph(MoAState)
    builder.add_node("proposer", proposer)
    builder.add_node("aggregate", aggregate)
    # add_conditional_edges from START: dispatch() decides which nodes to Send to.
    builder.add_conditional_edges(START, dispatch, ["proposer"])
    builder.add_edge("proposer", "aggregate")
    builder.add_edge("aggregate", END)
    return builder.compile()
