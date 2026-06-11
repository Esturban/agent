from typing import Annotated, TypedDict

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# ── Inline knowledge base (replaces external documents) ───────────────────────
DOCS = [
    "LangGraph was created by LangChain Inc. and released in January 2024.",
    "LangGraph is built on top of LangChain and uses its message and tool abstractions.",
    "LangGraph supports human-in-the-loop workflows via interrupt() and Command(resume=...).",
    "LangGraph StateGraph compiles into a runnable that can be invoked or streamed.",
    "LangChain was founded by Harrison Chase in 2022 and raised a Series A in 2023.",
    "MemorySaver is a built-in LangGraph checkpointer that stores state in memory.",
    "LangGraph supports parallel execution using the Send API for map-reduce patterns.",
    "The LangGraph prebuilt create_react_agent handles the ReAct loop automatically.",
    "LangChain's LCEL (LangChain Expression Language) uses the | pipe operator for chains.",
    "LangGraph graphs can have conditional edges that route based on node return values.",
]

SAMPLE_QUERIES = [
    "When was LangGraph released and who made it?",
    "How does LangGraph handle human-in-the-loop workflows?",
]

DRAFT_SYSTEM = (
    "You are a knowledgeable AI assistant. Answer the question in 3-4 sentences "
    "using your training knowledge. Be specific and factual."
)

CLAIM_SYSTEM = (
    "Extract the distinct factual claims from the given answer as a numbered list. "
    "Each claim should be a single checkable fact. Output ONLY the numbered list."
)

SUPPORT_SYSTEM = (
    "You are a fact-checker. Given a claim and retrieved context, determine if the "
    "context SUPPORTS, CONTRADICTS, or is UNRELATED to the claim. "
    "Reply with exactly one word: SUPPORTED, CONTRADICTED, or UNRELATED."
)

REVISE_SYSTEM = (
    "You are a precise editor. Given an original answer and verified evidence, "
    "revise ONLY the parts that are unsupported or contradicted. "
    "Keep well-supported parts unchanged. Return the full revised answer."
)


class SpeculativeState(TypedDict):
    query: str
    draft: str
    claims: list[str]
    evidence: list[str]         # retrieved doc per claim
    support_labels: list[str]   # SUPPORTED / CONTRADICTED / UNRELATED
    revised: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def build_vectorstore() -> Chroma:
    from langchain_core.documents import Document
    docs = [Document(page_content=d) for d in DOCS]
    return Chroma.from_documents(docs, embeddings)
