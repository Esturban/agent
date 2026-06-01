# 5-react-agent-lg

LangGraph ReAct agent with a two-node critique loop: a **Summarizer** drafts a PDF summary, a **Reviewer** grades it and suggests improvements, and the loop continues until the reviewer approves. Demonstrates multi-turn agent reasoning with `MemorySaver` checkpointing.

![State graph](./assets/stategraph.png)

```bash
python examples/5-react-agent-lg/main.py
```
