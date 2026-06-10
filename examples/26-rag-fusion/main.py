from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTIONS
from src.workflow import create_workflow


def main():
    app = create_workflow()

    for question in SAMPLE_QUESTIONS:
        print(f"\nQ: {question}")
        result = app.invoke(
            {
                "question": question,
                "variants": [],
                "ranked_docs": [],
                "fused_docs": [],
                "answer": "",
            }
        )
        print(f"Variants generated: {len(result['variants'])}")
        print(f"Docs after fusion: {len(result['fused_docs'])}")
        print(f"A: {result['answer']}")


if __name__ == "__main__":
    main()
