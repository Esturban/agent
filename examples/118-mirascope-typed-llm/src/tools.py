"""
Pydantic models and typed call functions for example 118 — Mirascope.

Demonstrates Pydantic-first LLM calls with provider switching
by decorating the same function with @openai.call vs @anthropic.call.
"""

from pydantic import BaseModel, Field
from mirascope.core import openai, anthropic, prompt_template


# ── Output model ───────────────────────────────────────────────────────────


class MeetingSummary(BaseModel):
    """Structured summary of a business meeting."""

    topic: str = Field(description="The main topic or purpose of the meeting")
    key_points: list[str] = Field(
        description="The most important points discussed, as concise bullet items"
    )
    next_steps: list[str] = Field(
        description="Concrete next steps or action items agreed upon"
    )
    mood: str = Field(
        description="Overall tone of the meeting: productive, tense, inconclusive, etc."
    )


# ── Sample meeting transcript ──────────────────────────────────────────────

SAMPLE_TRANSCRIPT = """
Product roadmap sync — June 18, 2024

Attendees: Alex (CPO), Jamie (Engineering), Sam (Design), Riley (Marketing)

Alex opened by noting that the Q2 launch hit 94% of target metrics — strong result.
The team discussed the H2 roadmap. Jamie flagged that the real-time collaboration feature
will require a backend rewrite and estimated 8 weeks of engineering time.
Sam presented three UI directions for the new dashboard; the team voted unanimously for
option B (the minimal dark-mode design). Riley raised concerns about the October launch
window conflicting with a competitor's announcement and suggested moving to September 15th.
Alex agreed to the earlier date and asked Jamie to reassess the timeline.
Action items: Jamie to provide revised estimate by Friday; Sam to finalize design specs
by June 25th; Riley to draft the press release outline by June 30th.
The mood was collaborative and the team ended on a positive note.
"""


# ── OpenAI typed call ──────────────────────────────────────────────────────


@openai.call(model="gpt-4o-mini", response_model=MeetingSummary)
@prompt_template(
    """
    You are an expert meeting analyst.
    Summarize the following meeting transcript into structured output.

    Transcript:
    {transcript}
    """
)
def summarize_with_openai(transcript: str) -> openai.OpenAIDynamicConfig:
    return {"computed_fields": {"transcript": transcript}}


# ── Anthropic typed call (same task, provider switch) ─────────────────────


@anthropic.call(model="claude-haiku-4-5", response_model=MeetingSummary)
@prompt_template(
    """
    You are an expert meeting analyst.
    Summarize the following meeting transcript into structured output.

    Transcript:
    {transcript}
    """
)
def summarize_with_anthropic(transcript: str) -> anthropic.AnthropicDynamicConfig:
    return {"computed_fields": {"transcript": transcript}}
