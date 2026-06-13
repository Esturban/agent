from dotenv import load_dotenv

load_dotenv()

from src.tools import GOLDEN_QA_SET  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    scores: list[float] = []

    print(f"Evaluating {len(GOLDEN_QA_SET)} QA pairs...\n")
    for pair in GOLDEN_QA_SET:
        result = app.invoke({"question": pair["question"], "expected": pair["expected"], "actual": "", "result": {}})
        r = result["result"]
        scores.append(r["score"])
        status = "PASS" if r["exact_match"] or r["semantic_match"] else "FAIL"
        print(f"  [{status}] Q: {pair['question']}")
        print(f"         Expected: {pair['expected']}")
        print(f"         Actual:   {result['actual'][:80]}")
        print(f"         Score: {r['score']}  cosine: {r['cosine_similarity']}\n")

    avg_score = sum(scores) / len(scores)
    pass_rate = sum(1 for s in scores if s >= 0.80) / len(scores)
    print(f"Summary: avg_score={avg_score:.2f}  pass_rate={pass_rate:.0%} ({int(pass_rate * len(scores))}/{len(scores)})")


if __name__ == "__main__":
    main()
