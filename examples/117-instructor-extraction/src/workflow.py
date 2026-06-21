"""
Extraction workflow for example 117 — Instructor.

Demonstrates all 3 extraction tasks and shows the automatic retry
behavior on validation failure by running them sequentially.
"""

import instructor
from openai import OpenAI

from src.tools import (
    MeetingNotes,
    ProductReview,
    UserAddress,
    make_client,
    extract_meeting_notes,
    extract_product_review,
    extract_address,
    MEETING_TRANSCRIPT,
    PRODUCT_REVIEW,
    ADDRESS_TEXT,
)


def create_workflow() -> dict:
    """
    Run all 3 extraction tasks and return results as a dict.

    Tasks:
      1. MeetingNotes  — from a Q3 planning transcript
      2. ProductReview — from a mixed wireless keyboard review
      3. UserAddress   — from an address spelled out in words

    Each uses instructor.from_openai() with max_retries=3.
    On ValidationError, instructor automatically re-prompts with the
    error details, giving the model up to 3 attempts to produce valid output.
    """
    client = make_client()

    print("  [1/3] Extracting meeting notes...")
    notes: MeetingNotes = extract_meeting_notes(client, MEETING_TRANSCRIPT)

    print("  [2/3] Extracting product review...")
    review: ProductReview = extract_product_review(client, PRODUCT_REVIEW)

    print("  [3/3] Extracting address...")
    address: UserAddress = extract_address(client, ADDRESS_TEXT)

    return {
        "meeting_notes": notes,
        "product_review": review,
        "address": address,
    }


def demonstrate_retry_behavior() -> None:
    """
    Show what happens when validation fails: instructor reasks the model.

    We deliberately pass deliberately ambiguous address text that might
    produce an invalid ZIP or state, then let instructor retry.
    """
    client = make_client()

    tricky_text = (
        "Send it to 800 N Michigan Ave, Chicago, Illinois, six zero six one one. "
        "Buzz unit 4C if no one answers."
    )

    print("  Extracting address from text with numbers spelled out...")
    addr = extract_address(client, tricky_text)
    print(f"  Result: {addr.street}, {addr.city}, {addr.state} {addr.zip_code}")
    print(f"  ZIP valid (5 digits): {addr.zip_code.isdigit() and len(addr.zip_code) == 5}")
