from dotenv import load_dotenv

load_dotenv()

from src.tools import DEBATE_TOPICS  # noqa: E402
from src.workflow import run_debate  # noqa: E402


def main():
    topic = DEBATE_TOPICS[0]
    print(f"\n{'=' * 60}")
    print(f"Proposition: {topic}")
    print(f"{'=' * 60}\n")

    history = run_debate(topic)

    for msg in history:
        name = msg.get("name") or msg.get("role", "unknown")
        content = msg.get("content", "")
        if content:
            print(f"[{name.upper()}]\n{content}\n")


if __name__ == "__main__":
    main()
