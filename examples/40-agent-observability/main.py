from dotenv import load_dotenv
from src.tools import DEMO_TASKS, ObservabilityCallback
from src.workflow import create_workflow


def main():
    load_dotenv()
    cb = ObservabilityCallback()
    app = create_workflow(callback=cb)

    for task in DEMO_TASKS:
        print(f"\nTASK: {task}")
        result = app.invoke({"task": task, "response": ""})
        print(f"Response: {result['response'][:120]}")

    print("\n--- Telemetry Report ---")
    report = cb.report()
    for k, v in report.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
