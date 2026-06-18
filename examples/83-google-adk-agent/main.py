from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUERIES  # noqa: E402
from src.workflow import create_agent, run_query  # noqa: E402

# Framework contrast quick reference:
#
#   LangGraph  → StateGraph(MyState) → add_node/add_edge → compile() → app.invoke()
#   ADK        → LlmAgent(model, tools) → Runner → run_async() over event stream
#
# The ADK runner handles the tool-call loop internally; you only see final responses.
# Trade-off: less control, less code.

CONTRAST = """
┌────────────────┬──────────────────────────────────┬───────────────────────┐
│ Framework      │ How you build the agent          │ Tool schema source    │
├────────────────┼──────────────────────────────────┼───────────────────────┤
│ LangGraph      │ Explicit graph: nodes + edges    │ Pydantic / @tool dec. │
│ Google ADK     │ Declare LlmAgent, ADK loops      │ Python docstrings     │
│ Agno           │ Agent(model, tools)              │ Python docstrings     │
└────────────────┴──────────────────────────────────┴───────────────────────┘
"""


def main() -> None:
    print("=== 83 · Google ADK Agent ===\n")
    print(CONTRAST)

    agent = create_agent()  # LlmAgent instance — reuse across queries

    for query in SAMPLE_QUERIES:
        print(f"Q: {query}")
        answer = run_query(query, agent)
        print(f"A: {answer}\n")


if __name__ == "__main__":
    main()
