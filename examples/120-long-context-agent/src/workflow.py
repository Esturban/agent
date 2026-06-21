"""
120 — Long-Context Agent
Workflow: run 5 questions through full-context and chunked-RAG, compare results.
"""

import time

from .tools import (
    QUESTIONS,
    answer_with_chunked_rag,
    answer_with_full_context,
    load_sample_long_document,
    score_answer,
)


def create_workflow() -> dict:
    """Compare full-context vs chunked RAG on 5 multi-hop questions."""
    doc = load_sample_long_document()
    print(f"Document: {len(doc.split())} words, {len(doc)} chars\n")

    # Full-context pass
    t0 = time.time()
    full_answers = answer_with_full_context(doc, QUESTIONS)
    full_latency = time.time() - t0

    # Chunked RAG pass
    t1 = time.time()
    rag_answers = answer_with_chunked_rag(doc, QUESTIONS)
    rag_latency = time.time() - t1

    # Score both
    results = []
    for i, q in enumerate(QUESTIONS):
        full_score = score_answer(full_answers[i], q["expected"])
        rag_score = score_answer(rag_answers[i], q["expected"])
        results.append({
            "question": q["q"][:60],
            "expected": q["expected"],
            "full_answer": full_answers[i][:80],
            "rag_answer": rag_answers[i][:80],
            "full_score": full_score,
            "rag_score": rag_score,
        })

    # Print comparison
    print(f"{'Q':<3} {'Expected':<20} {'Full':>6} {'RAG':>6}")
    print("-" * 45)
    for i, r in enumerate(results, 1):
        print(f"{i:<3} {r['expected']:<20} {r['full_score']:>6.2f} {r['rag_score']:>6.2f}")

    avg_full = sum(r["full_score"] for r in results) / len(results)
    avg_rag = sum(r["rag_score"] for r in results) / len(results)

    print(f"\nAvg score:  full={avg_full:.2f}  rag={avg_rag:.2f}")
    print(f"Latency:    full={full_latency:.1f}s  rag={rag_latency:.1f}s")

    return {
        "results": results,
        "avg_full_score": avg_full,
        "avg_rag_score": avg_rag,
        "full_latency_s": round(full_latency, 2),
        "rag_latency_s": round(rag_latency, 2),
    }
