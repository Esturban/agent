---
teaching_ready: true
---
# 51-deepeval-conversational

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
pip install deepeval
python examples/51-deepeval-conversational/main.py
```

DeepEval conversational metrics: KnowledgeRetention, ConversationCompleteness, ConversationRelevancy. Evaluates multi-turn chatbot conversations end-to-end and shows the score difference between stateful (with history) and stateless (no memory) chatbots.

---

### Graph

```
stateful:   turn 1 → turn 2 → turn 3   (full message history passed each turn)
stateless:  turn 1   turn 2   turn 3   (each turn sees only system prompt)

Both → ConversationalTestCase → deepeval.evaluate()
```

### Conversational metrics

| Metric | Measures | Fails when |
|--------|----------|-----------|
| KnowledgeRetention | Bot remembers facts from earlier turns | Bot forgets name/info after turn 3 |
| ConversationCompleteness | All user intents are addressed | Bot ignores part of multi-intent question |
| ConversationRelevancy | Replies stay on topic throughout | Bot goes off-topic mid-conversation |

### Key: ConversationalTestCase vs LLMTestCase

- `LLMTestCase` — single turn: one input → one output
- `ConversationalTestCase` — full conversation: list of `LLMTestCase` turns evaluated together
