import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

from src.tools import EXPECTED_FIX, TASK_PROMPT, format_result  # noqa: E402
from src.workflow import SWEAgent  # noqa: E402

SANDBOX_MODES = """
┌──────────────────────────┬───────────────────────────┬────────────────────────┐
│ Provider                 │ Shell access              │ Use case               │
├──────────────────────────┼───────────────────────────┼────────────────────────┤
│ LocalSandboxProvider     │ File tools only (no bash) │ Dev / low-risk tasks   │
│ AioSandboxProvider       │ Containerised bash        │ CI-style coding tasks  │
└──────────────────────────┴───────────────────────────┴────────────────────────┘
⚠  Never expose DeerFlow's sandbox endpoint on an untrusted network.
"""

BASE_URL = os.getenv("DEERFLOW_BASE_URL", "http://localhost:8000")
THREAD_ID = "demo-thread-136"
FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "buggy_repo"


def main() -> None:
    print("=== 136 · DeerFlow Sandboxed SWE Agent ===\n")
    print(SANDBOX_MODES)

    agent = SWEAgent(base_url=BASE_URL, thread_id=THREAD_ID)

    print("── Upload buggy repo ──")
    try:
        for name in ["calculator.py", "test_calculator.py"]:
            content = (FIXTURES / name).read_text()
            print(f"  {name} → {agent.upload(name, content)}")
    except Exception as exc:
        print(f"  [failed: {exc}]\n  → Is DeerFlow running? See runtime/README.md")
        return

    print(f"\n── Bug state (before) ──\n  add(2, 3) → 2  ✗  (returns a − b)")
    print(f"\n── Run SWE agent ──\n  {TASK_PROMPT[:88]}…\n")

    events: list[tuple[str, dict]] = []
    for et, data in agent.stream(TASK_PROMPT):
        events.append((et, data))
        if et == "message_chunk":
            print(data.get("content", ""), end="", flush=True)
        elif et == "end":
            print()

    result = format_result(events)
    fixed = EXPECTED_FIX in result
    print(f"\n── Fix verified ──  {'✓ PASS' if fixed else '? check output above'}")
    print(f"   looking for: {EXPECTED_FIX!r}  found: {fixed}")

    counts: dict[str, int] = {}
    for et, _ in events:
        counts[et] = counts.get(et, 0) + 1
    print(f"\n── Summary ──  thread={THREAD_ID}  events={counts}")


if __name__ == "__main__":
    main()
