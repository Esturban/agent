from langchain_chroma import Chroma
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings

_DOCS = [
    Document(
        page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs."
    ),
    Document(
        page_content="RAG combines a retriever with a generative model to ground answers in source documents."
    ),
    Document(
        page_content="Self-RAG uses reflection tokens to decide whether retrieval is needed per query."
    ),
    Document(
        page_content="Human-in-the-loop checkpointing pauses graph execution and waits for human approval."
    ),
    Document(
        page_content="Adaptive RAG classifies each query and routes it to the cheapest correct retrieval path."
    ),
]

_store = Chroma.from_documents(_DOCS, OpenAIEmbeddings())
_retriever = _store.as_retriever(search_kwargs={"k": 2})
_duck = DuckDuckGoSearchResults(max_results=3)


@tool
def vectorstore_search(query: str) -> str:
    """Search the internal knowledge base about LangGraph and RAG patterns."""
    docs = _retriever.invoke(query)
    return "\n\n".join(d.page_content for d in docs) or "No results found."


@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo for current information."""
    return _duck.run(query)


@tool
def calculator(expression: str) -> str:
    """Evaluate a Python math expression. Example: '2 ** 10' or '(5 + 3) * 7'."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))  # noqa: S307
    except Exception as e:
        return f"Error: {e}"


def create_tools() -> list:
    return [vectorstore_search, web_search, calculator]
