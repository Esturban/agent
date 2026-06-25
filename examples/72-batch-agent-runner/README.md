---
teaching_ready: true
---
# 72-batch-agent-runner

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- 9 sample tasks are inline in src/tools.py
**Colab:** not applicable -- requires local execution

```bash
python examples/72-batch-agent-runner/main.py
```

Batch Agent Runner: processes 9 tasks in parallel batches of 3 using `asyncio.gather`. Each task retries up to MAX_RETRIES=3 times with exponential backoff on failure. Batches run sequentially to respect rate limits — only BATCH_SIZE concurrent requests at once. Shows per-task status (OK/error), attempt count, and a completion summary.

---

### Graph

```
SAMPLE_TASKS (9 tasks)
  |
split into batches of BATCH_SIZE=3
  |
for each batch:
  asyncio.gather(*[process_task(llm, task, idx) for task in batch])
    |
    process_task: ainvoke -> on error -> exponential backoff -> retry up to MAX_RETRIES
  |
collect results -> print summary
```
