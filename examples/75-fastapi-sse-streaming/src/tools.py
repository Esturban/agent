from typing import TypedDict

MODEL = "gpt-5-nano"


class AgentState(TypedDict):
    question: str
    answer: str
