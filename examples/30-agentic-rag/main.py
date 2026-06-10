from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
from src.workflow import create_workflow

QUESTIONS = [
    "What is Self-RAG and how does it differ from Corrective RAG?",  # vectorstore
    "What is 144 divided by 12, then multiplied by 7?",  # calculator
    "Who won the most recent FIFA World Cup?",  # web
]


def main():
    agent = create_workflow()
    for q in QUESTIONS:
        print(f"\n{'─' * 60}")
        print(f"Q: {q}")
        result = agent.invoke({"messages": [HumanMessage(content=q)]})
        print(f"A: {result['messages'][-1].content}")


if __name__ == "__main__":
    main()
