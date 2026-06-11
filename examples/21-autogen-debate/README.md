# 21-autogen-debate

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — topics are hardcoded inline
**Colab:** not applicable — requires pyautogen which conflicts with Colab's pre-installed packages

```bash
python examples/21-autogen-debate/main.py
```

Implements a **two-agent debate** using Microsoft AutoGen's `ConversableAgent`. A Proponent and an Opponent are each given a system prompt defining their stance, then argue back and forth via `initiate_chat` for `MAX_TURNS` (default: 4) exchanges. Demonstrates AutoGen's agent-to-agent communication model as a framework contrast to LangGraph's explicit StateGraph — here the turn loop is managed by the framework, not a graph.

---

### Agent Communication Flow

```
Proponent                              Opponent
    |                                      |
    +-- "Proposition: '...'. I argue FOR." ──► |
    |                                      |
    | ◄── [Counter-argument] ──────────────+
    |                                      |
    +── [Rebuttal] ────────────────────────►
    |                                      |
    ...  (MAX_TURNS = 4 exchanges)
    |                                      |
   END  (chat_history returned)
```
