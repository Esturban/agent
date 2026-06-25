---
teaching_ready: true
---
# 53-chunking-strategies

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- sample text is inline
**Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/53-chunking-strategies/chunking_workbook.ipynb)

```bash
jupyter notebook examples/53-chunking-strategies/chunking_workbook.ipynb
```

Open `chunking_workbook.ipynb` in Colab or Jupyter. Compares four chunking strategies on the same document: fixed-size, recursive, sentence-window, and semantic (cosine boundary detection), indexing each into a separate Chroma collection and comparing RAG answer quality.

---

### Pattern (notebook)

```
Document
   |
   +-- Fixed-size (CharacterTextSplitter)        -> uniform N-char blocks, ignores structure
   +-- Recursive (RecursiveCharacterTextSplitter) -> splits on \n\n then \n then space
   +-- Sentence-window                            -> embed sentence, store with k neighbors
   +-- Semantic (cosine boundary detection)       -> split where similarity drops below threshold
        |
     Chroma vectorstore -> similarity_search -> ChatOpenAI generate
```
