# 117-instructor-extraction

## Prerequisites
**Keys:** `OPENAI_API_KEY` in `.env`
**Deps:** `pip install instructor`
**Colab:** see workbook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/117-instructor-extraction/instructor_extraction_workbook.ipynb)

```bash
python examples/117-instructor-extraction/main.py
```

`instructor` is a thin wrapper around any OpenAI-compatible client that adds Pydantic
model validation and automatic retry on `ValidationError`. This example extracts 3 typed
models — `MeetingNotes`, `ProductReview`, `UserAddress` — from real sample texts,
demonstrating how instructor turns unstructured text into type-safe Python objects.

---

### Pattern

```
client = instructor.from_openai(OpenAI())

result = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=MeetingNotes,   # <-- Pydantic model
    max_retries=3,                 # <-- auto-retry on ValidationError
    messages=[...]
)
# result is a validated MeetingNotes instance, not a string
```
