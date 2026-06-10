# 24-graph-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — knowledge base is hardcoded inline
**Colab:** not applicable — requires local package installation (networkx)

```bash
python examples/24-graph-rag/main.py
```

Implements **Graph RAG** in LangGraph: an LLM extracts `(subject, predicate, object)` triples from each document into a NetworkX directed graph, then answers queries by traversing entity neighbours rather than similarity-ranking documents. The key insight is that multi-hop questions — "who founded the company that makes LangGraph?" — require connecting facts *across* documents. Vector search finds documents similar to the query; graph traversal finds the relational path between entities, surfacing answers that similarity alone cannot reach. Inspired by Microsoft's GraphRAG (Edge et al., 2024).

---

### Graph

```
START
  |
find_entities    <- LLM extracts named entities from the question,
  |                 matches them to known graph nodes
retrieve_subgraph <- collect in/out edges for matched entities (subgraph)
  |
generate         <- LLM answers from the relational facts, not documents
  |
END
```

### Why this outperforms vector RAG on relational questions

```
Question: "Who founded the company that makes LangGraph?"

Vector RAG:  retrieves docs about LangGraph → finds "LangGraph is built on LangChain"
             → misses the connection to Harrison Chase (different document)

Graph RAG:   LangGraph → [built_on] → LangChain → [founded_by] → Harrison Chase
             → answers correctly via two-hop traversal
```
