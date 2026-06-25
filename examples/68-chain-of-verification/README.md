---
teaching_ready: true
---
# 68-chain-of-verification

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- sample questions inline in src/tools.py
**Colab:** not applicable -- requires local execution

```bash
python examples/68-chain-of-verification/main.py
```

Chain-of-Verification (Dhuliawala et al. 2023): reduces hallucination by forcing claim-level fact-checking. Generates an initial answer, extracts individual verifiable claims, checks each claim independently, then revises the answer to fix any failures.

---

### Graph

```
START
  |
generate          <- LLM produces initial answer
  |
plan_verification <- extract specific verifiable claims (ClaimList structured output)
  |
execute_verification <- verify each claim independently (ClaimVerification per claim)
  |
revise            <- rewrite answer replacing failed claims with corrections
  |
END
```
