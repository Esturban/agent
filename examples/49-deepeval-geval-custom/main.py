from dotenv import load_dotenv
from src.tools import TEST_CASES
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()
    print("Generating responses for G-Eval demo...\n")
    for case in TEST_CASES[:2]:
        result = app.invoke({"input": case["input"], "output": "", "score": 0.0})
        print(f"Q: {case['input']}")
        print(f"A: {result['output'][:200]}\n")


if __name__ == "__main__":
    main()
