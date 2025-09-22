import os
import json
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from time import time
from langchain.tools import tool
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import HuggingFaceDatasetLoader
from langchain_community.tools import BraveSearch
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState
from langgraph.graph.message import add_messages

from qdrant_client import QdrantClient

from qdrant_client.http.models import VectorParams
from src.utils import preprocess_dataset
from src.checksum import compute_checksum
from src.dedup import missing_documents_by_checksum


#Load the environment variables
load_dotenv()
qdrant_key = os.getenv("QDRANT_KEY")
qdrant_url = os.getenv("QDRANT_URL")
brave_key = os.getenv("BRAVE_API_KEY")
start_time = time()
#Let's load the text from a predefined dataset in HuggingFace
hugging_face_doc = HuggingFaceDatasetLoader("m-ric/huggingface_doc","text")
transformers_doc = HuggingFaceDatasetLoader("m-ric/transformers_documentation_en","text")

end_time = time()
print(f"Time taken to load the documents: {end_time - start_time:.2f} seconds")

start_time = time()
#Split the documents into chunks for embeddings
#Complete set of documents taken from the hugging face documentation
# number_of_docs = len(hugging_face_doc.load())
number_of_docs = 40
hf_splits = preprocess_dataset(hugging_face_doc.load()[:number_of_docs])
#Complete set of documents taken from the transformers documentation
# number_of_docs = len(transformers_doc.load())
transformer_splits = preprocess_dataset(transformers_doc.load()[:number_of_docs])
end_time = time()
print(f"Time taken to preprocess the documents: {end_time - start_time:.2f} seconds")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
#A way to quickly make a retriever for a specific datastore
def create_retriever(collection_name, doc_splits):
    "Definition of the retriever, for a specific datastore"

    # Prepare docs for dedup check: extract content and keep original mapping
    docs_for_check = []
    for d in doc_splits:
        content = getattr(d, "page_content", None) or getattr(d, "content", None) or str(d)
        docs_for_check.append({"content": content})

    # Ask the dedup helper which original docs are missing in the collection
    # Create client with increased timeout to tolerate larger writes
    client = QdrantClient(url=qdrant_url, api_key=qdrant_key, timeout=60)
    try:
        missing_docs = missing_documents_by_checksum(client, collection_name, doc_splits, compute_checksum)
    except Exception:
        # If metadata lookup fails, fall back to indexing all documents (best-effort)
        missing_docs = list(doc_splits)

    # Attach checksum/doc_id metadata to missing docs
    for d in missing_docs:
        content = getattr(d, "page_content", None) or getattr(d, "content", None) or str(d)
        cs = compute_checksum(content or "")
        try:
            if hasattr(d, "metadata"):
                d.metadata = {**getattr(d, "metadata", {}), "content_checksum": cs, "doc_id": cs}
            else:
                d.metadata = {"content_checksum": cs, "doc_id": cs}
        except Exception:
            # immutable or unexpected object - ignore metadata attach
            pass

    # Only index missing documents to avoid re-writing existing points
    docs_to_index = missing_docs

    # Try to index missing docs with retries to handle transient write timeouts
    vectorstore = None
    if docs_to_index:
        import time as _time
        attempts = 3
        backoff = 1.0
        for attempt in range(1, attempts + 1):
            try:
                # Diagnostic logging before attempting upsert
                total_bytes = sum(len((getattr(d, "page_content", None) or getattr(d, "content", None) or str(d)).encode("utf-8")) for d in docs_to_index)
                sample_checksums = [getattr(d, "metadata", {}).get("content_checksum") or compute_checksum(getattr(d, "page_content", None) or getattr(d, "content", None) or str(d)) for d in docs_to_index[:10]]
                batch_size = 64
                print(f"Indexing {len(docs_to_index)} docs (est {total_bytes} bytes), sample checksums: {sample_checksums}, batch_size={batch_size}")

                vectorstore = QdrantVectorStore.from_documents(
                    docs_to_index,
                    OpenAIEmbeddings(model="text-embedding-3-small"),
                    url=qdrant_url,
                    api_key=qdrant_key,
                    collection_name=collection_name,
                    batch_size=batch_size,
                )
                break
            except Exception as e:
                # Log and retry with backoff
                print(f"Attempt {attempt} failed to upsert {len(docs_to_index)} docs: {e}")
                if attempt == attempts:
                    raise
                _time.sleep(backoff)
                backoff *= 2
    else:
        # No new docs to index; create a lightweight vectorstore wrapper
        vectorstore = QdrantVectorStore.from_documents(
            [],
            OpenAIEmbeddings(model="text-embedding-3-small"),
            url=qdrant_url,
            api_key=qdrant_key,
            collection_name=collection_name,
            batch_size=1,
        )

    return vectorstore.as_retriever()

start_time = time()
hf_retriever = create_retriever("hugging_face_documentation", hf_splits)
transformer_retriever = create_retriever("transformer_documentation", transformer_splits)
end_time = time()
print(f"Time taken to create the retrievers: {end_time - start_time:.2f} seconds")


@tool("retriever_hugging_face_documentation", description="Search and return information about hugging face documentation; returns concatenated page contents.")
def hf_retriever_tool(query: str) -> str:
    docs = hf_retriever.get_relevant_documents(query)
    return "\n".join([getattr(d, "page_content", "") for d in docs])


@tool("retriever_transformer", description="Search and return information specifically about transformers library; returns concatenated page contents.")
def transformer_retriever_tool(query: str) -> str:
    docs = transformer_retriever.get_relevant_documents(query)
    return "\n".join([getattr(d, "page_content", "") for d in docs])
@tool("web_search_tool")
def search_tool(query):
    """
    Search the web for the most relevant information about the query.
    """
    search = BraveSearch.from_api_key(api_key=brave_key, search_kwargs={"count": 3})
    return search.run(query)

tools = [hf_retriever_tool, transformer_retriever_tool, search_tool]
end_time = time()
print(f"Time taken to create the tools: {end_time - start_time} seconds")

tool_node = ToolNode(tools=tools)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

llm_with_tools = llm.bind_tools(tools)