import os
from dotenv import load_dotenv

from src.tools import TASK
from src.workflow import create_workflow

load_dotenv()

if not os.environ.get("OPENAI_API_KEY", "").startswith("sk-"):
    raise RuntimeError("OPENAI_API_KEY is required for the browser agent.")


def main():
    graph = create_workflow()
    result = graph.invoke({"messages": [{"role": "user", "content": TASK}]})
    final = result["messages"][-1]
    print(final.content)


if __name__ == "__main__":
    main()
