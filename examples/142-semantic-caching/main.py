import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from src.workflow import create_workflow

load_dotenv()

QUERIES = [
    "What is machine learning?",
    "Can you explain machine learning to me?",
    "What is deep learning?",
    "How does deep learning work?",
    "What is machine learning?",
    "Tell me about reinforcement learning.",
    "Explain reinforcement learning please.",
]

if __name__ == "__main__":
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    workflow = create_workflow()
    config = {"configurable": {"client": client}}

    result = workflow.invoke({
        "queries": QUERIES,
        "threshold": 0.92,
        "responses": [],
        "cache_stats": {},
    }, config=config)

    print("=== Semantic Cache Demo ===\n")
    for r in result["responses"]:
        label = "[CACHE HIT]" if r["source"] == "cache" else f"[LLM {r['latency_ms']}ms]"
        print(f"{label} Q: {r['query']}")
        print(f"  A: {r['response'][:80]}...\n")

    print(f"Stats: {json.dumps(result['cache_stats'], indent=2)}")
