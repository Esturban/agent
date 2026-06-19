"""
Example 70 — Prompt Injection Defense (RAG pipeline)

What this shows:
  A RAG pipeline that classifies each retrieved chunk for injection risk
  BEFORE passing it to the LLM.  High-risk chunks — those containing
  instructions like "Ignore previous instructions" — are dropped.

Why it matters:
  Indirect prompt injection is the #1 attack vector for retrieval-augmented
  agents.  Classifying context before it reaches the model is a practical,
  low-latency first line of defense.

Key files:
  src/tools.py    — poisoned knowledge base with injected instructions
  src/workflow.py — retrieve → classify → filter → answer nodes
"""

from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_QUESTION  # noqa: E402
from src.workflow import InjectionDefenseState, create_workflow  # noqa: E402


def main() -> None:
    print("Prompt Injection Defense — classify-then-filter RAG pipeline")
    print("Injected instructions embedded in retrieved chunks are detected and dropped.\n")
    app = create_workflow()
    print(f"Question : {SAMPLE_QUESTION}\n")
    result: InjectionDefenseState = app.invoke(
        {"question": SAMPLE_QUESTION, "raw_chunks": [], "classifications": [], "safe_chunks": [], "answer": ""}
    )
    blocked = [c for c in result["classifications"] if c["risk"] == "high"]
    print(f"Retrieved : {len(result['raw_chunks'])} chunks")
    print(f"Blocked   : {len(blocked)} injection attempts")
    for b in blocked:
        print(f"  > {b['chunk'][:80]}...")
    print(f"Safe      : {len(result['safe_chunks'])} chunks passed filter")
    print(f"\nAnswer    : {result['answer']}")


if __name__ == "__main__":
    main()
