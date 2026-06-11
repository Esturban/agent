from dotenv import load_dotenv
from src.tools import HAND_WRITTEN_GOLDENS
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow(k=3)
    print("Running RAG pipeline (k=3)...\n")
    for golden in HAND_WRITTEN_GOLDENS:
        result = app.invoke({"query": golden["input"], "context": [], "answer": ""})
        print(f"Q: {golden['input']}")
        print(f"A: {result['answer'][:200]}\n")


if __name__ == "__main__":
    main()
