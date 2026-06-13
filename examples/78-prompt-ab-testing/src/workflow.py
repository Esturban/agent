from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from src.tools import VARIANT_A_PROMPT, VARIANT_B_PROMPT, score_response


class ABState(TypedDict):
    question: str
    response_a: str
    response_b: str
    score_a: float
    score_b: float


def run_variant_a(state: ABState) -> ABState:
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    prompt = VARIANT_A_PROMPT.format(question=state["question"])
    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content.strip()
    return {**state, "response_a": text, "score_a": score_response(text)}


def run_variant_b(state: ABState) -> ABState:
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    prompt = VARIANT_B_PROMPT.format(question=state["question"])
    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content.strip()
    return {**state, "response_b": text, "score_b": score_response(text)}


def create_workflow():
    graph = StateGraph(ABState)
    graph.add_node("run_variant_a", run_variant_a)
    graph.add_node("run_variant_b", run_variant_b)
    graph.set_entry_point("run_variant_a")
    graph.add_edge("run_variant_a", "run_variant_b")
    graph.add_edge("run_variant_b", END)
    return graph.compile()
