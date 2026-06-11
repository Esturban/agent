from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.documents import Document

SAMPLE_DOCS = [
    Document(
        page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain with the ability to coordinate multiple chains in a graph of nodes and edges, supporting cycles, branching, and checkpointing."
    ),
    Document(
        page_content="Corrective RAG (CRAG) improves retrieval by grading each retrieved document for relevance. Irrelevant documents trigger a query rewrite followed by a web search, replacing low-quality local context with fresh information."
    ),
    Document(
        page_content="RAG (Retrieval Augmented Generation) grounds LLM responses in a knowledge base. A retriever fetches relevant documents; those documents become the context an LLM uses to generate a factual, sourced answer."
    ),
    Document(
        page_content="LangGraph StateGraph lets you define typed state, add nodes as Python functions, and wire them with edges and conditional edges. The compiled graph handles state transitions, streaming, and optional persistence via checkpointers."
    ),
    Document(
        page_content="ChromaDB is an open-source embedding database. LangChain's Chroma integration stores document embeddings locally and supports cosine-similarity retrieval via the as_retriever() interface."
    ),
]

web_search = DuckDuckGoSearchResults(max_results=3)
