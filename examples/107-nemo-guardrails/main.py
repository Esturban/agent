from dotenv import load_dotenv
load_dotenv()

from src.tools import TEST_INPUTS
from src.workflow import load_rails, query


def main():
    print("\nNeMo Guardrails — input/output rails via Colang DSL")
    print("=" * 55)
    print("Rails active: jailbreak (input), off-topic (input), toxicity (output)\n")

    rails = load_rails()

    for category, prompt in TEST_INPUTS:
        short = prompt[:60] + ("..." if len(prompt) > 60 else "")
        response = query(rails, prompt)
        blocked = any(kw in response.lower() for kw in ["can't help", "outside", "can't provide"])
        tag = "BLOCKED" if blocked else "ALLOWED"
        color = "\033[91m" if blocked else "\033[92m"
        reset = "\033[0m"
        print(f"[{category.upper():10}] {color}{tag}{reset}")
        print(f"  Input : {short}")
        print(f"  Reply : {response[:100].strip()}")
        print()


if __name__ == "__main__":
    main()
