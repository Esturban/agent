import re

import numpy as np
from langchain_openai import OpenAIEmbeddings

# Sample document used across all strategies
SAMPLE_TEXT = """Neural networks are computing systems loosely inspired by biological neural networks. Deep learning uses multiple layers to progressively extract higher-level features from raw input. Training these networks requires large labelled datasets and significant compute resources.

The transformer architecture introduced in 2017 revolutionized natural language processing. It replaces recurrent networks with self-attention, allowing all tokens to attend to each other simultaneously. This parallelism enables training on much larger datasets than earlier sequential models.

Retrieval-augmented generation (RAG) combines a language model with an external knowledge base. When a question arrives, a retriever fetches relevant documents, and the generator conditions its output on both the question and the retrieved context. This grounds the model in factual sources and reduces hallucination.

Vector databases store high-dimensional embeddings and support approximate nearest-neighbor search. Systems like ChromaDB, Qdrant, and Pinecone make it practical to search millions of document chunks in milliseconds. The embedding quality is as important as the retrieval algorithm itself.

Evaluation of RAG pipelines requires specialized metrics. Faithfulness checks whether the answer is grounded in the retrieved context. Context recall checks whether all necessary information was retrieved. Answer relevancy checks whether the answer directly addresses the question."""

DEMO_QUERY = "How does RAG ground model outputs in factual sources?"


def sentence_window_chunks(text: str, window: int = 1) -> list[dict]:
    """Split into sentences; embed the sentence, store a wider context window."""
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    result = []
    for i, sent in enumerate(sents):
        lo = max(0, i - window)
        hi = min(len(sents), i + window + 1)
        result.append({"sentence": sent, "context": " ".join(sents[lo:hi])})
    return result


def _cosine_sim(a: list[float], b: list[float]) -> float:
    a_arr, b_arr = np.array(a), np.array(b)
    return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr) + 1e-10))


def semantic_chunks(text: str, threshold: float = 0.75, emb_model: OpenAIEmbeddings = None) -> list[str]:
    """Split on cosine similarity drops between consecutive sentence embeddings."""
    if emb_model is None:
        emb_model = OpenAIEmbeddings(model="text-embedding-3-small")
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    embeddings = emb_model.embed_documents(sents)
    sims = [_cosine_sim(embeddings[i], embeddings[i + 1]) for i in range(len(sents) - 1)]
    chunks, current = [], [sents[0]]
    for i, sim in enumerate(sims):
        if sim < threshold:
            chunks.append(" ".join(current))
            current = [sents[i + 1]]
        else:
            current.append(sents[i + 1])
    if current:
        chunks.append(" ".join(current))
    return chunks
