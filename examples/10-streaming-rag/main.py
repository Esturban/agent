from dotenv import load_dotenv
from src.workflow import create_workflow

load_dotenv()


def main():
    graph = create_workflow()
    question = "What is a Python list and how do you use it?"

    print(f"Question: {question}")
    print("=" * 60)
    print("Streaming node-by-node (stream_mode='updates'):\n")

    # .stream() with stream_mode="updates" yields {node_name: update} for each
    # node as it finishes -- contrast with .invoke() which blocks until the end.
    for chunk in graph.stream(
        {"question": question, "context": "", "answer": ""},
        stream_mode="updates",
    ):
        for node_name, update in chunk.items():
            print(f"[{node_name}]")
            if "context" in update and update["context"]:
                preview = update["context"][:120].replace("\n", " ")
                print(f"  context: {preview}...")
            if "answer" in update:
                print(f"  answer: {update['answer']}")
            print()

    print("=" * 60)


if __name__ == "__main__":
    main()
