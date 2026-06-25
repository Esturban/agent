import json
from pathlib import Path


def transcribe(audio_path: str, client) -> str:
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(model="whisper-1", file=f)
    return result.text


def classify_and_extract(transcript: str, client, model: str = "gpt-4o-mini") -> dict:
    prompt = f"""Analyze this support call transcript and respond with JSON only:
{{
  "intent": "billing|technical|general|complaint|cancellation",
  "urgency": "low|medium|high",
  "product_mentioned": "string or null",
  "action_required": "string describing next step",
  "sentiment": "positive|neutral|negative"
}}

Transcript: {transcript}"""
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
    )
    text = resp.choices[0].message.content.strip().strip("```json").strip("```")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


ROUTING_MAP = {
    "billing": "billing-queue",
    "technical": "tier1-support",
    "complaint": "customer-success",
    "cancellation": "retention-team",
    "general": "general-support",
}


def route(intent: str) -> str:
    return ROUTING_MAP.get(intent, "general-support")
