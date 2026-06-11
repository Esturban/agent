from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import DOCUMENTS, RAGState, embeddings, llm

_vectorstore = None

ANSWER_PROMPT = """Answer using ONLY the context below. If insufficient, say "I don't know."

Context:
{context}

Question: {query}"""


def build_vectorstore(k: int = 3) -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma.from_texts(DOCUMENTS, embeddings, collection_name="synthesizer_demo")
    return _vectorstore


def retrieve(state: RAGState, k: int = 3) -> dict:
    vs = build_vectorstore()
    docs = vs.similarity_search(state["query"], k=k)
    return {"context": [d.page_content for d in docs]}


def generate(state: RAGState) -> dict:
    context_text = "\n".join(f"- {c}" for c in state["context"])
    result = llm.invoke([HumanMessage(content=ANSWER_PROMPT.format(context=context_text, query=state["query"]))])
    return {"answer": result.content}


def create_workflow(k: int = 3):
    """k controls retrieval depth — change to simulate pipeline degradation."""
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", lambda s: retrieve(s, k=k))
    graph.add_node("generate", generate)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
