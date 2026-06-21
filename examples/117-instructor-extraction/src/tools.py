"""
Pydantic models and extraction functions for example 117 — Instructor.

Demonstrates type-safe structured extraction with automatic retry
on validation failure using the instructor library.
"""

from typing import Literal
from pydantic import BaseModel, Field, field_validator
import instructor
from openai import OpenAI


# ── Pydantic models ────────────────────────────────────────────────────────


class MeetingNotes(BaseModel):
    """Structured output for a meeting transcript."""

    attendees: list[str] = Field(description="Names of all meeting attendees")
    decisions: list[str] = Field(description="Decisions made during the meeting")
    action_items: list[str] = Field(
        description="Action items with owner and deadline where mentioned"
    )
    next_meeting: str | None = Field(
        default=None, description="Date/time of next meeting if mentioned"
    )


class ProductReview(BaseModel):
    """Structured output for a product review."""

    sentiment: Literal["positive", "negative", "mixed", "neutral"] = Field(
        description="Overall sentiment of the review"
    )
    key_features: list[str] = Field(
        description="Product features mentioned in the review (positive or negative)"
    )
    score: float = Field(
        description="Numeric score from 1.0 to 5.0 inferred from the review tone",
        ge=1.0,
        le=5.0,
    )
    would_recommend: bool = Field(
        description="Whether the reviewer would recommend this product"
    )


class UserAddress(BaseModel):
    """Structured output for an address extracted from free text."""

    street: str = Field(description="Street number and name")
    city: str = Field(description="City name")
    state: str = Field(description="Two-letter US state code (e.g. CA, NY)")
    zip_code: str = Field(description="5-digit ZIP code")

    @field_validator("state")
    @classmethod
    def normalize_state(cls, v: str) -> str:
        return v.upper().strip()

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, v: str) -> str:
        digits = v.strip().replace("-", "")[:5]
        if not digits.isdigit() or len(digits) != 5:
            raise ValueError(f"ZIP code must be 5 digits, got: {v!r}")
        return digits


# ── Sample texts for demos ─────────────────────────────────────────────────

MEETING_TRANSCRIPT = """
Q3 Planning Meeting — September 15, 2024
Attendees: Sarah Chen (PM), Marcus Webb (Engineering Lead), Priya Nair (Design), Tom Okafor (QA)

Sarah opened the meeting at 10:00 AM.

After reviewing the Q2 metrics, the team decided to push the mobile launch to October 28th
instead of October 15th to allow additional testing time. Marcus agreed to have the API
endpoints finalized by September 30th. Priya will deliver final design assets by September 25th.
Tom is responsible for setting up the automated test suite by October 10th.

The team also decided to drop the offline mode feature from the initial release and revisit it
in Q4. Sarah will communicate this decision to stakeholders by end of day Friday.

Next meeting is scheduled for September 22nd at 10 AM.
"""

PRODUCT_REVIEW = """
I've been using this wireless keyboard for three months now and I have mixed feelings.
The build quality is excellent — it feels solid and the keys have a satisfying tactile click.
Battery life is impressive: I charged it once and it's been going for 6 weeks.
However, the Bluetooth connection drops at least twice a day, which is incredibly frustrating
during video calls. The software customization app only works on Windows, which means Mac
users are stuck with default settings. For the price ($120), I expected better reliability.
I might keep it because of the battery life and feel, but I wouldn't recommend it to colleagues
unless they're okay with the connection issues.
"""

ADDRESS_TEXT = """
Please ship my order to John Martinez at twelve forty-five West Oak Boulevard,
apartment three B, in San Francisco, California, nine four one zero two.
The buzzer code is 4521 but you can just leave it at the front desk.
"""


# ── Extraction functions ───────────────────────────────────────────────────


def make_client() -> instructor.Instructor:
    """Create an instructor-patched OpenAI client."""
    return instructor.from_openai(OpenAI())


def extract_meeting_notes(client: instructor.Instructor, text: str) -> MeetingNotes:
    """Extract structured meeting notes from a transcript."""
    return client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=MeetingNotes,
        max_retries=3,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert meeting notes extractor. "
                    "Extract structured information from meeting transcripts accurately."
                ),
            },
            {
                "role": "user",
                "content": f"Extract structured notes from this meeting transcript:\n\n{text}",
            },
        ],
    )


def extract_product_review(client: instructor.Instructor, text: str) -> ProductReview:
    """Extract structured review data from a product review text."""
    return client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=ProductReview,
        max_retries=3,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at analyzing product reviews. "
                    "Extract sentiment, key features, and scoring from reviews."
                ),
            },
            {
                "role": "user",
                "content": f"Analyze this product review:\n\n{text}",
            },
        ],
    )


def extract_address(client: instructor.Instructor, text: str) -> UserAddress:
    """Extract a structured US address from free-form text."""
    return client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=UserAddress,
        max_retries=3,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at parsing US mailing addresses from unstructured text. "
                    "Always return a valid 5-digit ZIP code and 2-letter state code."
                ),
            },
            {
                "role": "user",
                "content": f"Extract the mailing address from this text:\n\n{text}",
            },
        ],
    )
