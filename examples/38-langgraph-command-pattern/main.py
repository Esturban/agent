from dotenv import load_dotenv
from src.tools import TASKS
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for task in TASKS:
        print(f"\nTASK: {task}\n{'─' * 60}")
        result = app.invoke({"task": task, "route": "", "result": ""})
        print(f"Route: {result['route']}")
        print(f"Result:\n{result['result'][:300]}")


if __name__ == "__main__":
    main()
