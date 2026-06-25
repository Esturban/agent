---
teaching_ready: true
---
# 3-prospect-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY` (optional: `BRAVE_API_KEY`, `OPENROUTER_API_KEY`)
**Files:** `data/Connections.csv` — a sample is at `examples/3-prospect-agent/data/sample_connections.csv`

```bash
python examples/3-prospect-agent/main.py --input examples/3-prospect-agent/data/sample_connections.csv
```

Prospect research agent: reads LinkedIn connections from a CSV, searches the web for each person, and writes a personalized outreach message with a confidence score.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/3-prospect-agent/prospect_agent_workbook.ipynb)

Output is written to `data/aug/connections_aug_<timestamp>.csv`.

---

### Graph

```
START
  ↓
researcher   ← web search per prospect, extracts facts and source URLs
  ↓
copywriter   ← LLM writes personalized outreach with confidence score
  ↓
END
```