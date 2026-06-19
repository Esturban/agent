# 109 - PII Redaction Pipeline

Bi-directional PII sanitization using Microsoft Presidio. Stage 1 scrubs names, emails, phone numbers, SSNs, and credit card numbers from documents *before* they reach the LLM — so PII never enters the model context. Stage 2 scrubs any PII the LLM leaks in its response before delivery to the user.

Requires `pip install presidio-analyzer presidio-anonymizer spacy && python -m spacy download en_core_web_lg`.

## Run

```bash
cp .env.example .env  # add OPENAI_API_KEY
pip install presidio-analyzer presidio-anonymizer spacy
python -m spacy download en_core_web_lg
python main.py
```
