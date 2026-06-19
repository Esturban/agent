"""
130 — AgentDojo Harness
=======================
Runs a LangGraph agent against the AgentDojo benchmark (ICLR 2025) and
measures two independent dimensions: task utility and attack success rate.

AgentDojo's key contribution: forcing you to report BOTH metrics.
A defense that kills all injections by refusing every tool call is useless.
A defense must keep utility high while driving ASR toward zero.

Paper: arxiv:2406.13352 — "AgentDojo: A Dynamic Environment to Evaluate
       Attacks and Defenses for LLM Agents" (ICLR 2025)

Install: pip install agentdojo  (falls back to synthetic demo tasks if absent)
"""

import sys
import argparse
from dotenv import load_dotenv

load_dotenv()

from src.harness import run_suite, AGENTDOJO_AVAILABLE
from src.agent_factory import create_agent
from src.defenses import DEFENSES
from src.reporter import print_report

SUITES = ["banking", "travel"]

RED   = "\033[91m"
GREEN = "\033[92m"
CYAN  = "\033[96m"
BOLD  = "\033[1m"
RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(description="AgentDojo benchmark harness")
    parser.add_argument(
        "--suite", choices=SUITES + ["all"], default="banking",
        help="Task suite to run (default: banking)",
    )
    parser.add_argument(
        "--defense", default="all",
        help="Defense to test: undefended | spotlighting_delimit | spotlighting_encode | all",
    )
    parser.add_argument(
        "--max-tasks", type=int, default=3,
        help="Max tasks per suite (default: 3 for speed)",
    )
    args = parser.parse_args()

    print(f"\n{BOLD}=== 130 — AgentDojo Benchmark Harness ==={RESET}")
    print("Paper: arxiv:2406.13352 (ICLR 2025)\n")

    if not AGENTDOJO_AVAILABLE:
        print(f"{CYAN}[demo mode] agentdojo not installed — running synthetic tasks")
        print(f"Install with: pip install agentdojo\n{RESET}")
    else:
        print(f"{GREEN}[live mode] agentdojo loaded{RESET}\n")

    suites_to_run = SUITES if args.suite == "all" else [args.suite]
    defenses_to_run = (
        DEFENSES if args.defense == "all"
        else [(d, fn) for d, fn in DEFENSES if d == args.defense]
    )

    if not defenses_to_run:
        print(f"Unknown defense '{args.defense}'. Choose from: {[d for d, _ in DEFENSES]}")
        sys.exit(1)

    clean_results = {}
    attacked_results = {}

    for defense_name, defense_fn in defenses_to_run:
        agent_fn = create_agent(defense_fn=defense_fn if defense_name != "undefended" else None)
        for suite in suites_to_run:
            key = f"{defense_name}|{suite}"
            print(f"  Running {defense_name} on {suite} (clean)...")
            clean_results[key] = run_suite(
                suite, agent_fn, defense_name,
                with_injections=False, max_tasks=args.max_tasks,
            )
            print(f"  Running {defense_name} on {suite} (with injections)...")
            attacked_results[key] = run_suite(
                suite, agent_fn, defense_name,
                with_injections=True, max_tasks=args.max_tasks,
            )

    print()
    print_report(clean_results, attacked_results)

    print(f"\n{BOLD}Key lesson:{RESET}")
    print("AgentDojo measures two independent axes that naive benchmarks miss:")
    print("  1. Utility rate — does the agent do what the USER asked?")
    print("  2. ASR          — does it do what the ATTACKER asked?")
    print("Only a defense that keeps utility high AND drives ASR to zero succeeds.")
    print("Spotlighting-encode achieves 0-1.8% ASR with <5pp utility loss (paper).")


if __name__ == "__main__":
    main()
