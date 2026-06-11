from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import KNOWLEDGE_BASE, RAGState, embeddings, llm

_vectorstore: Chroma | None = None

ANSWER_PROMPT = """Answer the question using ONLY the provided context. If the context doesn't contain the answer, say "I don't know."

Context:
{context}

Question: {query}

Answer:"""


def build_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma.from_texts(KNOWLEDGE_BASE, embeddings, collection_name="deepeval_demo")
    return _vectorstore


def retrieve(state: RAGState) -> dict:
    vs = build_vectorstore()
    docs = vs.similarity_search(state["query"], k=3)
    context = [d.page_content for d in docs]
    return {"context": context}


def generate(state: RAGState) -> dict:
    context_text = "\n".join(f"- {c}" for c in state["context"])
    prompt = ANSWER_PROMPT.format(context=context_text, query=state["query"])
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"answer": result.content}


def create_workflow():
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
