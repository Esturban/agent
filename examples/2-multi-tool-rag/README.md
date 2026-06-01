# RAG Agent - External Vector DB

## Prerequisites
**Keys:** `OPENAI_API_KEY` · `QDRANT_URL` · `QDRANT_KEY` · `BRAVE_API_KEY`
**Files:** none
**Colab:** ✅ all services are cloud-hosted; set keys in your Colab secrets

```bash
python examples/2-multi-tool-rag/main.py
```

The following working repo is a directory of implementing multiple tools and different RAG tools and web search.

The way it works:

- `/src/` - contains the different checksums and deduping functionalities to be able to handle upsert into the database
- `main.py` - sample runtime example of the definition of the rag agent


## Benefits 
- Showcases how to use a cloud-hosted vector DB to create a RAG agent
- Handle multiple tools with a RAG agent, including web search

## Drawbacks
- The model will not be able to recall previous responses so it will mostly repeat the answer without much variation. Especially since temperature is 0.


## References  

- [Building Agentic RAG with Qdrant Vector Database](https://qdrant.tech/documentation/agentic-rag-langgraph/) - possibly one of the worst RAG examples I've ever seen