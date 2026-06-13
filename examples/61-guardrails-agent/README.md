# 61-guardrails-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- test queries are inline in src/tools.py
**Colab:** not applicable -- requires local execution

```bash
python examples/61-guardrails-agent/main.py
```

Guardrails Agent: validates input queries with a Pydantic-enforced `InputGuard` (on-topic + PII check) and output responses with `OutputGuard` (word limit + factuality). Off-topic queries or PII-containing inputs are blocked before reaching the agent. Includes deliberate failures: SSN query gets blocked, off-topic blocked, valid coding queries pass through.

---

### Graph

```
START
  |
validate_input   <- InputGuard classifier (is_on_topic, contains_pii)
  |
  +-- blocked --> blocked node --> END
  |
  +-- passed --> agent (ChatOpenAI coding assistant)
                  |
              validate_output  <- OutputGuard (word_count, passes)
                  |
                 END
```
