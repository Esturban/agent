from dotenv import load_dotenv
load_dotenv()

from src.tools import ATTACK_SAMPLES
from src.workflow import create_workflow

COLORS = {"BENIGN": "\033[92m", "BLOCKED": "\033[91m", "RESET": "\033[0m"}


def main():
    app = create_workflow()

    print("\nJailbreak Detection — 5 attack families + 2 benign baselines")
    print("=" * 65)

    for family, prompt in ATTACK_SAMPLES:
        short = prompt[:60].replace("\n", " ") + ("..." if len(prompt) > 60 else "")
        result = app.invoke({"user_input": prompt, "category": "", "confidence": 0.0, "reasoning": "", "response": ""})
        blocked = "[BLOCKED]" in result["response"]
        tag = f"{COLORS['BLOCKED']}BLOCKED{COLORS['RESET']}" if blocked else f"{COLORS['BENIGN']}ALLOWED{COLORS['RESET']}"
        print(f"\n[{family}] {tag}")
        print(f"  Input : {short}")
        if blocked:
            print(f"  Detect: {result['category']} ({result['confidence']:.0%}) — {result['reasoning']}")
        else:
            resp_short = result["response"][:80].replace("\n", " ")
            print(f"  Reply : {resp_short}...")


if __name__ == "__main__":
    main()
