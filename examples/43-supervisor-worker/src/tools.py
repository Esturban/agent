from typing import Literal, TypedDict

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

SAMPLE_TASKS = [
    "Research the latest developments in quantum computing.",
    "Summarize the key points of the React documentation.",
    "Analyze the pros and cons of microservices vs monoliths.",
]

WORKER_PROMPTS = {
    "researcher": "You are a researcher. Provide 3-5 factual, well-sourced points about: {task}",
    "summarizer": "You are a summarizer. Give a concise 3-bullet summary of key points about: {task}",
    "analyst": "You are an analyst. Provide a structured analysis with pros/cons/recommendation for: {task}",
}


class WorkerRoute(BaseModel):
    worker: Literal["researcher", "summarizer", "analyst"]
    rationale: str


class SupervisorState(TypedDict):
    task: str
    worker_type: str
    rationale: str
    worker_result: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
router_llm = llm.with_structured_output(WorkerRoute)
