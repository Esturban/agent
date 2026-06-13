from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

MODEL = "gpt-5-nano"

# Inline knowledge base for the RAG pipeline under evaluation
DOCS = [
    Document(page_content="LangGraph is a library for building stateful multi-actor applications with LLMs."),
    Document(page_content="RAGAS evaluates RAG pipelines on faithfulness, answer relevancy, and context recall."),
    Document(page_content="ChromaDB is an open-source embedding database for AI applications."),
    Document(page_content="Retrieval-augmented generation combines vector search with language model generation."),
    Document(page_content="LangSmith provides tracing and evaluation for LangChain and LangGraph applications."),
]

# 5-row QA dataset: question, ground_truth, contexts are pre-loaded
QA_ROWS = [
    {
        "question": "What is LangGraph?",
        "ground_truth": "LangGraph is a library for building stateful multi-actor applications with LLMs.",
        "contexts": ["LangGraph is a library for building stateful multi-actor applications with LLMs."],
    },
    {
        "question": "What does RAGAS evaluate?",
        "ground_truth": "RAGAS evaluates RAG pipelines on faithfulness, answer relevancy, and context recall.",
        "contexts": ["RAGAS evaluates RAG pipelines on faithfulness, answer relevancy, and context recall."],
    },
    {
        "question": "What is ChromaDB?",
        "ground_truth": "ChromaDB is an open-source embedding database for AI applications.",
        "contexts": ["ChromaDB is an open-source embedding database for AI applications."],
    },
    {
        "question": "What is retrieval-augmented generation?",
        "ground_truth": "RAG combines vector search with language model generation.",
        "contexts": ["Retrieval-augmented generation combines vector search with language model generation."],
    },
    {
        "question": "What is LangSmith used for?",
        "ground_truth": "LangSmith provides tracing and evaluation for LangChain applications.",
        "contexts": ["LangSmith provides tracing and evaluation for LangChain and LangGraph applications."],
    },
]


def build_rag_chain():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(DOCS, embeddings, collection_name="ragas-eval")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    llm = ChatOpenAI(model=MODEL, temperature=0)
    return retriever, llm
