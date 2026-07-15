import os

from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY", "").startswith("sk-"):
    raise RuntimeError("OPENAI_API_KEY is required for LATM tool synthesis.")

from src.tools import DEMO_TASKS  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()

    for task in DEMO_TASKS:
        print(f"\nTask: {task}")
        result = app.invoke({"task": task, "chosen_tool": "", "tool_result": ""})
        print(f"  Tool used  : {result['chosen_tool']}")
        print(f"  Result     : {result['tool_result'][:120]}")

    print("\nDone. Observe that tasks 2 and 4 reuse synthesized tools (no new synthesis).")


if __name__ == "__main__":
    main()
