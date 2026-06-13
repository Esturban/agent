from pydantic import BaseModel, Field


class ClaimList(BaseModel):
    claims: list[str] = Field(description="List of specific, verifiable factual claims extracted from the answer")


class ClaimVerification(BaseModel):
    claim: str = Field(description="The claim being verified")
    correct: bool = Field(description="True if the claim is factually accurate")
    correction: str = Field(description="The correct information if the claim is wrong, else empty string")


SAMPLE_QUESTIONS = [
    "Tell me about Albert Einstein: when was he born, what nationality was he, and what did he win the Nobel Prize for?",
    "What year was Python created, who created it, and what was its first major release?",
]
