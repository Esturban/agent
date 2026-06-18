"""Example 100: Computer Use Agent (Anthropic).

Shows the computer-use action loop: the model requests bash/editor
tool calls, we execute them locally, feed results back, and repeat
until the model signals end_turn or exhausts MAX_STEPS.

No display is needed — bash_20241022 + text_editor_20241022 run
headlessly. Add computer_20241022 + Xvfb for full GUI control.
"""

import os
from dotenv import load_dotenv
from src.tools import TASK
from src.workflow import run_agent

load_dotenv()


def main() -> None:
    # Confirm the API key is present before making any network calls.
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY not set in .env")

    print("Task:", TASK)
    print("=" * 60)

    steps = run_agent(TASK)

    for step in steps:
        if step["type"] == "text":
            # Model narration between tool calls.
            print(f"\n[model] {step['content']}")
        else:
            # A concrete tool action and its output.
            print(f"\n[{step['tool']}] input: {step['input']}")
            print(f"        output: {step['output'][:200]}")

    print("\n" + "=" * 60)
    print(f"Done — {len(steps)} steps recorded.")


if __name__ == "__main__":
    main()
