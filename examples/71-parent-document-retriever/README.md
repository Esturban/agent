# 71-parent-document-retriever

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- 3 long AI/ML paragraphs are inline in src/tools.py
**Colab:** not applicable -- requires local execution

```bash
python examples/71-parent-document-retriever/main.py
```

Parent Document Retriever: solves the precision vs context tradeoff in RAG. Small child chunks (100 chars) are indexed for precise similarity search. When a child is retrieved, its full parent document (600 chars) is returned for generation. Output shows child count vs parent doc size — proving small-to-large retrieval gives richer context without sacrificing precision.

---

### Graph

```
START
  |
retrieve_parent  <- child similarity_search finds small chunks,
                    ParentDocumentRetriever maps them to full parent docs
  |
generate         <- ChatOpenAI answers using parent doc context
  |
END
```
