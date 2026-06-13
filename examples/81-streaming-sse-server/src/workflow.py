from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END


class ThinkAnswerState(TypedDict):
    question: str
    answer: str


def think_node(state: ThinkAnswerState) -> dict:
    llm = ChatOpenAI(model="gpt-5-nano")
    messages = [
        SystemMessage(content="Think briefly about the question."),
        HumanMessage(content=state["question"]),
    ]
    response = llm.invoke(messages)
    return {"answer": response.content}


def answer_node(state: ThinkAnswerState) -> dict:
    llm = ChatOpenAI(model="gpt-5-nano")
    messages = [
        SystemMessage(content="Give a final concise answer."),
        HumanMessage(content=state["question"]),
    ]
    final = llm.invoke(messages)
    return {"answer": final.content}


def create_simple_graph():
    graph = StateGraph(ThinkAnswerState)
    graph.add_node("think_node", think_node)
    graph.add_node("answer_node", answer_node)
    graph.add_edge(START, "think_node")
    graph.add_edge("think_node", "answer_node")
    graph.add_edge("answer_node", END)
    return graph.compile()
