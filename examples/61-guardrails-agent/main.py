from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_INPUTS  # noqa: E402
from src.workflow import GuardrailsState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    for query, expected_pass in SAMPLE_INPUTS:
        print(f"\n{'=' * 60}")
        print(f"Query    : {query}")
        result: GuardrailsState = app.invoke(
            {"query": query, "input_decision": {}, "answer": "", "output_decision": {}, "blocked": False, "block_reason": ""}
        )
        status = "BLOCKED" if result["blocked"] else "PASSED"
        expected = "PASS" if expected_pass else "BLOCK"
        print(f"Status   : {status}  (expected: {expected})")
        print(f"Answer   : {result['answer'][:200]}")
        if not result["blocked"] and result["output_decision"]:
            od = result["output_decision"]
            print(f"Output   : passes={od.get('passes')} words={od.get('word_count')} reason={od.get('reason','')[:80]}")


if __name__ == "__main__":
    main()
