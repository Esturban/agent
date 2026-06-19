"""
130 — AgentDojo Harness
=======================
Runs a real agent against the AgentDojo benchmark (ICLR 2025) and measures
two independent dimensions on the v1 banking and travel task suites:

  - Utility rate: did the agent accomplish the USER's goal?
  - ASR:          did the ATTACKER's injected instruction execute?

AgentDojo's core contribution: forcing both metrics to be reported together.
A defense that blocks all injections by refusing tool calls isn't useful.
The benchmark penalises both excessive caution (low utility) and compliance
with injections (high ASR).

Defenses tested:
  - undefended:    baseline, no protection
  - spotlighting:  XML-wrap tool outputs + system prompt policy (arxiv:2403.14720)
  - keyword_block: heuristic keyword blocklist (weak, educational)

Paper: arxiv:2406.13352 — "AgentDojo: A Dynamic Environment to Evaluate
       Attacks and Defenses for LLM Agents" (ICLR 2025)
"""

import argparse
from dotenv import load_dotenv

load_dotenv()

from agentdojo.attacks.baseline_attacks import IgnorePreviousAttack
from agentdojo.attacks.important_instructions_attacks import ImportantInstructionsAttack

from src.harness import build_pipeline, run_clean, run_attacked, utility_rate, asr
from src.defenses import SpotlightingElement, KeywordBlocklistElement
from src.reporter import print_comparison_table, print_task_breakdown

BOLD  = "\033[1m"
GREEN = "\033[92m"
RESET = "\033[0m"

SUITES = ["banking", "travel"]

DEFENSES = [
    ("undefended",     None),
    ("spotlighting",   SpotlightingElement()),
    ("keyword_block",  KeywordBlocklistElement()),
]

ATTACKS = [
    ("ignore_previous",         IgnorePreviousAttack()),
    ("important_instructions",  ImportantInstructionsAttack()),
]


def main():
    parser = argparse.ArgumentParser(description="AgentDojo benchmark harness")
    parser.add_argument("--suite", choices=SUITES + ["all"], default="banking")
    parser.add_argument("--defense", default="all",
                        help="undefended | spotlighting | keyword_block | all")
    parser.add_argument("--attack", default="ignore_previous",
                        help="ignore_previous | important_instructions")
    parser.add_argument("--verbose", action="store_true",
                        help="Print per-task breakdown")
    args = parser.parse_args()

    print(f"\n{BOLD}=== 130 — AgentDojo Harness ==={RESET}")
    print("Paper: arxiv:2406.13352 (ICLR 2025)\n")

    suites_to_run = SUITES if args.suite == "all" else [args.suite]
    defenses_to_run = (
        DEFENSES if args.defense == "all"
        else [(d, e) for d, e in DEFENSES if d == args.defense]
    )
    attack_obj = next((a for n, a in ATTACKS if n == args.attack), ATTACKS[0][1])
    attack_name = args.attack

    print(f"Attack: {attack_name}")
    print(f"Defenses: {[d for d, _ in defenses_to_run]}")
    print(f"Suites: {suites_to_run}\n")

    table_rows = []

    for suite_name in suites_to_run:
        print(f"  Suite: {suite_name}")
        for defense_name, defense_el in defenses_to_run:
            pipeline = build_pipeline(defense_element=defense_el)

            print(f"    [{defense_name}] running clean...")
            clean = run_clean(suite_name, pipeline)

            print(f"    [{defense_name}] running with {attack_name} attack...")
            attacked = run_attacked(suite_name, pipeline, attack_obj)

            table_rows.append((defense_name, suite_name, clean, attacked))

            if args.verbose:
                print_task_breakdown(f"clean ({defense_name})", clean)
                print_task_breakdown(f"attacked ({defense_name})", attacked)

    print(f"\n{'=' * 95}")
    print(f"\n{BOLD}Results — Attack: {attack_name}{RESET}\n")
    print_comparison_table(table_rows)

    print(f"\n{BOLD}Key lesson:{RESET}")
    print("AgentDojo forces you to measure utility AND security together.")
    print("A naive defense (refuse all tool calls) gets ASR=0 but utility=0 too.")
    print("Spotlighting-encode in the paper achieves 0–1.8% ASR with <5pp utility loss.")
    print("The undefended baseline ASR on banking tasks is ~17–40% depending on attack.")


if __name__ == "__main__":
    main()
