from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from .tools import (
    CLAIM_SYSTEM,
    DRAFT_SYSTEM,
    REVISE_SYSTEM,
    SUPPORT_SYSTEM,
    SpeculativeState,
    build_vectorstore,
    llm,
)

_retriever = None


def _get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = build_vectorstore().as_retriever(search_kwargs={"k": 2})
    return _retriever


def draft(state: SpeculativeState) -> dict:
    """Generate an answer directly from LLM training knowledge — no retrieval."""
    result = llm.invoke([SystemMessage(DRAFT_SYSTEM), HumanMessage(state["query"])])
    return {"draft": result.content, "claims": [], "evidence": [], "support_labels": []}


def extract_claims(state: SpeculativeState) -> dict:
    """Parse the draft into individual checkable facts."""
    result = llm.invoke([
        SystemMessage(CLAIM_SYSTEM),
        HumanMessage(f"Answer to fact-check:\n{state['draft']}"),
    ])
    lines = [l.strip() for l in result.content.strip().split("\n") if l.strip()]
    claims = [l.split(". ", 1)[-1] if l[0].isdigit() else l for l in lines]
    return {"claims": claims}


def retrieve_and_grade(state: SpeculativeState) -> dict:
    """Retrieve evidence for each claim and label it SUPPORTED/CONTRADICTED/UNRELATED."""
    retriever = _get_retriever()
    evidence, labels = [], []
    for claim in state["claims"]:
        docs = retriever.invoke(claim)
        context = "\n".join(d.page_content for d in docs)
        label = llm.invoke([
            SystemMessage(SUPPORT_SYSTEM),
            HumanMessage(f"Claim: {claim}\n\nContext:\n{context}"),
        ])
        evidence.append(context)
        labels.append(label.content.strip().upper())
    return {"evidence": evidence, "support_labels": labels}


def needs_revision(state: SpeculativeState) -> str:
    unsupported = [l for l in state["support_labels"] if l != "SUPPORTED"]
    print(f"  Labels: {state['support_labels']} — {'revising' if unsupported else 'no revision needed'}")
    return "revise" if unsupported else "end"


def revise(state: SpeculativeState) -> dict:
    """Rewrite only the unsupported parts of the draft using retrieved evidence."""
    evidence_block = "\n\n".join(
        f"Claim: {c}\nStatus: {l}\nEvidence: {e}"
        for c, l, e in zip(state["claims"], state["support_labels"], state["evidence"])
    )
    result = llm.invoke([
        SystemMessage(REVISE_SYSTEM),
        HumanMessage(f"Original answer:\n{state['draft']}\n\nFact-check results:\n{evidence_block}"),
    ])
    return {"revised": result.content}


def create_workflow():
    graph = StateGraph(SpeculativeState)
    graph.add_node("draft", draft)
    graph.add_node("extract_claims", extract_claims)
    graph.add_node("retrieve_and_grade", retrieve_and_grade)
    graph.add_node("revise", revise)

    graph.set_entry_point("draft")
    graph.add_edge("draft", "extract_claims")
    graph.add_edge("extract_claims", "retrieve_and_grade")
    graph.add_conditional_edges(
        "retrieve_and_grade", needs_revision, {"revise": "revise", "end": END}
    )
    graph.add_edge("revise", END)
    return graph.compile()
