from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph

from src.tools import build_route_embeddings, find_best_route

HANDLER_PROMPTS = {
    "code": "You are a coding assistant. Answer this programming question concisely:\n{query}",
    "billing": "You are a billing support agent. Answer this account/payment question:\n{query}",
    "general": "You are a general support agent. Answer this question:\n{query}",
}


class SemanticRouterState(TypedDict):
    query: str
    route: str
    scores: dict
    answer: str


def create_workflow():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    route_vecs = build_route_embeddings(embeddings)

    def route_query(state: SemanticRouterState) -> dict:
        query_vec = embeddings.embed_query(state["query"])
        best_route, scores = find_best_route(query_vec, route_vecs)
        return {"route": best_route, "scores": scores}

    def handle(state: SemanticRouterState) -> dict:
        prompt = HANDLER_PROMPTS[state["route"]].format(query=state["query"])
        answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
        return {"answer": answer}

    graph = StateGraph(SemanticRouterState)
    graph.add_node("route_query", route_query)
    graph.add_node("handle", handle)
    graph.add_edge(START, "route_query")
    graph.add_edge("route_query", "handle")
    graph.add_edge("handle", END)
    return graph.compile()
