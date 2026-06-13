from dotenv import load_dotenv

load_dotenv()

from src.tools import SESSION_MESSAGES, USER_ID, get_redis_client  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()
    r = get_redis_client()

    # Flush prior run data so each demo starts fresh
    r.delete(f"history:{USER_ID}")

    # Seed Redis with prior conversation context
    import json
    key = f"history:{USER_ID}"
    for msg in SESSION_MESSAGES:
        r.rpush(key, json.dumps(msg))

    queries = [
        "What's my name and what do I love?",
        "What editor do I use?",
        "What am I learning this week?",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n=== Session {i} ===")
        history_len = r.llen(key)
        print(f"[Redis has {history_len} turns in history]")
        result = app.invoke({
            "user_id": USER_ID,
            "query": query,
            "history": [],
            "answer": "",
        })
        print(f"Q: {query}")
        print(f"A: {result['answer']}")


if __name__ == "__main__":
    main()
