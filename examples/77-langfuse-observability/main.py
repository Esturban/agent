import uuid

from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_TASKS  # noqa: E402
from src.workflow import SimpleTraceHandler, create_workflow  # noqa: E402

TASKS_TO_RUN = 3


def main() -> None:
    print(f"Running {TASKS_TO_RUN} tasks with observability tracing...\n")

    for i, task in enumerate(SAMPLE_TASKS[:TASKS_TO_RUN]):
        trace_id = str(uuid.uuid4())[:8]
        handler = SimpleTraceHandler(trace_id=trace_id)
        app = create_workflow(handler)

        result = app.invoke({"task": task, "answer": "", "trace_id": trace_id})
        print(f"  Task {i + 1}: {task}")
        print(f"  Answer: {result['answer']}")
        print(f"  Events captured: {len(handler.events)}")
        for event in handler.events:
            print(f"    [{event['event']}] trace={event['trace_id']} | {list(event.values())[2][:60]}")
        print()


if __name__ == "__main__":
    main()
