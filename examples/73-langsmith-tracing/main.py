import os

from dotenv import load_dotenv

load_dotenv()

# LangSmith tracing is enabled when these env vars are set:
#   LANGCHAIN_API_KEY=<your-key>
#   LANGCHAIN_TRACING_V2=true
#   LANGCHAIN_PROJECT=73-langsmith-tracing  (optional, groups runs)

from src.tools import SAMPLE_QUESTIONS  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    tracing = os.getenv("LANGCHAIN_TRACING_V2", "false").lower()
    print(f"LangSmith tracing: {tracing}\n")

    graph = create_workflow()

    for question in SAMPLE_QUESTIONS:
        result = graph.invoke({"question": question, "answer": ""})
        print(f"Q: {result['question']}")
        print(f"A: {result['answer']}\n")

    print("Runs visible at https://smith.langchain.com if LANGCHAIN_TRACING_V2=true")


if __name__ == "__main__":
    main()
