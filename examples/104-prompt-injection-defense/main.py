"""
Example 104 — Indirect Prompt Injection Defense (Spotlighting)

What this shows:
  Two runs of the same web-scraping agent — one undefended, one defended.
  The defended version uses two techniques from the Microsoft Spotlighting
  paper (arxiv:2403.14720):
    1. Instruction hierarchy — system prompt asserts authority over tool output
    2. Spotlighting — data sections are delimited so the LLM treats them as
       untrusted content, not executable instructions

Why it matters:
  Without these defenses, an attacker who controls any web page the agent
  visits can hijack agent behavior.  Spotlighting reduces attack success rate
  from ~80% to <2% on GPT-4 in the paper.

Key files:
  src/tools.py    — PAGES dict with benign and malicious web content
  src/workflow.py — fetch_pages → summarize nodes; defended/undefended variants
"""

import os

from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY", "").startswith("sk-"):
    raise RuntimeError("OPENAI_API_KEY is required for prompt-injection defense.")

from src.tools import PAGES  # noqa: E402
from src.workflow import create_workflow  # noqa: E402

URLS = list(PAGES.keys())


def run(defended: bool) -> list[str]:
    app = create_workflow()
    result = app.invoke({"urls": URLS, "defended": defended, "summaries": []})
    return result["summaries"]


def main() -> None:
    print("=" * 60)
    print("UNDEFENDED AGENT (no instruction hierarchy, no spotlighting)")
    print("=" * 60)
    for s in run(defended=False):
        print(s)
        print()

    print("=" * 60)
    print("DEFENDED AGENT (instruction hierarchy + spotlighting)")
    print("=" * 60)
    for s in run(defended=True):
        print(s)
        print()

    print("Compare the responses on the three malicious pages to see")
    print("how the defended agent rejects injected instructions.")


if __name__ == "__main__":
    main()
