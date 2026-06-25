from langgraph.graph import StateGraph, END
from typing import TypedDict
from .tools import load_pdf_bytes, pdf_page_to_b64, extract_page


class DocState(TypedDict):
    pdf_source: str
    schema_prompt: str
    page_count: int
    results: list


def load_node(state: DocState, config: dict) -> DocState:
    pdf_bytes = load_pdf_bytes(state["pdf_source"])
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf_bytes)
    return {**state, "_pdf_bytes": pdf_bytes, "page_count": len(doc)}


def extract_node(state: DocState, config: dict) -> DocState:
    client = config["configurable"]["client"]
    model = config["configurable"].get("model", "gpt-4o-mini")
    pdf_bytes = state["_pdf_bytes"]
    results = []
    for i in range(state["page_count"]):
        b64 = pdf_page_to_b64(pdf_bytes, i)
        result = extract_page(b64, state["schema_prompt"], client, model)
        result["page"] = i + 1
        results.append(result)
    return {**state, "results": results}


def create_workflow():
    graph = StateGraph(DocState)
    graph.add_node("load", load_node)
    graph.add_node("extract", extract_node)
    graph.set_entry_point("load")
    graph.add_edge("load", "extract")
    graph.add_edge("extract", END)
    return graph.compile()
