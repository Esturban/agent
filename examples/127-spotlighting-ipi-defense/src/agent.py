"""
Document summarization agent.

Accepts a system prompt (one of the 4 variants from system_prompts.py)
and a document (possibly with an injected payload and spotlighting applied).
Returns the agent's response — we check this for signs of injection compliance.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def summarize(document: str, system_prompt: str) -> str:
    """Run the summarization agent and return its response."""
    return _llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Please summarize the following document:\n\n{document}"),
    ]).content
