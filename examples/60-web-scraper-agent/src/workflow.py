from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import TOP_K, build_vectorstore, chunk_text, fetch_page, parse_html


class WebScraperState(TypedDict):
    url: str
    question: str
    raw_html: str
    text: str
    chunks: list[str]
    context: list[str]
    answer: str


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

    def fetch(state: WebScraperState) -> dict:
        return {"raw_html": fetch_page(state["url"])}

    def parse(state: WebScraperState) -> dict:
        text = parse_html(state["raw_html"])
        chunks = chunk_text(text)
        return {"text": text, "chunks": chunks}

    def index_and_retrieve(state: WebScraperState) -> dict:
        vs = build_vectorstore(state["chunks"])
        docs = vs.similarity_search(state["question"], k=TOP_K)
        return {"context": [d.page_content for d in docs]}

    def answer(state: WebScraperState) -> dict:
        context = "\n\n".join(state["context"])
        prompt = f"Use this context to answer the question.\n\nContext:\n{context}\n\nQuestion: {state['question']}"
        return {"answer": llm.invoke([HumanMessage(content=prompt)]).content.strip()}

    graph = StateGraph(WebScraperState)
    graph.add_node("fetch", fetch)
    graph.add_node("parse", parse)
    graph.add_node("index_and_retrieve", index_and_retrieve)
    graph.add_node("answer", answer)
    graph.add_edge(START, "fetch")
    graph.add_edge("fetch", "parse")
    graph.add_edge("parse", "index_and_retrieve")
    graph.add_edge("index_and_retrieve", "answer")
    graph.add_edge("answer", END)
    return graph.compile()
