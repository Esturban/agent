from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUERIES  # noqa: E402
from src.workflow import CompressionState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    for query in SAMPLE_QUERIES:
        print(f"\n{'=' * 60}")
        print(f"Query     : {query}")
        result: CompressionState = app.invoke(
            {"query": query, "raw_docs": [], "compressed": [], "answer": ""}
        )
        saved = len(result["raw_docs"]) - len(result["compressed"])
        print(f"Raw docs  : {len(result['raw_docs'])}")
        print(f"Compressed: {len(result['compressed'])} (filtered {saved} irrelevant)")
        print(f"Answer    : {result['answer'][:200]}")


if __name__ == "__main__":
    main()
