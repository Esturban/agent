from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .tools import TOOLS

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)


def create_workflow():
    return create_react_agent(llm, tools=TOOLS)


def run_and_collect(app, task: str) -> tuple[str, list[str]]:
    """Run the agent and collect tool names that were called."""
    result = app.invoke({"messages": [{"role": "user", "content": task}]})
    messages = result["messages"]

    tools_called = []
    final_answer = ""
    for msg in messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tools_called.extend(tc["name"] for tc in msg.tool_calls)
        if hasattr(msg, "content") and msg.content and not getattr(msg, "tool_calls", None):
            final_answer = msg.content

    return final_answer, tools_called
