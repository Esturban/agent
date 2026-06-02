from typing import TypedDict, Literal

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, StateGraph

from src.tools import SAMPLE_DOCS, web_search


class RAGState(TypedDict):
    question: str
    context: str
    answer: str


def create_workflow():
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(SAMPLE_DOCS)
    vectorstore = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), collection_name="streaming-rag"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model="gpt-5-nano")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the question using only the context below.\n\nContext:\n{context}"),
        ("human", "{question}"),
    ])

    def retrieve(state: RAGState) -> dict:
        docs = retriever.invoke(state["question"])
        return {"context": "\n\n".join(d.page_content for d in docs)}

    def web_fallback(state: RAGState) -> dict:
        results = web_search.invoke(state["question"])
        return {"context": str(results)}

    def should_use_web(state: RAGState) -> Literal["web_fallback", "generate"]:
        return "web_fallback" if len(state["context"]) < 50 else "generate"

    def generate(state: RAGState) -> dict:
        response = (prompt | llm).invoke(
            {"context": state["context"], "question": state["question"]}
        )
        return {"answer": response.content}

    graph = StateGraph(RAGState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("web_fallback", web_fallback)
    graph.add_node("generate", generate)
    graph.add_edge(START, "retrieve")
    graph.add_conditional_edges("retrieve", should_use_web)
    graph.add_edge("web_fallback", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
