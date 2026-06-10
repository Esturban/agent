# 6-multi-agent-graph

Two specialist agents in a single LangGraph: **ProductQnA** answers product questions, **OrdersAgent** handles order lookup and quantity updates. A supervisor node routes messages between them based on intent.

**Keys:** `OPENAI_API_KEY`
**Files:** `data/product/Laptop pricing.csv` · `data/product/Laptop Orders.csv` · `data/product/Laptop product descriptions.pdf`

```bash
python examples/6-multi-agent-graph/main.py
```
