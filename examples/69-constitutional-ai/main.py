from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_PROMPTS  # noqa: E402
from src.workflow import CAIState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    for prompt in SAMPLE_PROMPTS:
        print(f"\n{'=' * 60}")
        print(f"Prompt      : {prompt}")
        result: CAIState = app.invoke(
            {"prompt": prompt, "response": "", "critiques": [], "revision_count": 0, "violations": []}
        )
        violations = [c for c in result["critiques"] if c["violated"]]
        print(f"Revisions   : {result['revision_count']}")
        print(f"Violations  : {len(violations)} remaining")
        print(f"Final answer: {result['response'][:300]}")


if __name__ == "__main__":
    main()
