from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

DOCUMENTS = [
    Document(
        page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs, built on top of LangChain.",
        metadata={"source": "langgraph-docs"},
    ),
    Document(
        page_content="RAG (Retrieval-Augmented Generation) combines a retriever with a generative model to ground answers in source documents.",
        metadata={"source": "rag-overview"},
    ),
    Document(
        page_content="Corrective RAG grades each retrieved document for relevance and rewrites the query if any documents score irrelevant.",
        metadata={"source": "crag-paper"},
    ),
    Document(
        page_content="Self-RAG generates reflection tokens to decide whether retrieval is needed before fetching any documents.",
        metadata={"source": "self-rag-paper"},
    ),
    Document(
        page_content="Human-in-the-loop checkpointing pauses graph execution at an interrupt node and waits for human approval before resuming.",
        metadata={"source": "hitl-docs"},
    ),
]


def build_rag_chain():
    store = Chroma.from_documents(DOCUMENTS, OpenAIEmbeddings())
    retriever = store.as_retriever(search_kwargs={"k": 2})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Answer using only the provided context. Be concise."),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ]
    )

    def run(question: str) -> str:
        docs = retriever.invoke(question)
        ctx = "\n\n".join(d.page_content for d in docs)
        return (prompt | llm | StrOutputParser()).invoke(
            {"context": ctx, "question": question}
        )

    return run
