# 51-deepeval-conversational

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/51-deepeval-conversational/conversational_eval_workbook.ipynb)

DeepEval conversational metrics: KnowledgeRetention, ConversationCompleteness, ConversationRelevancy. Evaluates multi-turn chatbot conversations end-to-end and shows the score difference between stateful (with history) and stateless (no memory) chatbots.

**Keys:** `OPENAI_API_KEY`

```bash
pip install deepeval
python examples/51-deepeval-conversational/main.py
```

---

### Conversational metrics

| Metric | Measures | Fails when |
|--------|----------|-----------|
| KnowledgeRetention | Bot remembers facts from earlier turns | Bot forgets name/info after turn 3 |
| ConversationCompleteness | All user intents are addressed | Bot ignores part of multi-intent question |
| ConversationRelevancy | Replies stay on topic throughout | Bot goes off-topic mid-conversation |

### Key: ConversationalTestCase vs LLMTestCase

- `LLMTestCase` — single turn: one input → one output
- `ConversationalTestCase` — full conversation: list of `LLMTestCase` turns evaluated together
