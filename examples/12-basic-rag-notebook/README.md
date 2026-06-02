# 12-basic-rag-notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/12-basic-rag-notebook/rag_workbook.ipynb)

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — all documents are hardcoded inline
**Colab:** ✅ fully self-contained; the notebook installs its own dependencies on Colab

A step-by-step workbook teaching basic RAG: load hardcoded documents, chunk with `RecursiveCharacterTextSplitter`, embed with OpenAI `text-embedding-3-small`, store in an in-memory ChromaDB, and generate answers with `gpt-4o-mini` via `create_retrieval_chain`. Works on Google Colab or locally with no configuration.

```bash
# local
jupyter notebook examples/12-basic-rag-notebook/rag_workbook.ipynb
```
