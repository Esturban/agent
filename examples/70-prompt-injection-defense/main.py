from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTION  # noqa: E402
from src.workflow import InjectionDefenseState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    print(f"Question : {SAMPLE_QUESTION}\n")
    result: InjectionDefenseState = app.invoke(
        {"question": SAMPLE_QUESTION, "raw_chunks": [], "classifications": [], "safe_chunks": [], "answer": ""}
    )
    blocked = [c for c in result["classifications"] if c["risk"] == "high"]
    print(f"Retrieved : {len(result['raw_chunks'])} chunks")
    print(f"Blocked   : {len(blocked)} injection attempts")
    for b in blocked:
        print(f"  > {b['chunk'][:80]}...")
    print(f"Safe      : {len(result['safe_chunks'])} chunks passed filter")
    print(f"\nAnswer    : {result['answer']}")


if __name__ == "__main__":
    main()
