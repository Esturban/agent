import os
import uuid

from dotenv import load_dotenv

load_dotenv()

from src.tools import FOLLOW_UP_QUERIES, SEED_CONVERSATION  # noqa: E402
from src.workflow import create_workflow                      # noqa: E402


def _seed_session(session_id: str, user_id: str) -> None:
    """Load past conversation turns into Zep before running queries.

    This simulates a returning user — Zep will have already summarized and
    extracted entities from these turns by the time we query memory.
    """
    from zep_cloud.client import Zep
    from zep_cloud.types import Message

    zep = Zep(api_key=os.environ["ZEP_API_KEY"])

    # Create the session and attach it to the user.
    try:
        zep.memory.add_session(session_id=session_id, user_id=user_id)
    except Exception:
        pass  # session may already exist

    messages = [
        Message(
            role=turn["role"],
            role_type=turn["role"],
            content=turn["content"],
        )
        for turn in SEED_CONVERSATION
    ]
    zep.memory.add(session_id=session_id, messages=messages)
    print(f"Seeded {len(messages)} turns into session {session_id[:8]}...\n")


def main() -> None:
    print("=== 94 · Zep Memory Server ===")
    print("Docs: getzep.com | Requires: ZEP_API_KEY\n")
    print("Zep auto-summarizes history, extracts entities, and returns a compressed context string.\n")

    # Use a stable session ID so re-runs accumulate memory across calls.
    USER_ID    = "demo-user-94"
    SESSION_ID = f"session-{USER_ID}"

    app = create_workflow()

    print("--- Seeding past conversation ---")
    _seed_session(SESSION_ID, USER_ID)

    print("--- Running follow-up queries ---\n")
    for query in FOLLOW_UP_QUERIES:
        print(f"Query: {query}")

        result = app.invoke({
            "user_id":    USER_ID,
            "session_id": SESSION_ID,
            "query":      query,
            "context":    "",
            "response":   "",
        })

        # Show whether Zep provided memory context.
        if result["context"]:
            preview = result["context"][:150].replace("\n", " ")
            print(f"Zep context injected: {preview}...")
        else:
            print("Zep context: (empty — memory not ready yet)")

        print(f"Response: {result['response']}")
        print("-" * 60)

    print("\nNote: Zep summarizes history asynchronously. Re-run after a few seconds")
    print("to see the compressed `context` field populated with entity facts.")


if __name__ == "__main__":
    main()
