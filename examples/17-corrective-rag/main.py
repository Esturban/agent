from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow  # noqa: E402


def main():
    app = create_workflow()

    questions = [
        "What is Corrective RAG and how does it improve retrieval?",
        "How does LangGraph StateGraph handle conditional branching?",
        "Who won the 2024 US presidential election?",  # not in corpus → triggers web search
    ]

    for question in questions:
        print(f"\n{'=' * 60}")
        print(f"Q: {question}")
        result = app.invoke({
            "question": question,
            "documents": [],
            "generation": "",
            "web_search": False,
        })
        used_web = result["web_search"]
        doc_count = len(result["documents"])
        print(f"Web search triggered: {used_web}  |  Docs used: {doc_count}")
        print(f"A: {result['generation']}")


if __name__ == "__main__":
    main()
