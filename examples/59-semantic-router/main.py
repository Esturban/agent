from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUERIES  # noqa: E402
from src.workflow import SemanticRouterState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    for query in SAMPLE_QUERIES:
        print(f"\n{'=' * 60}")
        print(f"Query   : {query}")
        result: SemanticRouterState = app.invoke({"query": query, "route": "", "scores": {}, "answer": ""})
        scores_str = "  ".join(f"{r}={s:.3f}" for r, s in sorted(result["scores"].items()))
        print(f"Route   : {result['route']}  ({scores_str})")
        print(f"Answer  : {result['answer'][:200]}")


if __name__ == "__main__":
    main()
