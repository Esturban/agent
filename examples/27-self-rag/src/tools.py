from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

DOCUMENTS = [
    Document(
        page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs.",
        metadata={"source": "langgraph-docs"},
    ),
    Document(
        page_content="Self-RAG teaches LLMs to generate reflection tokens that decide when to retrieve.",
        metadata={"source": "self-rag-paper"},
    ),
    Document(
        page_content="Corrective RAG grades retrieved documents and rewrites the query when docs are irrelevant.",
        metadata={"source": "crag-paper"},
    ),
    Document(
        page_content="RAG Fusion generates multiple query variants then merges results via Reciprocal Rank Fusion.",
        metadata={"source": "rag-fusion"},
    ),
    Document(
        page_content="The Eiffel Tower is 330 metres tall and stands in Paris, France.",
        metadata={"source": "general"},
    ),
    Document(
        page_content="Adaptive RAG classifies each query and routes it to the cheapest correct retrieval path.",
        metadata={"source": "adaptive-rag"},
    ),
]


def build_retriever():
    store = Chroma.from_documents(DOCUMENTS, OpenAIEmbeddings())
    return store.as_retriever(search_kwargs={"k": 2})
