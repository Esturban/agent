# 4-basic-react-agent

ReAct agent with two tools: semantic search over a CSV pricing table and PDF retrieval from a product spec document. Maintains full conversation history across turns with `MemorySaver`.

**Keys:** `OPENAI_API_KEY`
**Files:** `data/product/Laptop pricing.csv` · `data/product/Laptop product descriptions.pdf`

```bash
python examples/4-basic-react-agent/main.py
```