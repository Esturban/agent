"""
LangGraph agent workflows: undefended vs defended.

Undefended: tools → LLM → response. The LLM sees raw tool output including injections.
Defended:   tools → validator → (pass or block) → LLM → response.

Both use the same user query. The difference is whether the validator
intercepts and sanitizes tool output before it reaches the LLM.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from .validator import validate_tool_output

AGENT_SYSTEM = """\
You are a helpful assistant. You have access to calculator, web_search, weather_api, and memory_read tools.
Use the tools to answer the user's question. Report your findings clearly.\
"""

_llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)


def _run_with_tools(query: str, tools: list, validate: bool) -> dict:
    """
    Run one tool call manually (not full ReAct loop) for clarity in the demo.
    Picks the first tool from the list based on query content.
    Returns {tool_used, raw_output, validated, sanitized_output, response}.
    """
    tool_map = {t.name: t for t in tools}

    # Decide which tool to call based on query keywords
    if any(word in query.lower() for word in ("calculat", "math", "times", "plus")):
        tool_name, tool_input = "calculator", "2 + 2"
    elif "weather" in query.lower():
        tool_name, tool_input = "weather_api", "London"
    elif "memory" in query.lower() or "session" in query.lower():
        tool_name, tool_input = "memory_read", "session_id"
    else:
        tool_name, tool_input = "web_search", query

    tool = tool_map.get(tool_name)
    raw_output = tool.invoke(tool_input) if tool else "{}"

    sanitized_output = raw_output
    is_safe = True
    reason = "no validation"

    if validate:
        is_safe, reason, _ = validate_tool_output(raw_output)
        if not is_safe:
            sanitized_output = f"[SANITIZED — injection detected: {reason}]"

    messages = [
        SystemMessage(content=AGENT_SYSTEM),
        HumanMessage(content=query),
        AIMessage(content="", tool_calls=[{"name": tool_name, "args": {"input": tool_input}, "id": "demo-call-1", "type": "tool_call"}]),
        ToolMessage(content=sanitized_output, tool_call_id="demo-call-1"),
    ]
    response = _llm.invoke(messages).content

    return {
        "tool_used":   tool_name,
        "raw_output":  raw_output[:200],
        "validated":   validate,
        "is_safe":     is_safe,
        "reason":      reason,
        "response":    response,
    }


def run_undefended(query: str, poisoned_tools: list) -> dict:
    return _run_with_tools(query, poisoned_tools, validate=False)


def run_defended(query: str, poisoned_tools: list) -> dict:
    return _run_with_tools(query, poisoned_tools, validate=True)
