from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_PROBLEMS  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    print("=== 91 · Analogical Reasoning ===")
    print("Ref: Webb et al. 2023 — nature.com/articles/s41562-023-01659-w\n")
    print("Key: the model generates its OWN analogous examples — no human-curated few-shots.\n")

    app = create_workflow()

    for problem in SAMPLE_PROBLEMS:
        print(f"Problem: {problem}")
        print("-" * 60)

        result = app.invoke({
            "problem": problem,
            "analogies": "",
            "answer": "",
        })

        # Show a preview of the self-generated analogies (first 300 chars).
        analogies_preview = result["analogies"][:300].replace("\n", " ")
        print(f"Self-generated analogies (preview):\n  {analogies_preview}...\n")
        print(f"Answer:\n{result['answer']}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
