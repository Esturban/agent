---
teaching_ready: true
---
# 140 — Audio Agent

Transcribes an audio file with Whisper, classifies intent and extracts entities with a chat LLM, then routes the call to the right support queue. Shows speech-to-text → structured analysis → conditional routing.

**Run:** `python main.py path/to/call.mp3` — requires `OPENAI_API_KEY` in `.env`
