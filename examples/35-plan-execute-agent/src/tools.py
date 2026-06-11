import operator
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

SAMPLE_TASKS = [
    "Write a 3-step launch plan for a developer tool startup.",
    "Outline how to learn LangGraph in 4 weeks as a Python developer.",
]

PLANNER_SYSTEM = (
    "You are a task planner. Break the user's task into 3-5 clear, sequential steps. "
    "Each step should be a concrete action that moves toward the goal. "
    "Return ONLY the structured plan, no preamble."
)

EXECUTOR_SYSTEM = (
    "You are a task executor. Complete the given step thoroughly in 2-3 sentences. "
    "Reference prior results where relevant."
)

SYNTHESIZER_SYSTEM = (
    "You are a synthesizer. Combine all completed step results into a coherent, "
    "final response to the original task. Be concise and well-structured."
)


class Step(BaseModel):
    step: str


class Plan(BaseModel):
    steps: list[Step]


class PlanState(TypedDict):
    task: str
    steps: list[str]
    results: Annotated[list[str], operator.add]
    final_answer: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
planner_llm = llm.with_structured_output(Plan)
