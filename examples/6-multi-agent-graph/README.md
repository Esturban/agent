# 6-multi-agent-graph

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** `data/product/Laptop pricing.csv` · `data/product/Laptop Orders.csv` · `data/product/Laptop product descriptions.pdf`
**Colab:** ⚠️ upload the `data/product/` files to your Colab session before running

Two specialist agents wired into a single LangGraph: a **ProductQnA** agent answers product questions and an **OrdersAgent** handles order lookup and quantity updates. A supervisor routes messages between them. Demonstrates how to compose independent agents into one graph with shared state.

```bash
python examples/6-multi-agent-graph/main.py
```
