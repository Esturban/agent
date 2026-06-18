from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_TASKS  # noqa: E402
from src.workflow import FRAMEWORK_CONTRAST, create_agent, run_task  # noqa: E402


def main() -> None:
    print("=== 85 · Agno Agent ===\n")
    print(FRAMEWORK_CONTRAST)

    agent = create_agent()

    for task in SAMPLE_TASKS:
        print(f"Task: {task}")
        result = run_task(agent, task)
        print(f"Result: {result}\n")
        print("-" * 60)


if __name__ == "__main__":
    main()
