# 14-sql-agent

ReAct agent that queries a local SQLite database using `create_react_agent`.
Seeds a sample sales table on first run -- no external DB needed.

```bash
python main.py
```

Try: "Which product had the highest total sales?" or "Show me all North region sales above $1000."
