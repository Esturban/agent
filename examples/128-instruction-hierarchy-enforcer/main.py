"""
Example 128 — Instruction Hierarchy Enforcer (OpenAI, 2024)
arxiv: 2404.13208

What this shows:
  An explicit privilege hierarchy enforcer that blocks lower-trust sources
  from overriding higher-trust instructions, even when the override is subtle.

  SYSTEM (3) > OPERATOR (2) > USER (1) > TOOL (0)

  The paper finds that models trained on this hierarchy refuse ~95% of
  privilege escalation attempts. This example implements the enforcement
  logic explicitly (without special training) via a two-layer check:
    Layer 1: Fast keyword check for explicit escalation language
    Layer 2: LLM semantic check for implicit scope violations

  Run all 6 scenarios to see which attacks are blocked vs allowed.
"""

from dotenv import load_dotenv
load_dotenv()

import os

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is required; add it to .env before running this example.")

from src.scenarios import SCENARIOS       # noqa: E402
from src.workflow import create_workflow, HierarchyState  # noqa: E402

GREEN = "\033[92m"
RED   = "\033[91m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"


def main() -> None:
    print(f"{BOLD}Instruction Hierarchy Enforcer (OpenAI 2024 / arxiv:2404.13208){RESET}")
    print("Privilege levels: SYSTEM (3) > OPERATOR (2) > USER (1) > TOOL (0)")
    print("Lower-trust sources cannot override higher-trust instructions.\n")

    app = create_workflow()
    correct = 0

    for scenario in SCENARIOS:
        print(f"{'─' * 60}")
        print(f"{BOLD}{scenario['name']}{RESET}")
        print(f"Trust level : {scenario['incoming'].trust_level.name} → {scenario['incoming'].source_label}")
        print(f"Instruction : {scenario['incoming'].content[:100]}{'...' if len(scenario['incoming'].content) > 100 else ''}")

        state: HierarchyState = {
            "instruction": scenario["incoming"],
            "context":     scenario["context"],
            "allowed":     False,
            "decision":    "",
            "reasoning":   "",
            "response":    "",
        }
        result = app.invoke(state)

        expected = scenario["expected"]
        actual   = result["decision"]
        correct_flag = actual == expected
        if correct_flag:
            correct += 1

        mark = f"{GREEN}CORRECT{RESET}" if correct_flag else f"{RED}WRONG  {RESET}"
        outcome_color = GREEN if actual == "allow" else RED
        print(f"Expected    : {expected}  |  Got: {outcome_color}{actual}{RESET}  [{mark}]")
        print(f"Reasoning   : {result['reasoning']}")
        if actual == "block":
            print(f"{DIM}Response    : {result['response'][:120]}{RESET}")
        print()

    print(f"{'=' * 60}")
    print(f"Accuracy: {correct}/{len(SCENARIOS)} scenarios correctly enforced")
    print(f"\nPaper finding: a hierarchy-trained model achieves ~95% accuracy.")
    print("Key lesson: explicit enforcement helps, but training on the hierarchy is more robust.")


if __name__ == "__main__":
    main()
