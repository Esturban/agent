"""
121 — Structured Generation with Outlines
Workflow: demo JSON, regex, and choice constrained generation vs instructor retry.
"""

import re

from .tools import (
    ExtractedPerson,
    ParsedDate,
    extract_with_instructor,
    generate_constrained_choice,
    generate_constrained_json,
    generate_constrained_regex,
)

# Use a small model that's fast to load if outlines is available
LOCAL_MODEL = "microsoft/phi-2"
PHONE_REGEX = r"\d{3}-\d{3}-\d{4}"
SENTIMENT_CHOICES = ["positive", "negative", "neutral"]


def create_workflow() -> dict:
    """Demo all 3 constraint types with outlines, then compare to instructor."""
    print("=== 121 — Structured Generation with Outlines ===\n")

    # 1. JSON constrained to Pydantic schema
    print("Constraint 1: JSON → ExtractedPerson")
    person_prompt = "Extract: 'Dr. James Kim, 45, is a senior machine learning engineer at Acme AI.'"
    outlines_person = generate_constrained_json(LOCAL_MODEL, ExtractedPerson, person_prompt)
    print(f"  outlines:   {outlines_person}")

    print("\nConstraint 1 (comparison): instructor retry approach")
    instructor_person = extract_with_instructor(person_prompt, ExtractedPerson)
    print(f"  instructor: {instructor_person}")

    # 2. Regex constrained (phone number)
    print("\nConstraint 2: regex → phone number format")
    phone_prompt = "What is a typical US phone number format? Give me one example."
    outlines_phone = generate_constrained_regex(LOCAL_MODEL, PHONE_REGEX, phone_prompt)
    print(f"  outlines:   {outlines_phone}")
    print(f"  matches regex {PHONE_REGEX!r}: {re.match(PHONE_REGEX, outlines_phone) is not None}")

    # 3. Choice constrained (sentiment)
    print("\nConstraint 3: choice → sentiment classification")
    sentiment_prompt = "The product was amazing and exceeded all my expectations! Sentiment:"
    outlines_sentiment = generate_constrained_choice(LOCAL_MODEL, SENTIMENT_CHOICES, sentiment_prompt)
    print(f"  outlines:   {outlines_sentiment!r} (guaranteed in {SENTIMENT_CHOICES})")

    # For instructor comparison, call OpenAI directly with choice constraint
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Classify sentiment as exactly one word — positive, negative, or neutral: '{sentiment_prompt}'"}],
    )
    instructor_sentiment = resp.choices[0].message.content.strip().lower()
    print(f"  instructor: {instructor_sentiment!r} (may need cleanup: {instructor_sentiment not in SENTIMENT_CHOICES})")

    # 4. Key comparison
    print("\n--- Approach Comparison ---")
    print("outlines:   CFG sampling — guarantees valid output in ONE pass, no API calls needed")
    print("instructor: tool-calling + retry — may take 2-3 API calls, needs OpenAI API key")
    print("Use outlines for: local models, guaranteed format, no retries")
    print("Use instructor for: hosted models, complex schemas, existing OpenAI setup")

    return {
        "outlines_person": outlines_person,
        "instructor_person": instructor_person,
        "phone": outlines_phone,
        "sentiment_outlines": outlines_sentiment,
        "sentiment_instructor": instructor_sentiment,
    }
