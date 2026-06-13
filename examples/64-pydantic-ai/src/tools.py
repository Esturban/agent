from pydantic import BaseModel, Field


class ResearchResult(BaseModel):
    topic: str = Field(description="The research topic")
    summary: str = Field(description="A 2-3 sentence factual summary")
    key_facts: list[str] = Field(description="3-5 key bullet-point facts")
    confidence: float = Field(description="Confidence level 0.0-1.0", ge=0.0, le=1.0)


RESEARCH_QUERIES = [
    "The invention of the transformer architecture in machine learning",
    "How gradient descent works in neural networks",
    "The difference between supervised and unsupervised learning",
]
