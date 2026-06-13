import redis

USER_ID = "demo-user-001"
REDIS_URL = "redis://localhost:6379"
SESSION_MESSAGES = [
    {"role": "user", "content": "Hi, I'm Alice. I love hiking and Python."},
    {"role": "assistant", "content": "Nice to meet you, Alice!"},
    {"role": "user", "content": "My favourite editor is Neovim."},
    {"role": "assistant", "content": "Great choice — Neovim is very powerful."},
    {"role": "user", "content": "I'm learning LangGraph this week."},
]


def get_redis_client() -> redis.Redis:
    return redis.from_url(REDIS_URL, decode_responses=True)
