"""
Example 127 — Spotlighting: Indirect Prompt Injection Defense
arxiv: 2403.14720, Microsoft Research 2024.

What this shows:
  Three spotlighting techniques that reduce indirect prompt injection ASR
  on GPT-4 from ~80% (no defense) to near zero (encoding variant).
  Also demonstrates the adaptive attack that breaks encoding when the
  attacker knows the defense is in use.

Spotlighting methods:
  Delimiting:  Wrap external content in XML tags → tells model it's data.
               ASR: ~40% (halves it but still high)
  Datamarking: Prefix each word with invisible Unicode (U+2062).
               ASR: ~16%
  Encoding:    Base64-encode external content.
               ASR: ~0-2% under standard attack.
               BUT: adaptive attacker who knows the encoding bypasses this.

What to watch:
  - Compliance rate drops dramatically from 'none' to 'encoding'
  - Encoding is near-zero on standard attack but adaptive attack breaks it
  - This is the arms-race dynamic: format-based defences have known bypasses

Run:
  python main.py               # runs none/delimiting/encoding, 5 injections each
  python main.py --all         # all 10 injections (more API calls)
"""

from dotenv import load_dotenv
load_dotenv()

import sys
from src.benchmark import run_benchmark  # noqa: E402

RED   = "\033[91m"
GREEN = "\033[92m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"


def print_table(results: list[dict]) -> None:
    """Print compliance summary table grouped by variant."""
    from collections import defaultdict
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        groups[r["variant"]].append(r)

    for variant, rows in groups.items():
        total = len(rows)
        complied = sum(1 for r in rows if r["complied"])
        asr = complied / total if total else 0
        color = RED if asr > 0.3 else (GREEN if asr < 0.1 else "\033[93m")
        print(f"\n{BOLD}{variant:25}{RESET}  ASR: {color}{complied}/{total} ({asr:.0%}){RESET}")
        for r in rows:
            mark = f"{RED}COMPLIED{RESET}" if r["complied"] else f"{GREEN}blocked {RESET}"
            snippet = r["response"][:60].replace("\n", " ")
            print(f"  [{r['family']:20}] {mark} — {snippet}...")


def main() -> None:
    all_injections = "--all" in sys.argv
    max_inj = 10 if all_injections else 5

    print(f"{BOLD}Spotlighting IPI Defense (Microsoft Research 2024 / arxiv:2403.14720){RESET}")
    print("Testing 3 variants: none / delimiting / encoding (+ adaptive attack on encoding)")
    print(f"Injections: {max_inj}  |  Families: instruction-override, role-swap, data-exfil, persona-assign\n")

    results = run_benchmark(max_injections=max_inj)
    print_table(results)

    print(f"\n{BOLD}Paper finding:{RESET}")
    print("  No defense   → ~80% ASR")
    print("  Delimiting   → ~40% ASR (halves it)")
    print("  Encoding     → ~0-2% ASR (standard attack)")
    print("  Encoding+adp → still vulnerable (adaptive attacker who knows the encoding)")
    print("\nKey lesson: format-based defences can be bypassed by an informed attacker.")
    print("Encode + semantic instruction hierarchy (example 128) is the production combination.")


if __name__ == "__main__":
    main()
