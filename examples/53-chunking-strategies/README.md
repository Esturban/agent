# 53-chunking-strategies

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- sample text is inline
**Colab:** fully self-contained; notebook installs its own dependencies

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/53-chunking-strategies/chunking_workbook.ipynb)

```bash
jupyter notebook examples/53-chunking-strategies/chunking_workbook.ipynb
```

Compares four chunking strategies on the same document: fixed-size (CharacterTextSplitter), recursive (RecursiveCharacterTextSplitter), sentence-window, and semantic (embedding cosine boundary detection). Indexes each strategy into a separate Chroma collection and compares RAG answer quality for the same question.

---

### Strategies

```
Document
   |
   +-- Fixed-size (CharacterTextSplitter)    -> uniform N-char blocks, ignores structure
   +-- Recursive (RecursiveCharacterTextSplitter) -> splits on \n\n then \n then space
   +-- Sentence-window                        -> embed sentence, store with k neighbors
   +-- Semantic (cosine boundary detection)   -> split where similarity drops below threshold
        |
     Chroma vectorstore -> similarity_search -> ChatOpenAI generate
```
