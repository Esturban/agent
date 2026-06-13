from typing import TypedDict

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import TOP_K, build_vectorstore


class CompressionState(TypedDict):
    query: str
    raw_docs: list[str]
    compressed: list[str]
    answer: str


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    vs = build_vectorstore()
    base_retriever = vs.as_retriever(search_kwargs={"k": TOP_K})
    compressor = LLMChainFilter.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever,
    )

    def retrieve(state: CompressionState) -> dict:
        docs = base_retriever.invoke(state["query"])
        return {"raw_docs": [d.page_content for d in docs]}

    def compress(state: CompressionState) -> dict:
        docs = compression_retriever.invoke(state["query"])
        return {"compressed": [d.page_content for d in docs]}

    def generate(state: CompressionState) -> dict:
        context = "\n".join(state["compressed"]) if state["compressed"] else "No relevant context found."
        msg = HumanMessage(content=f"Context:\n{context}\n\nQuestion: {state['query']}")
        return {"answer": llm.invoke([msg]).content}

    graph = StateGraph(CompressionState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("compress", compress)
    graph.add_node("generate", generate)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "compress")
    graph.add_edge("compress", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
