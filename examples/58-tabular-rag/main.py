from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTIONS  # noqa: E402
from src.workflow import TabularState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    for question in SAMPLE_QUESTIONS:
        print(f"\n{'=' * 60}")
        print(f"Question   : {question}")
        result: TabularState = app.invoke(
            {"question": question, "schema": "", "query_code": "", "result": "", "error": "", "iterations": 0}
        )
        status = "OK" if not result["error"] else f"FAILED after {result['iterations']} tries"
        print(f"Expression : {result['query_code']}")
        print(f"Result     : {result['result'] or result['error']}")
        print(f"Status     : {status}")


if __name__ == "__main__":
    main()
