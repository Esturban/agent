import operator
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI

# Multi-turn conversation that tests knowledge retention
STATEFUL_CONVERSATION = [
    ("user", "My name is Alex and I'm a Python developer."),
    ("user", "I'm currently working on a RAG application."),
    ("user", "What's my name?"),  # Should remember "Alex"
    ("user", "What am I working on?"),  # Should remember "RAG application"
    ("user", "Can you summarize what you know about me?"),
]

# Conversation that tests topic relevance
RELEVANCE_CONVERSATION = [
    ("user", "Tell me about Python programming."),
    ("user", "What are the main data structures?"),
    ("user", "How does garbage collection work in Python?"),
    ("user", "What is the GIL?"),
]

SYSTEM_PROMPT_STATEFUL = (
    "You are a helpful assistant. Remember everything the user tells you about themselves."
)
SYSTEM_PROMPT_STATELESS = "You are a helpful assistant. Answer each question independently."


class ChatState(TypedDict):
    messages: Annotated[list, operator.add]
    history: list[dict]  # stores (role, content) pairs for evaluation


llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0.2)
