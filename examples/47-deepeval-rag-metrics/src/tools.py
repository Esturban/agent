from typing import TypedDict
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

KNOWLEDGE_BASE = [
    "LangGraph is a library for building stateful, multi-actor applications with LLMs using graph-based workflows.",
    "LangChain provides tools for building LLM applications, including chains, agents, and retrieval systems.",
    "RAG (Retrieval-Augmented Generation) combines vector search with LLM generation to reduce hallucinations.",
    "ChromaDB is an open-source vector database for storing and retrieving embeddings at local scale.",
    "Embeddings are dense numerical representations of text that capture semantic meaning.",
    "FAISS is Facebook's library for efficient similarity search over large vector datasets.",
    "Faithfulness measures whether an LLM answer is grounded in the retrieved context (no hallucinations).",
    "Answer Relevancy measures whether the answer actually addresses the user's question.",
    "Contextual Precision measures whether the retrieved chunks that appear earlier are more relevant than later ones.",
    "Contextual Recall measures how much of the expected answer is covered by the retrieved context.",
]

GOLDEN_DATASET = [
    {
        "input": "What is LangGraph?",
        "expected_output": "LangGraph is a library for building stateful, multi-actor LLM applications using graph-based workflows.",
        "context": ["LangGraph is a library for building stateful, multi-actor applications with LLMs using graph-based workflows."],
    },
    {
        "input": "What does Faithfulness measure?",
        "expected_output": "Faithfulness measures whether the LLM answer is grounded in the retrieved context, preventing hallucinations.",
        "context": ["Faithfulness measures whether an LLM answer is grounded in the retrieved context (no hallucinations)."],
    },
    {
        "input": "What is ChromaDB used for?",
        "expected_output": "ChromaDB is an open-source vector database for storing and querying embeddings locally.",
        "context": ["ChromaDB is an open-source vector database for storing and retrieving embeddings at local scale."],
    },
]

HALLUCINATED_ANSWERS = [
    "LangGraph is a cloud service by OpenAI that costs $99/month.",
    "Faithfulness measures the length of the answer in words.",
    "ChromaDB requires a PostgreSQL database to function.",
]


class RAGState(TypedDict):
    query: str
    context: list[str]
    answer: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
