# 60-web-scraper-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- fetches a live Wikipedia URL at runtime
**Colab:** not applicable -- requires local execution

```bash
python examples/60-web-scraper-agent/main.py
```

Web Scraper Agent: given a URL and questions, fetches the page with requests, strips navigation/footer noise with BeautifulSoup, splits into chunks, embeds into an ephemeral Chroma collection, and answers via RAG. No pre-built index needed — the entire pipeline runs on demand from any URL.

---

### Graph

```
START
  |
fetch             <- requests.get(url), raise_for_status
  |
parse             <- BeautifulSoup strip nav/footer/scripts, RecursiveCharacterTextSplitter
  |
index_and_retrieve <- Chroma.from_texts(chunks), similarity_search(question, k=4)
  |
answer            <- ChatOpenAI answers question from retrieved chunks
  |
END
```
