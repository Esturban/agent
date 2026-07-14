"""
Example 106 — Jailbreak Detection

What this shows:
  An LLM-based classifier that recognises five jailbreak attack families
  (DAN, ROLEPLAY, ENCODING, MANY_SHOT, OVERRIDE) and either blocks or
  passes the input through to a responding agent.

Why it matters:
  Keyword filtering misses novel phrasings.  Using a prompted classifier
  lets you describe attack patterns in natural language, which generalises
  much better than regex or blocklists.

Key files:
  src/tools.py    — ATTACK_SAMPLES corpus + CLASSIFIER_SYSTEM prompt
  src/workflow.py — classify_node → route → block_node or respond_node
"""

import os

from dotenv import load_dotenv
load_dotenv()

if not os.environ.get("OPENAI_API_KEY", "").startswith("sk-"):
    raise RuntimeError("OPENAI_API_KEY must be set before running this live example.")

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
