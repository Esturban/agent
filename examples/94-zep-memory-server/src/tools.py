# Zep Cloud (getzep.com) — production memory layer for LLM applications.
#
# What Zep does automatically (vs. DIY Redis):
#   - Auto-summarizes conversation history when it grows long
#   - Extracts named entities (people, places, facts) into a searchable graph
#   - Applies temporal decay so stale facts matter less over time
#   - Returns a ready-to-inject `context` string for the system prompt
#
# Tradeoff summary:
#   Redis: full control, manual compaction, O(N) history scan
#   Zep:   batteries-included, managed memory, less raw control

# Sample multi-turn conversation to load into Zep memory before querying.
# This simulates a user who has chatted before — Zep will have summarized it.
SEED_CONVERSATION = [
    {"role": "user",      "content": "My name is Alex and I'm a backend engineer at a fintech startup."},
    {"role": "assistant", "content": "Hi Alex! Fintech is a fast-moving space. What stack are you using?"},
    {"role": "user",      "content": "Mostly Python — FastAPI, Celery, and PostgreSQL. We're evaluating moving to async queues."},
    {"role": "assistant", "content": "Async queues like RabbitMQ or Kafka could help with throughput. What's the bottleneck?"},
    {"role": "user",      "content": "Payment processing. We need to handle 10k transactions per minute during peak hours."},
    {"role": "assistant", "content": "At that scale Kafka is worth considering — it handles millions of events per second."},
]

# Follow-up queries that should benefit from memory context about Alex.
FOLLOW_UP_QUERIES = [
    "What was I working on last time we spoke?",
    "What database am I using?",
    "Given what you know about me, what memory solution would you recommend for my use case?",
]
