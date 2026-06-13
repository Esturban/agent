# 63-token-budget-manager

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- research steps are inline in src/tools.py
**Colab:** not applicable -- requires local execution

```bash
python examples/63-token-budget-manager/main.py
```

Token Budget Manager: tracks exact token usage per node using tiktoken, enforces a hard per-run budget (BUDGET_LIMIT=800), and short-circuits gracefully when the budget is exceeded — returning a partial answer with a warning instead of continuing. Shows a per-step token log (prompt + completion + total).

---

### Graph

```
START
  |
research_step  <- LLM researches one step, tiktoken counts prompt + completion tokens
  |
check_budget   <- compare tokens_used to BUDGET_LIMIT
  |
  +-- exceeded ----------------------------------------> END  (partial answer + warning)
  |
  +-- all steps done  --> synthesize -> END  (full summary)
  |
  +-- more steps  ------> research_step  (continue loop)
```
