from typing import TypedDict

from langchain_openai import ChatOpenAI

TASKS = [
    "Write a Python function to calculate fibonacci numbers.",
    "Explain what a REST API is in simple terms.",
    "What is 42 * 17? Show your work.",
    "Tell me a short joke about programming.",
]

ROUTER_PROMPT = """Classify this task into exactly one category: code, explain, math, or creative.

Task: {task}

Respond with only the category name (no punctuation, no explanation)."""

CODE_PROMPT = "You are an expert programmer. Write clean, working code for: {task}"
EXPLAIN_PROMPT = "You are a great teacher. Explain this clearly in 3-5 sentences: {task}"
MATH_PROMPT = "You are a math tutor. Solve this step by step: {task}"
CREATIVE_PROMPT = "You are a creative writer. Respond with creativity and humor: {task}"


class CommandState(TypedDict):
    task: str
    route: str
    result: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
