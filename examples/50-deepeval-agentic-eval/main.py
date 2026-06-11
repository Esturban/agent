from dotenv import load_dotenv

from src.tools import AGENT_TASKS
from src.workflow import create_workflow, run_and_collect


def main():
    load_dotenv()
    app = create_workflow()

    print("Running agent on test tasks...\n")
    for task in AGENT_TASKS:
        answer, tools = run_and_collect(app, task["input"])
        print(f"Task: {task['input']}")
        print(f"Tools called: {tools}")
        print(f"Expected: {task['expected_tools']}")
        match = set(tools) == set(task["expected_tools"])
        print(f"Tool match: {'PASS' if match else 'FAIL'}\n")


if __name__ == "__main__":
    main()
