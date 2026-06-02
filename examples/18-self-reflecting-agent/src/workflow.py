from typing import Literal, TypedDict

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

MAX_ITERATIONS = 3


class Confidence(BaseModel):
    score: Literal["low", "medium", "high"]
    critique: str


class ReflexionState(TypedDict):
    question: str
    answer: str
    critique: str
    iterations: int
    confident: bool


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano")
    evaluator = llm.with_structured_output(Confidence)

    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the question thoroughly and accurately."),
        ("human", "{question}"),
    ])
    revise_prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Improve your answer based on the critique below.\n\n"
            "Original answer:\n{answer}\n\nCritique:\n{critique}\n\n"
            "Write a better answer that addresses every point raised."
        )),
        ("human", "{question}"),
    ])
    critique_prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Evaluate this answer. Identify factual errors, gaps, or unclear explanations. "
            "Then rate your confidence that the answer is now correct and complete: "
            "low / medium / high."
        )),
        ("human", "Question: {question}\n\nAnswer: {answer}"),
    ])

    def generate(state: ReflexionState) -> dict:
        if state["answer"]:
            response = (revise_prompt | llm).invoke({
                "question": state["question"],
                "answer": state["answer"],
                "critique": state["critique"],
            })
        else:
            response = (answer_prompt | llm).invoke({"question": state["question"]})
        return {"answer": response.content, "iterations": state["iterations"] + 1}

    def critique(state: ReflexionState) -> dict:
        result = (critique_prompt | evaluator).invoke({
            "question": state["question"],
            "answer": state["answer"],
        })
        return {"critique": result.critique, "confident": result.score == "high"}

    def should_continue(state: ReflexionState) -> Literal["generate", "__end__"]:
        if state["confident"] or state["iterations"] >= MAX_ITERATIONS:
            return END
        return "generate"

    graph = StateGraph(ReflexionState)
    graph.add_node("generate", generate)
    graph.add_node("critique", critique)

    graph.add_edge(START, "generate")
    graph.add_edge("generate", "critique")
    graph.add_conditional_edges("critique", should_continue)

    return graph.compile()
