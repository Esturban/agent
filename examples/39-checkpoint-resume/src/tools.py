from typing import TypedDict

from langchain_openai import ChatOpenAI

TASKS = [
    "Explain the three laws of robotics.",
    "What are the key benefits of using LangGraph for agent development?",
]

STEP_PROMPTS = [
    "Briefly introduce the topic in 1-2 sentences: {task}",
    "List 3 key points about the topic: {task}",
    "Write a concise conclusion (1-2 sentences): {task}",
]

DB_PATH = "/tmp/checkpoint_39.sqlite"


class CheckpointState(TypedDict):
    task: str
    step: int
    outputs: list[str]
    done: bool


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
