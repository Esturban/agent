# 14-sql-agent

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/14-sql-agent/sql_workbook.ipynb)

ReAct agent over a local SQLite database using `create_react_agent`. Seeds a sample sales table on first run — no external DB needed. The workbook walks through the full ReAct loop, builds all three tools from scratch, includes exercises, and has an answer key.

**Keys:** `OPENAI_API_KEY`

```bash
# local notebook (recommended)
jupyter notebook examples/14-sql-agent/sql_workbook.ipynb

# or run the script
python examples/14-sql-agent/main.py
```

Try: *"Which product had the highest total sales?"* or *"Show me all North region sales above $1000."*
