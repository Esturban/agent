"""
Example 125 — Sycophancy-Based Prompt Leakage (Salesforce, EMNLP 2024)
arxiv: 2404.16251

What this shows:
  Flattery-based social engineering raises system prompt leakage ASR from
  17.7% (direct extraction) to 86.2% (sycophancy combined) on GPT-3.5-turbo.

  Four attacks × three defense variants × three system prompt strictness levels
  → a 4×3 matrix showing which combinations leak the canary token.

Why it matters:
  This is not a technical exploit.  No injections, no special tokens.
  Just compliments and false claims — pure social manipulation.
  It works because RLHF trains models to please users, creating a systematic
  vulnerability to sycophantic framing.

What to watch:
  - 'leaked' column: did the canary token appear in the response?
  - Combined attack almost always leaks, even with strict guards
  - Canary injection tells you WHEN leakage happened, not WHETHER it will

Run:
  python main.py

Output:
  4×3 matrix (attacks × defenses) per system prompt variant.
  Canary leakage highlighted per cell.
"""

from dotenv import load_dotenv
load_dotenv()

import os

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is required; add it to .env before running this example.")

from src.comparison import build_matrix  # noqa: E402
from prompts.attack_variants import ATTACKS  # noqa: E402
from prompts.defenses import DEFENSES  # noqa: E402
from prompts.system_prompt import VARIANTS  # noqa: E402

RED   = "\033[91m"
GREEN = "\033[92m"
BOLD  = "\033[1m"
RESET = "\033[0m"


def print_matrix(results: list[dict]) -> None:
    """Print a 4-row × 3-col matrix for each system prompt variant."""
    sys_names = [v[0] for v in VARIANTS]
    atk_names = [a[0] for a in ATTACKS]
    def_names = [d[0] for d in DEFENSES]

    for sys_name in sys_names:
        print(f"\n{BOLD}System prompt: {sys_name.upper()}{RESET}")
        # Header
        header = f"{'Attack':15}" + "".join(f"{d:15}" for d in def_names)
        print(header)
        print("-" * len(header))

        for atk in atk_names:
            row = f"{atk:15}"
            for def_name in def_names:
                cell = next(
                    (r for r in results if r["system"] == sys_name and r["defense"] == def_name and r["attack"] == atk),
                    None,
                )
                if cell:
                    leaked = cell["leaked"]
                    mark = f"{RED}LEAKED{RESET} " if leaked else f"{GREEN}SAFE  {RESET} "
                    row += f"{mark:24}"
                else:
                    row += f"{'N/A':15}"
            print(row)


def main() -> None:
    print("Sycophancy Prompt Leakage (Salesforce, EMNLP 2024 / arxiv:2404.16251)")
    print("Running 4 attacks × 3 defenses × 3 system prompts...")
    print("(72 target-model calls total)\n")

    results = build_matrix()
    print_matrix(results)

    leakage_count = sum(1 for r in results if r["leaked"])
    total = len(results)
    print(f"\nLeakage rate: {leakage_count}/{total} ({leakage_count/total:.0%})")
    combined_leaked = sum(1 for r in results if r["attack"] == "combined" and r["leaked"])
    combined_total  = sum(1 for r in results if r["attack"] == "combined")
    print(f"Combined attack ASR: {combined_leaked}/{combined_total} ({combined_leaked/combined_total:.0%})")
    print(f"\nPaper finding: flattery alone raises ASR from 17.7% → 86.2% on GPT-3.5-turbo.")
    print("Key takeaway: canary tokens detect leakage; instruction guards reduce but don't eliminate it.")


if __name__ == "__main__":
    main()
