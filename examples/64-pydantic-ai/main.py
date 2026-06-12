from dotenv import load_dotenv

load_dotenv()

from src.tools import RESEARCH_QUERIES, ResearchResult  # noqa: E402
from src.workflow import run_agent  # noqa: E402


def main() -> None:
    for query in RESEARCH_QUERIES:
        print(f"\n{'=' * 60}")
        print(f"Query      : {query}")
        result: ResearchResult = run_agent(query)
        print(f"Summary    : {result.summary}")
        print(f"Confidence : {result.confidence:.2f}")
        print("Key facts  :")
        for fact in result.key_facts:
            print(f"  - {fact}")


if __name__ == "__main__":
    main()
