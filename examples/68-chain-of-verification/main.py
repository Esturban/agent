from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTIONS  # noqa: E402
from src.workflow import CoVeState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    for question in SAMPLE_QUESTIONS:
        print(f"\n{'=' * 60}")
        print(f"Question : {question}")
        result: CoVeState = app.invoke(
            {"question": question, "initial_answer": "", "claims": [], "verifications": [], "revised_answer": ""}
        )
        print(f"\nInitial  : {result['initial_answer'][:300]}")
        print(f"\nClaims   : {len(result['claims'])}")
        failed = [v for v in result["verifications"] if not v["correct"]]
        print(f"Failures : {len(failed)}")
        for v in failed:
            print(f"  - WRONG: {v['claim']}")
            print(f"    FIX  : {v['correction']}")
        if failed:
            print(f"\nRevised  : {result['revised_answer'][:300]}")
        else:
            print("\nNo corrections needed.")


if __name__ == "__main__":
    main()
