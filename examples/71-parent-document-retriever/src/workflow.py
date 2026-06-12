from typing import TypedDict

from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, StateGraph

from src.tools import CHILD_CHUNK_SIZE, PARENT_CHUNK_SIZE, SAMPLE_DOCS


class ParentDocState(TypedDict):
    question: str
    child_chunks: list[str]
    parent_docs: list[str]
    answer: str


def create_workflow():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

    child_splitter = RecursiveCharacterTextSplitter(chunk_size=CHILD_CHUNK_SIZE, chunk_overlap=10)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=PARENT_CHUNK_SIZE, chunk_overlap=50)

    vectorstore = Chroma(collection_name="parent-doc-children", embedding_function=embeddings)
    docstore = InMemoryStore()

    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=docstore,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )

    docs = [Document(page_content=d) for d in SAMPLE_DOCS]
    retriever.add_documents(docs)

    def retrieve_parent(state: ParentDocState) -> dict:
        parent_docs = retriever.invoke(state["question"])
        child_docs = vectorstore.similarity_search(state["question"], k=4)
        return {
            "parent_docs": [d.page_content for d in parent_docs],
            "child_chunks": [d.page_content for d in child_docs],
        }

    def generate(state: ParentDocState) -> dict:
        context = "\n\n".join(state["parent_docs"])
        prompt = f"Answer using the provided context:\n\nContext:\n{context}\n\nQuestion: {state['question']}"
        answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
        return {"answer": answer}

    graph = StateGraph(ParentDocState)
    graph.add_node("retrieve_parent", retrieve_parent)
    graph.add_node("generate", generate)
    graph.add_edge(START, "retrieve_parent")
    graph.add_edge("retrieve_parent", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
