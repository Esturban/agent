from dotenv import load_dotenv

load_dotenv()

from src.tools import SPECIALIST_TASKS
from src.workflow import create_workflow


def main():
    graph = create_workflow()

    for task in SPECIALIST_TASKS:
        question = task["question"]
        routed_to = None
        answer = None

        for update in graph.stream(
            {"question": question, "next": "", "answer": ""},
            stream_mode="updates",
        ):
            if "supervisor" in update:
                routed_to = update["supervisor"]["next"]
            for agent in ("math_agent", "history_agent", "science_agent"):
                if agent in update:
                    answer = update[agent]["answer"]

        print(f"Q: {question}")
        print(f"   Routed to : {routed_to}")
        print(f"   Answer    : {answer}")
        print()


if __name__ == "__main__":
    main()
