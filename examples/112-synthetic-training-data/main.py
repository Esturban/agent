from dotenv import load_dotenv

from src.workflow import create_workflow


def main():
    load_dotenv()
    print("=== 112 — Synthetic Training Data Generation ===\n")
    print("Task: generate diverse labeled training examples for tone classification")
    print("Pipeline: GPT-4o generator → embedding dedup → LLM judge → JSONL export\n")
    result = create_workflow(n_per_label=6, skip_judge=False)
    print(f"\nPipeline complete:")
    print(f"  Generated:   {result['generated']} raw examples")
    print(f"  After dedup: {result['after_dedup']} (dropped {result['n_dropped_dedup']})")
    print(f"  Valid:       {result['n_valid']} | Rejected: {result['n_rejected']}")
    print(f"  Exported:    {result['exported']} → {result['output_path']}")
    print(f"  Label split: {result['label_breakdown']}")


if __name__ == "__main__":
    main()
