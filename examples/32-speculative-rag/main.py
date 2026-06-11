from dotenv import load_dotenv
from src.tools import SAMPLE_QUERIES
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for query in SAMPLE_QUERIES:
        print(f"\nQUERY: {query}\n{'─' * 60}")
        result = app.invoke(
            {
                "query": query,
                "draft": "",
                "claims": [],
                "evidence": [],
                "support_labels": [],
                "revised": "",
            }
        )
        print(f"DRAFT:\n{result['draft']}")
        print(f"\nCLAIMS CHECKED: {len(result['claims'])}")
        for i, (claim, label) in enumerate(zip(result["claims"], result["support_labels"]), 1):
            print(f"  {i}. [{label}] {claim}")
        if result["revised"]:
            print(f"\nREVISED ANSWER:\n{result['revised']}")
        else:
            print("\nNo revision needed — all claims supported.")


if __name__ == "__main__":
    main()
