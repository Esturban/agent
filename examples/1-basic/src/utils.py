from typing import List
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.tools import tool
from langgraph.graph import StateGraph
import os
from pathlib import Path

# Optional: Graphviz export helpers
try:
    from graphviz import Digraph
    _HAS_GRAPHVIZ = True
except Exception:
    _HAS_GRAPHVIZ = False

@tool
def retrieve_context(query: str) -> str:
    """Search for relevant documents."""
    urls = [
        "https://docs.python.org/3/tutorial/index.html",
        "https://realpython.com/python-basics/",
        "https://www.learnpython.org/",
    ]
    # Loading all of the URLs
    loader = UnstructuredURLLoader(urls=urls)
    docs = loader.load()
    # Splitting the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
    doc_splits = text_splitter.split_documents(docs)

    # Creating the vectorstore with chroma
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="python_docs",
        embedding=OpenAIEmbeddings(),
    )
    retriever = vectorstore.as_retriever()
    results = retriever.invoke(query)
    return "\n".join([doc.page_content for doc in results])


# --- Export the stategraph as an image -------------------------------------------------
def export_stategraph(graph: StateGraph, out_path: str = "examples/1-basic/assets/stategraph.png") -> str:
    """Export a StateGraph (or compiled graph) by calling its mermaid PNG drawer.

    This uses `graph.get_graph().draw_mermaid_png()` when available and writes
    the resulting bytes to `out_path`. Fails fast with clear errors.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Accept either a compiled graph (has get_graph) or a StateGraph (has compile)
    if hasattr(graph, "get_graph"):
        gv = graph.get_graph()
    elif hasattr(graph, "compile"):
        compiled = graph.compile()
        if hasattr(compiled, "get_graph"):
            gv = compiled.get_graph()
        else:
            raise RuntimeError("compiled graph does not expose get_graph()")
    else:
        raise RuntimeError("Provided object has neither get_graph() nor compile()")

    if not hasattr(gv, "draw_mermaid_png"):
        raise RuntimeError("Graph object has no draw_mermaid_png() method")

    png_bytes = gv.draw_mermaid_png()
    if not isinstance(png_bytes, (bytes, bytearray)):
        raise RuntimeError("draw_mermaid_png() did not return bytes")

    out_path.write_bytes(png_bytes)
    return str(out_path)


