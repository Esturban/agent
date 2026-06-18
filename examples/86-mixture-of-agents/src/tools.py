# Wang et al. 2024 — "Mixture-of-Agents Enhances Large Language Model Capabilities"
# arxiv.org/abs/2406.04692
#
# Core insight: aggregating outputs from multiple independent LLMs beats any single model.
# Even if each proposer is the same model, different system prompts = different perspectives.

SAMPLE_QUESTIONS = [
    "What are the most important skills for a software engineer to develop in 2025?",
    "Explain the tradeoffs between microservices and a monolithic architecture.",
    "What makes a great code review? Give specific practices.",
]

# Three proposers with distinct analytical lenses.
# In a real MoA deployment: use different model providers for true diversity.
# Here: same gpt-4o-mini, different system prompts — demonstrates the pattern cheaply.
PERSONAS = [
    {
        "name": "pragmatist",
        "system": (
            "You are a pragmatic senior engineer with 15 years of production experience. "
            "Focus on what actually works in real teams. Be concrete and opinionated."
        ),
    },
    {
        "name": "theorist",
        "system": (
            "You are a computer science researcher who bridges theory and practice. "
            "Ground your answer in first principles and relevant research findings."
        ),
    },
    {
        "name": "educator",
        "system": (
            "You are a technical educator who teaches engineers at all levels. "
            "Prioritise clarity, analogies, and a progression from simple to complex."
        ),
    },
]
