from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTIONS  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main():
    app = create_workflow()

    for question in SAMPLE_QUESTIONS[:3]:
        print(f"\n{'=' * 60}")
        print(f"Q: {question}")
        result = app.invoke({
            "question": question,
            "answer": "",
            "critique": "",
            "iterations": 0,
            "confident": False,
        })
        print(f"Iterations: {result['iterations']}  |  Confident: {result['confident']}")
        print(f"\nAnswer:\n{result['answer']}")


if __name__ == "__main__":
    main()
