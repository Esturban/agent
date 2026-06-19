"""
Turn-by-turn transcript formatter for the Crescendo demo.

Prints each turn as it happens so the student can watch the escalation live.
"""

RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
RED   = "\033[91m"
YELLOW = "\033[93m"


def compliance_bar(score: int, threshold: int) -> str:
    filled = score
    empty = 10 - score
    color = GREEN if score >= threshold else (YELLOW if score >= 5 else DIM)
    return f"{color}{'█' * filled}{'░' * empty}{RESET} {score}/10"


def print_turn(turn: int, level: int, user_msg: str, assistant_msg: str, score: int, threshold: int, what_worked: str) -> None:
    print(f"\n{BOLD}── Turn {turn}  (L{level}) ──{RESET}")
    print(f"{CYAN}User:{RESET} {user_msg[:200].replace(chr(10), ' ')}{'...' if len(user_msg) > 200 else ''}")
    print(f"{DIM}Target:{RESET} {assistant_msg[:300].replace(chr(10), ' ')}{'...' if len(assistant_msg) > 300 else ''}")
    print(f"Score: {compliance_bar(score, threshold)}")
    if what_worked:
        print(f"{DIM}Worked: {what_worked[:100]}{RESET}")


def print_summary(scores: list[int], converged: bool, threshold: int, final_turn: int) -> None:
    print(f"\n{'=' * 60}")
    print(f"{BOLD}CRESCENDO SUMMARY{RESET}")
    print(f"{'=' * 60}")
    print("Score progression:")
    for i, s in enumerate(scores, 1):
        label = f" ← converged (L{i})" if converged and i == len(scores) else ""
        print(f"  Turn {i}: {compliance_bar(s, threshold)}{label}")
    if converged:
        print(f"\n{RED}[CONVERGED]{RESET} Target complied at turn {final_turn}. Threshold {threshold}/10 reached.")
        print("Key finding: multi-turn context-building lowered the refusal threshold.")
    else:
        print(f"\n{GREEN}[EXHAUSTED]{RESET} Max turns reached without compliance. Target held the line.")


def print_baseline_comparison(baseline_score: int, best_crescendo_score: int, threshold: int) -> None:
    print(f"\n{BOLD}Baseline vs Crescendo{RESET}")
    print(f"  Single-turn (direct request): {compliance_bar(baseline_score, threshold)}")
    print(f"  Crescendo (multi-turn):       {compliance_bar(best_crescendo_score, threshold)}")
    delta = best_crescendo_score - baseline_score
    direction = f"{RED}+{delta}{RESET}" if delta > 0 else f"{GREEN}{delta}{RESET}"
    print(f"  Delta: {direction} points")
