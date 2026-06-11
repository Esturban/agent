import os

from dotenv import load_dotenv
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_redis import RedisVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]


def doc_retriever(
    urls=urls,
    chunk_size=2048,
    chunk_overlap=256,
    vs="rag-redis",
    tool_name="retrieve_blog_posts",
    tool_description="Search and return information about Lilian Weng blog posts on LLM agents, prompt engineering, and adversarial attacks on LLMs.",
    debug=None,
    **search_kwargs,
):
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    # Chunk the documents to provide some overlap and complete sections
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    doc_splits = text_splitter.split_documents(docs_list)
    if debug:
        print(f"Number of chunks: {len(doc_splits)}")
        for i, chunk in enumerate(doc_splits[:3]):  # Check first few chunks
            print(f"Chunk {i}: {chunk.page_content[:200]}...")
    # Add to document chunks to Redis
    vectorstore = RedisVectorStore.from_documents(
        doc_splits, OpenAIEmbeddings(), redis_url=REDIS_URL, index_name=vs
    )
    # get RedisVectorStore as a retriever
    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)

    retriever_tool = create_retriever_tool(
        retriever,
        tool_name,
        tool_description,
    )
    return retriever_tool
