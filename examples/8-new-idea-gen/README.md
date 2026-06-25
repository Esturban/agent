---
teaching_ready: true
---
# 8-new-idea-gen

## Prerequisites
**Keys:** `OPENAI_API_KEY`, `BRAVE_API_KEY`
**Files:** none — fetches the free-for-dev list from GitHub at runtime

```bash
python examples/8-new-idea-gen/main.py
```

Two-stage pipeline: parse the [free-for-dev](https://github.com/ripienaar/free-for-dev) list from GitHub at runtime, then generate structured, scored ideas for agentic tools built on free APIs.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/8-new-idea-gen/new_idea_gen_workbook.ipynb)

---

### Graph

```
START
  ↓
parser          ← fetches free-for-dev markdown, extracts tool names/categories
  ↓
idea_generator  ← LLM proposes tool combinations with confidence scores
  ↓
END             → ideas_<timestamp>.json
```
