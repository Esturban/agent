from pydantic_ai import Agent

from src.tools import ResearchResult

_agent = Agent(
    "openai:gpt-5.4-nano",
    result_type=ResearchResult,
    system_prompt=(
        "You are an expert researcher. Given a topic, produce a factual summary, "
        "3-5 key facts, and a confidence score between 0.0 and 1.0."
    ),
)


def run_agent(query: str) -> ResearchResult:
    result = _agent.run_sync(query)
    return result.data
