import os
import tempfile
from dotenv import load_dotenv

from src.tools import DEMO_QUESTION, text_to_speech
from src.workflow import create_workflow

load_dotenv()

if not os.environ.get("OPENAI_API_KEY", "").startswith("sk-"):
    raise RuntimeError("OPENAI_API_KEY is required for the voice pipeline.")


def main() -> None:
    # Generate synthetic input audio so the demo is fully self-contained.
    print("Step 0: generating synthetic user question audio...")
    audio_in = tempfile.mktemp(suffix=".mp3")
    text_to_speech(DEMO_QUESTION, audio_in)
    size_kb = os.path.getsize(audio_in) // 1024
    print(f"  Input audio: {audio_in} ({size_kb} KB)")
    print(f"  Question text: {DEMO_QUESTION}")

    print("\nRunning voice pipeline (STT → LLM → TTS)...")
    print("=" * 60)

    app = create_workflow()
    result = app.invoke({
        "audio_in": audio_in,
        "transcript": "",
        "response": "",
        "audio_out": "",
    })

    out_kb = os.path.getsize(result["audio_out"]) // 1024
    print(f"\nTranscript : {result['transcript']}")
    print(f"\nResponse   : {result['response'][:300]}")
    print(f"\nOutput audio: {result['audio_out']} ({out_kb} KB)")
    print("\nPlay both mp3 files to hear the full round-trip.")


if __name__ == "__main__":
    main()
