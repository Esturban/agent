import os

from dotenv import load_dotenv

load_dotenv()

from src.tools import SAMPLE_CORPUS, SAMPLE_QUERIES, format_event  # noqa: E402
from src.workflow import DeerFlowClient  # noqa: E402

# What each approach hands to the caller vs. keeps internally.
CONTRAST = """
┌─────────────────┬────────────────────────────────┬─────────────────────────┐
│ Approach        │ How you drive it               │ Runtime owns            │
├─────────────────┼────────────────────────────────┼─────────────────────────┤
│ LangGraph       │ app.invoke(state) — own graph  │ Nothing                 │
│ Google ADK      │ runner.run_async() — ADK loop  │ Tool-call loop          │
│ DeerFlow client │ client.stream() → events       │ Skills, memory, tools   │
└─────────────────┴────────────────────────────────┴─────────────────────────┘
"""

BASE_URL = os.getenv("DEERFLOW_BASE_URL", "http://localhost:8000")
THREAD_ID = "demo-thread-134"


def main() -> None:
    print("=== 134 · DeerFlow Embedded Client ===\n")
    print(CONTRAST)
    client = DeerFlowClient(base_url=BASE_URL, thread_id=THREAD_ID)

    print("── Upload corpus ──")
    try:
        artifact_id = client.upload("course-notes.md", SAMPLE_CORPUS)
        print(f"  artifact_id: {artifact_id}\n")
    except Exception as exc:
        print(f"  [failed: {exc}]\n  → Is DeerFlow running? See runtime/README.md")
        return

    query = SAMPLE_QUERIES[0]
    print(f"── Stream (plan_mode=True) ──\nQ: {query}\n")
    events: list[tuple[str, dict]] = []
    for et, data in client.stream(query, plan_mode=True):
        events.append((et, data))
        if line := format_event(et, data).strip():
            print(f"  {line}")

    query2 = SAMPLE_QUERIES[1]
    print(f"\n── Blocking chat ──\nQ: {query2}\nA: {client.chat(query2)}")

    counts = {et: sum(1 for e, _ in events if e == et) for et, _ in events}
    print(f"\n── Summary ──  thread={THREAD_ID}  events={counts}")


if __name__ == "__main__":
    main()
