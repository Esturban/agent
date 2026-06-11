from dotenv import load_dotenv
from src.tools import SAMPLE_TASKS
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for task in SAMPLE_TASKS:
        print(f"\nTASK: {task}\n{'─' * 60}")
        result = app.invoke({"task": task, "plans": [], "evidence": {}, "final_answer": ""})
        print(f"\nEVIDENCE ({len(result['evidence'])} vars): {list(result['evidence'].keys())}")
        print(f"\nFINAL ANSWER:\n{result['final_answer']}")


if __name__ == "__main__":
    main()
