from typing import List
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.tools import tool


@tool
def retrieve_context(query: str) -> str:
    """Search for relevant documents."""
    urls = [
        "https://docs.python.org/3/tutorial/index.html",
        "https://realpython.com/python-basics/",
        "https://www.learnpython.org/"
    ]
    #Loading all of the URLs
    loader = UnstructuredURLLoader(urls=urls)
    docs = loader.load()
    #Splitting the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
    doc_splits = text_splitter.split_documents(docs)
    
    # Creating the vectorstore with chroma
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="python_docs",
        embedding=OpenAIEmbeddings(),
    )
    retriever = vectorstore.as_retriever()
    results = retriever.invoke(query)
    return "\n".join([doc.page_content for doc in results])


