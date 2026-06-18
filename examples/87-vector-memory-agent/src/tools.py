import uuid
import chromadb
from langchain_openai import OpenAIEmbeddings

# text-embedding-3-small: 1536-dim, fast, cheap — good for memory retrieval
_embedder = OpenAIEmbeddings(model="text-embedding-3-small")

# In-memory ChromaDB: no disk, resets each process.
# Swap for chromadb.PersistentClient("./memory_db") for cross-session persistence.
_chroma = chromadb.Client()
COLLECTION = _chroma.get_or_create_collection("agent_memory")

USER_ID = "learner-87"

# Seed conversation that the agent will embed and later retrieve from.
# The magic: the agent doesn't load ALL of these on every query — only the relevant ones.
SEED_TURNS = [
    "User: My name is Alex and I'm a machine learning engineer at a fintech company.",
    "Assistant: Nice to meet you, Alex!",
    "User: I mostly work with PyTorch and transformers. I love the Mamba architecture paper.",
    "Assistant: Great taste in papers! Mamba's selective SSM is elegant.",
    "User: I'm building a real-time speech recognition system as a side project.",
    "Assistant: Whisper + streaming is a popular approach — are you fine-tuning or using it off-the-shelf?",
    "User: I prefer Python over any other language. I hate Java.",
    "Assistant: Noted — Python all the way!",
]


def store_turn(text: str, user_id: str = USER_ID) -> None:
    """Embed and store a conversation turn in the vector memory."""
    embedding = _embedder.embed_query(text)
    COLLECTION.add(
        ids=[str(uuid.uuid4())],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"user_id": user_id}],
    )


def retrieve_relevant(query: str, user_id: str = USER_ID, k: int = 3) -> list[str]:
    """Return the k most semantically relevant stored turns for the query."""
    query_embedding = _embedder.embed_query(query)
    results = COLLECTION.query(
        query_embeddings=[query_embedding],
        n_results=k,
        where={"user_id": user_id},
    )
    # results["documents"] is a list-of-lists (one per query)
    return results["documents"][0] if results["documents"] else []
