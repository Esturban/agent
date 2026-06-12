from pydantic import BaseModel, Field

MAX_REVISIONS = 3

CONSTITUTION = [
    "Be factually accurate — do not state things that are false.",
    "Be concise — stay under 80 words.",
    "Use plain language — avoid jargon a non-expert would not understand.",
    "Be helpful — directly address the question asked.",
    "Cite sources or acknowledge uncertainty when making specific factual claims.",
]

SAMPLE_PROMPTS = [
    "Explain how the internet works.",
    "What causes inflation?",
]


class Critique(BaseModel):
    principle: str = Field(description="The constitutional principle being checked")
    violated: bool = Field(description="True if the response violates this principle")
    reason: str = Field(description="Explanation of why it is or is not violated")
