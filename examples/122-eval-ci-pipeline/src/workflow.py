"""
122 — Eval CI Pipeline
Workflow: evaluate good vs degraded pipeline, show CI pass/fail pattern.
"""

from .tools import (
    build_test_case,
    degraded_pipeline,
    load_golden_dataset,
    run_pipeline,
    score_faithfulness_simple,
    score_relevancy_simple,
)

PASS_THRESHOLD = 0.5  # minimum average score to "pass" CI


def _evaluate_pipeline(pipeline_fn, dataset: list[dict], label: str) -> dict:
    """Run pipeline on dataset and score each response."""
    print(f"\n--- {label} ---")
    test_cases = []
    faithfulness_scores = []
    relevancy_scores = []

    for row in dataset:
        actual = pipeline_fn(row["question"], row["context"])
        tc = build_test_case(row, actual)
        f_score = score_faithfulness_simple(actual, row["context"])
        r_score = score_relevancy_simple(actual, row["question"])
        faithfulness_scores.append(f_score)
        relevancy_scores.append(r_score)
        test_cases.append(tc)

    avg_f = sum(faithfulness_scores) / len(faithfulness_scores)
    avg_r = sum(relevancy_scores) / len(relevancy_scores)
    avg = (avg_f + avg_r) / 2

    print(f"  Faithfulness:   {avg_f:.3f}  (threshold: {PASS_THRESHOLD})")
    print(f"  Answer Relevancy: {avg_r:.3f}  (threshold: {PASS_THRESHOLD})")
    print(f"  Combined avg:   {avg:.3f}")
    passed = avg >= PASS_THRESHOLD
    print(f"  CI status:      {'PASS' if passed else 'FAIL'}")

    return {
        "label": label,
        "avg_faithfulness": avg_f,
        "avg_relevancy": avg_r,
        "avg_combined": avg,
        "passed": passed,
        "test_cases": test_cases,
    }


def create_workflow() -> dict:
    """Run golden dataset evaluation on both pipelines and show CI pass/fail."""
    print("=== 122 — Eval CI Pipeline ===\n")
    print("Using simple local scoring (keyword overlap).")
    print("Replace score_faithfulness_simple/score_relevancy_simple with DeepEval for production.\n")

    dataset = load_golden_dataset()
    print(f"Golden dataset: {len(dataset)} Q&A pairs\n")

    good_result = _evaluate_pipeline(run_pipeline, dataset, "Good Pipeline (uses context)")
    bad_result = _evaluate_pipeline(degraded_pipeline, dataset, "Degraded Pipeline (ignores context)")

    # Show pytest pattern
    print("\n--- Equivalent pytest pattern (with DeepEval) ---")
    print("""
  # tests/test_pipeline_eval.py
  import pytest
  from deepeval import assert_test
  from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
  from deepeval.test_case import LLMTestCase

  @pytest.mark.parametrize("row", load_golden_dataset())
  def test_pipeline_faithfulness(row):
      actual = run_pipeline(row["question"], row["context"])
      test_case = LLMTestCase(input=row["question"], actual_output=actual,
                               expected_output=row["expected_output"],
                               retrieval_context=[row["context"]])
      assert_test(test_case, [FaithfulnessMetric(threshold=0.5)])
    """)

    return {"good": good_result, "degraded": bad_result}
