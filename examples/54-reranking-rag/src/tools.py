from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

MAX_RETRIEVE = 20
MAX_RERANK = 4

SAMPLE_DOCS = [
    "The transformer architecture uses self-attention to process all tokens in parallel.",
    "BERT is a bidirectional encoder trained on masked language modeling and next sentence prediction.",
    "GPT models are autoregressive decoders that generate text left to right, one token at a time.",
    "Self-attention computes a weighted sum of all token representations in a sequence.",
    "Fine-tuning adapts a pretrained language model to a specific downstream task.",
    "Chain-of-thought prompting improves multi-step reasoning by showing intermediate steps.",
    "Retrieval-augmented generation fetches external documents to ground LLM responses.",
    "Vector databases store dense embeddings and support approximate nearest neighbor queries.",
    "Chunking splits documents into smaller pieces to fit within the retrieval context window.",
    "Cross-encoders score query-document pairs jointly, providing higher accuracy than bi-encoders.",
    "Bi-encoders embed query and document independently, enabling fast offline indexing.",
    "Reranking is a two-stage approach: retrieve many candidates cheaply, then score precisely.",
    "Reciprocal Rank Fusion merges multiple ranked lists without requiring calibrated scores.",
    "BM25 is a keyword-based ranking function that works well for exact-match queries.",
    "Hybrid search combines sparse BM25 retrieval with dense vector retrieval for better coverage.",
    "Cosine similarity measures the angle between two embedding vectors, ignoring magnitude.",
    "In-context learning allows LLMs to adapt to new tasks without gradient updates.",
    "Instruction tuning trains models on diverse task descriptions to improve zero-shot performance.",
    "Hallucination occurs when a model generates plausible-sounding but factually incorrect content.",
    "Faithfulness measures whether an answer is supported by the retrieved context.",
]

SAMPLE_QUERIES = [
    "How do transformers process sequences efficiently?",
    "What is the difference between BERT and GPT architectures?",
    "Why is reranking more accurate than single-stage retrieval?",
]


def build_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma.from_texts(
        SAMPLE_DOCS,
        embeddings,
        collection_name="reranking-demo",
    )
