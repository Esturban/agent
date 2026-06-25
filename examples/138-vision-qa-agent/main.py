import os
from dotenv import load_dotenv
from openai import OpenAI
from src.workflow import create_workflow

load_dotenv()

DEMO_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/240px-PNG_transparency_demonstration_1.png"
QUESTIONS = [
    "What do you see in this image?",
    "What colors are most prominent?",
    "Describe the geometric shapes present.",
]

if __name__ == "__main__":
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    workflow = create_workflow()
    config = {"configurable": {"client": client, "model": "gpt-4o-mini"}}

    for question in QUESTIONS:
        result = workflow.invoke(
            {"image_source": DEMO_IMAGE, "question": question, "answer": ""},
            config=config,
        )
        print(f"Q: {question}")
        print(f"A: {result['answer']}\n")
