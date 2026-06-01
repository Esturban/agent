# 14-sql-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — SQLite database is created and seeded automatically on first run
**Colab:** ✅ use the workbook (`sql_workbook.ipynb`); the script requires an interactive terminal

ReAct agent that queries a local SQLite database using `create_react_agent`.
Seeds a sample sales table on first run -- no external DB needed.

## Run as a script

```bash
python main.py
```

Try: "Which product had the highest total sales?" or "Show me all North region sales above $1000."

## Run as a workbook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/14-sql-agent/sql_workbook.ipynb)

```bash
jupyter notebook examples/14-sql-agent/sql_workbook.ipynb
```

The notebook is fully self-contained -- walks through the ReAct loop, builds all three tools from scratch, includes exercises, and has an answer key at the end.
