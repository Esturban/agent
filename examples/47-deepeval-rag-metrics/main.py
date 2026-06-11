from dotenv import load_dotenv
from src.tools import GOLDEN_DATASET
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()
    print("Running RAG pipeline on golden dataset...\n")
    for case in GOLDEN_DATASET:
        result = app.invoke({"query": case["input"], "context": [], "answer": ""})
        print(f"Q: {case['input']}")
        print(f"A: {result['answer'][:200]}")
        print(f"Context chunks: {len(result['context'])}\n")


if __name__ == "__main__":
    main()
