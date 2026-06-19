"""
130 — AgentDojo Harness
=======================
Runs a real agent against the AgentDojo v1 benchmark (ICLR 2025) and measures
utility rate and ASR on banking and travel task suites.

AgentDojo's core contribution: every evaluation must report BOTH metrics.
  Utility rate = % of user tasks completed correctly
  ASR          = % of injection tasks that succeeded (lower is better)
  Overhead     = utility_clean − utility_attacked

Three defenses, matching the paper's methodology:
  undefended    — baseline, raw tool output
  spotlighting  — << >> delimiters + system prompt instructs model to ignore them
  keyword_block — heuristic blocklist (shown to be weak; easily bypassed)

Two attacks from agentdojo's built-in registry:
  ignore_previous        — "Ignore previous instructions. Do X instead."
  important_instructions — More sophisticated, uses model name and user name

Paper: arxiv:2406.13352 — AgentDojo (ICLR 2025)
Spotlighting: arxiv:2403.14720 (Microsoft Research 2024)
"""

import argparse
from dotenv import load_dotenv

load_dotenv()

from agentdojo.attacks.baseline_attacks import IgnorePreviousAttack
from agentdojo.attacks.important_instructions_attacks import ImportantInstructionsAttack

from src.harness import build_pipeline, run_clean, run_attacked
from src.defenses import DEFENSES
from src.reporter import print_comparison_table, print_task_breakdown

BOLD  = "\033[1m"
RESET = "\033[0m"

SUITES = ["banking", "travel"]

ATTACKS = {
    "ignore_previous":        IgnorePreviousAttack(),
    "important_instructions": ImportantInstructionsAttack(),
}


def main():
    parser = argparse.ArgumentParser(description="AgentDojo benchmark harness")
    parser.add_argument("--suite", choices=SUITES + ["all"], default="banking",
                        help="Task suite (default: banking)")
    parser.add_argument("--defense", default="all",
                        help="undefended | spotlighting | keyword_block | all")
    parser.add_argument("--attack", choices=list(ATTACKS), default="ignore_previous",
                        help="Attack type (default: ignore_previous)")
    parser.add_argument("--verbose", action="store_true",
                        help="Print per-task breakdown")
    args = parser.parse_args()

    print(f"\n{BOLD}=== 130 — AgentDojo Harness ==={RESET}")
    print("Paper: arxiv:2406.13352 (ICLR 2025)\n")

    suites_to_run = SUITES if args.suite == "all" else [args.suite]
    defenses_to_run = (
        DEFENSES if args.defense == "all"
        else [(n, fmt, sfx) for n, fmt, sfx in DEFENSES if n == args.defense]
    )
    if not defenses_to_run:
        print(f"Unknown defense '{args.defense}'. Options: {[d[0] for d in DEFENSES]}")
        return

    attack_obj = ATTACKS[args.attack]
    print(f"Attack:   {args.attack}")
    print(f"Defenses: {[d[0] for d in defenses_to_run]}")
    print(f"Suites:   {suites_to_run}\n")

    table_rows = []

    for suite_name in suites_to_run:
        for defense_name, formatter, system_suffix in defenses_to_run:
            pipeline = build_pipeline(formatter=formatter, system_suffix=system_suffix)

            print(f"  [{suite_name}] [{defense_name}] running clean...")
            clean = run_clean(suite_name, pipeline)

            print(f"  [{suite_name}] [{defense_name}] running with {args.attack} attack...")
            attacked = run_attacked(suite_name, pipeline, attack_obj)

            table_rows.append((defense_name, suite_name, clean, attacked))

            if args.verbose:
                print_task_breakdown(f"{suite_name}/{defense_name} clean", clean)
                print_task_breakdown(f"{suite_name}/{defense_name} attacked", attacked)

    print(f"\n{'=' * 95}")
    print(f"\n{BOLD}Results — Attack: {args.attack}{RESET}\n")
    print_comparison_table(table_rows)

    print(f"\n{BOLD}Key lessons:{RESET}")
    print("  1. Utility and ASR are independent axes — optimise both.")
    print("  2. Spotlighting reduces ASR to 0–1.8% with <5pp utility overhead (paper).")
    print("  3. Keyword blocklists are bypassable; they exist here for contrast.")
    print("  4. important_instructions attack is significantly stronger than ignore_previous.")


if __name__ == "__main__":
    main()
