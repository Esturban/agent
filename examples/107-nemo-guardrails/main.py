"""
Example 107 — NeMo Guardrails (Colang DSL)

What this shows:
  NVIDIA NeMo Guardrails intercept every request at the framework level
  using a domain-specific language called Colang.  Rails are declared as
  conversation flows, not Python code — making them auditable by
  non-engineers.

Why it matters:
  LangGraph/LangChain guardrails live in Python and can be bypassed if a
  developer forgets to wire them.  NeMo rails are injected at the LLM call
  layer, so every interaction is covered automatically.

Key files:
  config/rails.co  — Colang DSL rail definitions (jailbreak, off-topic, toxicity)
  config/config.yml — NeMo config (model, embeddings, colang path)
  src/workflow.py  — load_rails() → query() wrappers
"""

import os

from dotenv import load_dotenv
load_dotenv()

if not os.environ.get("OPENAI_API_KEY", "").startswith("sk-"):
    raise RuntimeError("OPENAI_API_KEY must be set before running this live example.")

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
