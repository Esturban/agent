from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUERIES  # noqa: E402
from src.workflow import RerankState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    for query in SAMPLE_QUERIES:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        result: RerankState = app.invoke(
            {"query": query, "documents": [], "reranked": [], "answer": ""}
        )
        print(f"Retrieved : {len(result['documents'])} docs")
        print(f"Reranked  : {len(result['reranked'])} docs")
        print(f"Top doc   : {result['reranked'][0][:80]}..." if result["reranked"] else "")
        print(f"Answer    : {result['answer'][:200]}")


if __name__ == "__main__":
    main()
