import operator
from typing import Annotated, TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from .tools import SAMPLE_DOCS


class State(TypedDict):
    documents: list
    doc: str  # per-branch: set by Send for each worker
    summaries: Annotated[list, operator.add]  # fan-in: all worker results merged here
    final_summary: str


_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def distribute(state: State):
    """Fan-out: dispatch one Send per document."""
    return [Send("summarize", {"doc": doc, "summaries": []}) for doc in state["documents"]]


def summarize(state: State) -> dict:
    """Worker node — runs in parallel for each document."""
    prompt = ChatPromptTemplate.from_messages(
        [("human", "Summarize this in exactly one sentence:\n\n{doc}")]
    )
    s = (prompt | _llm | StrOutputParser()).invoke({"doc": state["doc"]})
    return {"summaries": [s]}


def aggregate(state: State) -> dict:
    """Fan-in: called once after ALL workers finish."""
    bullet_list = "\n".join(f"- {s}" for s in state["summaries"])
    prompt = ChatPromptTemplate.from_messages(
        [("human", "Write a 2-sentence synthesis from these summaries:\n{items}")]
    )
    result = (prompt | _llm | StrOutputParser()).invoke({"items": bullet_list})
    return {"final_summary": result}


def create_workflow():
    g = StateGraph(State)
    g.add_node("summarize", summarize)
    g.add_node("aggregate", aggregate)

    # distribute() returns [Send(...), ...] → LangGraph runs all in parallel
    g.add_conditional_edges(START, distribute, ["summarize"])
    g.add_edge("summarize", "aggregate")
    g.add_edge("aggregate", END)
    return g.compile()
