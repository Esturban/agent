from dotenv import load_dotenv

from src.tools import TOPIC
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    initial_state = {
        "topic": TOPIC,
        "position_a": "",
        "position_b": "",
        "critique_a": "",
        "critique_b": "",
        "round": 0,
        "verdict": "",
    }

    print(f"DEBATE TOPIC: {TOPIC}\n{'=' * 60}\n")
    result = app.invoke(initial_state)

    print("POSITION A — Specialization:")
    print(result["position_a"])
    print("\nPOSITION B — Generalization:")
    print(result["position_b"])
    print(f"\n{'=' * 60}\nJUDGE'S VERDICT:\n{result['verdict']}")


if __name__ == "__main__":
    main()
