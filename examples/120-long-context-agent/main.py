"""
120 — Long-Context Agent
Entry point: compare full-document context vs chunked RAG on 5 multi-hop questions.
Run: python examples/120-long-context-agent/main.py
"""

from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow


def main():
    print("=== 120 — Long-Context Agent ===")
    print("Comparing: full document in context vs. keyword-overlap chunked RAG\n")
    result = create_workflow()
    print(f"\nFull-context wins: {result['avg_full_score'] >= result['avg_rag_score']}")
    print("Key insight: full-context is more faithful but slower and costlier.")
    print("Use full-context for multi-hop questions; use RAG for fact lookup at scale.")


if __name__ == "__main__":
    main()
