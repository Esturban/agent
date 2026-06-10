# 12-basic-rag-notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/12-basic-rag-notebook/rag_workbook.ipynb)

Step-by-step workbook: chunk documents with `RecursiveCharacterTextSplitter`, embed with OpenAI `text-embedding-3-small`, store in an in-memory ChromaDB, and answer questions with `gpt-4o-mini` via `create_retrieval_chain`. Fully self-contained — no local setup needed.

**Keys:** `OPENAI_API_KEY`

```bash
# local
jupyter notebook examples/12-basic-rag-notebook/rag_workbook.ipynb
```
