# 8-new-idea-gen

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/8-new-idea-gen/new_idea_gen_workbook.ipynb)

Two-stage pipeline: parse the [free-for-dev](https://github.com/ripienaar/free-for-dev) list from GitHub at runtime, then generate structured, scored ideas for agentic tools built on free APIs.

**Keys:** `OPENAI_API_KEY` · `BRAVE_API_KEY`
**Files:** none — fetches the list from GitHub at runtime

```bash
python examples/8-new-idea-gen/main.py

# Custom output location
python examples/8-new-idea-gen/main.py --output data/ideas/my_ideas
```

Output is a JSON file with ideas, confidence scores, effort level, and next steps.

---

### Pipeline

```
free-for-dev list (GitHub URL)
  |
Parser Agent     <- extracts tool names and categories from markdown
  |
Idea Generator   <- LLM proposes tool combinations with confidence scores
  |
ideas_<timestamp>.json
```
