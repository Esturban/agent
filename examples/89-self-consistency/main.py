from dotenv import load_dotenv

load_dotenv()

from src.tools import N_PATHS, SAMPLE_PROBLEMS  # noqa: E402
from src.workflow import create_workflow         # noqa: E402


def main() -> None:
    print("=== 89 · Self-Consistency ===")
    print("Ref: Wang et al. 2022 — arxiv.org/abs/2203.11171\n")
    print(f"Sampling {N_PATHS} independent reasoning paths per question.\n")

    app = create_workflow()

    for item in SAMPLE_PROBLEMS:
        question = item["question"]
        known_answer = item["answer"]

        print(f"Question: {question}")
        print(f"Known answer: {known_answer}")
        print("-" * 60)

        result = app.invoke({
            "question": question,
            "reasoning_paths": [],
            "final_answer": "",
        })

        # Show a preview of each reasoning path — first 100 chars of final line.
        print(f"Generated {len(result['reasoning_paths'])} reasoning paths:")
        for i, path in enumerate(result["reasoning_paths"], 1):
            # Show the last non-empty line (usually contains 'Final answer:').
            last_line = next(
                (ln.strip() for ln in reversed(path.split("\n")) if ln.strip()),
                path[:80]
            )
            print(f"  Path {i}: ...{last_line[:90]}")

        print(f"\nMajority vote: {result['final_answer']}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
