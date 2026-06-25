def make_lora_config(r: int, target_modules: list[str], alpha: int | None = None):
    from peft import LoraConfig, TaskType
    return LoraConfig(
        r=r,
        lora_alpha=alpha or r * 2,
        target_modules=target_modules,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )


def count_trainable(model) -> dict:
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {"trainable": trainable, "total": total, "pct": round(100 * trainable / total, 4)}


def run_training_run(model_name: str, lora_config, n_steps: int = 20) -> dict:
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
    from peft import get_peft_model
    from datasets import Dataset

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    base = AutoModelForCausalLM.from_pretrained(model_name)
    model = get_peft_model(base, lora_config)
    params = count_trainable(model)

    texts = ["Question: What is LoRA? Answer: LoRA adds low-rank adapter matrices."] * 20
    tokenized = tokenizer(texts, truncation=True, max_length=64, padding="max_length", return_tensors="pt")
    ds = Dataset.from_dict({k: v.tolist() for k, v in tokenized.items()})
    ds = ds.map(lambda x: {"labels": x["input_ids"]})

    args = TrainingArguments(output_dir="/tmp/ablation", max_steps=n_steps, per_device_train_batch_size=2,
                             learning_rate=2e-4, logging_steps=n_steps, save_strategy="no", report_to="none")
    trainer = Trainer(model=model, args=args, train_dataset=ds,
                      data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False))
    result = trainer.train()
    return {"params": params, "final_loss": round(result.training_loss, 4)}
