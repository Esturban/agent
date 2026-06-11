from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_DOCS
from src.workflow import create_workflow


def main():
    workflow = create_workflow()
    n = len(SAMPLE_DOCS)
    print(f"Fan-out: {n} documents summarized in parallel\n")

    result = workflow.invoke({"documents": SAMPLE_DOCS, "summaries": []})

    print("Individual summaries (one per parallel worker):")
    for i, s in enumerate(result["summaries"], 1):
        print(f"  {i}. {s}")

    print(f"\nAggregated synthesis:\n{result['final_summary']}")


if __name__ == "__main__":
    main()
