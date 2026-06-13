from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

TOP_K = 8

SAMPLE_DOCS = [
    "The transformer model introduced multi-head self-attention for sequence modeling.",
    "RAG pipelines retrieve documents and pass them to the generator as context.",
    "Chunking splits long documents into smaller pieces that fit in a context window.",
    "Contextual compression filters retrieved chunks to keep only the relevant sentences.",
    "LLMChainFilter asks the LLM to decide if a passage answers the query.",
    "Cross-encoders can be used as compressors to score passage-level relevance.",
    "Embedding models map text to dense vectors for fast similarity search.",
    "The context window of GPT-4o-mini is 128k tokens, supporting long documents.",
    "Faithfulness measures whether an answer is supported by the provided context.",
    "Vector stores like ChromaDB index embeddings for approximate nearest-neighbor search.",
]

SAMPLE_QUERIES = [
    "What is contextual compression in RAG pipelines?",
    "How does LLMChainFilter decide which passages to keep?",
    "What is the context window size of GPT-4o-mini?",
]


def build_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma.from_texts(SAMPLE_DOCS, embeddings, collection_name="compression-demo")
