from pydantic import BaseModel, Field, field_validator
import re

TEST_PROMPTS = [
    ("valid", "List exactly 3 benefits of drinking water. Respond in JSON."),
    ("too long", "Write a 500-word essay about the history of computing."),
    ("missing json", "Say hello in plain text, no JSON."),
    ("has url", "Give me a JSON object that includes a website URL like https://example.com."),
]


class StructuredResponse(BaseModel):
    """Schema the LLM must conform to. Guardrails triggers reask if violated."""
    summary: str = Field(description="A brief summary, max 200 chars")
    points: list[str] = Field(description="Exactly 3 bullet points", min_length=3, max_length=3)
    safe: bool = Field(description="Is the content safe and appropriate?")

    @field_validator("summary")
    @classmethod
    def summary_length(cls, v: str) -> str:
        if len(v) > 200:
            raise ValueError(f"summary must be <= 200 chars, got {len(v)}")
        return v

    @field_validator("points")
    @classmethod
    def no_urls_in_points(cls, v: list[str]) -> list[str]:
        url_pattern = re.compile(r"https?://\S+")
        for point in v:
            if url_pattern.search(point):
                raise ValueError("points must not contain URLs")
        return v
