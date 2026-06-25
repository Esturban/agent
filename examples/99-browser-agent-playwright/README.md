---
teaching_ready: true
---
# 99 — Browser Agent (Playwright)

A ReAct agent that controls a real browser via Playwright to navigate pages, read content, and summarise — no scraping hacks needed.

**Install:** `pip install playwright && playwright install chromium`

**Env:** `OPENAI_API_KEY` in `.env`

**Run:** `python main.py`

The agent navigates `https://example.com`, extracts the page text using browser tools, and returns a 2–3 sentence summary. Foundation for web research agents and RPA automation.
