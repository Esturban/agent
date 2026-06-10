# 22-hybrid-search-rag

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/22-hybrid-search-rag/hybrid_search_rag_workbook.ipynb)

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — knowledge base is hardcoded inline
**Colab:** not applicable — requires local package installation (rank-bm25, chromadb)

```bash
python examples/22-hybrid-search-rag/main.py
```

Implements **Hybrid Search RAG** in LangGraph by combining BM25 keyword search with OpenAI vector embeddings via LangChain's `EnsembleRetriever`. Pure vector search excels at semantic paraphrases but fails on exact identifiers — model numbers, product codes, legal article references. BM25 (Robertson & Walker, 1994), the algorithm behind Elasticsearch and Google's initial retrieval stage, handles exact matches precisely. Merging both via Reciprocal Rank Fusion gives the production-grade approach used by Pinecone, Weaviate, and OpenSearch.

**Direct complement to** [12-basic-rag-notebook](../12-basic-rag-notebook/) — run that first to understand pure vector RAG, then compare retrieval quality here.

---

### Why the knowledge base uses product model codes

The sample docs contain specific model names (`Apex-X200`, `Vertex-Pro`) that embedding models treat as nearly synonymous — they look similar in vector space even when they're different products. BM25 treats them as distinct terms. The annotated `SAMPLE_QUESTIONS` in `src/tools.py` mark which retriever wins each query, making the tradeoff concrete and observable.

---

### Graph

```
START
  |
retrieve   <- EnsembleRetriever: BM25 (keyword) + Chroma (semantic), weights [0.5, 0.5]
  |          Reciprocal Rank Fusion merges the two ranked lists
generate   <- LLM answers from retrieved context only
  |
END
```

### Tuning the weights

`weights=[0.5, 0.5]` is the neutral starting point. In production:
- Keyword-heavy corpora (legal, medical, product catalogs): increase BM25 weight → `[0.7, 0.3]`
- Conversational or conceptual queries: increase vector weight → `[0.3, 0.7]`
- Run A/B tests with RAGAS (see [16-rag-eval-notebook](../16-rag-eval-notebook/)) to find the optimal split
