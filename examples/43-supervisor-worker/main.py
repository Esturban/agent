from dotenv import load_dotenv
from src.tools import SAMPLE_TASKS
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for task in SAMPLE_TASKS:
        print(f"\nTASK: {task}\n{'─' * 60}")
        result = app.invoke({"task": task, "worker_type": "", "rationale": "", "worker_result": ""})
        print(f"Worker: {result['worker_type']}")
        print(f"Result:\n{result['worker_result'][:300]}")


if __name__ == "__main__":
    main()
