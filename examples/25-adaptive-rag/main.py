from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTIONS
from src.workflow import create_workflow


def main():
    app = create_workflow()

    for question in SAMPLE_QUESTIONS:
        print(f"\nQ: {question}")
        result = app.invoke({"question": question, "strategy": "", "context": "", "answer": ""})
        print(f"Strategy: {result['strategy']}")
        print(f"A: {result['answer']}")


if __name__ == "__main__":
    main()
