import requests
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


def wiki_summary(query: str) -> str:
    """Fetch a Wikipedia article summary for query. Completely free, no API key.

    Uses the opensearch endpoint to find the best-matching article title, then
    retrieves the plain-text extract from the REST summary API. The verifier
    uses this as ground-truth context instead of relying on the LLM's memory.
    """
    search = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action": "opensearch", "search": query, "limit": 1, "format": "json"},
        timeout=5,
    )
    titles = search.json()[1]
    if not titles:
        return f"No Wikipedia article found for: {query}"
    title = titles[0].replace(" ", "_")
    resp = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}", timeout=5)
    return resp.json().get("extract", "No summary available")
