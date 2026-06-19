"""
LLM-as-judge workflow.

The judge scores each RAG answer on three dimensions:
  Relevance   — does the answer address the question?
  Faithfulness — is every claim grounded in the retrieved context?
  Completeness — does it cover what the context allows?

No labelled data needed: the LLM itself is the evaluator.
"""

import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ── Prompts ──────────────────────────────────────────────────────────────────

# The judge is given the question, the context the RAG retrieved, and the
# answer the RAG produced.  It must score each dimension 1–5 and explain why.
JUDGE_SYSTEM = """\
You are an evaluation judge for a RAG (Retrieval-Augmented Generation) system.
Score the given answer on three dimensions. Be critical — a score of 5 is rare.

Dimensions:
  Relevance    (1–5): Does the answer directly address the question asked?
  Faithfulness (1–5): Is every claim in the answer supported by the provided context?
                      Penalise hallucinated facts not in the context.
  Completeness (1–5): Given the context available, how fully does the answer respond?

Return ONLY valid JSON:
{
  "relevance": <1-5>,
  "faithfulness": <1-5>,
  "completeness": <1-5>,
  "reasoning": "<one sentence per dimension, separated by |>"
}"""

JUDGE_USER = """\
Question: {question}

Retrieved context:
{context}

Answer to evaluate:
{answer}"""

# ── Test set ──────────────────────────────────────────────────────────────────

# These questions exercise different failure modes: hallucination risk,
# partial retrieval, and off-topic deflection.
TEST_QUESTIONS = [
    "What is LangGraph used for?",
    "How does Corrective RAG decide when to rewrite a query?",
    "What are reflection tokens in Self-RAG?",
    "How does human-in-the-loop checkpointing work?",
    "What is the difference between RAG and a standard LLM?",
]

# ── Judge logic ───────────────────────────────────────────────────────────────

_judge = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def judge_answer(question: str, context: str, answer: str) -> dict:
    """Call the LLM judge and return parsed scores + reasoning."""
    raw = _judge.invoke([
        SystemMessage(content=JUDGE_SYSTEM),
        HumanMessage(content=JUDGE_USER.format(
            question=question, context=context, answer=answer
        )),
    ]).content
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {"relevance": 0, "faithfulness": 0, "completeness": 0, "reasoning": "parse error"}


def run_eval(rag_chain_fn) -> list[dict]:
    """Run all test questions through the RAG chain, then judge each answer."""
    from .tools import build_rag_chain
    chain = rag_chain_fn or build_rag_chain()
    results = []
    for q in TEST_QUESTIONS:
        answer, context = chain(q)
        scores = judge_answer(q, context, answer)
        results.append({"question": q, "answer": answer, "context": context, **scores})
    return results
