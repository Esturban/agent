from typing import TypedDict
from .tools import get_bnb_config, load_quantized_model, count_trainable, get_vram_mb, load_sample_dataset


class QLoRAState(TypedDict):
    model_name: str
    lora_rank: int
    n_steps: int
    vram_before_mb: float
    vram_after_mb: float
    param_stats: dict
    final_loss: float


def run_qlora(state: QLoRAState) -> QLoRAState:
    from peft import get_peft_model, LoraConfig, TaskType
    from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling
    from datasets import Dataset

    bnb = get_bnb_config()
    vram_before = get_vram_mb()
    model, tokenizer = load_quantized_model(state["model_name"], bnb)

    lora_cfg = LoraConfig(
        r=state.get("lora_rank", 8),
        lora_alpha=state.get("lora_rank", 8) * 2,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    model = get_peft_model(model, lora_cfg)
    param_stats = count_trainable(model)
    vram_after = get_vram_mb()

    raw = load_sample_dataset(50)
    texts = [f"Q: {r['prompt']}\nA: {r['response']}" for r in raw]
    enc = tokenizer(texts, truncation=True, max_length=128, padding="max_length", return_tensors="pt")
    ds = Dataset.from_dict({k: v.tolist() for k, v in enc.items()})
    ds = ds.map(lambda x: {"labels": x["input_ids"]})

    args = TrainingArguments(output_dir="/tmp/qlora", max_steps=state.get("n_steps", 30),
                             per_device_train_batch_size=1, learning_rate=2e-4,
                             logging_steps=10, save_strategy="no", report_to="none")
    trainer = Trainer(model=model, args=args, train_dataset=ds,
                      data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False))
    result = trainer.train()

    return {**state, "vram_before_mb": vram_before, "vram_after_mb": vram_after,
            "param_stats": param_stats, "final_loss": round(result.training_loss, 4)}


def create_workflow():
    def run(state: QLoRAState) -> QLoRAState:
        return run_qlora(state)
    return run
