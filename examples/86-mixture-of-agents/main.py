from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTIONS  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    print("=== 86 · Mixture of Agents ===")
    print("Ref: Wang et al. 2024 — arxiv.org/abs/2406.04692\n")

    app = create_workflow()

    for question in SAMPLE_QUESTIONS:
        print(f"Question: {question}")
        print("-" * 60)

        result = app.invoke({"question": question, "proposals": [], "final_answer": ""})

        print("Individual proposals:")
        for i, p in enumerate(result["proposals"], 1):
            # Show just the first 80 chars of each proposal for readability
            preview = p.split("\n")[1][:80] + "..." if len(p) > 80 else p
            print(f"  {i}. {preview}")

        print(f"\nSynthesised answer:\n{result['final_answer']}\n")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
