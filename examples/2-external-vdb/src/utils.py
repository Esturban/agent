from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph
from pathlib import Path

def preprocess_dataset(docs_list):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=700,
        chunk_overlap=50,
        disallowed_special=()
    )
    doc_splits = text_splitter.split_documents(docs_list)
    return doc_splits

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