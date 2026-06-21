import json
import random
import time
from pathlib import Path

from openai import OpenAI


LABELS = ["formal", "informal", "urgent"]

FORMAL_TEMPLATES = [
    "I am writing to inquire about the status of my order #{order_id}.",
    "Could you please provide an update regarding my recent purchase?",
    "I would like to request information about your return policy.",
    "Please advise on the estimated delivery timeline for order #{order_id}.",
    "I wish to formally request a refund for the defective item received.",
    "Kindly confirm receipt of my previous correspondence.",
    "I am following up on the unresolved issue submitted on {date}.",
    "May I inquire about the terms and conditions for warranty claims?",
    "I respectfully request escalation of this matter to a senior representative.",
    "Please provide written confirmation of the agreed resolution.",
]

INFORMAL_TEMPLATES = [
    "Hey, where's my order? It's been a week!",
    "Just checking in — did you guys get my return?",
    "Hi! Can you help me figure out what happened to my package?",
    "Any update on when my stuff will show up?",
    "Hey there, I need help changing my delivery address.",
    "Quick question — can I swap this for a different color?",
    "Yo, my order shows delivered but I don't have it??",
    "Hey can someone look into this for me please?",
    "Got the wrong item lol, how do I fix this?",
    "Just wondering if there's a discount code I can use.",
]

URGENT_TEMPLATES = [
    "URGENT: My event is tomorrow and the order hasn't arrived!!!",
    "This is critical — I need this resolved TODAY or I'm disputing the charge.",
    "EMERGENCY: The item I received is dangerous and I need an immediate callback.",
    "I have been waiting 3 weeks. This needs to be fixed RIGHT NOW.",
    "My client presentation is in 2 hours and the product is missing. Help!!",
    "Critical issue: the system is sending me duplicate charges, need immediate fix.",
    "I need a supervisor NOW — this has gone on long enough.",
    "ASAP — I'm at the store trying to return this and your system is down.",
    "My order is perishable and it's now 4 days late. I need action immediately.",
    "CRITICAL: Wrong medication dosage label — need callback within the hour.",
]


def generate_training_examples(n: int = 50, seed: int = 42) -> list[dict]:
    """
    Generate N synthetic training examples for tone classification.
    Each example: {messages: [{role, content}, {role, content}]}
    Labels are balanced across formal / informal / urgent.
    """
    random.seed(seed)
    examples = []
    templates = {
        "formal": FORMAL_TEMPLATES,
        "informal": INFORMAL_TEMPLATES,
        "urgent": URGENT_TEMPLATES,
    }

    system_msg = (
        "You are a tone classifier for customer service messages. "
        "Classify each message as exactly one of: formal, informal, urgent. "
        "Reply with only the label — no explanation."
    )

    for i in range(n):
        label = LABELS[i % len(LABELS)]
        tmpl = random.choice(templates[label])
        message = tmpl.format(order_id=random.randint(10000, 99999), date="2024-01-15")
        examples.append(
            {
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": label},
                ]
            }
        )
    return examples


def generate_eval_examples(n: int = 12, seed: int = 99) -> list[dict]:
    """Generate N held-out evaluation examples (not in training set)."""
    random.seed(seed)
    examples = []
    templates = {
        "formal": [
            "I would appreciate your earliest response to my outstanding query.",
            "Please provide documentation confirming my subscription cancellation.",
            "I am requesting a formal acknowledgment of the delay in my order.",
            "Kindly review the attached invoice discrepancy at your earliest convenience.",
        ],
        "informal": [
            "Can u guys check on my order? Thanks!",
            "Lol I think I ordered the wrong size, can I change it?",
            "Hey is there any way to track my package?",
            "Oh no I think I gave you the wrong address — help!",
        ],
        "urgent": [
            "I NEED THIS FIXED IMMEDIATELY — my business depends on it.",
            "Emergency: the device exploded and I need a recall report NOW.",
            "DROP EVERYTHING — I've been double-billed $500 and need it reversed today.",
            "URGENT URGENT URGENT: wrong address, delivery attempt tomorrow morning!!!",
        ],
    }

    for i in range(n):
        label = LABELS[i % len(LABELS)]
        msg = random.choice(templates[label])
        examples.append({"message": msg, "label": label})
    return examples


def write_jsonl(examples: list[dict], path: Path) -> Path:
    """Write training examples to JSONL format required by OpenAI."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")
    return path


def upload_training_file(client: OpenAI, jsonl_path: Path) -> str:
    """Upload JSONL to OpenAI Files API. Returns file_id."""
    with open(jsonl_path, "rb") as f:
        response = client.files.create(file=f, purpose="fine-tune")
    return response.id


def create_finetuning_job(client: OpenAI, file_id: str, model: str = "gpt-4o-mini-2024-07-18") -> str:
    """Launch a fine-tuning job. Returns job_id."""
    job = client.fine_tuning.jobs.create(
        training_file=file_id,
        model=model,
        hyperparameters={"n_epochs": 3},
    )
    return job.id


def poll_job_until_done(client: OpenAI, job_id: str, poll_interval: int = 30) -> dict:
    """Poll fine-tuning job until status is succeeded or failed."""
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        status = job.status
        print(f"  Job {job_id[:20]}... status: {status}")
        if status in ("succeeded", "failed", "cancelled"):
            return {
                "status": status,
                "fine_tuned_model": getattr(job, "fine_tuned_model", None),
                "trained_tokens": getattr(job, "trained_tokens", None),
                "error": getattr(job, "error", None),
            }
        time.sleep(poll_interval)


def classify_message(client: OpenAI, model: str, message: str) -> str:
    """Run single tone classification call. Returns predicted label."""
    system_msg = (
        "You are a tone classifier for customer service messages. "
        "Classify each message as exactly one of: formal, informal, urgent. "
        "Reply with only the label — no explanation."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": message},
        ],
        temperature=0,
        max_tokens=10,
    )
    return response.choices[0].message.content.strip().lower()


def run_evaluation(
    client: OpenAI, base_model: str, finetuned_model: str, eval_examples: list[dict]
) -> dict:
    """
    Run the same eval set against both models.
    Returns accuracy scores and per-example breakdown.
    """
    base_results = []
    ft_results = []

    for ex in eval_examples:
        msg = ex["message"]
        expected = ex["label"]

        base_pred = classify_message(client, base_model, msg)
        ft_pred = classify_message(client, finetuned_model, msg)

        base_results.append(
            {"message": msg[:60], "expected": expected, "predicted": base_pred, "correct": base_pred == expected}
        )
        ft_results.append(
            {"message": msg[:60], "expected": expected, "predicted": ft_pred, "correct": ft_pred == expected}
        )

    base_acc = sum(r["correct"] for r in base_results) / len(base_results)
    ft_acc = sum(r["correct"] for r in ft_results) / len(ft_results)

    return {
        "base_model": base_model,
        "finetuned_model": finetuned_model,
        "n_eval": len(eval_examples),
        "base_accuracy": base_acc,
        "finetuned_accuracy": ft_acc,
        "improvement": ft_acc - base_acc,
        "base_results": base_results,
        "ft_results": ft_results,
    }
