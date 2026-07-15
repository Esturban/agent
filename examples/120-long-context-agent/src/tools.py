"""
120 — Long-Context Agent
Tools: document loading, full-context answering, chunked RAG, answer scoring.
"""

import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

MODEL = "gpt-5.4-nano"

# ~3000 word synthetic technical report about AI systems
LONG_DOCUMENT = """
# Annual AI Systems Performance Report 2024

## Executive Summary

This report covers the performance, reliability, and economic impact of enterprise AI deployments
across 847 organizations surveyed in Q4 2024. Key findings indicate that organizations adopting
multi-agent architectures achieved 34% higher task completion rates compared to single-agent
deployments. The average token cost per production query decreased by 41% year-over-year,
driven by model efficiency improvements and better prompt engineering practices.

## Section 1: Deployment Patterns

### 1.1 Single-Agent vs. Multi-Agent

Among surveyed organizations, 62% use single-agent architectures for customer-facing applications,
while 38% have adopted multi-agent systems. The shift toward multi-agent is accelerating:
in 2023, only 18% of organizations used multi-agent architectures.

Key drivers of multi-agent adoption:
- Complex task decomposition (cited by 78% of adopters)
- Specialization and tool isolation (cited by 65%)
- Parallel processing of independent subtasks (cited by 54%)
- Reduced context window pressure per agent (cited by 47%)

### 1.2 Context Window Utilization

Average context utilization across all deployments: 34% of available context window.
Organizations using RAG systems average 28% utilization.
Organizations using long-context full-document approaches average 67% utilization.

The "lost in the middle" phenomenon (Liu et al., 2023, arxiv:2307.03172) was observed in
42% of long-context deployments. When documents exceeded 32K tokens, models showed
an 18% decrease in accuracy for questions about content in the middle third of the document.

### 1.3 Model Selection Patterns

GPT-4o-mini: 44% of production queries (cost optimization)
GPT-4o: 31% of production queries (quality-critical tasks)
Claude Sonnet: 15% of production queries (long context + document tasks)
Other models: 10% (specialized or on-premise deployments)

## Section 2: Performance Metrics

### 2.1 Faithfulness and Hallucination Rates

Faithfulness measures whether model outputs are grounded in the provided context.
Average faithfulness scores by approach:

| Approach | Faithfulness | Latency (p50) | Cost per 1K queries |
|----------|-------------|---------------|---------------------|
| Full document in context | 0.91 | 4.2s | $0.84 |
| Chunked RAG (top-3) | 0.83 | 1.8s | $0.22 |
| Chunked RAG (top-5) | 0.87 | 2.1s | $0.28 |
| No context (pure LLM) | 0.61 | 0.9s | $0.09 |

Key insight: full-context approaches show 9.6% higher faithfulness than chunked RAG,
but at 3.8x higher latency and 3x higher cost.

### 2.2 Multi-Hop Reasoning

Multi-hop questions require connecting information from multiple sections of a document.
Example: "What percentage cost reduction was achieved by organizations that use the
most popular model for production queries?"

Full-context approaches answered 89% of multi-hop questions correctly.
Chunked RAG answered 67% correctly — a 25% gap.
The gap widens for questions requiring 3+ hops: 82% vs 41%.

### 2.3 Latency Distribution

P50 latency (full context): 4.2 seconds
P95 latency (full context): 12.1 seconds
P50 latency (chunked RAG): 1.8 seconds
P95 latency (chunked RAG): 4.3 seconds

Time-to-first-token for full context is 2.3x slower than chunked RAG at p50.

## Section 3: Economic Analysis

### 3.1 Cost Per Accurate Answer

When adjusting for accuracy rates, the true cost per correct answer narrows:

Full context cost per correct answer: $0.92
Chunked RAG cost per correct answer: $0.27 (at 83% faithfulness)

At scale (1M queries/month), the cost difference is $650K annually.
However, for applications where faithfulness is critical (legal, medical, financial),
the accuracy premium of full-context approaches may justify the cost.

### 3.2 Break-Even Analysis

For tasks requiring >88% faithfulness, full-context approaches are cost-justified.
For tasks tolerating 80-88% faithfulness, chunked RAG is optimal.
For tasks tolerating <80% faithfulness, no-context LLM calls are sufficient.

### 3.3 Token Cost Trends

Year-over-year token cost reduction: 41%
Projected 2025 reduction: additional 35% (based on model releases and competition)
Organizations with dedicated prompt engineering teams: 29% lower costs on average.

## Section 4: Operational Findings

### 4.1 Chunk Size Optimization

Optimal chunk size for general document QA: 512-768 tokens.
Optimal overlap: 10-15% of chunk size (51-77 tokens for 512-token chunks).
Chunks below 256 tokens showed 23% higher hallucination rates.
Chunks above 1024 tokens showed 18% degraded retrieval precision.

### 4.2 Embedding Model Selection

text-embedding-3-small: 89% of chunked RAG deployments (cost-accuracy tradeoff)
text-embedding-3-large: 8% of deployments (highest accuracy)
Legacy ada-002: 3% of deployments (being phased out)

Retrieval accuracy (NDCG@5):
- text-embedding-3-small: 0.847
- text-embedding-3-large: 0.891
- ada-002: 0.801

### 4.3 Failure Modes

Top failure modes in production:
1. Context truncation (29%): documents exceeding context window silently truncated
2. Lost-in-the-middle (24%): relevant content present but not retrieved correctly
3. Retrieval misses (19%): correct chunk not in top-K results
4. Chunk boundary splits (16%): key information split across chunk boundaries
5. Embedding drift (12%): query embedding style mismatches document embedding style

## Section 5: Recommendations

### 5.1 Decision Framework

Use full-context approach when:
- Document is under 50K tokens
- Task requires multi-hop reasoning (3+ information sources)
- Faithfulness requirement exceeds 88%
- Latency tolerance exceeds 3 seconds

Use chunked RAG when:
- Document corpus exceeds 100K tokens
- Queries are fact-lookup style (single-hop)
- Cost sensitivity is high
- Latency requirement is under 2 seconds

Use hybrid (initial RAG + local rerank + full context on selected chunks) when:
- Corpus is large but most queries are concentrated in 20% of content
- Teams have engineering capacity for two-stage retrieval

### 5.2 Implementation Checklist

For chunked RAG deployments:
- [ ] Set chunk size 512-768 tokens with 10-15% overlap
- [ ] Use text-embedding-3-small as the default embedding model
- [ ] Implement fallback to top-5 chunks if top-3 returns low confidence results
- [ ] Monitor retrieval recall weekly; retune if below 0.85 NDCG@5
- [ ] Log all context truncations as high-severity events

For full-context deployments:
- [ ] Set explicit document length limits with hard error (not silent truncation)
- [ ] Position the most critical information in the first and last thirds of the prompt
- [ ] Use caching (prompt caching) to reduce cost for repeated document queries
- [ ] Monitor for "lost in the middle" indicators (accuracy vs. position correlation)

## Conclusion

The choice between full-context and chunked RAG is not binary. Organizations achieving the
highest accuracy-cost ratios use a tiered approach: fast RAG for high-volume standard queries,
full-context for critical or complex queries, and human escalation for edge cases.

The 41% year-over-year cost reduction makes full-context approaches increasingly viable.
By 2026, we project that 60% of enterprise AI deployments will use full-context for
documents under 100K tokens, up from the current 23%.

Document word count: approximately 3,000 words.
"""

QUESTIONS = [
    {
        "q": "What percentage of organizations use multi-agent architectures?",
        "expected": "38%",
    },
    {
        "q": "What is the faithfulness score for the full-document approach compared to chunked RAG top-3?",
        "expected": "0.91 vs 0.83",
    },
    {
        "q": "What is the optimal chunk size range for general document QA?",
        "expected": "512-768 tokens",
    },
    {
        "q": "How much did token costs decrease year-over-year?",
        "expected": "41%",
    },
    {
        "q": "What percentage cost reduction was achieved by organizations that use the most popular model (GPT-4o-mini at 44%) and also have dedicated prompt engineering teams?",
        "expected": "29% lower costs",
    },
]


def load_sample_long_document() -> str:
    """Return the ~3000 word synthetic AI systems report."""
    return LONG_DOCUMENT


def answer_with_full_context(document: str, questions: list[dict]) -> list[str]:
    """Answer questions by loading the full document into context."""
    client = ChatOpenAI(model=MODEL, temperature=0)
    system = f"You are a precise document analyst. Answer questions based ONLY on the provided document. Be brief and cite specific numbers.\n\nDOCUMENT:\n{document}"
    answers = []
    for item in questions:
        msg = [SystemMessage(content=system), HumanMessage(content=item["q"])]
        response = client.invoke(msg)
        answers.append(response.content.strip())
    return answers


def _simple_chunk(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """Split text into overlapping word-count chunks."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i: i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def _retrieve(query: str, chunks: list[str], top_k: int = 3) -> list[str]:
    """Simple keyword-overlap retrieval — no vector DB needed."""
    query_words = set(query.lower().split())
    scored = []
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k] if _ > 0]


def answer_with_chunked_rag(document: str, questions: list[dict]) -> list[str]:
    """Answer questions using keyword-overlap chunked retrieval."""
    client = ChatOpenAI(model=MODEL, temperature=0)
    chunks = _simple_chunk(document)
    answers = []
    for item in questions:
        retrieved = _retrieve(item["q"], chunks)
        if not retrieved:
            answers.append("No relevant chunks found.")
            continue
        context = "\n\n---\n\n".join(retrieved)
        system = f"Answer the question using ONLY the retrieved context below. Be brief.\n\nCONTEXT:\n{context}"
        msg = [SystemMessage(content=system), HumanMessage(content=item["q"])]
        response = client.invoke(msg)
        answers.append(response.content.strip())
    return answers


def score_answer(predicted: str, expected: str) -> float:
    """Simple partial-match score: 1.0 if expected substring in predicted, else 0.5 if any word matches."""
    if expected.lower() in predicted.lower():
        return 1.0
    expected_words = set(expected.lower().replace("%", "").split())
    predicted_words = set(predicted.lower().replace("%", "").split())
    overlap = len(expected_words & predicted_words)
    return round(overlap / max(len(expected_words), 1), 2)
