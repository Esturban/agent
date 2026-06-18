from agno.agent import Agent
from agno.models.openai import OpenAIChat

from src.tools import SAMPLE_TASKS, add_knowledge, list_topics, search_knowledge

# Agno contrast with LangGraph:
#   LangGraph: explicit graph (StateGraph, nodes, edges, TypedDict state).
#   Agno:      single Agent(...) call — tool loop managed internally.
#              Trades control for brevity: ~5 lines vs ~30 lines for the same agent.

FRAMEWORK_CONTRAST = """
┌──────────────┬─────────────────────────────────────┬─────────────────────┐
│ Framework    │ How the tool loop works             │ State management    │
├──────────────┼─────────────────────────────────────┼─────────────────────┤
│ LangGraph    │ Explicit nodes + edges in StateGraph│ TypedDict, you own  │
│ Agno         │ Agent() manages loop internally     │ Handled for you     │
│ Google ADK   │ Runner + LlmAgent, async events     │ InMemorySessionSvc  │
└──────────────┴─────────────────────────────────────┴─────────────────────┘
"""


def create_agent() -> Agent:
    """Create an Agno agent with three knowledge-base tools."""
    return Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        description="You are a helpful assistant with a technology knowledge base.",
        instructions=[
            "Use search_knowledge to look up topics before answering.",
            "Use add_knowledge when the user provides a new fact to store.",
            "Use list_topics to show what's available when asked.",
            "Be concise — one short paragraph max unless asked for more.",
        ],
        # Agno infers tool schemas from type hints + docstrings — no decorators needed.
        tools=[search_knowledge, add_knowledge, list_topics],
        show_tool_calls=True,  # prints tool calls to stdout for teaching visibility
    )


def run_task(agent: Agent, task: str) -> str:
    """Run a task through the agent and return the response text."""
    response = agent.run(task)
    # response.content is the final assistant message string
    return response.content if response.content else "(no response)"
