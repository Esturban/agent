from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTIONS, SAMPLE_TARGET  # noqa: E402
from src.workflow import WebScraperState, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    print(f"Scraping: {SAMPLE_TARGET}\n")
    for question in SAMPLE_QUESTIONS:
        print(f"{'=' * 60}")
        print(f"Question : {question}")
        result: WebScraperState = app.invoke(
            {"url": SAMPLE_TARGET, "question": question, "raw_html": "", "text": "", "chunks": [], "context": [], "answer": ""}
        )
        print(f"Chunks   : {len(result['chunks'])}")
        print(f"Answer   : {result['answer'][:300]}\n")


if __name__ == "__main__":
    main()
