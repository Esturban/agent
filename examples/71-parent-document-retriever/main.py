from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTIONS  # noqa: E402
from src.workflow import ParentDocState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    for question in SAMPLE_QUESTIONS:
        print(f"\n{'=' * 60}")
        print(f"Question      : {question}")
        result: ParentDocState = app.invoke(
            {"question": question, "child_chunks": [], "parent_docs": [], "answer": ""}
        )
        child_count = len(result["child_chunks"])
        parent_count = len(result["parent_docs"])
        child_avg = sum(len(c) for c in result["child_chunks"]) // max(child_count, 1)
        parent_avg = sum(len(d) for d in result["parent_docs"]) // max(parent_count, 1)
        print(f"Child chunks  : {child_count}  (avg {child_avg} chars each)")
        print(f"Parent docs   : {parent_count}  (avg {parent_avg} chars each)")
        print(f"Answer        : {result['answer'][:300]}")


if __name__ == "__main__":
    main()
