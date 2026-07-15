import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from src.workflow import create_workflow

def main(audio_path: str) -> None:
    load_dotenv()
    path = Path(audio_path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"Audio file not found: {path}")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required to transcribe and classify audio.")

    client = OpenAI(api_key=api_key)
    workflow = create_workflow()
    config = {"configurable": {"client": client, "model": "gpt-5.4-nano"}}

    result = workflow.invoke(
        {"audio_path": str(path), "transcript": "", "analysis": {}, "queue": ""},
        config=config,
    )
    print(f"Transcript: {result['transcript']}\n")
    print(f"Analysis:\n{json.dumps(result['analysis'], indent=2)}\n")
    print(f"Routed to: {result['queue']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python main.py path/to/audio.wav")
    main(sys.argv[1])
