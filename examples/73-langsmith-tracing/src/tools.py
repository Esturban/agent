from typing import TypedDict

from langchain_openai import ChatOpenAI

MODEL = "gpt-5-nano"

SAMPLE_QUESTIONS = [
    "What is retrieval-augmented generation?",
    "Explain the ReAct agent pattern in two sentences.",
    "What is LangSmith used for?",
]


class TraceState(TypedDict):
    question: str
    answer: str


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model=MODEL, temperature=0)
