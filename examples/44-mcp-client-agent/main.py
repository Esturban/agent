from dotenv import load_dotenv

from src.tools import SAMPLE_QUERIES
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for query in SAMPLE_QUERIES:
        print(f"\nQUERY: {query}")
        result = app.invoke({
            "query": query, "available_tools": [], "tool_name": "",
            "tool_args": {}, "tool_result": "", "final_answer": "",
        })
        print(f"Tool: {result['tool_name']} → {result['tool_result']}")
        print(f"Answer: {result['final_answer'][:150]}")


if __name__ == "__main__":
    main()
