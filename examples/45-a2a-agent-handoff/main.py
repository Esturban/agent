from dotenv import load_dotenv

from src.tools import SAMPLE_REQUESTS
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for request in SAMPLE_REQUESTS:
        print(f"\nREQUEST: {request}")
        print("─" * 60)
        result = app.invoke({
            "original_request": request,
            "task_dict": None,
            "execution_result": "",
            "final_synthesis": "",
        })
        task = result["task_dict"]
        print(f"\nTask ID: {task['task_id']} | Type: {task['task_type']}")
        print(f"Final Answer:\n{result['final_synthesis'][:400]}")


if __name__ == "__main__":
    main()
