"""LoRA fine-tuning workflow — attach adapters, train, merge, compare before/after."""
from .tools import load_sample_dataset, tokenize_for_training, count_trainable_params, generate_response


def create_workflow(
    model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct",
    num_epochs: int = 1,
) -> dict:
    """
    Full LoRA fine-tuning pipeline:
    1. Load base model + tokenizer
    2. Count params WITHOUT LoRA (all trainable)
    3. Attach LoRA adapters (r=8, lora_alpha=16)
    4. Count params WITH LoRA (~0.1% trainable)
    5. Load and tokenize Python Q&A dataset
    6. Train with Trainer
    7. Merge and unload adapters
    8. Run 5 before/after inference comparisons

    Returns results dict.
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
    from peft import LoraConfig, get_peft_model, TaskType

    torch.manual_seed(42)
    print(f"Step 1: Loading base model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    base_model = AutoModelForCausalLM.from_pretrained(model_name)

    print("\nStep 2: Parameter count WITHOUT LoRA")
    params_no_lora = count_trainable_params(base_model)
    print(f"  Trainable: {params_no_lora['trainable_params']:,} ({params_no_lora['percentage']:.1f}%)")

    print("\nStep 3: Generating BEFORE responses...")
    test_prompts = [
        "How do you reverse a list in Python?",
        "What is a list comprehension in Python?",
        "How do you handle exceptions in Python?",
        "What is a lambda function in Python?",
        "How do you use enumerate() in Python?",
    ]
    responses_before = [generate_response(base_model, tokenizer, p) for p in test_prompts]

    print("\nStep 4: Attaching LoRA adapters...")
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    model_lora = get_peft_model(base_model, lora_config)

    print("\nStep 5: Parameter count WITH LoRA")
    params_with_lora = count_trainable_params(model_lora)
    print(f"  Trainable: {params_with_lora['trainable_params']:,} ({params_with_lora['percentage']:.2f}%)")
    print(f"  Total:     {params_with_lora['total_params']:,}")

    print("\nStep 6: Loading and tokenizing dataset...")
    examples = load_sample_dataset(n=50)
    train_dataset = tokenize_for_training(examples, tokenizer, max_length=256)
    print(f"  Dataset: {len(train_dataset)} examples")

    print("\nStep 7: Training...")
    training_args = TrainingArguments(
        output_dir="./lora_output",
        num_train_epochs=num_epochs,
        per_device_train_batch_size=2,
        learning_rate=2e-4,
        logging_steps=10,
        save_strategy="no",
        report_to="none",
    )
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    trainer = Trainer(
        model=model_lora,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
    )
    train_result = trainer.train()

    print("\nStep 8: Merging LoRA adapters into base model...")
    merged_model = model_lora.merge_and_unload()
    params_merged = count_trainable_params(merged_model)
    print(f"  After merge: {params_merged['trainable_params']:,} trainable ({params_merged['percentage']:.1f}%)")

    print("\nStep 9: Generating AFTER responses...")
    responses_after = [generate_response(merged_model, tokenizer, p) for p in test_prompts]

    return {
        "model": model_name,
        "num_epochs": num_epochs,
        "params_no_lora": params_no_lora,
        "params_with_lora": params_with_lora,
        "params_merged": params_merged,
        "n_train_examples": len(train_dataset),
        "train_loss": train_result.training_loss if hasattr(train_result, "training_loss") else None,
        "test_prompts": test_prompts,
        "responses_before": responses_before,
        "responses_after": responses_after,
    }
