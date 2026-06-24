import os

from dotenv import load_dotenv

load_dotenv()

from src.tools import REPORT_PROMPT_DEEP, SOURCE_FILES  # noqa: E402
from src.workflow import ResearchRun  # noqa: E402

BASE_URL = os.getenv("DEERFLOW_BASE_URL", "http://localhost:8000")
THREAD_ID = "demo-thread-135"
_ICONS = {"message_chunk": "·", "tool_call": "⚙", "tool_result": "✓", "end": "■"}


def main() -> None:
    print("=== 135 · DeerFlow Research Skill ===\n")
    run = ResearchRun(base_url=BASE_URL, thread_id=THREAD_ID)

    print("── Upload source files ──")
    try:
        for filename, content in SOURCE_FILES.items():
            print(f"  {filename} → {run.upload(filename, content)}")
    except Exception as exc:
        print(f"  [failed: {exc}]\n  → Is DeerFlow running? See runtime/README.md")
        return

    print(f"\n── Activate skill ──  plan_mode=True  subagent_enabled=True")
    print(f"  {REPORT_PROMPT_DEEP!r}\n")

    events: list[tuple[str, dict]] = []
    for et, data in run.stream(REPORT_PROMPT_DEEP):
        events.append((et, data))
        icon = _ICONS.get(et, "?")
        if et == "message_chunk":
            print(f"  {icon} {data.get('content', '')}", end="", flush=True)
        elif et in ("tool_call", "tool_result", "end"):
            print(f"\n  {icon} [{et}]")

    if artifact := run.artifact_path(events):
        print(f"\n── Report artifact ──\n  {artifact}")

    counts: dict[str, int] = {}
    for et, _ in events:
        counts[et] = counts.get(et, 0) + 1
    print(f"\n── Summary ──  thread={THREAD_ID}  events={counts}")


if __name__ == "__main__":
    main()
