import os
from dotenv import load_dotenv

load_dotenv()

from src.tools import QUESTIONS        # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    print("=== 98 · Skeleton-of-Thought ===")
    print("Serial: one LLM call builds the outline")
    print("Parallel: each point expanded concurrently via Send()")
    print("Ref: Ning et al. 2023 — arxiv.org/abs/2307.15337\n")

    app = create_workflow()

    for question in QUESTIONS:
        print(f"Q: {question}\n")

        result = app.invoke({
            "question":   question,
            "skeleton":   [],
            "expansions": [],
            "answer":     "",
        })

        print("Skeleton (generated in one call):")
        for point in result["skeleton"]:
            print(f"  {point}")
        print(f"\nExpanded in parallel ({len(result['skeleton'])} concurrent LLM calls):")
        print("-" * 60)
        print(result["answer"])
        print("=" * 70)
        print()

    print("Note: wall-clock time ≈ skeleton call + ONE expand call (not N).")
    print("LangGraph fires all expand nodes concurrently; idx sorts the result.")


if __name__ == "__main__":
    main()
