from operator import add
from typing import Annotated, TypedDict

from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph

from src.tools import DOCS, NUM_VARIANTS, RRF_K, K

# ---------------------------------------------------------------------------
# RAG Fusion — why it exists
#
# A single query is a single point of failure. Different users phrase the same
# question differently, and a query that misses your index's sweet spot returns
# weak or irrelevant documents. RAG Fusion (Lawrence 2024) fixes this by:
#
#   1. Fan-out: generate N query paraphrases in parallel (LangGraph Send API)
#   2. Retrieve top-k for each paraphrase independently
#   3. Merge: Reciprocal Rank Fusion re-ranks the union of all retrieved docs
#      RRF score = sum(1 / (k + rank_i)) across all ranked lists
#   4. Generate from the fused, de-duplicated context
#
# The Send API is the key LangGraph primitive — it lets you dispatch the same
# "retrieve" node N times with different inputs, collect all results into a
# shared state list via Annotated[list, add], then continue to merge.
#
# Follow-on to 22-hybrid-search-rag (ensemble retrieval) and
# 25-adaptive-rag (query-level routing). This is about improving recall
# at the retrieval level, not routing around retrieval.
# ---------------------------------------------------------------------------


class VariantState(TypedDict):
    """State for one parallel retrieval branch."""

    variant: str
    ranked_docs: list[str]


class RAGFusionState(TypedDict):
    question: str
    variants: list[str]
    # Annotated[list, add] merges results from all parallel Send branches
    ranked_docs: Annotated[list[list[str]], add]
    fused_docs: list[str]
    answer: str


def _rrf_merge(all_ranked_lists: list[list[str]], k: int = RRF_K) -> list[str]:
    """Reciprocal Rank Fusion across multiple ranked document lists."""
    scores: dict[str, float] = {}
    for ranked_list in all_ranked_lists:
        for rank, doc in enumerate(ranked_list, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=scores.__getitem__, reverse=True)


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(DOCS, embeddings, collection_name="rag_fusion")
    retriever = vectorstore.as_retriever(search_kwargs={"k": K})

    def generate_variants(state: RAGFusionState) -> dict:
        """LLM generates N semantically diverse paraphrases of the original query."""
        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        f"Generate exactly {NUM_VARIANTS} alternative phrasings of the user's question. "
                        "Each should approach the topic from a slightly different angle. "
                        f"Return only the {NUM_VARIANTS} questions, one per line, no numbering."
                    )
                ),
                HumanMessage(content=state["question"]),
            ]
        )
        raw = response.content.strip().split("\n")
        variants = [q.strip() for q in raw if q.strip()][:NUM_VARIANTS]
        # Always include the original
        if state["question"] not in variants:
            variants = [state["question"]] + variants[: NUM_VARIANTS - 1]
        return {"variants": variants}

    def fan_out(state: RAGFusionState):
        """Dispatch one Send per variant — parallel retrieval via LangGraph Send API."""
        return [
            Send("retrieve_variant", {"variant": v, "ranked_docs": []}) for v in state["variants"]
        ]

    def retrieve_variant(state: VariantState) -> dict:
        """Retrieve top-k for a single query variant. Runs in parallel across all variants."""
        docs = retriever.invoke(state["variant"])
        return {"ranked_docs": [d.page_content for d in docs]}

    def fuse(state: RAGFusionState) -> dict:
        """Apply RRF to merge all parallel ranked lists into one unified context."""
        fused = _rrf_merge(state["ranked_docs"])
        return {"fused_docs": fused}

    def generate(state: RAGFusionState) -> dict:
        context = "\n\n".join(state["fused_docs"])
        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Answer using only the context below. "
                        "The context was retrieved and fused from multiple query paraphrases "
                        "for better recall.\n\nContext:\n" + context
                    )
                ),
                HumanMessage(content=state["question"]),
            ]
        )
        return {"answer": response.content}

    graph = StateGraph(RAGFusionState)
    graph.add_node("generate_variants", generate_variants)
    graph.add_node("retrieve_variant", retrieve_variant)
    graph.add_node("fuse", fuse)
    graph.add_node("generate", generate)

    graph.add_edge(START, "generate_variants")
    graph.add_conditional_edges("generate_variants", fan_out, ["retrieve_variant"])
    graph.add_edge("retrieve_variant", "fuse")
    graph.add_edge("fuse", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
