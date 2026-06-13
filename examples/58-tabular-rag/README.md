# 58-tabular-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- 10-row product sales CSV is inline in src/tools.py
**Colab:** not applicable -- requires local execution

```bash
python examples/58-tabular-rag/main.py
```

Tabular RAG: answer natural language questions over structured data using LLM-generated pandas expressions. The LLM receives the DataFrame schema and sample rows, writes a single Python expression to answer the question, and the expression is executed in a sandboxed eval. On error, the LLM retries with the error message up to MAX_ITERATIONS=3 times.

---

### Graph

```
START
  |
load_table    <- pd.read_csv(SAMPLE_CSV), build schema description
  |
write_query   <- LLM generates pandas expression from schema + question (+ error feedback on retry)
  |
execute_query <- eval(query_code, {"df": df, "pd": pd}), capture result or error
  |
  +-- error + iterations < MAX_ITERATIONS --> write_query  (retry loop)
  |
  +-- success or max retries reached ------> END
```
