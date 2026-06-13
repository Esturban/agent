from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_TASKS  # noqa: E402
from src.workflow import create_agent, run_sandboxed_demo  # noqa: E402

FRAMEWORK_CONTRAST = """
┌─────────────┬──────────────────────────────────────┬──────────────────────┐
│ Framework   │ How reasoning works                  │ Output type          │
├─────────────┼──────────────────────────────────────┼──────────────────────┤
│ LangGraph   │ Nodes + edges + TypedDict state      │ Structured dict      │
│ CrewAI      │ Roles + tasks + crew delegation      │ Natural language      │
│ SmolAgents  │ LLM writes Python → runs directly    │ Any Python value     │
└─────────────┴──────────────────────────────────────┴──────────────────────┘
"""


def main() -> None:
    print("=== 66 · SmolAgents: Code-Executing Agent ===\n")

    # Step 1: sandboxing concern — part of the demo, not a footnote
    run_sandboxed_demo()

    # Step 2: normal task runs with the safe agent
    print("--- Safe agent running sample tasks ---")
    agent = create_agent(safe_mode=True)
    for task in SAMPLE_TASKS:
        result = agent.run(task)
        print(f"Task   : {task}")
        print(f"Result : {result}\n")

    # Step 3: framework contrast
    print("--- Framework comparison ---")
    print(FRAMEWORK_CONTRAST)


if __name__ == "__main__":
    main()
