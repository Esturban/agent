from dotenv import load_dotenv
from src.tools import SAMPLE_TASKS
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for task in SAMPLE_TASKS:
        print(f"\nTASK: {task}\n{'─' * 60}")
        result = app.invoke({"task": task, "steps": [], "results": [], "final_answer": ""})
        print(f"\nPLAN EXECUTED ({len(result['results'])} steps)")
        print(f"\nFINAL ANSWER:\n{result['final_answer']}")


if __name__ == "__main__":
    main()
