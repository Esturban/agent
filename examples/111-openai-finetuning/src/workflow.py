from pathlib import Path

from openai import OpenAI

from .tools import (
    create_finetuning_job,
    generate_eval_examples,
    generate_training_examples,
    poll_job_until_done,
    run_evaluation,
    upload_training_file,
    write_jsonl,
)


def create_workflow(dry_run: bool = True, base_model: str = "gpt-4o-mini-2024-07-18"):
    """
    Full OpenAI fine-tuning pipeline.

    Stages:
      1. Generate synthetic JSONL training data (50 examples)
      2. Upload to OpenAI Files API
      3. Launch fine-tuning job
      4. Poll until complete
      5. Run evaluation: base vs. fine-tuned accuracy

    dry_run=True: stops after upload (no actual training job launched).
                  Saves ~$0.02-0.05 during demos.
    """
    client = OpenAI()
    out_dir = Path(__file__).parent.parent / "data"

    print("Stage 1: Generating training data...")
    train_examples = generate_training_examples(n=50)
    eval_examples = generate_eval_examples(n=12)

    jsonl_path = out_dir / "train.jsonl"
    write_jsonl(train_examples, jsonl_path)
    print(f"  Written {len(train_examples)} examples → {jsonl_path}")

    print("\nStage 2: Uploading to OpenAI Files API...")
    file_id = upload_training_file(client, jsonl_path)
    print(f"  File uploaded: {file_id}")

    if dry_run:
        print("\n[DRY RUN] Stopping before job creation (set dry_run=False to train).")
        return {
            "stage": "uploaded",
            "file_id": file_id,
            "train_count": len(train_examples),
            "eval_count": len(eval_examples),
        }

    print("\nStage 3: Launching fine-tuning job...")
    job_id = create_finetuning_job(client, file_id, model=base_model)
    print(f"  Job created: {job_id}")

    print("\nStage 4: Polling job status (this typically takes 5-20 min)...")
    job_result = poll_job_until_done(client, job_id)

    if job_result["status"] != "succeeded":
        print(f"  Job failed: {job_result}")
        return job_result

    finetuned_model = job_result["fine_tuned_model"]
    print(f"  Fine-tuned model ready: {finetuned_model}")
    print(f"  Trained tokens: {job_result['trained_tokens']}")

    print("\nStage 5: Running evaluation (base vs. fine-tuned)...")
    results = run_evaluation(client, base_model, finetuned_model, eval_examples)

    print(f"\n{'='*50}")
    print(f"Base model accuracy:       {results['base_accuracy']:.0%}")
    print(f"Fine-tuned model accuracy: {results['finetuned_accuracy']:.0%}")
    print(f"Improvement:               {results['improvement']:+.0%}")
    print(f"{'='*50}")

    return results
