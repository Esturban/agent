from dotenv import load_dotenv

from src.tools import STATEFUL_CONVERSATION
from src.workflow import run_stateful_chat, run_stateless_chat


def main():
    load_dotenv()
    print("Running stateful conversation...\n")
    stateful = run_stateful_chat(STATEFUL_CONVERSATION)
    for turn in stateful:
        prefix = "User:" if turn["role"] == "user" else "Bot: "
        print(f"{prefix} {turn['content'][:120]}")
    print("\n--- Stateless version ---")
    stateless = run_stateless_chat(STATEFUL_CONVERSATION)
    for turn in stateless[-4:]:
        prefix = "User:" if turn["role"] == "user" else "Bot: "
        print(f"{prefix} {turn['content'][:120]}")


if __name__ == "__main__":
    main()
