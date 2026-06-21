from dotenv import load_dotenv

from src.workflow import create_workflow


def main():
    load_dotenv()
    print("=== 113 — DPO: Direct Preference Optimization ===\n")
    print("Aligning a small model toward safe refusals using DPO (no reward model needed).\n")
    result = create_workflow(
        model_name="HuggingFaceTB/SmolLM2-135M-Instruct",
        n_examples=50,
        num_train_epochs=1,
    )
    print("\n--- Before/After Safety Comparison ---")
    report = result["safety_report"]
    print(f"Refusal rate BEFORE: {report['before_refusal_rate']:.0%}")
    print(f"Refusal rate AFTER:  {report['after_refusal_rate']:.0%}")
    print("\nPer-prompt breakdown:")
    for c in report["comparisons"]:
        print(f"\n  Prompt: {c['prompt'][:80]}")
        print(f"  Before ({'+refusal' if c['before_is_refusal'] else '-unsafe'}): {c['before'][:100]}")
        print(f"  After  ({'+refusal' if c['after_is_refusal'] else '-unsafe'}): {c['after'][:100]}")


if __name__ == "__main__":
    main()
