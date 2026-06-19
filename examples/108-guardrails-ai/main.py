"""
Example 108 — Guardrails AI (Pydantic schema validation)

What this shows:
  Guardrails AI wraps the LLM call and validates the output against a
  Pydantic schema.  If validation fails, it automatically reasks the model
  (up to max_reasks times) with the validation errors appended.

Why it matters:
  Structured output is hard to guarantee with a plain LLM call.  The reask
  mechanism gives you automatic retry-with-feedback without custom code —
  and the Guard keeps an audit trail of every attempt.

Key files:
  src/tools.py    — StructuredResponse Pydantic model with field validators
  src/workflow.py — SYSTEM_PROMPT + create_guard() + validate_response()
"""

from dotenv import load_dotenv
load_dotenv()

from src.tools import TEST_PROMPTS
from src.workflow import create_guard, validate_response


def main():
    print("\nGuardrails AI — Pydantic schema validation with automatic reask")
    print("=" * 62)
    print("Validators: max 200-char summary, exactly 3 points, no URLs\n")

    guard = create_guard(max_reasks=2)

    for label, prompt in TEST_PROMPTS:
        short = prompt[:55] + ("..." if len(prompt) > 55 else "")
        result = validate_response(guard, prompt)

        if result["passed"]:
            v = result["validated"]
            tag = "\033[92mPASSED\033[0m"
            print(f"[{label.upper():12}] {tag} | reasks: {len(result['reasks'])}")
            print(f"  Prompt : {short}")
            if isinstance(v, dict):
                print(f"  Summary: {v.get('summary', '')[:80]}")
                print(f"  Points : {len(v.get('points', []))} items")
        else:
            tag = "\033[91mFAILED\033[0m "
            print(f"[{label.upper():12}] {tag} | reasks: {len(result['reasks'])}")
            print(f"  Prompt : {short}")
            print(f"  Error  : {str(result['error'])[:100]}")
        print()


if __name__ == "__main__":
    main()
