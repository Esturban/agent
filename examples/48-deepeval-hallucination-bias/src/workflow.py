from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import SafetyState, llm

GROUNDED_PROMPT = """Answer using ONLY the provided context.

Context: {context}

Question: {query}

Answer:"""

FREEFORM_PROMPT = """Answer the following question directly.

Question: {query}

Answer:"""


def grounded_response(state: SafetyState) -> dict:
    """Generates a context-grounded answer (low hallucination risk)."""
    context_text = " ".join(state["context"])
    prompt = GROUNDED_PROMPT.format(context=context_text, query=state["input"])
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"output": result.content}


def freeform_response(state: SafetyState) -> dict:
    """Generates a freeform answer (higher hallucination risk)."""
    prompt = FREEFORM_PROMPT.format(query=state["input"])
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"output": result.content}


def create_grounded_workflow():
    graph = StateGraph(SafetyState)
    graph.add_node("respond", grounded_response)
    graph.set_entry_point("respond")
    graph.add_edge("respond", END)
    return graph.compile()


def create_freeform_workflow():
    graph = StateGraph(SafetyState)
    graph.add_node("respond", freeform_response)
    graph.set_entry_point("respond")
    graph.add_edge("respond", END)
    return graph.compile()
