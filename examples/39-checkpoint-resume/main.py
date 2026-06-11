from dotenv import load_dotenv

from src.tools import TASKS
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for i, task in enumerate(TASKS):
        thread_id = f"thread-{i}"
        config = {"configurable": {"thread_id": thread_id}}

        print(f"\nTASK: {task}\n{'─' * 60}")
        result = app.invoke(
            {"task": task, "step": 0, "outputs": [], "done": False},
            config=config,
        )
        print(f"Steps completed: {len(result['outputs'])}")
        print(f"Output preview: {result['outputs'][-1][:150] if result['outputs'] else 'none'}")

        # Demonstrate resume: invoke again with same thread_id
        print(f"\nResuming thread '{thread_id}'...")
        resumed = app.get_state(config)
        print(f"Resumed state — step: {resumed.values.get('step')}, done: {resumed.values.get('done')}")


if __name__ == "__main__":
    main()
