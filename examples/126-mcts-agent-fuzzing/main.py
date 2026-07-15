"""
Example 126 — MCTS Agent Fuzzing (AgentVigil, Berkeley 2025)
arxiv: 2505.05849

What this shows:
  Monte Carlo Tree Search (MCTS) applied to prompt injection fuzzing.
  Instead of trying prompts randomly, MCTS uses UCB1 to intelligently
  explore the mutation space — balancing exploitation (refine what works)
  with exploration (try different mutation branches).

  AgentVigil achieves 71% ASR vs 38% for random baseline on AgentDojo.

How MCTS works here:
  - Each node = one prompt variant
  - Each edge = one mutation operator applied (paraphrase, encode, roleframe, authority, split, combine)
  - UCB1 = avg_reward + C * sqrt(ln(parent_visits) / node_visits)
  - High UCB1 = unexplored OR consistently successful

What to watch:
  - Which mutation operators score highest (roleframe and authority tend to win)
  - Score progression: MCTS should improve faster than random
  - The ASCII tree output showing which branches were explored

Run:
  python main.py                    # fuzz one seed (fictional-framing), 10 iterations
  python main.py --seed 4           # pick a different seed (0-9)
  python main.py --budget 20        # more iterations
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is required; add it to .env before running this example.")

from corpus.seed_injections import SEEDS  # noqa: E402
from src.fuzzer import run_mcts            # noqa: E402
from src.mcts import best_path             # noqa: E402

BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"
GREEN = "\033[92m"
RED   = "\033[91m"


def print_tree(node, prefix: str = "", is_last: bool = True) -> None:
    """Print ASCII tree of explored nodes."""
    connector = "└── " if is_last else "├── "
    score_bar = "█" * int(node.best_score * 8) + "░" * (8 - int(node.best_score * 8))
    prompt_short = node.prompt[:50].replace("\n", " ") + ("..." if len(node.prompt) > 50 else "")
    print(f"{prefix}{connector}[{node.mutation_applied}] {prompt_short}")
    print(f"{prefix}{'    ' if is_last else '│   '} score=[{score_bar}] best={node.best_score:.2f} visits={node.visits}")
    children = node.children
    for i, child in enumerate(children):
        print_tree(child, prefix + ("    " if is_last else "│   "), i == len(children) - 1)


def main() -> None:
    args = sys.argv[1:]
    seed_idx = 4  # default: fictional-framing (expected_effectiveness: high)
    budget = 10
    i = 0
    while i < len(args):
        if args[i] == "--seed" and i + 1 < len(args):
            seed_idx = int(args[i + 1]); i += 2
        elif args[i] == "--budget" and i + 1 < len(args):
            budget = int(args[i + 1]); i += 2
        else:
            i += 1

    seed = SEEDS[seed_idx % len(SEEDS)]

    print(f"{BOLD}MCTS Agent Fuzzing (AgentVigil, Berkeley 2025 / arxiv:2505.05849){RESET}")
    print(f"Seed [{seed_idx}]: {seed['family']} — {seed['mechanism'][:80]}")
    print(f"Budget: {budget} iterations  |  Mutation operators: paraphrase/encode/roleframe/authority/split/combine\n")

    best_prompt, best_score, root, history = run_mcts(
        seed_prompt=seed["prompt"],
        budget=budget,
        verbose=True,
    )

    print(f"\n{BOLD}── Results ──{RESET}")
    print(f"Best score  : {best_score:.2f}/1.0")
    print(f"Best prompt : {best_prompt[:200]}")

    print(f"\n{BOLD}── Mutation tree ──{RESET}")
    print_tree(root)

    print(f"\n{BOLD}── Best path (root → best node) ──{RESET}")
    path = best_path(root)
    for p in path:
        print(f"  {p.mutation_applied:12} → score {p.best_score:.2f}")

    print(f"\n{BOLD}Paper finding:{RESET} MCTS achieves 71% ASR vs 38% random baseline on AgentDojo.")
    print("Key mechanism: UCB1 focuses budget on mutation operators that worked, not random spray.")


if __name__ == "__main__":
    main()
