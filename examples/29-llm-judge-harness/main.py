"""
Example 29 — LLM-as-Judge Harness

What this shows:
  How to evaluate a RAG pipeline WITHOUT labelled data.
  An LLM judge scores each answer on three dimensions:
    - Relevance:    does the answer address the question?
    - Faithfulness: are all claims grounded in retrieved context?
    - Completeness: how fully does it answer given the context?

Why it matters:
  Traditional eval requires ground-truth labels.
  LLM-as-judge scales to any domain with no annotation cost.
  The tradeoff: judge bias and consistency — that's why we score three dimensions.
"""

from dotenv import load_dotenv
load_dotenv()

from src.tools import build_rag_chain
from src.workflow import run_eval, TEST_QUESTIONS


def score_bar(score: int, max_score: int = 5) -> str:
    return "█" * score + "░" * (max_score - score)


def print_result(i: int, r: dict) -> None:
    avg = (r["relevance"] + r["faithfulness"] + r["completeness"]) / 3
    print(f"\n[Q{i}] {r['question']}")
    print(f"  Answer     : {r['answer'][:120].strip()}{'...' if len(r['answer']) > 120 else ''}")
    print(f"  Relevance  : [{score_bar(r['relevance'])}] {r['relevance']}/5")
    print(f"  Faithful   : [{score_bar(r['faithfulness'])}] {r['faithfulness']}/5")
    print(f"  Complete   : [{score_bar(r['completeness'])}] {r['completeness']}/5")
    print(f"  Avg score  : {avg:.1f}/5")
    reasoning = r.get("reasoning", "")
    if reasoning:
        parts = reasoning.split("|")
        for part in parts:
            if part.strip():
                print(f"  Note       : {part.strip()}")


def main():
    print("LLM-as-Judge Harness — evaluating a RAG pipeline without labelled data")
    print("=" * 68)
    print(f"Test set   : {len(TEST_QUESTIONS)} questions")
    print(f"Dimensions : Relevance, Faithfulness, Completeness (each 1–5)")
    print(f"Judge      : gpt-4o-mini  |  RAG model: gpt-4o-mini\n")
    print("Building RAG index...")

    chain = build_rag_chain()
    results = run_eval(chain)

    for i, r in enumerate(results, 1):
        print_result(i, r)

    # Aggregate summary — useful for comparing pipeline variants
    print("\n" + "=" * 68)
    print("AGGREGATE SCORES")
    for dim in ("relevance", "faithfulness", "completeness"):
        avg = sum(r[dim] for r in results) / len(results)
        print(f"  {dim.capitalize():14}: {avg:.2f} / 5.0  [{score_bar(round(avg))}]")

    overall = sum(
        (r["relevance"] + r["faithfulness"] + r["completeness"]) / 3
        for r in results
    ) / len(results)
    print(f"\n  Overall avg : {overall:.2f} / 5.0")
    print("\nTip: swap the RAG chain in tools.py to compare pipeline variants side-by-side.")


if __name__ == "__main__":
    main()
