"""
Example 105 — Automated Red Teaming (parallel attack chains)

What this shows:
  A LangGraph workflow that fans out N independent attack chains in parallel
  using Send().  Each chain crafts a jailbreak attempt, submits it to a
  target model, and a judge scores the response for policy violations.
  The final Attack Success Rate (ASR) summarises how vulnerable the target is.

Why it matters:
  Manual red teaming is slow and coverage-limited.  This pattern mirrors
  industrial-scale automated red-teaming (Meta's purple llama, Anthropic's
  Constitutional AI red team).  ASR across variants becomes a safety metric.

Key files:
  src/tools.py    — SEED_GOAL, N_ATTACKS, ATTACKER_SYSTEM, TARGET_SYSTEM, JUDGE_SYSTEM
  src/workflow.py — fan-out with Send() → attack → judge → collect results
"""

import os

from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY", "").startswith("sk-"):
    raise RuntimeError("OPENAI_API_KEY is required for automated red teaming.")

from src.tools import N_ATTACKS, SEED_GOAL  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    print("Automated Red Teaming — parallel attack chains with ASR measurement")
    print(f"Goal  : {SEED_GOAL}")
    print(f"Attack chains : {N_ATTACKS} (parallel)")
    print("=" * 60)

    app = create_workflow()
    result = app.invoke({
        "goal": SEED_GOAL,
        "results": [],
        "attack_success_rate": 0.0,
    })

    for i, r in enumerate(result["results"], 1):
        status = "SUCCEEDED" if r["success"] else "blocked"
        print(f"\n[{i}] {status}")
        print(f"     Attack : {r['attack']}")
        print(f"     Reason : {r['reason']}")

    asr = result["attack_success_rate"]
    print(f"\nAttack Success Rate: {asr:.0%} ({int(asr * N_ATTACKS)}/{N_ATTACKS} attacks succeeded)")


if __name__ == "__main__":
    main()
