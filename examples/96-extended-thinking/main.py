import os
from dotenv import load_dotenv

load_dotenv()

from src.tools import PUZZLES      # noqa: E402
from src.workflow import ask        # noqa: E402


def main() -> None:
    print("=== 96 · Extended Thinking ===")
    print("claude-3-7-sonnet | thinking budget: 8 000 tokens")
    print("Thinking blocks are private — they improve quality but are never returned to users.\n")

    for puzzle in PUZZLES:
        label  = puzzle["label"]
        prompt = puzzle["prompt"]
        print(f"[{label}]")
        print(f"Q: {prompt}\n")

        plain   = ask(prompt, thinking=False)
        thought = ask(prompt, thinking=True)

        print(f"  Without thinking ({plain['output_tokens']} tokens):")
        print(f"    {plain['answer'][:200]}")
        print()
        print(f"  With thinking ({thought['output_tokens']} tokens | ~{thought['thinking_words']} thinking words):")
        print(f"    {thought['answer'][:200]}")
        print()
        print(f"  Thinking preview: {thought['thinking_preview']}...")
        print("-" * 70)
        print()

    print("Takeaway: extended thinking helps most on problems where the first")
    print("intuitive answer is wrong (CRT) or requires step-by-step calculation.")


if __name__ == "__main__":
    main()
