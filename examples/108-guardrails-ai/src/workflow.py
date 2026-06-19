from guardrails import Guard
from .tools import StructuredResponse

SYSTEM_PROMPT = """You are a concise AI assistant. Respond ONLY in valid JSON matching this schema:
{
  "summary": "<brief summary, max 200 chars>",
  "points": ["<point 1>", "<point 2>", "<point 3>"],
  "safe": true
}
Provide exactly 3 points. No URLs. No prose outside the JSON."""


def create_guard(max_reasks: int = 2) -> Guard:
    return Guard.for_pydantic(
        output_class=StructuredResponse,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}],
        num_reasks=max_reasks,
    )


def validate_response(guard: Guard, prompt: str) -> dict:
    try:
        result = guard(
            model="gpt-4o-mini",
            msg_history=[{"role": "user", "content": prompt}],
        )
        return {
            "validated": result.validated_output,
            "reasks": result.reasks,
            "passed": True,
            "error": None,
        }
    except Exception as e:
        return {
            "validated": None,
            "reasks": getattr(guard.history.last, "reasks", []) if guard.history else [],
            "passed": False,
            "error": str(e),
        }
