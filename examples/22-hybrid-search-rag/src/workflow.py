from typing import TypedDict

from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph

from src.tools import DOCS, K


class HybridRAGState(TypedDict):
    question: str
    documents: list   # list[str] — retrieved doc contents
    answer: str


def create_workflow():
    """
    Build a two-node RAG graph backed by EnsembleRetriever.

    Why hybrid?
    - BM25 (Robertson & Walker, 1994) is the standard for exact keyword matching.
      It powers Elasticsearch, Lucene, and Google's initial retrieval stage.
      Excels on precise terms: model numbers, names, identifiers.
    - Vector search captures semantic intent — handles paraphrases and concept queries.
    - Together, they cover each other's blind spots. The weights=[0.5, 0.5] split
      can be tuned per domain; keyword-heavy corpora benefit from higher BM25 weight.
    """
    llm = ChatOpenAI(model="gpt-5-nano")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    bm25_retriever = BM25Retriever.from_texts(DOCS)
    bm25_retriever.k = K

    vectorstore = Chroma.from_texts(DOCS, embeddings, collection_name="hybrid_rag")
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": K})

    # Reciprocal Rank Fusion merges the two ranked lists —
    # a document appearing in both gets a strong combined score.
    ensemble = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5],
    )

    def retrieve(state: HybridRAGState) -> dict:
        docs = ensemble.invoke(state["question"])
        return {"documents": [d.page_content for d in docs]}

    def generate(state: HybridRAGState) -> dict:
        context = "\n\n".join(state["documents"])
        response = llm.invoke([
            SystemMessage(content=(
                "Answer using only the context below. "
                "If the answer is not in the context, say 'I don't have that information.'\n\n"
                f"Context:\n{context}"
            )),
            HumanMessage(content=state["question"]),
        ])
        return {"answer": response.content}

    graph = StateGraph(HybridRAGState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
