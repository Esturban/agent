from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from .tools import ChatState, SYSTEM_PROMPT_STATEFUL, SYSTEM_PROMPT_STATELESS, llm


def run_stateful_chat(turns: list[tuple[str, str]]) -> list[dict]:
    """Run a multi-turn conversation with full message history."""
    messages = [SystemMessage(content=SYSTEM_PROMPT_STATEFUL)]
    history = []
    for role, content in turns:
        messages.append(HumanMessage(content=content))
        response = llm.invoke(messages)
        messages.append(AIMessage(content=response.content))
        history.append({"role": "user", "content": content})
        history.append({"role": "assistant", "content": response.content})
    return history


def run_stateless_chat(turns: list[tuple[str, str]]) -> list[dict]:
    """Run a multi-turn conversation without history (stateless)."""
    history = []
    for role, content in turns:
        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT_STATELESS),
            HumanMessage(content=content),
        ])
        history.append({"role": "user", "content": content})
        history.append({"role": "assistant", "content": response.content})
    return history
