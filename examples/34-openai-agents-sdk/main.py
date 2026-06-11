from agents import Runner
from dotenv import load_dotenv
from src.tools import SAMPLE_QUESTIONS
from src.workflow import create_triage_agent


def main():
    load_dotenv()
    triage = create_triage_agent()

    for question in SAMPLE_QUESTIONS:
        print(f"\nQ: {question}\n{'─' * 60}")
        result = Runner.run_sync(triage, question)
        print(f"A: {result.final_output}")


if __name__ == "__main__":
    main()
