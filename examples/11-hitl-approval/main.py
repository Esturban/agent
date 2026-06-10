from dotenv import load_dotenv
from langgraph.types import Command
from src.workflow import create_workflow

load_dotenv()


def main():
    graph = create_workflow()
    # thread_id ties both .stream() calls to the same saved checkpoint.
    config = {"configurable": {"thread_id": "hitl-demo"}}

    print("Agent starting — drafting action...\n")

    # First .stream(): runs nodes until interrupt() fires mid-graph.
    # Unlike .invoke() which blocks until END, this yields a special
    # __interrupt__ event and stops, leaving state saved in the checkpointer.
    interrupted = None
    for chunk in graph.stream(
        {"action": "", "approved": False, "result": ""},
        config,
        stream_mode="updates",
    ):
        if "__interrupt__" in chunk:
            interrupted = chunk["__interrupt__"][0].value
            break
        for node, update in chunk.items():
            if update.get("action"):
                print(f"[{node}] drafted: {update['action']}")

    if not interrupted:
        print("No interrupt raised — graph ran to completion.")
        return

    print(f"\n[PAUSED] {interrupted['question']}")
    print(f"  Action: {interrupted['action']}")

    raw = input("\nApprove? [y/n]: ").strip().lower()
    approved = raw == "y"

    print(f"\nResuming with: {'APPROVED' if approved else 'REJECTED'}\n")

    # Second .stream() with Command(resume=...) picks up exactly where
    # the graph stopped. The checkpointer replays saved state, the
    # await_approval node re-runs, and interrupt() returns the decision.
    for chunk in graph.stream(Command(resume=approved), config, stream_mode="updates"):
        for node, update in chunk.items():
            if update.get("result"):
                print(f"[{node}] {update['result']}")

    print("\nDone.")


if __name__ == "__main__":
    main()
