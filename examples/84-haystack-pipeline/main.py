from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTIONS  # noqa: E402
from src.workflow import create_pipeline, run_query  # noqa: E402

# Framework contrast quick reference:
#
#   LangGraph  → shared mutable TypedDict state flows through nodes.
#   Haystack   → stateless DAG: each component passes data via named output ports.
#
# Haystack's stateless model makes pipelines easy to test in isolation —
# you can call pipeline.run() for one component at a time.


def main() -> None:
    print("=== 84 · Haystack Pipeline ===\n")

    pipeline, store = create_pipeline()
    print(f"Document store loaded with {store.count_documents()} documents.\n")

    for question in SAMPLE_QUESTIONS:
        print(f"Q: {question}")
        answer = run_query(pipeline, question)
        print(f"A: {answer}\n")


if __name__ == "__main__":
    main()
