#!/usr/bin/env python3
"""
Generate rag_workbook.ipynb -- the 3-hour RAG workshop notebook.
Run with:  python generate_workbook.py
"""

import json, uuid, os

def cell_id():
    return uuid.uuid4().hex[:16]


def md(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id(),
        "metadata": {},
        "source": source,
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "id": cell_id(),
        "metadata": {},
        "source": source,
        "outputs": [],
        "execution_count": None,
    }


# ─── CELLS ────────────────────────────────────────────────────────────────────

cells = []

# ── Title ─────────────────────────────────────────────────────────────────────
cells.append(md("""\
# RAG from Zero to ChromaDB
## A 3-Hour Hands-On Workshop

**Retrieval-Augmented Generation (RAG)** is the most widely deployed pattern for\
 grounding LLM responses in real documents — reducing hallucinations and enabling\
 answers from private or recent knowledge. By the end of this session you will\
 understand *why* RAG works, *how* every component fits together, and *how* to\
 build a persistent, locally-hosted pipeline from scratch.

---

### Session Roadmap

| # | Topic | Time |
|---|-------|------|
| 1 | **Concepts** — What is RAG and why does it exist? | 15 min |
| 2 | **Text Splitting** — Turning documents into chunks | 30 min |
| 3 | **Embeddings** — Vectors and semantic similarity | 30 min |
| 4 | **ChromaDB** — Local vector store (in-memory → persistent) | 30 min |
| 5 | **Full RAG Pipeline** — End-to-end with LangChain | 30 min |
| 6 | **Real Documents** — PDFs, web pages, plain text | 15 min |
| 7 | **Debugging & Evaluation** — Know when RAG fails | 15 min |
| ★ | **Advanced Techniques** (bonus) | 15 min |

**Total: ~3 hours**

---

### Prerequisites
- Python 3.10 + (a `.venv` with the requirements already installed)
- An `OPENAI_API_KEY` set in `.env` (or Colab Secrets)

### Key References
> Lewis, P., Perez, E., et al. (2020). *Retrieval-Augmented Generation for\
 Knowledge-Intensive NLP Tasks.* NeurIPS 2020. https://arxiv.org/abs/2005.11401
> Gao, Y., Xiong, Y., et al. (2023). *Retrieval-Augmented Generation for Large\
 Language Models: A Survey.* https://arxiv.org/abs/2312.10997
> ChromaDB documentation: https://docs.trychroma.com
> LangChain RAG tutorial: https://python.langchain.com/docs/tutorials/rag/
"""))

# ── 0-A  Install (Colab guard) ─────────────────────────────────────────────────
cells.append(code("""\
# Install dependencies — runs only on Google Colab.
# Local users: your .venv already has everything from requirements.txt.
import sys

def _in_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False

if _in_colab():
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "langchain", "langchain-openai", "langchain-chroma",
                    "langchain-community", "langchain-text-splitters",
                    "chromadb", "python-dotenv", "pypdf", "beautifulsoup4",
                    "lxml"])
    print("Colab install complete.")
else:
    print("Local environment detected — skipping install.")
"""))

# ── 0-B  Imports & API key ────────────────────────────────────────────────────
cells.append(code("""\
import os, math, shutil, textwrap
from pathlib import Path
from typing import List

# ── API key ───────────────────────────────────────────────────────────────────
# Colab: set in Secrets panel (left sidebar key icon)
# Local: create a .env file containing  OPENAI_API_KEY=sk-...
try:
    from google.colab import userdata
    os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
except ImportError:
    from dotenv import load_dotenv
    load_dotenv()

# ── Core imports ──────────────────────────────────────────────────────────────
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import chromadb

# ── Sanity check ──────────────────────────────────────────────────────────────
key_ok = bool(os.environ.get("OPENAI_API_KEY"))
print(f"OPENAI_API_KEY present: {key_ok}")
if not key_ok:
    print()
    print("  ACTION REQUIRED — add your key before running embedding or LLM cells.")
    print("  Local: echo 'OPENAI_API_KEY=sk-...' >> .env")
    print("  Colab: Secrets panel → Add secret 'OPENAI_API_KEY'")
"""))

# ══ PART 1: CONCEPTS ══════════════════════════════════════════════════════════
cells.append(md("""\
---

## Part 1 — What Is RAG and Why Does It Exist?

⏱ *~15 minutes*

---

### The Problem

Large language models are trained on a static snapshot of the internet (knowledge\
 cutoff). They have **no access** to:
- Your internal documents, databases, or emails
- Information published after their training cutoff
- Proprietary or confidential data

When asked about these topics the model doesn't know, it **hallucinates** —\
 producing plausible-sounding but fabricated answers. RAG is the primary\
 production solution.

---

### Three Approaches Compared

| Approach | Cost | Latency | Private docs | Fresh data |
|----------|------|---------|--------------|------------|
| **Prompt stuffing** (put all docs in context) | High (token cost) | High | ✓ | ✓ |
| **Fine-tuning** | Very high (training run) | Low | Partial | ✗ |
| **RAG** | Low (retrieval + generation) | Medium | ✓ | ✓ |

RAG wins for most production use-cases: it's cheap, keeps data fresh without\
 retraining, and is auditable (you can see exactly which chunks the model used).

---

### Key Vocabulary

| Term | Definition |
|------|------------|
| **Chunk** | A small excerpt of a document (typically 100–500 words) |
| **Embedding** | A dense numeric vector representing the *meaning* of text |
| **Vector store** | A database that stores embeddings and supports similarity search |
| **Retriever** | A component that finds the top-k most relevant chunks for a query |
| **Context window** | The total tokens an LLM can read at once |
| **k** | Number of chunks returned by the retriever |
| **Hallucination** | Confident-sounding but fabricated information from an LLM |
"""))

cells.append(md("""\
### RAG Architecture

```
OFFLINE (run once when documents change)
─────────────────────────────────────────────────────

  Your documents
       │
       ▼
  ┌──────────────┐
  │ Text Splitter│  breaks text into overlapping
  └──────┬───────┘  chunks (e.g. 400 chars)
         │
         ▼
  ┌──────────────┐
  │Embedding Model│  converts each chunk to a
  └──────┬───────┘  numeric vector  [0.12, -0.7 ...]
         │
         ▼
  ┌──────────────┐
  │ Vector Store │  stores vectors + metadata on disk
  └──────────────┘  (ChromaDB in this workshop)


ONLINE (every user query)
─────────────────────────────────────────────────────

  User: "What is the refund policy?"
       │
       ▼
  ┌──────────────┐
  │Embedding Model│  convert query → query vector
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │ Vector Store │  cosine similarity search →
  └──────┬───────┘  return top-3 most similar chunks
         │
         ▼
  ┌──────────────────────────────────────────┐
  │ Prompt = system + retrieved chunks + query│
  └──────┬───────────────────────────────────┘
         │
         ▼
  ┌──────────────┐
  │     LLM      │  generates grounded answer
  └──────┬───────┘  using only the context provided
         │
         ▼
  "Refunds are accepted within 30 days..."
```

> **Source**: Architecture adapted from Lewis et al. (2020) — the original RAG paper\
 from Facebook AI Research.
"""))

# ── Concept demo: with vs without RAG ─────────────────────────────────────────
cells.append(code("""\
# Quick demo — ask a question that requires private knowledge.
# We'll show the difference between: (a) LLM alone, (b) LLM + RAG.
# This runs a single LLM call with and without context — no retrieval yet.

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

PRIVATE_FACT = (
    "Our product, VaultDB, was acquired by Apex Corp on March 3, 2024 "
    "for $47 million. The integration is expected to complete by Q3 2025."
)

question = "When was VaultDB acquired and for how much?"

# Without context
response_no_rag = llm.invoke(question)
print("WITHOUT RAG:")
print(response_no_rag.content)
print()

# With context injected manually
prompt_with_context = (
    f"Use the following context to answer the question.\\n\\n"
    f"Context: {PRIVATE_FACT}\\n\\nQuestion: {question}"
)
response_with_rag = llm.invoke(prompt_with_context)
print("WITH RAG (context injected):")
print(response_with_rag.content)
"""))

# ══ PART 2: TEXT SPLITTING ════════════════════════════════════════════════════
cells.append(md("""\
---

## Part 2 — Text Splitting: Turning Documents into Chunks

⏱ *~30 minutes*

---

### Why Not Just Feed the Whole Document?

LLMs have a **context window limit** (e.g., 128k tokens for GPT-4o). But even with\
 large windows:

1. **Cost** — every token costs money; sending 500 pages when only 2 paragraphs are\
 relevant is wasteful.
2. **Quality** — LLMs perform worse when buried in irrelevant text\
 ("lost-in-the-middle" effect¹).
3. **Retrieval precision** — smaller chunks produce more targeted similarity\
 matches.

> ¹ Liu, N. et al. (2023). *Lost in the Middle: How Language Models Use Long\
 Contexts.* https://arxiv.org/abs/2307.03172

---

### Splitter Comparison

| Splitter | Strategy | Best for |
|----------|----------|----------|
| `CharacterTextSplitter` | Split on a single separator | Simple, structured text |
| `RecursiveCharacterTextSplitter` | Try `\\n\\n`, `\\n`, ` `, `""` in order | General prose — **default choice** |
| `TokenTextSplitter` | Split by token count | When token budget matters precisely |
| `MarkdownTextSplitter` | Aware of `#`, `##`, code blocks | Markdown documentation |
| `HTMLHeaderTextSplitter` | Aware of `<h1>`, `<h2>` tags | HTML pages |

---

### `chunk_size` and `chunk_overlap`

```
Document text:
  "The capital of France is Paris. Paris has a population of 2 million..."

chunk_size=50, chunk_overlap=10:

  Chunk 0: "The capital of France is Paris. Paris has a"
  Chunk 1: "Paris has a population of 2 million..."
            ──────────── overlap ────────────
```

**Why overlap?** Without it, a sentence that straddles a chunk boundary gets split\
 and may be missed. Overlap ensures every sentence appears in at least one complete\
 chunk.

**Rule of thumb:**
- `chunk_size`: 300–600 characters for general prose
- `chunk_overlap`: 10–15% of chunk_size
"""))

cells.append(code("""\
# ─── 2-A: CharacterTextSplitter ──────────────────────────────────────────────
# Splits ONLY on the specified separator — simple but can produce uneven chunks.

sample_text = \"\"\"
Artificial intelligence (AI) refers to the simulation of human intelligence by machines.
The term was coined by John McCarthy in 1956 at the Dartmouth Conference.

Machine learning is a subset of AI that enables systems to learn from data.
It was popularized in the 1980s and 1990s with the rise of neural networks.

Deep learning is a subset of machine learning that uses multi-layer neural networks.
The AlexNet breakthrough in 2012 marked the modern deep learning era.

Natural language processing (NLP) allows computers to understand human language.
Large language models like GPT-4 and Claude represent the current state of the art.
\"\"\".strip()

char_splitter = CharacterTextSplitter(
    separator="\\n\\n",   # split only on blank lines
    chunk_size=200,
    chunk_overlap=20,
    length_function=len,
)
char_chunks = char_splitter.create_documents([sample_text])

print(f"CharacterTextSplitter: {len(char_chunks)} chunks\\n")
for i, chunk in enumerate(char_chunks):
    print(f"  Chunk {i} ({len(chunk.page_content)} chars):")
    print(f"    {chunk.page_content[:100].replace(chr(10), ' ')}...")
"""))

cells.append(code("""\
# ─── 2-B: RecursiveCharacterTextSplitter ─────────────────────────────────────
# Tries multiple separators in order: ["\\n\\n", "\\n", " ", ""]
# This is the DEFAULT for most RAG pipelines.

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30,
    length_function=len,
    separators=["\\n\\n", "\\n", ". ", " ", ""],
)
recursive_chunks = recursive_splitter.create_documents([sample_text])

print(f"RecursiveCharacterTextSplitter: {len(recursive_chunks)} chunks\\n")
for i, chunk in enumerate(recursive_chunks):
    print(f"  Chunk {i} ({len(chunk.page_content)} chars):")
    print(f"    {chunk.page_content[:100].replace(chr(10), ' ')}...")
"""))

cells.append(code("""\
# ─── 2-C: Inspect chunk boundaries and overlap ────────────────────────────────
# Good diagnostic: look for where chunks start/end.

print("=== FULL CHUNK CONTENTS ===\\n")
for i, chunk in enumerate(recursive_chunks):
    border = "─" * 60
    print(f"CHUNK {i}  ({len(chunk.page_content)} chars)")
    print(border)
    print(chunk.page_content)
    print()
"""))

cells.append(code("""\
# ─── 2-D: Experiment — how chunk_size changes the pipeline ───────────────────
# Smaller chunks = more precise retrieval but may miss context.
# Larger chunks = more context but noisier retrieval.

long_text = \"\"\"
The French Revolution began in 1789 and fundamentally transformed France.
King Louis XVI was executed in 1793, ending centuries of absolute monarchy.

The revolution spread democratic ideals across Europe and influenced constitutions worldwide.
Liberty, equality, and fraternity became the rallying cries of the movement.

Napoleon Bonaparte rose to power in 1799 following the revolution.
He modernized France's legal system with the Napoleonic Code, still influential today.

The Industrial Revolution began in Britain in the late 18th century.
Steam power, mechanized textile production, and iron manufacturing drove rapid change.

By 1850 railways connected major cities and coal production had tripled.
Urban populations swelled as workers migrated from the countryside to factories.
\"\"\".strip()

for size in [100, 300, 600]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=size // 10)
    chunks = splitter.create_documents([long_text])
    avg = sum(len(c.page_content) for c in chunks) / len(chunks)
    print(f"chunk_size={size:4d}  →  {len(chunks):2d} chunks  (avg {avg:.0f} chars)")
"""))

cells.append(md("""\
### Exercise 1 — Split Your Own Text

Paste any text (an article, a policy document, your own notes) into `my_text`\
 below and experiment with different `chunk_size` and `chunk_overlap` values.

**Goal:** Find settings where no chunk feels too short (< 50 chars) or too long\
 (> 600 chars) for your content.
"""))

cells.append(code("""\
# ── Exercise 1 Starter ───────────────────────────────────────────────────────
my_text = \"\"\"
Paste your own text here. It can be multiple paragraphs.
The longer the better — try at least 500 words.
\"\"\"

# TODO: adjust these values and re-run
MY_CHUNK_SIZE = 400
MY_CHUNK_OVERLAP = 50

splitter = RecursiveCharacterTextSplitter(
    chunk_size=MY_CHUNK_SIZE,
    chunk_overlap=MY_CHUNK_OVERLAP,
)
my_chunks = splitter.create_documents([my_text])

print(f"Your text: {len(my_text)} chars")
print(f"Settings: chunk_size={MY_CHUNK_SIZE}, overlap={MY_CHUNK_OVERLAP}")
print(f"Result:   {len(my_chunks)} chunks")
print()
for i, c in enumerate(my_chunks):
    print(f"  [{i}] {len(c.page_content)} chars — {c.page_content[:80].replace(chr(10),' ')}...")
"""))

# ══ PART 3: EMBEDDINGS ════════════════════════════════════════════════════════
cells.append(md("""\
---

## Part 3 — Embeddings: Vectors and Semantic Similarity

⏱ *~30 minutes*

---

### What Is an Embedding?

An **embedding** is a list of floating-point numbers — a vector — that encodes\
 the *meaning* of a piece of text. Texts with similar meanings produce vectors that\
 are close together in this high-dimensional space.

```
"I love cats"          →  [0.12, -0.45, 0.78, 0.02, ...]   (1536 numbers)
"I adore kittens"      →  [0.11, -0.43, 0.79, 0.01, ...]   ← very close!
"The stock market fell"→  [-0.62, 0.33, -0.21, 0.91, ...]  ← far away
```

Embedding models are trained to push **semantically similar** texts close together\
 regardless of exact wording. This is why RAG can retrieve "refund policy" content\
 when a user asks "can I get my money back?" — the phrasing differs but the\
 meaning is the same.

---

### How Is Similarity Measured?

**Cosine similarity** is the standard metric. It measures the angle between two\
 vectors:

```
cos(θ) = (A · B) / (|A| × |B|)
```

- **1.0** = identical direction = identical meaning
- **0.0** = perpendicular = unrelated
- **-1.0** = opposite direction = opposite meaning

ChromaDB uses **cosine distance** = 1 - cosine_similarity, so lower = more similar.

---

### Embedding Model Comparison

| Model | Dimensions | Cost | Use case |
|-------|-----------|------|----------|
| `text-embedding-3-small` | 1536 | Low | Default production choice |
| `text-embedding-3-large` | 3072 | Higher | Higher accuracy tasks |
| `text-embedding-ada-002` | 1536 | Low | Legacy (use 3-small instead) |
| `sentence-transformers/all-MiniLM-L6-v2` | 384 | Free (local) | No API key, offline use |

> Note: You must use the **same embedding model** for indexing and querying.\
 Mixing models produces garbage results.
"""))

cells.append(code("""\
# ─── 3-A: Generate embeddings and inspect ────────────────────────────────────

embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

sentences = [
    "I love cats",
    "I adore kittens",
    "The Eiffel Tower is in Paris",
    "The stock market fell sharply today",
]

vectors = embeddings_model.embed_documents(sentences)

print(f"Embedding model: text-embedding-3-small")
print(f"Vector dimensions: {len(vectors[0])}")
print()
for sentence, vector in zip(sentences, vectors):
    print(f"  '{sentence}'")
    print(f"    First 5 values: {[round(v, 4) for v in vector[:5]]}")
    print(f"    L2 norm: {math.sqrt(sum(v**2 for v in vector)):.4f}")
    print()
"""))

cells.append(code("""\
# ─── 3-B: Cosine similarity from scratch ─────────────────────────────────────

def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x**2 for x in a))
    mag_b = math.sqrt(sum(x**2 for x in b))
    return dot / (mag_a * mag_b)

# Compare all pairs
print("Cosine Similarity Matrix\\n")
print(f"{'':45}", end="")
for s in sentences:
    print(f"{s[:18]:20}", end="")
print()

for i, (s_i, v_i) in enumerate(zip(sentences, vectors)):
    print(f"{s_i[:44]:45}", end="")
    for j, (s_j, v_j) in enumerate(zip(sentences, vectors)):
        sim = cosine_similarity(v_i, v_j)
        print(f"{sim:+.3f}               ", end="")
    print()

print()
print("Observation: 'I love cats' and 'I adore kittens' are much more similar")
print("than either is to the Paris or stock market sentences.")
"""))

cells.append(code("""\
# ─── 3-C: Semantic clustering demo ───────────────────────────────────────────
# This illustrates why embedding-based search finds semantically related content
# even when the exact words differ.

test_phrases = [
    # Cluster A: Animals
    "dogs are great pets",
    "puppies are adorable",
    "felines make wonderful companions",
    # Cluster B: Finance
    "the interest rate was raised by the central bank",
    "inflation is reducing purchasing power",
    "bond yields rose to a 10-year high",
    # Cluster C: Technology
    "neural networks have revolutionized computer vision",
    "machine learning models require large datasets",
    "GPUs accelerate deep learning training",
]

phrase_vecs = embeddings_model.embed_documents(test_phrases)
query = "my cat is sick, what should I feed it?"
query_vec = embeddings_model.embed_query(query)

sims = [(phrase, cosine_similarity(query_vec, vec))
        for phrase, vec in zip(test_phrases, phrase_vecs)]
sims.sort(key=lambda x: -x[1])

print(f"Query: '{query}'\\n")
print("Most similar phrases (ranked):")
for phrase, sim in sims:
    bar = "█" * int(sim * 30)
    print(f"  {sim:.3f} {bar:30} {phrase}")
"""))

cells.append(md("""\
### Exercise 2 — Explore Semantic Space

Modify the `test_phrases` list above to include your own clusters (e.g., cooking,\
 sports, programming). Pick a query and observe which cluster it lands in.

**Challenge:** Can you find a phrase that the model ranks surprisingly high or low?\
 What does this tell you about the embedding model's training data?
"""))

# ══ PART 4: CHROMADB ══════════════════════════════════════════════════════════
cells.append(md("""\
---

## Part 4 — ChromaDB: Your Local Vector Store

⏱ *~30 minutes*

---

### What Is a Vector Store?

A vector store does three things:
1. **Stores** vectors alongside their original text and metadata
2. **Indexes** those vectors for fast approximate nearest-neighbour search
3. **Returns** the top-k closest vectors for any query vector

ChromaDB is the most popular open-source vector store for local development.\
 It supports both **in-memory** (fast, ephemeral) and **persistent** (on-disk)\
 modes. No Docker, no cloud account — it runs as a Python library.

```
In-memory:   chromadb.EphemeralClient()     ← data lost when process ends
Persistent:  chromadb.PersistentClient(path="./chroma_db")  ← survives restarts
```

---

### Direct ChromaDB API vs LangChain Wrapper

This section shows both:
- **Direct API**: Lower-level, more control, useful for non-LangChain projects
- **LangChain `Chroma`**: Higher-level, integrates with retrievers and chains
"""))

cells.append(code("""\
# ─── 4-A: Direct ChromaDB — EphemeralClient (in-memory) ─────────────────────
# Use this for quick experiments and testing. Data disappears when the cell ends.

client_mem = chromadb.EphemeralClient()
collection = client_mem.get_or_create_collection(
    name="workshop_test",
    metadata={"hnsw:space": "cosine"},  # use cosine distance
)

# Add documents (ChromaDB embeds internally or you can pass pre-computed vectors)
# Here we pass pre-computed embeddings for transparency.
docs_to_add = [
    "Python is a high-level programming language known for its readability.",
    "JavaScript runs in web browsers and enables interactive web pages.",
    "Rust is a systems programming language focused on memory safety.",
    "SQL is used to query and manipulate relational databases.",
    "Docker containers package applications with their dependencies.",
]
labels = ["python", "javascript", "rust", "sql", "docker"]

doc_vecs = embeddings_model.embed_documents(docs_to_add)

collection.add(
    ids=labels,
    documents=docs_to_add,
    embeddings=doc_vecs,
    metadatas=[{"category": "programming", "doc_id": i} for i in range(len(docs_to_add))],
)

print(f"Collection count: {collection.count()} documents")
"""))

cells.append(code("""\
# ─── 4-B: Query the collection ───────────────────────────────────────────────

query_text = "What language is safe for system programming?"
query_embedding = embeddings_model.embed_query(query_text)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=["documents", "metadatas", "distances"],
)

print(f"Query: '{query_text}'\\n")
for rank, (doc, meta, dist) in enumerate(zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
), start=1):
    similarity = 1 - dist  # cosine distance → similarity
    print(f"  Rank {rank} (similarity={similarity:.3f})")
    print(f"    {doc}")
    print(f"    metadata: {meta}")
    print()
"""))

cells.append(code("""\
# ─── 4-C: Metadata filtering ─────────────────────────────────────────────────
# In real pipelines you filter by source, date, department, etc.

# Add a document from a different category
collection.add(
    ids=["mysql"],
    documents=["MySQL is an open-source relational database management system."],
    embeddings=[embeddings_model.embed_documents(
        ["MySQL is an open-source relational database management system."])[0]],
    metadatas=[{"category": "database", "doc_id": 99}],
)

print("All documents:")
all_docs = collection.get(include=["documents", "metadatas"])
for doc, meta in zip(all_docs["documents"], all_docs["metadatas"]):
    print(f"  [{meta['category']:12}] {doc[:60]}")

print()

# Filter: only search in 'database' category
query_embedding = embeddings_model.embed_query("How do I store structured data?")
filtered = collection.query(
    query_embeddings=[query_embedding],
    n_results=2,
    where={"category": {"$eq": "database"}},
    include=["documents", "distances"],
)

print("Query with metadata filter (category='database'):")
for doc, dist in zip(filtered["documents"][0], filtered["distances"][0]):
    print(f"  similarity={1-dist:.3f}  {doc[:70]}")
"""))

# ── Persistent ChromaDB ────────────────────────────────────────────────────────
cells.append(md("""\
### Persistent ChromaDB — Surviving Restarts

The in-memory client is great for experiments. For production or multi-session\
 workflows, use a `PersistentClient` — ChromaDB writes the HNSW index and all\
 data to disk automatically.

```python
# Create (or open existing)
client = chromadb.PersistentClient(path="./chroma_db")

# From now on, every .add() is automatically saved to disk.
# To reload later in a new process:
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("my_collection")
```
"""))

cells.append(code("""\
# ─── 4-D: Persistent ChromaDB with LangChain ─────────────────────────────────
# LangChain's Chroma class wraps chromadb.PersistentClient when you pass
# persist_directory. This is the recommended pattern for production pipelines.

PERSIST_DIR = "./chroma_workshop_db"

# Remove old data from previous runs to start fresh
if Path(PERSIST_DIR).exists():
    shutil.rmtree(PERSIST_DIR)

knowledge_docs = [
    Document(
        page_content="The Python `with` statement is used for context management. "
                     "It ensures resources like files or database connections are "
                     "properly closed even if an exception occurs.",
        metadata={"source": "python-docs", "topic": "context-managers"},
    ),
    Document(
        page_content="List comprehensions in Python provide a concise way to create "
                     "lists. Syntax: [expression for item in iterable if condition]. "
                     "They are generally faster than equivalent for-loops.",
        metadata={"source": "python-docs", "topic": "list-comprehensions"},
    ),
    Document(
        page_content="Generators are functions that yield values lazily. They use "
                     "less memory than lists because they produce values one at a time. "
                     "Create with `yield` keyword or generator expressions.",
        metadata={"source": "python-docs", "topic": "generators"},
    ),
    Document(
        page_content="Decorators in Python wrap functions to modify their behaviour. "
                     "The @decorator syntax is syntactic sugar for func = decorator(func). "
                     "Common uses: logging, caching, access control.",
        metadata={"source": "python-docs", "topic": "decorators"},
    ),
    Document(
        page_content="Python's `dataclasses` module (Python 3.7+) auto-generates "
                     "__init__, __repr__, and __eq__ methods based on class annotations. "
                     "Use @dataclass decorator on the class.",
        metadata={"source": "python-docs", "topic": "dataclasses"},
    ),
]

# Split documents
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
split_docs = splitter.split_documents(knowledge_docs)

# Embed and persist to disk
vectorstore_persistent = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings_model,
    persist_directory=PERSIST_DIR,
    collection_name="python_knowledge",
)

print(f"Created persistent collection at: {PERSIST_DIR}/")
print(f"Stored {vectorstore_persistent._collection.count()} chunks")
print(f"Disk usage: {sum(f.stat().st_size for f in Path(PERSIST_DIR).rglob('*') if f.is_file()) / 1024:.1f} KB")
"""))

cells.append(code("""\
# ─── 4-E: Load the collection from disk in a new session ─────────────────────
# Simulate what happens when you restart Python and want to re-use the index.

vectorstore_loaded = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings_model,
    collection_name="python_knowledge",
)

print(f"Loaded collection from disk: {vectorstore_loaded._collection.count()} chunks")
print()

# Test a similarity search
results = vectorstore_loaded.similarity_search_with_score(
    "how do I make code run when the program exits?",
    k=2,
)

print("Query: 'how do I make code run when the program exits?'\\n")
for doc, score in results:
    print(f"  Score (distance): {score:.4f}  (lower = more similar)")
    print(f"  Topic: {doc.metadata.get('topic')}")
    print(f"  Content: {doc.page_content[:120]}...")
    print()
"""))

cells.append(md("""\
### Exercise 3 — Build Your Own Knowledge Base

Create a persistent ChromaDB collection on a topic of your choice.

1. Write at least 5 documents (can be copied from any article or docs page)
2. Store them in `./chroma_my_kb/`
3. Load the collection fresh and run at least 3 queries
4. Verify the retrieved chunks are sensible

**Starter template below:**
"""))

cells.append(code("""\
# ── Exercise 3 Starter ────────────────────────────────────────────────────────
MY_KB_DIR = "./chroma_my_kb"

my_documents = [
    Document(
        page_content="TODO: replace with your own content",
        metadata={"source": "my-source", "topic": "my-topic"},
    ),
    # Add more documents here...
]

# TODO: split, embed, and persist your documents
# TODO: load from disk and query
"""))

# ══ PART 5: FULL RAG PIPELINE ════════════════════════════════════════════════
cells.append(md("""\
---

## Part 5 — The Full RAG Pipeline End-to-End

⏱ *~30 minutes*

---

### Pipeline Components

```
Documents → Splitter → Embeddings → Vector Store (offline)

Query → Retriever → [top-k chunks] → Prompt → LLM → Answer (online)
```

LangChain provides two chains that wire this up:

| Chain | Purpose |
|-------|---------|
| `create_stuff_documents_chain` | Takes retrieved docs and stuffs them into the prompt |
| `create_retrieval_chain` | Runs retrieval then passes results to the document chain |

The retriever is the bridge between the vector store and the chain. You can\
 configure it independently from the underlying store.
"""))

cells.append(code("""\
# ─── 5-A: Build a richer knowledge base ──────────────────────────────────────
PIPELINE_DIR = "./chroma_pipeline_db"
if Path(PIPELINE_DIR).exists():
    shutil.rmtree(PIPELINE_DIR)

company_docs = [
    Document(
        page_content="Apex Corp was founded in 2010 by Sarah Chen and Marcus Webb. "
                     "The company started as a cloud storage provider and pivoted to "
                     "AI-powered data analytics in 2018. Headquarters: San Francisco.",
        metadata={"source": "company-overview", "department": "general"},
    ),
    Document(
        page_content="Our refund policy: customers may request a full refund within "
                     "30 days of purchase. Refunds are processed within 5-7 business days "
                     "to the original payment method. No refunds after 30 days.",
        metadata={"source": "refund-policy", "department": "support"},
    ),
    Document(
        page_content="Enterprise pricing: Starter plan $99/month (up to 5 users), "
                     "Growth plan $299/month (up to 25 users), Enterprise plan custom "
                     "pricing for 25+ users. Annual billing saves 20%.",
        metadata={"source": "pricing", "department": "sales"},
    ),
    Document(
        page_content="The DataPulse API uses REST with JSON payloads. Authentication "
                     "uses Bearer tokens. Rate limit: 1000 requests/minute per API key. "
                     "Base URL: https://api.apexcorp.io/v2/",
        metadata={"source": "api-docs", "department": "engineering"},
    ),
    Document(
        page_content="Our SLA guarantees 99.9% uptime for all paid plans. Scheduled "
                     "maintenance windows are Sundays 2-4am PST. Status page: "
                     "status.apexcorp.io. Incident notifications via email and Slack.",
        metadata={"source": "sla", "department": "engineering"},
    ),
    Document(
        page_content="To contact support: email support@apexcorp.io or open a ticket "
                     "in the dashboard. Enterprise customers get a dedicated CSM and "
                     "24/7 phone support. Response SLA: 4 hours for critical issues.",
        metadata={"source": "support", "department": "support"},
    ),
]

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=40)
split_company_docs = splitter.split_documents(company_docs)

vectorstore_company = Chroma.from_documents(
    documents=split_company_docs,
    embedding=embeddings_model,
    persist_directory=PIPELINE_DIR,
    collection_name="apex_corp",
)

print(f"Knowledge base ready: {vectorstore_company._collection.count()} chunks")
"""))

cells.append(code("""\
# ─── 5-B: Build the retriever and inspect retrieved chunks ───────────────────
# ALWAYS inspect what the retriever returns before trusting the LLM's answer.

retriever = vectorstore_company.as_retriever(
    search_type="similarity",   # alternatives: "mmr", "similarity_score_threshold"
    search_kwargs={"k": 3},
)

def show_retrieval(query: str):
    docs = retriever.invoke(query)
    print(f"Query: '{query}'")
    print(f"Retrieved {len(docs)} chunks:\\n")
    for i, doc in enumerate(docs, 1):
        print(f"  [{i}] source={doc.metadata.get('source')}")
        print(f"       {doc.page_content[:150]}...")
    print()

show_retrieval("How much does the Growth plan cost?")
show_retrieval("Can I get a refund after 6 weeks?")
"""))

cells.append(code("""\
# ─── 5-C: Build the full RAG chain ───────────────────────────────────────────

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# The system prompt instructs the model to ONLY use the provided context.
# This is critical for grounding — without it the model will mix retrieved
# content with its own knowledge.
system_prompt = (
    "You are a helpful customer support assistant for Apex Corp. "
    "Answer the user's question using ONLY the information in the context below. "
    "If the context doesn't contain the answer, say 'I don't have that information.' "
    "Do not make up details.\\n\\n"
    "Context:\\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

combine_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, combine_chain)

print("RAG chain built. Ready to query.")
"""))

cells.append(code("""\
# ─── 5-D: Run queries and inspect the full response ──────────────────────────

test_queries = [
    "What are your pricing plans?",
    "How long do I have to request a refund?",
    "What is your API rate limit?",
    "Can I get a discount if I pay annually?",
    "Where was Apex Corp founded?",         # in the docs
    "What programming languages do you use?",  # NOT in the docs
]

for query in test_queries:
    result = rag_chain.invoke({"input": query})
    sources = list({doc.metadata.get("source", "?") for doc in result["context"]})
    print(f"Q: {query}")
    print(f"A: {result['answer']}")
    print(f"   [sources: {', '.join(sources)}]")
    print()
"""))

cells.append(md("""\
### Exercise 4 — Build Your Own Company Bot

Use the knowledge base you created in Exercise 3, or create a new one about any\
 topic (a book, a product, a policy document).

1. Build a RAG chain that answers questions about your topic
2. Run at least 5 queries — mix questions the docs can answer and ones they can't
3. Verify the model says "I don't have that information" for out-of-scope questions

**Key insight:** If the model answers out-of-scope questions confidently, your\
 system prompt needs strengthening.
"""))

cells.append(code("""\
# ── Exercise 4 Starter ────────────────────────────────────────────────────────
# TODO: load your Exercise 3 knowledge base or create a new one

# your_vectorstore = Chroma(persist_directory="./chroma_my_kb", ...)
# your_retriever = your_vectorstore.as_retriever(search_kwargs={"k": 3})
# your_chain = ...

# test_questions = [
#     "...",
#     "...",
# ]
"""))

# ══ PART 6: REAL DOCUMENTS ═══════════════════════════════════════════════════
cells.append(md("""\
---

## Part 6 — Loading Real Documents

⏱ *~15 minutes*

---

In the previous sections we created `Document` objects manually. In production\
 you'll load from real sources. LangChain has 100+ document loaders.

| Loader | Package | Use for |
|--------|---------|---------|
| `TextLoader` | `langchain_community` | `.txt`, `.md` files |
| `PyPDFLoader` | `langchain_community` + `pypdf` | PDF files |
| `WebBaseLoader` | `langchain_community` + `beautifulsoup4` | Web pages |
| `DirectoryLoader` | `langchain_community` | Entire folders |
| `CSVLoader` | `langchain_community` | Spreadsheets |
| `UnstructuredMarkdownLoader` | `unstructured` | Markdown with structure |
"""))

cells.append(code("""\
# ─── 6-A: TextLoader — load a plain text file ────────────────────────────────
from langchain_community.document_loaders import TextLoader

# Create a sample text file to load
sample_file = Path("./sample_document.txt")
sample_file.write_text(\"\"\"
The Solar System
================

The Solar System consists of the Sun and the objects that orbit it.
The eight planets are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.

The Inner Planets
-----------------
Mercury is the smallest planet and closest to the Sun. A year on Mercury lasts 88 Earth days.
Venus is the hottest planet despite not being the closest to the Sun, due to its thick atmosphere.
Earth is the only known planet with liquid water on the surface and complex life.
Mars has the largest volcano in the Solar System: Olympus Mons, 22km tall.

The Outer Planets
-----------------
Jupiter is the largest planet, 2.5 times the mass of all other planets combined.
Saturn's iconic rings are made of ice and rock, ranging from 10 meters to 1km in size.
Uranus rotates on its side with an axial tilt of 98 degrees.
Neptune has the strongest winds in the Solar System, exceeding 2000 km/h.
\"\"\".strip())

loader = TextLoader(str(sample_file))
raw_docs = loader.load()
print(f"Loaded {len(raw_docs)} document(s)")
print(f"Characters: {len(raw_docs[0].page_content)}")
print(f"Metadata: {raw_docs[0].metadata}")
print()

# Split and show chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
file_chunks = splitter.split_documents(raw_docs)
print(f"Chunks: {len(file_chunks)}")
for i, chunk in enumerate(file_chunks):
    print(f"  [{i}] {chunk.page_content[:80].replace(chr(10),' ')}...")
"""))

cells.append(code("""\
# ─── 6-B: WebBaseLoader — load a live web page ───────────────────────────────
# Requires: beautifulsoup4 (already installed)
# Note: this cell requires internet access.

try:
    from langchain_community.document_loaders import WebBaseLoader
    import bs4

    loader = WebBaseLoader(
        web_paths=["https://en.wikipedia.org/wiki/Retrieval-augmented_generation"],
        bs_kwargs={"parse_only": bs4.SoupStrainer(id="bodyContent")},
    )
    web_docs = loader.load()
    web_chunks = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    ).split_documents(web_docs)

    print(f"Loaded: {len(web_docs)} page(s), {len(web_chunks)} chunks")
    print(f"First chunk preview:")
    print(web_chunks[0].page_content[:400] if web_chunks else "(empty)")
except Exception as e:
    print(f"Web load failed (possibly offline or page changed): {e}")
"""))

cells.append(code("""\
# ─── 6-C: PyPDFLoader — load a PDF ──────────────────────────────────────────
# Requires: pypdf (already installed)
# This cell creates a minimal test PDF then loads it.

try:
    from langchain_community.document_loaders import PyPDFLoader

    # For demo: load any local PDF. Change this path to a real PDF you have.
    pdf_path = "./sample.pdf"

    if Path(pdf_path).exists():
        loader = PyPDFLoader(pdf_path)
        pdf_docs = loader.load()
        print(f"Loaded {len(pdf_docs)} pages from PDF")
        for i, page in enumerate(pdf_docs[:3]):
            print(f"  Page {i}: {len(page.page_content)} chars — {page.page_content[:80]}...")
    else:
        print(f"No PDF found at {pdf_path}")
        print("To test: copy any PDF to the notebook directory and update pdf_path.")

except ImportError:
    print("pypdf not installed. Run: pip install pypdf")
except Exception as e:
    print(f"PDF load error: {e}")
"""))

# ══ PART 7: DEBUGGING ════════════════════════════════════════════════════════
cells.append(md("""\
---

## Part 7 — Debugging and Evaluation

⏱ *~15 minutes*

---

### Common RAG Failure Modes

| Failure | Symptom | Root cause | Fix |
|---------|---------|-----------|-----|
| **Irrelevant retrieval** | Wrong chunks returned | Poor chunking or embedding | Smaller chunks, better splitter |
| **Hallucination through** | Model ignores context | Weak system prompt | Stricter prompt |
| **Missing context** | Right topic, wrong detail | `k` too small | Increase `k` |
| **Context overflow** | Answers degraded for long docs | Chunks too large | Reduce `chunk_size` |
| **Metadata ignored** | No filtering happening | Filter not wired up | Use `search_kwargs` with `filter` |

---

### Debugging Checklist

1. **Print retrieved chunks** — the most important diagnostic step
2. **Check similarity scores** — low scores mean poor retrieval
3. **Vary k** — try k=2, k=5, k=10
4. **Vary chunk_size** — try 200, 400, 800
5. **Check the prompt** — print what the LLM actually receives
"""))

cells.append(code("""\
# ─── 7-A: Diagnostic — print what the LLM actually sees ─────────────────────
# This is the #1 debugging technique. Seeing the full prompt reveals most issues.

from langchain_core.callbacks import BaseCallbackHandler

class PromptInspector(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print("=== PROMPT SENT TO LLM ===")
        for i, prompt in enumerate(prompts):
            print(f"--- Prompt {i} ---")
            # Truncate for readability
            print(prompt[:1500])
            if len(prompt) > 1500:
                print(f"... [{len(prompt)-1500} more chars]")
        print("=" * 40)

# Use inspector for one query
inspector_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0,
                            callbacks=[PromptInspector()])
debug_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using only the context.\\n\\nContext:\\n{context}"),
    ("human", "{input}"),
])
debug_chain = create_retrieval_chain(
    retriever,
    create_stuff_documents_chain(inspector_llm, debug_prompt),
)
_ = debug_chain.invoke({"input": "What is the API rate limit?"})
"""))

cells.append(code("""\
# ─── 7-B: Experiment — effect of k on answer quality ─────────────────────────

def query_with_k(query: str, k: int) -> dict:
    ret = vectorstore_company.as_retriever(search_kwargs={"k": k})
    chain = create_retrieval_chain(
        ret,
        create_stuff_documents_chain(
            ChatOpenAI(model="gpt-4o-mini", temperature=0),
            ChatPromptTemplate.from_messages([
                ("system", "Answer using only the context below.\\n\\nContext:\\n{context}"),
                ("human", "{input}"),
            ]),
        ),
    )
    result = chain.invoke({"input": query})
    sources = [d.metadata.get("source", "?") for d in result["context"]]
    return {"answer": result["answer"], "sources": sources, "k": k}

query = "How can I contact support, and what is the response time?"
print(f"Query: '{query}'\\n")

for k_val in [1, 2, 3, 5]:
    r = query_with_k(query, k=k_val)
    print(f"k={k_val}: {r['answer'][:200]}")
    print(f"       sources: {r['sources']}")
    print()
"""))

cells.append(code("""\
# ─── 7-C: Experiment — effect of chunk_size ──────────────────────────────────
# Rebuild the index with different chunk sizes and compare retrieval quality.

def build_and_query(chunk_size: int, query: str):
    splitter_exp = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_size // 10,
    )
    exp_chunks = splitter_exp.split_documents(company_docs)
    exp_store = Chroma.from_documents(
        documents=exp_chunks,
        embedding=embeddings_model,
    )
    results = exp_store.similarity_search_with_score(query, k=2)
    return len(exp_chunks), results

test_query = "refund within 30 days"
print(f"Query: '{test_query}'\\n")

for chunk_sz in [100, 300, 600]:
    n_chunks, results = build_and_query(chunk_sz, test_query)
    best_score = 1 - results[0][1]
    print(f"chunk_size={chunk_sz:4d}  →  {n_chunks:2d} chunks  "
          f"best similarity={best_score:.3f}  "
          f"'{results[0][0].page_content[:80].replace(chr(10),' ')}...'")
"""))

# ══ PART 8: ADVANCED ══════════════════════════════════════════════════════════
cells.append(md("""\
---

## Part 8 ★ — Advanced Techniques (Bonus)

⏱ *~15 minutes*

---

### MMR — Maximal Marginal Relevance

Standard similarity search returns the k *most similar* chunks — but they often\
 repeat each other. **MMR** balances relevance with diversity:

```
MMR score = λ × similarity(chunk, query) - (1-λ) × max_similarity(chunk, already_selected)
```

Set `search_type="mmr"` to use it.

---

### Similarity Score Threshold

Only return chunks above a minimum similarity threshold. Prevents the model from\
 receiving weakly-related chunks when the knowledge base doesn't contain the answer.

```python
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.75},
)
```

---

### Multi-Query Retrieval

A single query may miss relevant chunks due to wording. Multi-query retrieval\
 generates several paraphrases of the query, retrieves for all of them, and deduplicates.

```python
from langchain.retrievers import MultiQueryRetriever
retriever = MultiQueryRetriever.from_llm(vectorstore.as_retriever(), llm)
```
"""))

cells.append(code("""\
# ─── 8-A: MMR vs standard similarity ─────────────────────────────────────────

# Build a store with some redundant documents to show the difference
redundant_docs = [
    Document(page_content="Python is a popular programming language. It is widely used in data science."),
    Document(page_content="Python is beloved by developers. It's popular in the data science community."),
    Document(page_content="JavaScript is the language of the web. It runs in every browser."),
    Document(page_content="TypeScript adds static typing to JavaScript. It is popular in large codebases."),
    Document(page_content="Rust is a systems language focused on memory safety and performance."),
]

mmr_store = Chroma.from_documents(redundant_docs, embeddings_model)
mmr_query = "tell me about Python"

print("Standard similarity (k=4) — note the repeated Python content:")
standard_results = mmr_store.similarity_search(mmr_query, k=4)
for i, doc in enumerate(standard_results, 1):
    print(f"  {i}. {doc.page_content[:80]}")

print()
print("MMR (k=4, fetch_k=10) — more diverse:")
mmr_results = mmr_store.max_marginal_relevance_search(
    mmr_query,
    k=4,
    fetch_k=10,     # fetch more candidates, then select diverse subset
    lambda_mult=0.5,  # 0 = max diversity, 1 = max similarity
)
for i, doc in enumerate(mmr_results, 1):
    print(f"  {i}. {doc.page_content[:80]}")
"""))

cells.append(code("""\
# ─── 8-B: Similarity score threshold retriever ───────────────────────────────
# Returns NO chunks when the query is out-of-domain.

threshold_retriever = vectorstore_company.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.6},
)

in_scope = "What is the refund policy?"
out_of_scope = "What is the best pasta recipe?"

for q in [in_scope, out_of_scope]:
    docs = threshold_retriever.invoke(q)
    print(f"Query: '{q}'")
    print(f"  Retrieved chunks: {len(docs)}", "(none = below threshold)" if not docs else "")
    if docs:
        print(f"  Best match: {docs[0].page_content[:100]}...")
    print()
"""))

cells.append(md("""\
---

## What's Next?

You now have a complete foundation in RAG. Here's where to go deeper:

### Immediate next steps
- **Evaluations**: Use `RAGAS` (https://docs.ragas.io) to measure Faithfulness,\
 Answer Relevance, and Context Recall automatically
- **Hybrid search**: Combine semantic search with BM25 keyword search for better\
 precision on exact terms (`langchain_community.retrievers.BM25Retriever`)
- **Re-ranking**: Use a cross-encoder after retrieval to re-rank chunks more\
 accurately (`langchain.retrievers.ContextualCompressionRetriever`)

### Production considerations
- **Index updates**: ChromaDB supports `.add()` and `.delete()` — no need to\
 rebuild from scratch when documents change
- **Observability**: Enable LangSmith tracing to see every retrieval + generation\
 step in a dashboard
- **Async**: LangChain chains support `ainvoke()` for non-blocking operation in\
 web servers

### Further reading
- Gao et al. (2023). *Retrieval-Augmented Generation for LLMs: A Survey.*\
 https://arxiv.org/abs/2312.10997
- *Advanced RAG Techniques* blog series:\
 https://towardsdatascience.com/advanced-rag-techniques-an-illustrated-overview-04d193d8fec6
- LangChain Expression Language (LCEL) for building more composable chains:\
 https://python.langchain.com/docs/concepts/lcel/

---

*Workshop complete. Commit your `.ipynb` and `chroma_*` directories to your repo.*
"""))

# ─────────────────────────────────────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.0",
        },
    },
    "cells": cells,
}

output_path = os.path.join(os.path.dirname(__file__), "rag_workbook.ipynb")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"Written: {output_path}")
print(f"Cells:   {len(cells)}")
print(f"Size:    {os.path.getsize(output_path) / 1024:.1f} KB")
