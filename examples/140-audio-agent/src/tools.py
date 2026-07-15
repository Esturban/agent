import json


INTENTS = {"billing", "technical", "general", "complaint", "cancellation"}
URGENCY_LEVELS = {"low", "medium", "high"}
SENTIMENTS = {"positive", "neutral", "negative"}


def transcribe(audio_path: str, client) -> str:
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(model="whisper-1", file=f)
    return result.text


def classify_and_extract(transcript: str, client, model: str = "gpt-5.4-nano") -> dict:
    if not transcript.strip():
        return {
            "intent": "general",
            "urgency": "low",
            "product_mentioned": None,
            "action_required": "No speech detected",
            "sentiment": "neutral",
        }

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
        response_format={"type": "json_object"},
        max_completion_tokens=256,
    )
    text = resp.choices[0].message.content or ""
    try:
        analysis = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError("The classifier returned invalid JSON") from None

    if analysis.get("intent") not in INTENTS:
        raise ValueError(f"The classifier returned an unsupported intent: {analysis.get('intent')!r}")
    if analysis.get("urgency") not in URGENCY_LEVELS:
        raise ValueError(f"The classifier returned an unsupported urgency: {analysis.get('urgency')!r}")
    if analysis.get("sentiment") not in SENTIMENTS:
        raise ValueError(f"The classifier returned an unsupported sentiment: {analysis.get('sentiment')!r}")
    if not isinstance(analysis.get("action_required"), str):
        raise ValueError("The classifier response is missing a text action_required field")
    return analysis


ROUTING_MAP = {
    "billing": "billing-queue",
    "technical": "tier1-support",
    "complaint": "customer-success",
    "cancellation": "retention-team",
    "general": "general-support",
}


def route(intent: str) -> str:
    return ROUTING_MAP.get(intent, "general-support")
