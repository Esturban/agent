import json
from typing import TypedDict

import networkx as nx
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from src.tools import DOCS, TOP_K

# ---------------------------------------------------------------------------
# Graph RAG — why it exists
#
# Vector search retrieves documents SIMILAR to a query. It finds "documents
# about LangGraph" — but answering "who founded the company that makes
# LangGraph?" requires connecting: LangGraph -> LangChain -> Harrison Chase
# across two documents. That multi-hop path is invisible to similarity search.
#
# Graph RAG extracts entities and relationships into a NetworkX graph.
# At query time, we find the query's entities, collect their graph neighbours,
# and feed the connected subgraph as context — capturing relational facts that
# pure vector retrieval misses.
# ---------------------------------------------------------------------------


class Triple(BaseModel):
    subject: str
    predicate: str
    object: str


class Triples(BaseModel):
    triples: list[Triple]


class GraphRAGState(TypedDict):
    question: str
    entities: list    # list[str] — entities found in the question
    context: str      # subgraph text assembled for the LLM
    answer: str


def _extract_triples(llm: ChatOpenAI, doc: str) -> list[Triple]:
    """Extract (subject, predicate, object) triples from a document."""
    extractor = llm.with_structured_output(Triples)
    result = extractor.invoke([
        SystemMessage(content=(
            "Extract factual (subject, predicate, object) triples from the text. "
            "Use short, canonical names for entities (e.g. 'LangChain', not 'the LangChain framework'). "
            "Return only triples clearly stated in the text."
        )),
        HumanMessage(content=doc),
    ])
    return result.triples


def _build_graph(llm: ChatOpenAI) -> nx.DiGraph:
    """Build a directed knowledge graph by extracting triples from all docs."""
    G = nx.DiGraph()
    for doc in DOCS:
        triples = _extract_triples(llm, doc)
        for t in triples:
            G.add_edge(t.subject, t.object, predicate=t.predicate, source=doc)
    return G


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano")

    print("Building knowledge graph from docs...")
    G = _build_graph(llm)
    print(f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    class EntityMatch(BaseModel):
        entities: list[str]

    def find_entities(state: GraphRAGState) -> dict:
        """Extract entities from the question that may appear in the graph."""
        matcher = llm.with_structured_output(EntityMatch)
        result = matcher.invoke([
            SystemMessage(content=(
                f"Extract the key named entities from this question. "
                f"Match them to names in this list where possible: {list(G.nodes())}. "
                "Return canonical entity names only."
            )),
            HumanMessage(content=state["question"]),
        ])
        return {"entities": result.entities}

    def retrieve_subgraph(state: GraphRAGState) -> dict:
        """Collect neighbours of matched entities from the knowledge graph."""
        facts = []
        seen = set()
        for entity in state["entities"]:
            # Find closest matching node (case-insensitive partial match)
            matches = [n for n in G.nodes() if entity.lower() in n.lower() or n.lower() in entity.lower()]
            for node in matches[:2]:
                for _, neighbor, data in G.out_edges(node, data=True):
                    fact = f"{node} {data['predicate']} {neighbor}"
                    if fact not in seen:
                        facts.append(fact)
                        seen.add(fact)
                for source, _, data in G.in_edges(node, data=True):
                    fact = f"{source} {data['predicate']} {node}"
                    if fact not in seen:
                        facts.append(fact)
                        seen.add(fact)
        context = "\n".join(facts[:TOP_K * 4]) if facts else "No relevant graph context found."
        return {"context": context}

    def generate(state: GraphRAGState) -> dict:
        response = llm.invoke([
            SystemMessage(content=(
                "Answer the question using only the knowledge graph facts below. "
                "If the answer cannot be derived from these facts, say so.\n\n"
                f"Graph facts:\n{state['context']}"
            )),
            HumanMessage(content=state["question"]),
        ])
        return {"answer": response.content}

    graph = StateGraph(GraphRAGState)
    graph.add_node("find_entities", find_entities)
    graph.add_node("retrieve_subgraph", retrieve_subgraph)
    graph.add_node("generate", generate)
    graph.add_edge(START, "find_entities")
    graph.add_edge("find_entities", "retrieve_subgraph")
    graph.add_edge("retrieve_subgraph", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
