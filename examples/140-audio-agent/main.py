import json
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from src.workflow import create_workflow

load_dotenv()

if __name__ == "__main__":
    audio_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not audio_path:
        print("Usage: python main.py path/to/audio.mp3")
        print("\nDemo mode: provide an audio file path as the first argument.")
        print("The agent will transcribe it, classify the intent, and route it.")
        sys.exit(0)

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    workflow = create_workflow()
    config = {"configurable": {"client": client, "model": "gpt-4o-mini"}}

    result = workflow.invoke(
        {"audio_path": audio_path, "transcript": "", "analysis": {}, "queue": ""},
        config=config,
    )
    print(f"Transcript: {result['transcript']}\n")
    print(f"Analysis:\n{json.dumps(result['analysis'], indent=2)}\n")
    print(f"Routed to: {result['queue']}")
