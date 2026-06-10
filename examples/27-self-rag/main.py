from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow

QUESTIONS = [
    "What is Self-RAG and how does it differ from standard RAG?",
    "What is 42 plus 17?",
    "How tall is the Eiffel Tower?",
]


def main():
    workflow = create_workflow()
    for q in QUESTIONS:
        print(f"\n{'─' * 60}")
        print(f"Q: {q}")
        result = workflow.invoke({"question": q})
        retrieved = result.get("should_retrieve", False)
        supported = result.get("supported", True)
        n_docs = len(result.get("documents") or [])
        print(f"Retrieved: {retrieved}  |  Docs kept: {n_docs}  |  Supported: {supported}")
        print(f"A: {result['generation']}")


if __name__ == "__main__":
    main()
