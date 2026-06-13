from dotenv import load_dotenv

load_dotenv()

from src.tools import TEST_INPUTS  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    scores_a: list[float] = []
    scores_b: list[float] = []

    print(f"{'Question':<30} {'Score A':>8} {'Score B':>8} {'Winner':>6}")
    print("-" * 56)

    for question in TEST_INPUTS:
        result = app.invoke({"question": question, "response_a": "", "response_b": "", "score_a": 0.0, "score_b": 0.0})
        sa, sb = result["score_a"], result["score_b"]
        scores_a.append(sa)
        scores_b.append(sb)
        winner = "A" if sa > sb else ("B" if sb > sa else "tie")
        print(f"  {question[:28]:<28} {sa:>8.2f} {sb:>8.2f} {winner:>6}")

    avg_a = sum(scores_a) / len(scores_a)
    avg_b = sum(scores_b) / len(scores_b)
    overall = "A" if avg_a > avg_b else ("B" if avg_b > avg_a else "tie")
    print("-" * 56)
    print(f"  {'AVERAGE':<28} {avg_a:>8.2f} {avg_b:>8.2f} {overall:>6}")
    print(f"\nWinner: Variant {overall}  (A avg={avg_a:.2f}, B avg={avg_b:.2f})")


if __name__ == "__main__":
    main()
