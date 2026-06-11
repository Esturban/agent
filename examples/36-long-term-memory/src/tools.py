from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.store.memory import InMemoryStore

USER_ID = "user-alice"
NAMESPACE = ("memories", USER_ID)

CONVERSATIONS = [
    (
        "thread-1",
        [
            "Hi! I'm Alice. I'm a Python developer working on LangGraph.",
            "I love building agentic systems and I prefer concise responses.",
        ],
    ),
    (
        "thread-2",
        [
            "What do I like about LangGraph?",
            "What's my background?",
        ],
    ),
]

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to long-term memory about the user. "
    "Retrieved memories: {memories}\n\n"
    "Use these memories to personalize your response. "
    "After each response, store any new facts about the user."
)


class MemoryState(TypedDict):
    thread_id: str
    messages: list[str]
    memories: list[str]
    response: str


store = InMemoryStore()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
