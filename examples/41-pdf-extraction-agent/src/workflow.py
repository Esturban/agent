from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import CHARS_LIMIT, MAX_RETRIES, ExtractionState, download_pdf_text, extractor


def download(state: ExtractionState) -> dict:
    if state["pdf_text"]:
        return {}
    text = download_pdf_text(state.get("url", ""))
    print(f"  Downloaded {len(text)} chars")
    return {"pdf_text": text[:CHARS_LIMIT]}


def extract(state: ExtractionState) -> dict:
    prompt = (
        f"Extract structured information from this academic paper text:\n\n{state['pdf_text']}\n\n"
        "Fill in: title, year (integer), key_contribution, architecture_name."
    )
    try:
        result = extractor.invoke([HumanMessage(content=prompt)])
        return {"extracted": result.model_dump(), "success": True}
    except Exception as e:
        print(f"  Extraction failed (attempt {state['retries'] + 1}): {e}")
        return {"extracted": {}, "success": False, "retries": state["retries"] + 1}


def should_retry(state: ExtractionState) -> str:
    if state["success"]:
        return END
    return "extract" if state["retries"] < MAX_RETRIES else END


def create_workflow():
    graph = StateGraph(ExtractionState)
    graph.add_node("download", download)
    graph.add_node("extract", extract)
    graph.set_entry_point("download")
    graph.add_edge("download", "extract")
    graph.add_conditional_edges("extract", should_retry, {"extract": "extract", END: END})
    return graph.compile()
