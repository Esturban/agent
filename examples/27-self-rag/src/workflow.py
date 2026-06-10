from typing import TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from .tools import build_retriever


class State(TypedDict):
    question: str
    documents: list
    generation: str
    should_retrieve: bool
    supported: bool


class BoolDecision(BaseModel):
    answer: bool


_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
_retriever = build_retriever()


def classify(state: State) -> dict:
    """Gate 1 — should we retrieve at all?"""
    result = _llm.with_structured_output(BoolDecision).invoke(
        f"Should I search a knowledge base to answer: '{state['question']}'? "
        "Say false for math, greetings, or simple facts the model already knows well."
    )
    return {"should_retrieve": result.answer}


def retrieve(state: State) -> dict:
    return {"documents": _retriever.invoke(state["question"])}


def grade_docs(state: State) -> dict:
    """Gate 2 — keep only relevant documents (isRelevant)."""
    relevant = [
        d
        for d in state["documents"]
        if _llm.with_structured_output(BoolDecision)
        .invoke(
            f"Is this document relevant to answering the question?\n"
            f"Question: {state['question']}\nDocument: {d.page_content}"
        )
        .answer
    ]
    return {"documents": relevant}


def generate(state: State) -> dict:
    ctx = "\n\n".join(d.page_content for d in state.get("documents", []))
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Answer using the context if provided, otherwise use your knowledge."),
            ("human", "Context:\n{ctx}\n\nQuestion: {question}"),
        ]
    )
    answer = (prompt | _llm | StrOutputParser()).invoke(
        {"ctx": ctx, "question": state["question"]}
    )
    return {"generation": answer}


def check_support(state: State) -> dict:
    """Gate 3 — is the answer grounded in the retrieved context (isSupported)?"""
    if not state.get("documents"):
        return {"supported": True}
    ctx = "\n\n".join(d.page_content for d in state["documents"])
    result = _llm.with_structured_output(BoolDecision).invoke(
        f"Is this answer fully supported by the context?\n"
        f"Context: {ctx}\nAnswer: {state['generation']}"
    )
    return {"supported": result.answer}


def create_workflow():
    g = StateGraph(State)
    g.add_node("classify", classify)
    g.add_node("retrieve", retrieve)
    g.add_node("grade_docs", grade_docs)
    g.add_node("generate", generate)
    g.add_node("check_support", check_support)

    g.add_edge(START, "classify")
    g.add_conditional_edges(
        "classify",
        lambda s: "retrieve" if s.get("should_retrieve") else "generate",
    )
    g.add_edge("retrieve", "grade_docs")
    g.add_edge("grade_docs", "generate")
    g.add_edge("generate", "check_support")
    g.add_edge("check_support", END)
    return g.compile()
