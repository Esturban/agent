from dotenv import load_dotenv

load_dotenv()

from src.tools import BUDGET_LIMIT, RESEARCH_STEPS, RESEARCH_TOPIC  # noqa: E402
from src.workflow import BudgetState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    print(f"Topic  : {RESEARCH_TOPIC}")
    print(f"Budget : {BUDGET_LIMIT} tokens  |  Steps: {len(RESEARCH_STEPS)}\n")

    result: BudgetState = app.invoke({
        "topic": RESEARCH_TOPIC,
        "steps": RESEARCH_STEPS,
        "current_step": 0,
        "notes": [],
        "tokens_used": 0,
        "token_log": [],
        "budget_exceeded": False,
        "final_answer": "",
    })

    print("Token log:")
    for entry in result["token_log"]:
        print(f"  Step {entry['step']}: prompt={entry['prompt_tokens']} completion={entry['completion_tokens']} total={entry['total']}")
    print(f"\nTotal tokens used: {result['tokens_used']} / {BUDGET_LIMIT}")
    print(f"Budget exceeded  : {result['budget_exceeded']}")
    print(f"\nFinal answer:\n{result['final_answer'][:500]}")


if __name__ == "__main__":
    main()
