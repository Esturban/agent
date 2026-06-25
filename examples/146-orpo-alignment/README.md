---
teaching_ready: true
---
# 146 — ORPO Alignment

Fine-tunes a small LLM using ORPO (Odds Ratio Preference Optimization) — a single-pass alignment method that combines SFT loss with a preference penalty, requiring no reference model. Measures preference rate before and after training.

**Run:** `python main.py` — requires Colab T4; install `trl` (`pip install trl`)
