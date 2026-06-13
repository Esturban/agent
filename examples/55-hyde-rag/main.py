from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUERIES  # noqa: E402
from src.workflow import HyDEState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    for query in SAMPLE_QUERIES:
        print(f"\n{'=' * 60}")
        print(f"Query     : {query}")
        result: HyDEState = app.invoke(
            {"query": query, "hypothesis": "", "documents": [], "answer": ""}
        )
        print(f"Hypothesis: {result['hypothesis'][:120]}...")
        print(f"Retrieved : {len(result['documents'])} docs")
        print(f"Answer    : {result['answer'][:200]}")


if __name__ == "__main__":
    main()
