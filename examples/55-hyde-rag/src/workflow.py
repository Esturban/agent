from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph

from src.tools import build_vectorstore


class HyDEState(TypedDict):
    query: str
    hypothesis: str
    documents: list[str]
    answer: str


HYPOTHESIS_PROMPT = (
    "Write a single-paragraph answer to the following question. "
    "It may contain hypothetical details — accuracy is not required. "
    "The goal is to produce text whose embedding is similar to a real answer."
)


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vs = build_vectorstore()

    def hypothesize(state: HyDEState) -> dict:
        msgs = [SystemMessage(content=HYPOTHESIS_PROMPT), HumanMessage(content=state["query"])]
        return {"hypothesis": llm.invoke(msgs).content}

    def retrieve(state: HyDEState) -> dict:
        hyp_vec = embeddings.embed_query(state["hypothesis"])
        docs = vs.similarity_search_by_vector(hyp_vec, k=3)
        return {"documents": [d.page_content for d in docs]}

    def generate(state: HyDEState) -> dict:
        context = "\n".join(state["documents"])
        msg = HumanMessage(content=f"Context:\n{context}\n\nQuestion: {state['query']}")
        return {"answer": llm.invoke([msg]).content}

    graph = StateGraph(HyDEState)
    graph.add_node("hypothesize", hypothesize)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_edge(START, "hypothesize")
    graph.add_edge("hypothesize", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
