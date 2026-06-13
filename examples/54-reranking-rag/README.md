# 54-reranking-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- 20-doc corpus is inline in src/tools.py
**Colab:** not applicable -- requires subprocess for flashrank model download

```bash
pip install flashrank
python examples/54-reranking-rag/main.py
```

Two-stage retrieval pipeline: Chroma bi-encoder retrieves 20 candidates by vector similarity, then FlashRank cross-encoder scores each (query, doc) pair jointly and returns the top 4. Teaches the bi-encoder vs cross-encoder tradeoff: bi-encoders are fast but score query and doc independently; cross-encoders are slower but capture full query-document interaction.

---

### Graph

```
START
  |
retrieve     <- Chroma similarity_search, k=MAX_RETRIEVE (20 candidates)
  |
rerank       <- FlashRank Ranker.rerank(), keep top MAX_RERANK (4)
  |
generate     <- ChatOpenAI with reranked context
  |
END
```
