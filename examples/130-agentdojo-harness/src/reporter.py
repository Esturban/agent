"""
Format AgentDojo SuiteResults as a readable comparison table.

SuiteResults structure (from agentdojo.benchmark):
  utility_results:  dict[(user_task_id, injection_task_id), bool]
  security_results: dict[(user_task_id, injection_task_id), bool]
"""

from agentdojo.benchmark import SuiteResults


def _pct(val: float) -> str:
    return f"{val * 100:.1f}%"


def print_comparison_table(
    rows: list[tuple[str, str, SuiteResults | None, SuiteResults | None]],
) -> None:
    """
    rows: list of (defense_name, suite_name, clean_results, attacked_results)
    clean_results may be None if not run.
    """
    header = f"{'Defense':<26} {'Suite':<10} {'Utility (clean)':>16} {'Utility (attacked)':>20} {'ASR':>8}  {'Overhead':>10}"
    print(header)
    print("-" * 95)

    for defense, suite, clean, attacked in rows:
        u_clean = _pct(sum(clean["utility_results"].values()) / max(len(clean["utility_results"]), 1)) if clean else "N/A"
        if attacked:
            u_atk_vals = list(attacked["utility_results"].values())
            s_vals = list(attacked["security_results"].values())
            u_atk = _pct(sum(u_atk_vals) / max(len(u_atk_vals), 1))
            asr_val = _pct(sum(s_vals) / max(len(s_vals), 1))
            if clean:
                u_c = sum(clean["utility_results"].values()) / max(len(clean["utility_results"]), 1)
                u_a = sum(u_atk_vals) / max(len(u_atk_vals), 1)
                overhead = _pct(u_c - u_a)
            else:
                overhead = "N/A"
        else:
            u_atk = asr_val = overhead = "N/A"

        print(f"  {defense:<24} {suite:<10} {u_clean:>16} {u_atk:>20} {asr_val:>8}  {overhead:>10}")


def print_task_breakdown(label: str, results: SuiteResults) -> None:
    print(f"\n  {label}:")
    for (ut, it), ok in results["utility_results"].items():
        sec = results["security_results"].get((ut, it), None)
        u = "OK" if ok else "FAIL"
        s = ("SAFE" if not sec else "INJECT") if sec is not None else "N/A"
        print(f"    {ut} × {it}:  utility={u}  security={s}")
