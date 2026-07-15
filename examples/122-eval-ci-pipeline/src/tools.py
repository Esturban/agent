"""
122 — Eval CI Pipeline
Tools: golden dataset, good/degraded pipelines, DeepEval test case builder.
"""

import os

from openai import OpenAI

MODEL = "gpt-5.4-nano"

GOLDEN_DATASET = [
    {
        "question": "What is a LangGraph node?",
        "context": "In LangGraph, a node is a Python function that receives the current state dict and returns an updated state dict. Nodes are the processing units in a LangGraph workflow.",
        "expected_output": "A LangGraph node is a Python function that receives and returns a state dict.",
    },
    {
        "question": "What does RAG stand for?",
        "context": "RAG stands for Retrieval-Augmented Generation. It combines a retrieval system (usually vector search) with a generative LLM to produce grounded, factual responses.",
        "expected_output": "RAG stands for Retrieval-Augmented Generation.",
    },
    {
        "question": "What is the purpose of temperature in LLM calls?",
        "context": "Temperature controls the randomness of LLM outputs. A temperature of 0 produces deterministic, focused outputs. Higher temperatures (0.7-1.0) produce more creative and varied outputs.",
        "expected_output": "Temperature controls randomness; 0 is deterministic, higher values increase creativity.",
    },
    {
        "question": "What is prompt injection?",
        "context": "Prompt injection is an attack where malicious content in user input or retrieved documents overrides the LLM's original instructions. It is a key security risk in agentic systems.",
        "expected_output": "Prompt injection overrides LLM instructions via malicious user input or retrieved content.",
    },
    {
        "question": "What is the difference between gpt-4o and gpt-4o-mini?",
        "context": "gpt-4o is OpenAI's flagship multimodal model with highest capability. gpt-4o-mini is a smaller, faster, and cheaper version optimized for cost-efficiency while maintaining strong performance on most tasks.",
        "expected_output": "gpt-4o is the flagship model; gpt-4o-mini is smaller, faster, and cheaper.",
    },
    {
        "question": "What is a vector database?",
        "context": "A vector database stores high-dimensional embeddings and supports similarity search (nearest neighbor). Examples include Chroma, Pinecone, and Weaviate. They are the retrieval backbone of most RAG systems.",
        "expected_output": "A vector database stores embeddings and enables similarity search for RAG retrieval.",
    },
    {
        "question": "What is tool calling in LLMs?",
        "context": "Tool calling (also called function calling) allows LLMs to request the execution of defined functions. The LLM outputs a structured JSON call, which the framework executes and returns results back to the LLM.",
        "expected_output": "Tool calling lets LLMs request function execution by outputting structured JSON calls.",
    },
    {
        "question": "What is the system prompt?",
        "context": "The system prompt is an instruction given to an LLM at the start of a conversation, before any user messages. It sets the AI's persona, task, constraints, and context.",
        "expected_output": "The system prompt sets the AI's persona, task, and constraints before conversation starts.",
    },
    {
        "question": "What is chain-of-thought prompting?",
        "context": "Chain-of-thought (CoT) prompting encourages LLMs to show their reasoning step by step before giving a final answer. It was shown to significantly improve performance on multi-step reasoning tasks.",
        "expected_output": "CoT prompting makes LLMs show step-by-step reasoning, improving multi-step task performance.",
    },
    {
        "question": "What is a hallucination in LLM outputs?",
        "context": "A hallucination is when an LLM generates factually incorrect or fabricated information presented as true. Hallucinations are more common when the model lacks context or is asked about obscure facts.",
        "expected_output": "A hallucination is when an LLM generates factually incorrect or fabricated information.",
    },
]


def load_golden_dataset() -> list[dict]:
    """Return the 10 Q&A pairs for evaluation."""
    return GOLDEN_DATASET


def run_pipeline(question: str, context: str) -> str:
    """The pipeline under test: answers using the provided context (good pipeline)."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required to run the live evaluation pipeline.")
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"Answer the question using ONLY the provided context. Be concise.\n\nContext: {context}"},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def degraded_pipeline(question: str, context: str) -> str:
    """Intentionally bad pipeline: ignores context and gives a generic non-answer."""
    _ = context  # intentionally ignored
    _ = question
    return "I don't know. Please consult relevant documentation for more information."


def build_test_case(row: dict, actual_output: str) -> dict:
    """Build a DeepEval-compatible test case dict."""
    return {
        "input": row["question"],
        "actual_output": actual_output,
        "expected_output": row["expected_output"],
        "context": [row["context"]],
    }


def score_faithfulness_simple(actual: str, context: str) -> float:
    """
    Simple local faithfulness proxy: fraction of context keywords in the answer.
    Used as fallback when DeepEval is not installed.
    """
    context_words = set(context.lower().split())
    actual_words = set(actual.lower().split())
    common = context_words & actual_words
    return round(min(len(common) / max(len(context_words) * 0.15, 1), 1.0), 3)


def score_relevancy_simple(actual: str, question: str) -> float:
    """
    Simple local answer relevancy proxy: fraction of question keywords in the answer.
    """
    q_words = set(question.lower().split()) - {"what", "is", "the", "a", "an", "of", "in", "does"}
    actual_words = set(actual.lower().split())
    if not q_words:
        return 1.0
    return round(len(q_words & actual_words) / len(q_words), 3)
