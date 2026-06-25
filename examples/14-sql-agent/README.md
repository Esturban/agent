---
teaching_ready: true
---
# 14-sql-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — SQLite database is seeded automatically on first run

```bash
python examples/14-sql-agent/main.py
```

ReAct agent over a local SQLite database using `create_react_agent`. Seeds a sample sales table on first run — no external DB needed.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/14-sql-agent/sql_workbook.ipynb)

---

### Graph

```
START
  ↓
agent   ← ReAct loop: reason → call tool → observe
  ↓
  ├─ tool: list_tables    ← list available tables
  ├─ tool: describe_table ← schema of a specific table
  ├─ tool: run_sql        ← execute a SQL query
  ↓
END
```
