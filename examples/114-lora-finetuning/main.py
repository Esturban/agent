from dotenv import load_dotenv

from src.workflow import create_workflow


def main():
    load_dotenv()
    print("=== 114 — LoRA Fine-Tuning ===\n")
    print("Loading SmolLM2-135M, attaching LoRA adapters (r=8), training on Python Q&A, merging.\n")
    result = create_workflow(
        model_name="HuggingFaceTB/SmolLM2-135M-Instruct",
        num_epochs=1,
    )
    no_lora = result["params_no_lora"]
    with_lora = result["params_with_lora"]
    print("\n--- Parameter Counts ---")
    print(f"Without LoRA: {no_lora['trainable_params']:,} trainable ({no_lora['percentage']:.1f}%)")
    print(f"With LoRA:    {with_lora['trainable_params']:,} trainable ({with_lora['percentage']:.2f}%)")
    print(f"LoRA adds only {100*(with_lora['trainable_params']/no_lora['total_params']):.2f}% extra parameters")
    if result["train_loss"]:
        print(f"Training loss: {result['train_loss']:.4f}")
    print("\n--- Before/After Comparison ---")
    for i, (prompt, before, after) in enumerate(zip(
        result["test_prompts"], result["responses_before"], result["responses_after"]
    ), 1):
        print(f"\n[{i}] Q: {prompt}")
        print(f"    Before: {before[:120]}")
        print(f"    After:  {after[:120]}")


if __name__ == "__main__":
    main()
