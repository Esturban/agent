"""
Format benchmark results as a markdown table with summary statistics.

Key metrics from AgentDojo (arxiv:2406.13352):
  Utility rate  = % of tasks where task_success == True
  ASR           = % of tasks where injection_success == True (lower is better)
  Defense overhead = utility_clean - utility_attacked (lower is better)
"""

from .harness import TaskResult


def _pct(num: int, den: int) -> str:
    if den == 0:
        return "N/A"
    return f"{100 * num / den:.1f}%"


def compute_stats(results: list[TaskResult]) -> dict:
    total = len(results)
    task_ok = sum(1 for r in results if r.task_success)
    inj_ok = sum(1 for r in results if r.injection_success)
    errors = sum(1 for r in results if r.error)
    return {
        "total": total,
        "utility_rate": _pct(task_ok, total),
        "asr": _pct(inj_ok, total),
        "error_rate": _pct(errors, total),
        "utility_n": task_ok,
        "asr_n": inj_ok,
    }


def format_results_table(all_results: dict[str, list[TaskResult]]) -> str:
    lines = []
    lines.append("## AgentDojo Benchmark Results\n")
    lines.append(
        f"{'Defense':<24} {'Suite':<12} {'Utility Rate':>14} {'ASR':>10} {'Errors':>8}"
    )
    lines.append("-" * 72)

    for key, results in all_results.items():
        defense, suite = key.split("|")
        stats = compute_stats(results)
        lines.append(
            f"{defense:<24} {suite:<12} {stats['utility_rate']:>14} "
            f"{stats['asr']:>10} {stats['error_rate']:>8}"
        )

    return "\n".join(lines)


def format_defense_comparison(
    clean_results: dict[str, list[TaskResult]],
    attacked_results: dict[str, list[TaskResult]],
) -> str:
    lines = []
    lines.append("\n## Defense Overhead (utility_clean − utility_attacked)\n")
    lines.append(f"{'Defense':<24} {'Suite':<12} {'Clean':>8} {'Attacked':>10} {'Overhead':>10} {'ASR':>10}")
    lines.append("-" * 76)

    for defense in {k.split("|")[0] for k in clean_results}:
        for suite in {k.split("|")[1] for k in clean_results}:
            c_key = f"{defense}|{suite}"
            a_key = f"{defense}|{suite}"
            if c_key not in clean_results or a_key not in attacked_results:
                continue
            c_stats = compute_stats(clean_results[c_key])
            a_stats = compute_stats(attacked_results[a_key])

            def to_float(pct_str):
                return float(pct_str.rstrip("%")) if pct_str != "N/A" else 0.0

            overhead = to_float(c_stats["utility_rate"]) - to_float(a_stats["utility_rate"])
            lines.append(
                f"{defense:<24} {suite:<12} {c_stats['utility_rate']:>8} "
                f"{a_stats['utility_rate']:>10} {overhead:>9.1f}% {a_stats['asr']:>10}"
            )

    lines.append("\nKey insight (AgentDojo paper): Spotlighting-encode reduces ASR")
    lines.append("to near 0% with minimal utility overhead (~2-5pp on most tasks.")
    lines.append("Undefended agents comply with injections ~17% of the time on")
    lines.append("benign-looking tasks, rising to >40% on targeted attack suites.")
    return "\n".join(lines)


def print_report(
    clean_results: dict[str, list[TaskResult]],
    attacked_results: dict[str, list[TaskResult]],
) -> None:
    print(format_results_table({**clean_results, **attacked_results}))
    print(format_defense_comparison(clean_results, attacked_results))
