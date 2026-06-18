from dotenv import load_dotenv

from src.tools import setup_workspace
from src.workflow import create_workflow

load_dotenv()


def main() -> None:
    workspace = setup_workspace()
    task = (
        f"Workspace: {workspace}\n"
        f"Files: {workspace}/buggy.py (contains bugs) and {workspace}/test_buggy.py (failing tests).\n"
        "Fix all bugs in buggy.py so that every test in test_buggy.py passes."
    )

    print("Workspace:", workspace)
    print("=" * 60)

    app = create_workflow()
    result = app.invoke({"messages": [{"role": "user", "content": task}]})

    for msg in result["messages"]:
        role = getattr(msg, "type", "?")
        content = str(getattr(msg, "content", ""))
        if not content:
            continue
        if role == "ai":
            print(f"\n[agent] {content[:400]}")
        elif role == "tool":
            print(f"  [tool] {content[:200]}")

    print("\n" + "=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
