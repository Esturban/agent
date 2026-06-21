from dotenv import load_dotenv

from src.workflow import create_workflow


def main():
    load_dotenv()
    print("=== 111 — OpenAI Fine-Tuning API ===\n")
    print("Task: customer service tone classification (formal / informal / urgent)")
    print("Training set: 50 synthetic examples | Eval: 12 held-out examples")
    print("dry_run=True → uploads data but does NOT launch a training job (~$0.02-0.05)\n")
    result = create_workflow(dry_run=True)
    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
