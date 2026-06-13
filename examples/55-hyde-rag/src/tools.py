from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

SAMPLE_DOCS = [
    "RAG grounds LLM responses by retrieving relevant documents before generation.",
    "The retriever fetches documents that match the query using vector similarity.",
    "Hallucination occurs when a language model invents facts not in its training data.",
    "Embeddings convert text to dense vectors so similar meanings cluster together.",
    "ChromaDB is a lightweight vector store that runs locally without a server.",
    "OpenAI text-embedding-3-small produces 1536-dimensional embeddings efficiently.",
    "Hypothetical Document Embeddings (HyDE) embeds a generated answer, not the query.",
    "A bi-encoder embeds query and document separately for fast approximate search.",
    "Cosine similarity measures how similar two embedding vectors are regardless of length.",
    "Prompt engineering shapes model outputs by crafting precise instruction text.",
]

SAMPLE_QUERIES = [
    "How does retrieval-augmented generation reduce hallucination?",
    "What is the difference between a bi-encoder and a cross-encoder?",
    "Why does embedding a hypothetical answer sometimes outperform embedding the query?",
]


def build_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma.from_texts(SAMPLE_DOCS, embeddings, collection_name="hyde-demo")
