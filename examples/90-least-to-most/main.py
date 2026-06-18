from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_PROBLEMS  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    print("=== 90 · Least-to-Most Prompting ===")
    print("Ref: Zhou et al. 2022 — arxiv.org/abs/2205.10625\n")

    app = create_workflow()

    for problem in SAMPLE_PROBLEMS:
        print(f"Problem: {problem}")
        print("-" * 60)

        result = app.invoke({
            "problem": problem,
            "subproblems": [],
            "solutions": [],
            "current_idx": 0,
            "final_answer": "",
        })

        print("Decomposed sub-problems:")
        for i, (sub, sol) in enumerate(
            zip(result["subproblems"], result["solutions"]), 1
        ):
            print(f"  Step {i}: {sub}")
            print(f"         → {sol[:100]}{'...' if len(sol) > 100 else ''}")

        print(f"\nFinal answer: {result['final_answer']}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
