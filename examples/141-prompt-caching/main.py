import json
import os
from dotenv import load_dotenv
import anthropic
from src.workflow import create_workflow

load_dotenv()

SYSTEM_PROMPT = """You are an expert on the Python programming language with deep knowledge of:
- Language specification and PEPs
- Standard library internals
- CPython implementation details
- Performance optimization techniques
- Concurrency patterns (threading, asyncio, multiprocessing)
- Packaging, testing, and deployment best practices
Answer questions accurately and concisely."""

QUESTIONS = [
    "What is the GIL and how does it affect multithreading?",
    "Explain the difference between __str__ and __repr__.",
    "How does Python's garbage collector handle circular references?",
    "What are descriptors and how do properties use them?",
]

if __name__ == "__main__":
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    workflow = create_workflow()
    config = {"configurable": {"client": client}}

    result = workflow.invoke({
        "system_prompt": SYSTEM_PROMPT,
        "questions": QUESTIONS,
        "uncached_results": [],
        "cached_results": [],
        "savings": {},
    }, config=config)

    print("=== Cache Benchmark Results ===\n")
    for i, (unc, cac) in enumerate(zip(result["uncached_results"], result["cached_results"])):
        print(f"Q{i+1}: {QUESTIONS[i]}")
        print(f"  Uncached: {unc['input_tokens']} tokens, {unc['latency_ms']}ms")
        print(f"  Cached:   {cac['input_tokens']} billed ({cac['cache_read']} from cache), {cac['latency_ms']}ms\n")

    print(f"Savings summary:\n{json.dumps(result['savings'], indent=2)}")
