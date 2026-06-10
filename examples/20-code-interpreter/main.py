from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_TASKS  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main():
    app = create_workflow()

    for task in SAMPLE_TASKS:
        print(f"\n{'=' * 60}")
        print(f"Task: {task}")
        result = app.invoke(
            {
                "task": task,
                "code": "",
                "output": "",
                "error": "",
                "iterations": 0,
            }
        )
        status = "SUCCESS" if result["output"] else "FAILED"
        print(f"Status: {status}  |  Iterations: {result['iterations']}")
        if result["output"]:
            print(f"\nOutput:\n{result['output'].rstrip()}")
        if result["error"]:
            print(f"\nError:\n{result['error'].rstrip()}")
        print(f"\nFinal code:\n{result['code']}")


if __name__ == "__main__":
    main()
