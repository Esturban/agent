import os

MAX_TURNS = 4  # back-and-forth exchanges between agents

DEBATE_TOPICS = [
    "Remote work is more productive than in-office work",
    "AI will create more jobs than it eliminates",
    "Open-source software is safer than proprietary software",
]


def get_llm_config() -> dict:
    """Build AutoGen LLM config dict from environment."""
    return {
        "model": "gpt-5-nano",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
