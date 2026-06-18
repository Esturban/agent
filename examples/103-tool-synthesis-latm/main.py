from dotenv import load_dotenv

from src.tools import DEMO_TASKS
from src.workflow import create_workflow

load_dotenv()


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
