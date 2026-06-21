from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow, demonstrate_retry_behavior  # noqa: E402


def main() -> None:
    print("=== 117 — Instructor: Type-Safe Structured Extraction ===\n")
    print("Running 3 extraction tasks with automatic retry on validation failure...\n")

    results = create_workflow()

    notes = results["meeting_notes"]
    review = results["product_review"]
    address = results["address"]

    print("\n--- Task 1: MeetingNotes ---")
    print(f"Attendees:    {', '.join(notes.attendees)}")
    print(f"Decisions:    {len(notes.decisions)} extracted")
    for d in notes.decisions:
        print(f"  - {d}")
    print(f"Action items: {len(notes.action_items)} extracted")
    for a in notes.action_items:
        print(f"  - {a}")
    if notes.next_meeting:
        print(f"Next meeting: {notes.next_meeting}")

    print("\n--- Task 2: ProductReview ---")
    print(f"Sentiment:       {review.sentiment}")
    print(f"Score:           {review.score}/5.0")
    print(f"Would recommend: {review.would_recommend}")
    print(f"Key features ({len(review.key_features)}):")
    for f in review.key_features:
        print(f"  - {f}")

    print("\n--- Task 3: UserAddress ---")
    print(f"Street:   {address.street}")
    print(f"City:     {address.city}")
    print(f"State:    {address.state}")
    print(f"ZIP:      {address.zip_code}")

    print("\n--- Retry behavior demo ---")
    demonstrate_retry_behavior()

    print("\nKey insight:")
    print("instructor.from_openai() wraps the OpenAI client so that response_model=")
    print("adds JSON schema to the tool definition and validates the response.")
    print("On ValidationError, instructor automatically reasks with the error message,")
    print("giving the model up to max_retries attempts to produce valid output.")


if __name__ == "__main__":
    main()
