"""DPO alignment workflow — generates preference dataset, trains with DPOTrainer, compares before/after."""
from .tools import generate_preference_dataset, save_as_hf_dataset, generate_response, evaluate_safety


def create_workflow(
    model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct",
    n_examples: int = 50,
    num_train_epochs: int = 10,
) -> dict:
    """
    Full DPO alignment pipeline:
    1. Generate preference dataset (chosen=safe refusal, rejected=unsafe response)
    2. Load base model + tokenizer
    3. Attach LoRA adapter (for memory-efficient DPO)
    4. Run DPOTrainer
    5. Compare before/after on 5 test prompts

    Returns results dict with training info and before/after comparisons.
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model, TaskType
    from trl import DPOTrainer, DPOConfig

    torch.manual_seed(42)
    print("Step 1: Generating preference dataset...")
    examples = generate_preference_dataset(n=n_examples)
    dataset = save_as_hf_dataset(examples)
    print(f"  Dataset: {len(dataset)} examples | columns: {dataset.column_names}")

    print(f"\nStep 2: Loading base model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(model_name)

    print("\nStep 3: Generating BEFORE responses (base model)...")
    eval_prompts = [ex["prompt"] for ex in examples[:5]]
    responses_before = [generate_response(base_model, tokenizer, p) for p in eval_prompts]

    print("\nStep 4: Attaching LoRA adapter for DPO training...")
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    model_with_lora = get_peft_model(base_model, lora_config)
    trainable = sum(p.numel() for p in model_with_lora.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model_with_lora.parameters())
    print(f"  Trainable params: {trainable:,} / {total:,} ({100*trainable/total:.2f}%)")

    print("\nStep 5: Running DPOTrainer...")
    dpo_config = DPOConfig(
        output_dir="./dpo_output",
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=2,
        learning_rate=1e-4,
        beta=0.1,
        logging_steps=10,
        remove_unused_columns=False,
        report_to="none",
    )

    trainer = DPOTrainer(
        model=model_with_lora,
        args=dpo_config,
        train_dataset=dataset,
        processing_class=tokenizer,
    )
    train_result = trainer.train()

    print("\nStep 6: Generating AFTER responses (aligned model)...")
    responses_after = [generate_response(model_with_lora, tokenizer, p) for p in eval_prompts]

    print("\nStep 7: Safety evaluation...")
    safety_report = evaluate_safety(responses_before, responses_after, eval_prompts)

    return {
        "model": model_name,
        "n_train_examples": n_examples,
        "num_train_epochs": num_train_epochs,
        "trainable_params": trainable,
        "total_params": total,
        "train_loss": train_result.training_loss if hasattr(train_result, "training_loss") else None,
        "safety_report": safety_report,
        "eval_prompts": eval_prompts,
        "responses_before": responses_before,
        "responses_after": responses_after,
    }
