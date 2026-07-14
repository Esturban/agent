from typing import TypedDict

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

DOCUMENTS = [
    "LangGraph is a library for building stateful, multi-actor applications with LLMs. It uses a graph-based workflow where nodes are Python functions and edges control flow.",
    "LangChain provides modular components for building LLM applications: chains, agents, retrievers, and output parsers. It integrates with 50+ LLM providers.",
    "RAG (Retrieval-Augmented Generation) improves LLM accuracy by retrieving relevant documents before generation. Key metrics: Faithfulness, AnswerRelevancy, ContextualPrecision.",
    "Vector databases store numerical embeddings for semantic similarity search. Popular options: ChromaDB (local), Pinecone (cloud), Weaviate (self-hosted).",
    "Agents use LLMs as reasoning engines to decide which tools to call and when. ReAct (Reason + Act) is the dominant pattern: think step-by-step, then act.",
    "Checkpointing in LangGraph allows saving and resuming agent state. SqliteSaver persists to disk; MemorySaver keeps state in memory only.",
]

HAND_WRITTEN_GOLDENS = [
    {
        "input": "What is LangGraph used for?",
        "expected_output": "LangGraph is used for building stateful, multi-actor LLM applications using graph-based workflows.",
        "context": [DOCUMENTS[0]],
    },
    {
        "input": "Name two vector databases mentioned.",
        "expected_output": "ChromaDB and Pinecone are mentioned as vector database options.",
        "context": [DOCUMENTS[3]],
    },
]


class RAGState(TypedDict):
    query: str
    context: list[str]
    answer: str


llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0.2)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
