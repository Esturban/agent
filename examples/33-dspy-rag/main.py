import dspy
from dotenv import load_dotenv

from src.tools import SAMPLE_QUESTIONS
from src.workflow import create_pipeline


def main():
    load_dotenv()
    dspy.configure(lm=dspy.LM("openai/gpt-4o-mini", temperature=0))

    print("Compiling RAG with BootstrapFewShot...")
    base_rag, compiled_rag = create_pipeline()

    for question in SAMPLE_QUESTIONS:
        print(f"\nQ: {question}\n{'─' * 60}")
        base_ans = base_rag(question=question)
        compiled_ans = compiled_rag(question=question)
        print(f"  [base]     {base_ans.answer}")
        print(f"  [compiled] {compiled_ans.answer}")


if __name__ == "__main__":
    main()
