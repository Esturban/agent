from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI


class SupervisorState(TypedDict):
    question: str
    next: str
    answer: str


def supervisor_node(state: SupervisorState) -> dict:
    llm = ChatOpenAI(model="gpt-5-nano")
    response = llm.invoke([
        {"role": "system", "content": "Classify the question into exactly one word: math, history, or science."},
        {"role": "user", "content": state["question"]},
    ])
    return {"next": response.content.strip().lower()}


def math_agent(state: SupervisorState) -> dict:
    llm = ChatOpenAI(model="gpt-5-nano")
    response = llm.invoke([
        {"role": "system", "content": "You are a math expert. Answer concisely."},
        {"role": "user", "content": state["question"]},
    ])
    return {"answer": response.content, "next": "END"}


def history_agent(state: SupervisorState) -> dict:
    llm = ChatOpenAI(model="gpt-5-nano")
    response = llm.invoke([
        {"role": "system", "content": "You are a history expert. Answer concisely."},
        {"role": "user", "content": state["question"]},
    ])
    return {"answer": response.content, "next": "END"}


def science_agent(state: SupervisorState) -> dict:
    llm = ChatOpenAI(model="gpt-5-nano")
    response = llm.invoke([
        {"role": "system", "content": "You are a science expert. Answer concisely."},
        {"role": "user", "content": state["question"]},
    ])
    return {"answer": response.content, "next": "END"}


def create_workflow():
    graph = StateGraph(SupervisorState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("math_agent", math_agent)
    graph.add_node("history_agent", history_agent)
    graph.add_node("science_agent", science_agent)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        lambda s: s["next"],
        {"math": "math_agent", "history": "history_agent", "science": "science_agent"},
    )
    graph.add_edge("math_agent", END)
    graph.add_edge("history_agent", END)
    graph.add_edge("science_agent", END)

    return graph.compile()
