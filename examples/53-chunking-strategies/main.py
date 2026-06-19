from dotenv import load_dotenv

load_dotenv()

from src.tools import DEMO_QUERY
from src.workflow import create_workflow


def main():
    print("Building chunking strategies and indexing into Chroma...")
    app = create_workflow()

    print(f"\nQuery: {DEMO_QUERY}\n")
    result = app.invoke({"query": DEMO_QUERY, "results": {}})

    for strategy, answer in result["results"].items():
        print(f"[{strategy}]")
        print(f"  {answer}\n")


if __name__ == "__main__":
    main()
