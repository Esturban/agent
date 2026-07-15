import os
from dotenv import load_dotenv
from openai import OpenAI
from src.workflow import create_workflow

load_dotenv()

DEMO_IMAGE = "https://raw.githubusercontent.com/github/explore/main/topics/python/python.png"
QUESTIONS = [
    "What do you see in this image?",
    "What colors are most prominent?",
    "Describe the geometric shapes present.",
]

if __name__ == "__main__":
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required; add it to .env before running this example.")
    client = OpenAI(api_key=api_key)
    workflow = create_workflow()
    config = {"configurable": {"client": client, "model": "gpt-5.4-nano"}}

    for question in QUESTIONS:
        result = workflow.invoke(
            {"image_source": DEMO_IMAGE, "question": question, "answer": ""},
            config=config,
        )
        print(f"Q: {question}")
        print(f"A: {result['answer']}\n")
