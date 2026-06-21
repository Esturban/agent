"""
Workflow for example 118 — Mirascope typed LLM calls.

Runs the same meeting summary task with both OpenAI and Anthropic,
then compares results side-by-side to demonstrate provider portability.
"""

from src.tools import (
    MeetingSummary,
    SAMPLE_TRANSCRIPT,
    summarize_with_openai,
    summarize_with_anthropic,
)


def create_workflow() -> dict:
    """
    Run MeetingSummary extraction with OpenAI then Anthropic.

    The only difference between the two calls is the decorator:
      @openai.call(model="gpt-4o-mini", response_model=MeetingSummary)
      @anthropic.call(model="claude-haiku-4-5", response_model=MeetingSummary)

    Everything else — the prompt template, the Pydantic model, the function
    signature — is identical.

    Returns:
        dict with "openai" and "anthropic" keys, each a MeetingSummary.
    """
    print("  [1/2] Running with OpenAI (gpt-4o-mini)...")
    openai_result: MeetingSummary = summarize_with_openai(SAMPLE_TRANSCRIPT)

    print("  [2/2] Running with Anthropic (claude-haiku-4-5)...")
    anthropic_result: MeetingSummary = summarize_with_anthropic(SAMPLE_TRANSCRIPT)

    return {
        "openai": openai_result,
        "anthropic": anthropic_result,
        "transcript_preview": SAMPLE_TRANSCRIPT[:120].strip(),
    }


def compare_results(openai_result: MeetingSummary, anthropic_result: MeetingSummary) -> None:
    """Print a side-by-side comparison of two MeetingSummary outputs."""
    print("\n  COMPARISON")
    print(f"  {'Field':<18} {'OpenAI':<35} {'Anthropic'}")
    print("  " + "-" * 80)

    print(f"  {'topic':<18} {openai_result.topic[:34]:<35} {anthropic_result.topic[:34]}")
    print(f"  {'mood':<18} {openai_result.mood:<35} {anthropic_result.mood}")

    max_points = max(len(openai_result.key_points), len(anthropic_result.key_points))
    for i in range(max_points):
        oai = openai_result.key_points[i][:34] if i < len(openai_result.key_points) else ""
        ant = anthropic_result.key_points[i][:34] if i < len(anthropic_result.key_points) else ""
        label = f"key_point[{i}]" if i > 0 else "key_points[0]"
        print(f"  {label:<18} {oai:<35} {ant}")

    max_steps = max(len(openai_result.next_steps), len(anthropic_result.next_steps))
    for i in range(max_steps):
        oai = openai_result.next_steps[i][:34] if i < len(openai_result.next_steps) else ""
        ant = anthropic_result.next_steps[i][:34] if i < len(anthropic_result.next_steps) else ""
        label = f"next_step[{i}]" if i > 0 else "next_steps[0]"
        print(f"  {label:<18} {oai:<35} {ant}")
