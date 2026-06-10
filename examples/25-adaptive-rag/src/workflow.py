from typing import Literal, TypedDict

from langchain_chroma import Chroma
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from src.tools import DOCS

# ---------------------------------------------------------------------------
# Adaptive RAG — why it exists
#
# A single retrieval strategy applied to every query wastes money and hurts quality:
# - Embedding "What is 2+2?" burns tokens for zero gain — the LLM knows this.
# - Asking the LLM alone about "yesterday's stock close" causes hallucination.
# - Running web search on every query is slow and expensive.
#
# An LLM classifier routes each query to the cheapest strategy that works:
#   "simple"      → LLM answers directly (no retrieval cost)
#   "vectorstore" → private KB retrieval (fast, deterministic)
#   "web"         → live DuckDuckGo search (for current events)
#
# Follow-on to 17-corrective-rag, which grades retrieved docs AFTER retrieval.
# This example decides WHETHER to retrieve before the retrieval step.
# ---------------------------------------------------------------------------

Strategy = Literal["simple", "vectorstore", "web"]


class RouteDecision(BaseModel):
    strategy: Strategy
    reasoning: str


class AdaptiveRAGState(TypedDict):
    question: str
    strategy: str
    context: str
    answer: str


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(DOCS, embeddings, collection_name="adaptive_rag")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    search = DuckDuckGoSearchResults(max_results=3)
    classifier = llm.with_structured_output(RouteDecision)

    def classify(state: AdaptiveRAGState) -> dict:
        """Route the query to the appropriate retrieval strategy."""
        decision = classifier.invoke(
            [
                SystemMessage(
                    content=(
                        "Classify this question into one of three retrieval strategies:\n"
                        "- 'simple': general knowledge the LLM knows well (math, history, definitions)\n"
                        "- 'vectorstore': questions about private/internal knowledge (policies, specs, internal docs)\n"
                        "- 'web': questions requiring current or real-time information (news, prices, recent events)\n"
                        "Choose the cheapest strategy that will answer correctly."
                    )
                ),
                HumanMessage(content=state["question"]),
            ]
        )
        return {"strategy": decision.strategy}

    def direct_answer(state: AdaptiveRAGState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(content="Answer the question directly and concisely."),
                HumanMessage(content=state["question"]),
            ]
        )
        return {"context": "none", "answer": response.content}

    def vectorstore_answer(state: AdaptiveRAGState) -> dict:
        docs = retriever.invoke(state["question"])
        context = "\n\n".join(d.page_content for d in docs)
        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Answer using only the context below. "
                        "If the answer is not there, say so.\n\nContext:\n" + context
                    )
                ),
                HumanMessage(content=state["question"]),
            ]
        )
        return {"context": context, "answer": response.content}

    def web_answer(state: AdaptiveRAGState) -> dict:
        results = search.invoke(state["question"])
        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Answer using the web search results below.\n\nResults:\n" + str(results)
                    )
                ),
                HumanMessage(content=state["question"]),
            ]
        )
        return {"context": str(results), "answer": response.content}

    def route(
        state: AdaptiveRAGState,
    ) -> Literal["direct_answer", "vectorstore_answer", "web_answer"]:
        return f"{state['strategy']}_answer"

    graph = StateGraph(AdaptiveRAGState)
    graph.add_node("classify", classify)
    graph.add_node("direct_answer", direct_answer)
    graph.add_node("vectorstore_answer", vectorstore_answer)
    graph.add_node("web_answer", web_answer)

    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify",
        route,
        {
            "direct_answer": "direct_answer",
            "vectorstore_answer": "vectorstore_answer",
            "web_answer": "web_answer",
        },
    )
    graph.add_edge("direct_answer", END)
    graph.add_edge("vectorstore_answer", END)
    graph.add_edge("web_answer", END)
    return graph.compile()
