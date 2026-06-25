---
teaching_ready: true
---
# 102 · Voice Pipeline

End-to-end voice agent: OpenAI TTS synthesises a user question → Whisper transcribes it back → a LangGraph agent answers → TTS speaks the response. No local model downloads — everything runs through `OPENAI_API_KEY`.

## Run

```bash
cp .env.example .env   # add OPENAI_API_KEY
python examples/102-voice-pipeline/main.py
```

The script writes two mp3 files to `/tmp/` — play them to hear the full round-trip.

## Key concepts

- `whisper-1` cloud API: `client.audio.transcriptions.create(model="whisper-1", file=...)`
- `tts-1` cloud API: `client.audio.speech.create(model="tts-1", voice="nova", input=...)`
- Three-node LangGraph: `transcribe → respond → speak` makes latency explicit — each stage is a named, measurable node
- TTFA optimisation (time-to-first-audio): in production, begin TTS as soon as the first sentence arrives rather than waiting for the full LLM response
