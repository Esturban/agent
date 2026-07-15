from dotenv import load_dotenv
from langgraph.types import Command

from src.tools import SAMPLE_ACTIONS, format_action
from src.workflow import create_workflow

load_dotenv()


def main():
    app = create_workflow()

    for i, action in enumerate(SAMPLE_ACTIONS):
        thread_id = f"action-{i}"
        config = {"configurable": {"thread_id": thread_id}}

        print(f"\n{'='*50}")
        print(f"Action: {format_action(action)}")

        # First stream: run until interrupt
        interrupted_payload = None
        for event in app.stream(
            {"action": action["action"], "risk": action["risk"], "approved": False, "result": ""},
            config=config,
        ):
            interrupts = event.get("__interrupt__", ())
            if interrupts:
                interrupted_payload = interrupts[0].value
                break

        if interrupted_payload:
            print(f"Interrupted: {interrupted_payload['question']}")
            print(f"  -> {interrupted_payload['action']} [{interrupted_payload['risk']}]")

        # Simulate human decision by risk level
        approved = action["risk"] != "high"
        decision_label = "APPROVED" if approved else "REJECTED"
        print(f"Auto-decision: {decision_label}")

        # Second stream: resume with human decision
        for event in app.stream(Command(resume=approved), config=config):
            if "await_approval" in event:
                result = event["await_approval"].get("result", "")
                if result:
                    print(f"Result: {result}")


if __name__ == "__main__":
    main()
