"""
Minimal RAG agent with a protectable system prompt.

In production, the system prompt contains business logic, persona definitions,
access rules, and confidential instructions. This demo simulates that with
a system prompt that contains a canary token — a detectable secret.

The knowledge base is synthetic but realistic-looking Acme Corp content.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

_KNOWLEDGE_BASE = [
    "Acme Corp Q3 revenue was $4.2M, up 12% from Q2.",
    "The refund policy allows returns within 30 days with original receipt.",
    "Employee handbook section 4.2 covers remote work policy.",
    "Product SKU-887 is discontinued as of November 2024.",
    "Support escalation: Tier 1 → Tier 2 → Engineering (max 48h SLA).",
]

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def query_agent(user_message: str, system_prompt: str) -> str:
    """Run the RAG agent with the given system prompt and return its response."""
    context = "\n".join(f"- {doc}" for doc in _KNOWLEDGE_BASE)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context from knowledge base:\n{context}\n\nUser question: {user_message}"),
    ]
    return _llm.invoke(messages).content
