from dotenv import load_dotenv

load_dotenv()

from src.tools import SESSION_1_MESSAGES, SESSION_2_QUERIES, USER_ID, format_memories  # noqa: E402
from src.workflow import _mem, create_workflow  # noqa: E402


def main() -> None:
    app = create_workflow()

    # Session 1: introduce the user and store facts
    print("=== SESSION 1: storing facts ===")
    print("Messages:")
    for msg in SESSION_1_MESSAGES:
        print(f"  [{msg['role']}] {msg['content']}")

    app.invoke({
        "user_id": USER_ID,
        "query": "Introduce yourself",
        "recalled": [],
        "answer": "",
        "messages": SESSION_1_MESSAGES,
    })

    # Memory dump: show what Mem0 extracted automatically
    all_memories = _mem.get_all(user_id=USER_ID)
    memories_list = all_memories.get("results", all_memories) if isinstance(all_memories, dict) else all_memories
    print(f"\nMem0 extracted {len(memories_list)} memories automatically:")
    print(format_memories(memories_list))

    # Session 2: fresh invocation, no messages passed — relies entirely on recall
    print("\n=== SESSION 2: recalling facts (no messages passed) ===")
    for query in SESSION_2_QUERIES:
        result = app.invoke({
            "user_id": USER_ID,
            "query": query,
            "recalled": [],
            "answer": "",
            "messages": [],
        })
        print(f"\nQ: {query}")
        print(f"A: {result['answer']}")

    print("\n[Compare to 36-long-term-memory: Mem0 extracts facts automatically;")
    print(" LangGraph InMemoryStore requires explicit key-value writes.]")


if __name__ == "__main__":
    main()
