---
teaching_ready: true
---
# 42-multimodal-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
pip install langchain-community chromadb httpx
python examples/42-multimodal-rag/main.py
```

Index images into a vector store using GPT-4o vision descriptions, then answer natural-language questions via similarity search over those descriptions.

---

### Graph

```
START → describe (vision LLM per image) → store (Chroma) → answer (similarity search) → END
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| `image_url` content block | Pass `data:image/jpeg;base64,...` to GPT-4o-mini vision |
| Description indexing | Convert images to text → embed → store in ChromaDB |
| Multimodal RAG | Query answers reference image content via text retrieval |
| `similarity_search(query, k=3)` | Retrieve top-k relevant image descriptions |
