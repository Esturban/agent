# 5-react-agent-lg

LangGraph ReAct agent with a two-node critique loop: a **Summarizer** drafts a PDF summary, a **Reviewer** grades it and suggests improvements, and the loop continues until approved. Demonstrates multi-turn agent reasoning with `MemorySaver` checkpointing.

**Keys:** `OPENAI_API_KEY`
**Files:** `data/product/EcoSprint_Specification_Document.pdf`

```bash
python examples/5-react-agent-lg/main.py
```

![State graph](./assets/stategraph.png)
