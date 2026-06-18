# Three memory tiers — cognitive science taxonomy applied to LLM agents.
# Ref: Tulving (1972) memory taxonomy; MemGPT (Packer et al. 2023, arxiv 2310.08560)
#
# Episodic  — *what happened* (ordered event log; retrieved by recency)
# Semantic  — *what is true about the world/user* (key-value facts; retrieved by key)
# Procedural — *how to behave* (rules/patterns; always prepended to system prompt)
#
# In production: episodic → Redis list, semantic → KV store, procedural → config file.
# Here: all three live in LangGraph state — the pattern is what matters.

from typing import TypedDict


class MemoryStore(TypedDict):
    """Three-tier memory store held in LangGraph state."""
    episodic:   list[str]       # ordered event log
    semantic:   dict[str, str]  # user facts: {"name": "Alex", "role": "ML engineer"}
    procedural: list[str]       # behavioural rules the agent always follows


# Seed data — a returning user whose preferences are already known.
INITIAL_MEMORY: MemoryStore = {
    "episodic": [
        "User asked about Python best practices.",
        "Agent recommended PEP 8 and type hints.",
    ],
    "semantic": {
        "name": "Jordan",
        "role": "product manager",
        "prefers": "bullet-point summaries over prose",
        "company": "Series-B fintech startup",
    },
    "procedural": [
        "Always respond with bullet points when summarising.",
        "When asked about timelines: ask about team size and blockers first.",
        "Keep responses under 150 words unless user asks for more detail.",
    ],
}

# Test queries that exercise different memory tiers.
DEMO_QUERIES = [
    "What's my name and what do I do?",            # semantic lookup
    "Summarise our conversation history.",          # episodic recall
    "I need help estimating a project timeline.",   # procedural rule applies
    "What do you know about me?",                   # semantic + episodic
]
