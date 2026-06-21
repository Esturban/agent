"""
122 — Eval CI Pipeline
Entry point: run golden dataset eval and show CI pass/fail pattern.
Run: python examples/122-eval-ci-pipeline/main.py
"""

from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow


def main():
    print("Concept: wire LLM evaluation metrics as pytest tests.")
    print("A score regression fails the CI build automatically.\n")
    results = create_workflow()
    good = results["good"]
    bad = results["degraded"]
    print(f"\nSummary:")
    print(f"  Good pipeline:    {'PASS' if good['passed'] else 'FAIL'} (score={good['avg_combined']:.3f})")
    print(f"  Degraded pipeline:{'PASS' if bad['passed'] else 'FAIL'} (score={bad['avg_combined']:.3f})")
    print("\nKey insight: degraded pipeline fails CI automatically — no manual review needed.")


if __name__ == "__main__":
    main()
