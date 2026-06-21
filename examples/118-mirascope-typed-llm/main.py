from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow, compare_results  # noqa: E402


def main() -> None:
    print("=== 118 — Mirascope: Pydantic-First LLM Calls with Provider Switching ===\n")
    print("Running the same MeetingSummary task with OpenAI and Anthropic...\n")

    results = create_workflow()

    oai = results["openai"]
    ant = results["anthropic"]

    print(f"\nTranscript preview: {results['transcript_preview']}...\n")

    print("--- OpenAI (gpt-4o-mini) ---")
    print(f"Topic:       {oai.topic}")
    print(f"Mood:        {oai.mood}")
    print(f"Key points:  {len(oai.key_points)}")
    for p in oai.key_points:
        print(f"  - {p}")
    print(f"Next steps:  {len(oai.next_steps)}")
    for s in oai.next_steps:
        print(f"  - {s}")

    print("\n--- Anthropic (claude-haiku-4-5) ---")
    print(f"Topic:       {ant.topic}")
    print(f"Mood:        {ant.mood}")
    print(f"Key points:  {len(ant.key_points)}")
    for p in ant.key_points:
        print(f"  - {p}")
    print(f"Next steps:  {len(ant.next_steps)}")
    for s in ant.next_steps:
        print(f"  - {s}")

    compare_results(oai, ant)

    print("\nKey insight:")
    print("The only difference between OpenAI and Anthropic calls is the decorator.")
    print("Mirascope handles prompt formatting, API call, and Pydantic parsing")
    print("identically across providers — true provider portability.")


if __name__ == "__main__":
    main()
