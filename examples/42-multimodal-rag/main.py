from dotenv import load_dotenv

from src.tools import QUERIES
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for query in QUERIES:
        print(f"\nQUERY: {query}")
        result = app.invoke({"descriptions": [], "query": query, "answer": ""})
        print(f"ANSWER: {result['answer'][:200]}")


if __name__ == "__main__":
    main()
