from guardrails import Guard
from .tools import StructuredResponse

SYSTEM_PROMPT = """You are a concise AI assistant. Respond ONLY in valid JSON matching this schema:
{
  "summary": "<brief summary, max 200 chars>",
  "points": ["<point 1>", "<point 2>", "<point 3>"],
  "safe": true
}
Provide exactly 3 points. No URLs. No prose outside the JSON."""
REASK_LIMITS: dict[int, int] = {}


def create_guard(max_reasks: int = 2) -> Guard:
    guard = Guard.for_pydantic(
        output_class=StructuredResponse,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}],
    )
    guard.configure(num_reasks=max_reasks, allow_metrics_collection=False)
    REASK_LIMITS[id(guard)] = max_reasks
    return guard


def _reask_count(guard: Guard) -> int:
    last_call = guard.history.last if guard.history else None
    return max(len(getattr(last_call, "iterations", [])) - 1, 0) if last_call else 0


def _reask_limit(guard: Guard) -> int:
    return REASK_LIMITS.get(id(guard), getattr(guard, "_num_reasks", 2) or 0)


def validate_response(guard: Guard, prompt: str) -> dict:
    try:
        result = guard(
            model="gpt-5.4-nano",
            messages=[{"role": "user", "content": prompt}],
            num_reasks=_reask_limit(guard),
        )
        return {
            "validated": result.validated_output,
            "reasks": _reask_count(guard),
            "passed": result.validation_passed,
            "error": None if result.validation_passed else "validation failed",
        }
    except Exception as e:
        return {
            "validated": None,
            "reasks": _reask_count(guard),
            "passed": False,
            "error": str(e),
        }
