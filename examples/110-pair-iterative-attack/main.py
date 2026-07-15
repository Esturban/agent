"""
Example 110 — PAIR: Prompt Automatic Iterative Refinement (Chao et al. 2023)

What this shows:
  The PAIR algorithm (arxiv:2310.08419) — an attacker LLM iteratively refines
  jailbreak prompts based on feedback from a judge.  Three LLMs in a loop:
    Attacker  — generates/refines attack prompts
    Target    — the model being red-teamed
    Judge     — scores how well the target fulfilled the objective (1-10)

Why it matters:
  PAIR achieves attack success in 20 queries on average vs. thousands for
  token-level gradient methods (GCG).  Understanding it is essential for
  anyone building AI safety systems or measuring model robustness.

Key files:
  src/tools.py    — ATTACKER_SYSTEM, TARGET_SYSTEM, JUDGE_SYSTEM prompts
  src/workflow.py — cyclic LangGraph: attacker → target → judge → (loop|done)
"""

import os

from dotenv import load_dotenv
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is required to run this live example.")

from src.tools import OBJECTIVE, MAX_ITER, THRESHOLD
from src.workflow import create_workflow, PAIRState


def main():
    print("\nPAIR — Prompt Automatic Iterative Refinement (Chao et al. 2023)")
    print("=" * 65)
    print(f"Objective : {OBJECTIVE}")
    print(f"Max iters : {MAX_ITER} | Convergence threshold: {THRESHOLD}/10\n")

    app = create_workflow()
    initial_state: PAIRState = {
        "iteration": 1,
        "attack_history": [],
        "current_prompt": "",
        "current_strategy": "",
        "target_response": "",
        "judge_score": 0,
        "judge_explanation": "",
        "scores": [],
        "converged": False,
    }

    result = app.invoke(initial_state)

    print("Score progression:")
    for i, score in enumerate(result["scores"], 1):
        bar = "█" * score + "░" * (10 - score)
        label = " ← CONVERGED" if i == len(result["scores"]) and result["converged"] else ""
        print(f"  Iter {i}: [{bar}] {score}/10{label}")

    print(f"\nFinal attack prompt:")
    print(f"  {result['current_prompt'][:200]}")
    print(f"\nFinal judge score: {result['judge_score']}/10")
    print(f"Explanation: {result['judge_explanation'][:200]}")

    if result["judge_score"] >= THRESHOLD:
        print("\n[PAIR converged] Attack succeeded within iteration budget.")
    else:
        print(f"\n[PAIR exhausted] Max {MAX_ITER} iterations reached without convergence.")


if __name__ == "__main__":
    main()
