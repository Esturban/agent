from agents import Agent, handoff

from .tools import keyword_search

MODEL = "gpt-4o-mini"


def create_triage_agent() -> Agent:
    researcher = Agent(
        name="Researcher",
        model=MODEL,
        instructions=(
            "You answer factual questions about the OpenAI Agents SDK. "
            "Always call keyword_search first to retrieve relevant facts, "
            "then compose a clear 2-3 sentence answer."
        ),
        tools=[keyword_search],
    )

    writer = Agent(
        name="Writer",
        model=MODEL,
        instructions=(
            "You receive research findings and rewrite them as a polished, "
            "readable paragraph suitable for a technical blog post."
        ),
    )

    triage = Agent(
        name="Triage",
        model=MODEL,
        instructions=(
            "Route the user's request: "
            "if they ask a factual question, hand off to Researcher. "
            "If they ask to explain, summarize, or write something, hand off to Writer. "
            "Do not answer directly — always hand off."
        ),
        handoffs=[handoff(researcher), handoff(writer)],
    )

    return triage
