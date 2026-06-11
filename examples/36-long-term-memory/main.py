from dotenv import load_dotenv
from src.tools import CONVERSATIONS
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for thread_id, messages in CONVERSATIONS:
        print(f"\n{'=' * 60}\nThread: {thread_id}")
        state = {
            "thread_id": thread_id,
            "messages": messages,
            "memories": [],
            "response": "",
        }
        result = app.invoke(state)
        print(f"Memories retrieved: {result['memories']}")
        print(f"Response: {result['response'][:200]}")


if __name__ == "__main__":
    main()
