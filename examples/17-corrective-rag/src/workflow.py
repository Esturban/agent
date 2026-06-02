from typing import Literal, TypedDict

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from src.tools import SAMPLE_DOCS, web_search


class GradeDocuments(BaseModel):
    score: Literal["yes", "no"]


class CRAGState(TypedDict):
    question: str
    documents: list
    generation: str
    web_search: bool


def create_workflow():
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(SAMPLE_DOCS)
    vectorstore = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), collection_name="crag-17"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    grader = llm.with_structured_output(GradeDocuments)

    grade_prompt = ChatPromptTemplate.from_messages([
        ("system", "Is this document relevant to the question? Reply 'yes' or 'no' only."),
        ("human", "Question: {question}\n\nDocument:\n{document}"),
    ])
    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer using only the context below. Be concise.\n\nContext:\n{context}"),
        ("human", "{question}"),
    ])
    rewrite_prompt = ChatPromptTemplate.from_messages([
        ("system", "Rewrite the question to make it more specific and searchable."),
        ("human", "{question}"),
    ])

    def retrieve(state: CRAGState) -> dict:
        docs = retriever.invoke(state["question"])
        return {"documents": docs, "web_search": False}

    def grade_documents(state: CRAGState) -> dict:
        relevant, needs_web = [], False
        for doc in state["documents"]:
            result = (grade_prompt | grader).invoke({
                "question": state["question"],
                "document": doc.page_content,
            })
            if result.score == "yes":
                relevant.append(doc)
            else:
                needs_web = True
        return {"documents": relevant, "web_search": needs_web}

    def transform_query(state: CRAGState) -> dict:
        rewritten = (rewrite_prompt | llm).invoke({"question": state["question"]})
        return {"question": rewritten.content}

    def web_search_node(state: CRAGState) -> dict:
        results = web_search.invoke(state["question"])
        web_docs = [Document(page_content=str(results))]
        return {"documents": state["documents"] + web_docs}

    def generate(state: CRAGState) -> dict:
        context = "\n\n".join(d.page_content for d in state["documents"])
        response = (answer_prompt | llm).invoke({
            "context": context,
            "question": state["question"],
        })
        return {"generation": response.content}

    def decide_after_grading(state: CRAGState) -> Literal["transform_query", "generate"]:
        return "transform_query" if state["web_search"] else "generate"

    graph = StateGraph(CRAGState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("grade_documents", grade_documents)
    graph.add_node("transform_query", transform_query)
    graph.add_node("web_search_node", web_search_node)
    graph.add_node("generate", generate)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "grade_documents")
    graph.add_conditional_edges("grade_documents", decide_after_grading)
    graph.add_edge("transform_query", "web_search_node")
    graph.add_edge("web_search_node", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
