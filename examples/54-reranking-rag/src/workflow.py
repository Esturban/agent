from typing import TypedDict

from flashrank import Ranker, RerankRequest
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import MAX_RERANK, MAX_RETRIEVE, build_vectorstore


class RerankState(TypedDict):
    query: str
    documents: list[str]
    reranked: list[str]
    answer: str


def create_workflow():
    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    vs = build_vectorstore()
    ranker = Ranker()

    def retrieve(state: RerankState) -> dict:
        docs = vs.similarity_search(state["query"], k=MAX_RETRIEVE)
        return {"documents": [d.page_content for d in docs]}

    def rerank(state: RerankState) -> dict:
        passages = [{"id": i, "text": t} for i, t in enumerate(state["documents"])]
        request = RerankRequest(query=state["query"], passages=passages)
        results = ranker.rerank(request)
        top = [r["text"] for r in results[:MAX_RERANK]]
        return {"reranked": top}

    def generate(state: RerankState) -> dict:
        context = "\n".join(state["reranked"])
        msg = HumanMessage(content=f"Context:\n{context}\n\nQuestion: {state['query']}")
        return {"answer": llm.invoke([msg]).content}

    graph = StateGraph(RerankState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("rerank", rerank)
    graph.add_node("generate", generate)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "rerank")
    graph.add_edge("rerank", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
