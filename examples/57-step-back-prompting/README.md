# 57-step-back-prompting

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- 10-doc corpus is inline in src/tools.py
**Colab:** not applicable -- requires local Chroma

```bash
python examples/57-step-back-prompting/main.py
```

Step-Back Prompting (Zheng et al. 2023): instead of retrieving on "What year did Einstein win the Nobel Prize?" (too specific), ask the LLM to first produce a broader question like "What are Einstein's major scientific achievements?" — then retrieve on that. The broader query finds richer context, which then answers the narrow original question.

---

### Graph

```
START
  |
step_back   <- LLM rewrites specific query as a broader background question
  |
retrieve    <- similarity_search on the abstract query, k=3
  |
answer      <- ChatOpenAI answers the ORIGINAL query using the background context
  |
END
```
