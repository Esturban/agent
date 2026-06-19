"""
Example 69 — Constitutional AI (CAI)

What this shows:
  The Anthropic CAI technique: generate a response, then critique it against
  a constitution of principles, then revise.  This loop runs until no
  violations remain (or a max-revision limit is hit).

Why it matters:
  RLHF requires human labellers.  CAI lets the model itself enforce a policy
  document — dramatically cheaper to iterate and fully auditable.

Key files:
  src/tools.py    — SAMPLE_PROMPTS and the CONSTITUTION principles
  src/workflow.py — LangGraph loop: generate → critique → (revise or done)
"""

from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_PROMPTS  # noqa: E402
from src.workflow import CAIState, create_workflow  # noqa: E402


def main() -> None:
    print("Constitutional AI — self-critique revision loop")
    print("Each response is checked against a constitution; violations trigger revision.\n")
    app = create_workflow()
    for prompt in SAMPLE_PROMPTS:
        print(f"\n{'=' * 60}")
        print(f"Prompt      : {prompt}")
        result: CAIState = app.invoke(
            {"prompt": prompt, "response": "", "critiques": [], "revision_count": 0, "violations": []}
        )
        violations = [c for c in result["critiques"] if c["violated"]]
        print(f"Revisions   : {result['revision_count']}")
        print(f"Violations  : {len(violations)} remaining")
        print(f"Final answer: {result['response'][:300]}")


if __name__ == "__main__":
    main()
