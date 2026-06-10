from langchain_core.documents import Document

# Knowledge base — RAG Fusion retrieves from this corpus for every query variant
DOCS = [
    Document(page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs using graph-based workflows."),
    Document(page_content="LangChain provides tools for building LLM applications including chains, agents, and retrieval systems."),
    Document(page_content="Vector databases store embeddings for semantic search. Popular options include Chroma, Pinecone, and Weaviate."),
    Document(page_content="Retrieval Augmented Generation (RAG) grounds LLM responses in external documents to reduce hallucination."),
    Document(page_content="Reciprocal Rank Fusion (RRF) merges ranked lists by summing inverse ranks: score = 1/(k + rank). Lower rank = higher score."),
    Document(page_content="The LangGraph Send API allows parallel node execution by sending the same event to multiple workers simultaneously."),
    Document(page_content="Query expansion generates multiple paraphrases of a question to improve recall across different embedding representations."),
    Document(page_content="BM25 is a keyword-based retrieval algorithm that ranks documents by term frequency and inverse document frequency."),
    Document(page_content="Hybrid search combines vector similarity and BM25 keyword search, merging results with ensemble or RRF methods."),
    Document(page_content="Self-RAG grades retrieved documents for relevance and generates reflection tokens to decide when to retrieve."),
]

# Each demonstrates a different angle on the same underlying question
SAMPLE_QUESTIONS = [
    "How does RAG Fusion work?",
    "What is the LangGraph Send API used for?",
    "Explain Reciprocal Rank Fusion for combining search results",
]

NUM_VARIANTS = 4  # number of query paraphrases to fan out
K = 3             # top-k documents per variant retrieval
RRF_K = 60        # RRF constant (standard value from Lawrence 2024)
