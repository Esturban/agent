"""Voice pipeline constants and I/O helpers.

Uses OpenAI's cloud APIs — no local model download required:
  - Whisper API (whisper-1): speech-to-text
  - TTS API (tts-1): text-to-speech
Both are covered by OPENAI_API_KEY; no extra keys needed.
"""

from openai import OpenAI

MODEL_LLM = "gpt-5.4-nano"
MODEL_STT = "whisper-1"   # OpenAI Whisper cloud endpoint
MODEL_TTS = "tts-1"       # OpenAI TTS endpoint
TTS_VOICE = "nova"

# Synthetic "user question" — converted to audio first so the demo is self-contained.
DEMO_QUESTION = "What are the three most important things to know about building LangGraph agents?"


def text_to_speech(text: str, out_path: str) -> str:
    """Call OpenAI TTS and write the mp3 to out_path; return the path."""
    client = OpenAI()
    resp = client.audio.speech.create(model=MODEL_TTS, voice=TTS_VOICE, input=text)
    resp.stream_to_file(out_path)
    return out_path


def speech_to_text(audio_path: str) -> str:
    """Transcribe an audio file via OpenAI Whisper; return the transcript string."""
    client = OpenAI()
    with open(audio_path, "rb") as f:
        resp = client.audio.transcriptions.create(model=MODEL_STT, file=f)
    return resp.text
