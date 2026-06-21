"""
121 — Structured Generation with Outlines
Tools: Pydantic schemas, outlines constrained generation, instructor retry comparison.
"""

import re
from typing import Literal

from pydantic import BaseModel

# ── Pydantic models ──────────────────────────────────────────────────────────

class ExtractedPerson(BaseModel):
    name: str
    age: int
    occupation: str


class ParsedDate(BaseModel):
    year: int
    month: int
    day: int


# ── Outlines constrained generation ─────────────────────────────────────────

def generate_constrained_json(model_name: str, schema_model: type, prompt: str) -> dict:
    """
    Generate JSON constrained to a Pydantic schema using outlines.
    Falls back to a mock response if outlines/transformers not installed.
    """
    try:
        import outlines
        model = outlines.models.transformers(model_name)
        generator = outlines.generate.json(model, schema_model)
        result = generator(prompt)
        return result.model_dump()
    except (ImportError, Exception) as e:
        # Graceful fallback: show what the output WOULD look like
        print(f"  [outlines not available: {type(e).__name__}] Returning mock output.")
        if schema_model is ExtractedPerson:
            return ExtractedPerson(name="Alice Chen", age=32, occupation="data scientist").model_dump()
        elif schema_model is ParsedDate:
            return ParsedDate(year=2024, month=3, day=15).model_dump()
        return {}


def generate_constrained_regex(model_name: str, pattern: str, prompt: str) -> str:
    """
    Generate a string matching a regex pattern using outlines.
    Falls back to a mock response if not installed.
    """
    try:
        import outlines
        model = outlines.models.transformers(model_name)
        generator = outlines.generate.regex(model, pattern)
        return generator(prompt)
    except (ImportError, Exception) as e:
        print(f"  [outlines not available: {type(e).__name__}] Returning mock output.")
        # Return a valid phone number as mock
        mock = "555-867-5309"
        if re.match(pattern, mock):
            return mock
        return "000-000-0000"


def generate_constrained_choice(model_name: str, choices: list[str], prompt: str) -> str:
    """
    Generate one of the given choices using outlines.
    Falls back to a mock response if not installed.
    """
    try:
        import outlines
        model = outlines.models.transformers(model_name)
        generator = outlines.generate.choice(model, choices)
        return generator(prompt)
    except (ImportError, Exception) as e:
        print(f"  [outlines not available: {type(e).__name__}] Returning mock output.")
        return choices[0]  # deterministic fallback


# ── Instructor (retry-based) comparison ──────────────────────────────────────

def extract_with_instructor(prompt: str, schema_model: type) -> dict:
    """
    Extract structured data using instructor (OpenAI tool-calling + Pydantic retry).
    This is the alternative approach: retries until schema is satisfied.
    """
    try:
        import instructor
        from openai import OpenAI
        client = instructor.from_openai(OpenAI())
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            response_model=schema_model,
            messages=[{"role": "user", "content": prompt}],
            max_retries=3,
        )
        return result.model_dump()
    except ImportError:
        # Fall back to direct OpenAI with JSON mode
        from openai import OpenAI
        import json
        client = OpenAI()
        schema_str = schema_model.model_json_schema()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": f"Extract data as JSON matching this schema: {json.dumps(schema_str)}"},
                {"role": "user", "content": prompt},
            ],
        )
        return json.loads(resp.choices[0].message.content)
