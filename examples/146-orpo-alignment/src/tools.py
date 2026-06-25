def build_preference_dataset(n: int = 20):
    from datasets import Dataset
    chosen = [
        "Here is a clear, step-by-step solution: First, identify the problem. Then, break it into subproblems.",
        "The answer is 42. This is computed by multiplying 6 by 7.",
        "To reverse a list in Python, use `my_list[::-1]` or `list(reversed(my_list))`.",
        "The capital of France is Paris, which has been the country's capital since 987 AD.",
        "Use `git commit -m 'message'` to commit staged changes with a descriptive message.",
    ]
    rejected = [
        "I dunno, maybe try something?",
        "The answer could be many things.",
        "You can do it lots of ways I guess.",
        "France has a capital city somewhere in Europe.",
        "Just run some git command or something.",
    ]
    prompts = [
        "How do you approach solving a complex problem?",
        "What is 6 times 7?",
        "How do you reverse a list in Python?",
        "What is the capital of France?",
        "How do you commit changes in git?",
    ]
    rows = [{"prompt": p, "chosen": c, "rejected": r}
            for p, c, r in zip(prompts, chosen, rejected)] * (n // len(prompts) + 1)
    return Dataset.from_list(rows[:n])


def get_orpo_config(output_dir: str = "/tmp/orpo", max_steps: int = 30):
    from trl import ORPOConfig
    return ORPOConfig(
        output_dir=output_dir,
        max_steps=max_steps,
        per_device_train_batch_size=1,
        learning_rate=8e-6,
        beta=0.1,
        max_length=128,
        max_prompt_length=64,
        logging_steps=10,
        save_strategy="no",
        report_to="none",
    )


def eval_preference_rate(model, tokenizer, dataset, n: int = 5) -> float:
    import torch
    wins = 0
    for row in list(dataset)[:n]:
        prompt = row["prompt"]
        chosen, rejected = row["chosen"], row["rejected"]
        inputs_c = tokenizer(prompt + chosen, return_tensors="pt").to(model.device)
        inputs_r = tokenizer(prompt + rejected, return_tensors="pt").to(model.device)
        with torch.no_grad():
            loss_c = model(**inputs_c, labels=inputs_c["input_ids"]).loss
            loss_r = model(**inputs_r, labels=inputs_r["input_ids"]).loss
        if loss_c < loss_r:
            wins += 1
    return round(wins / n, 3)
