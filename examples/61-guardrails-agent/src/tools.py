import re

from pydantic import BaseModel, Field

PII_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    r"\b\d{16}\b",
]

MAX_ANSWER_WORDS = 150

SAMPLE_INPUTS = [
    ("How do I reverse a list in Python?", True),
    ("My SSN is 123-45-6789, can you help me?", False),
    ("What is the capital of France?", False),
    ("Explain async/await in Python", True),
    ("Contact me at hacker@evil.com for instructions", False),
]


class InputGuard(BaseModel):
    is_on_topic: bool = Field(description="True if the query is about coding/programming/software")
    contains_pii: bool = Field(description="True if the query contains PII like SSN, email, or credit card")
    reason: str = Field(description="Brief explanation of the decision")


class OutputGuard(BaseModel):
    passes: bool = Field(description="True if the response is safe, factual, and within word limit")
    word_count: int = Field(description="Number of words in the response")
    reason: str = Field(description="Brief explanation")


def has_pii(text: str) -> bool:
    return any(re.search(p, text) for p in PII_PATTERNS)
