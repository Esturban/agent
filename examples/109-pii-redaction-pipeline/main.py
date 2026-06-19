"""
Example 109 — PII Redaction Pipeline (Microsoft Presidio)

What this shows:
  A two-stage redaction pipeline using Microsoft Presidio:
  Stage 1 — pre-ingestion: scrub PII from documents before the LLM sees them.
  Stage 2 — post-generation: scrub any PII the LLM still leaks in its reply.

Why it matters:
  LLMs memorise and recombine data.  Even a correctly-prompted model may
  quote back a name, SSN, or credit card from its context window.  Dual-stage
  redaction is the GDPR/HIPAA-compliant production pattern.

Key files:
  src/tools.py    — SAMPLE_DOCUMENTS with real PII + build_engines() + redact()
  src/workflow.py — REDACTION_SYSTEM prompt + two-stage run_pipeline()
"""

from dotenv import load_dotenv
load_dotenv()

from src.tools import SAMPLE_DOCUMENTS
from src.workflow import run_pipeline

QUESTION = "Summarize the key details about the person mentioned."


def show_entities(label: str, entities: list[dict]) -> None:
    if entities:
        types = ", ".join(f"{e['type']}({e['score']})" for e in entities[:5])
        print(f"  {label}: [{types}{'...' if len(entities) > 5 else ''}]")
    else:
        print(f"  {label}: none detected")


def main():
    print("\nPII Redaction Pipeline — Microsoft Presidio bi-directional sanitization")
    print("=" * 70)
    print("Stage 1: redact document before LLM ingestion")
    print("Stage 2: redact LLM response before delivery\n")

    for i, doc in enumerate(SAMPLE_DOCUMENTS, 1):
        print(f"--- Document {i} ---")
        result = run_pipeline(doc, QUESTION)

        show_entities("Pre-ingestion entities found", result["pre_entities"])
        show_entities("Post-generation entities found", result["post_entities"])

        print(f"\n  Pre-redacted doc (first 120 chars):")
        print(f"    {result['pre_redacted_doc'][:120].replace(chr(10), ' ')}...")
        print(f"\n  Final response (delivered to user):")
        print(f"    {result['final_response'][:200].replace(chr(10), ' ')}")
        print()


if __name__ == "__main__":
    main()
