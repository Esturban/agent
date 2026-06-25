import os
from dotenv import load_dotenv
from openai import OpenAI
from src.workflow import create_workflow

load_dotenv()

SAMPLE_CHUNKS = [
    "The Python programming language was created by Guido van Rossum and first released in 1991. "
    "Python's design philosophy emphasizes code readability with the use of significant indentation. "
    "It supports multiple programming paradigms, including structured, object-oriented, and functional programming.",

    "Python is dynamically typed and garbage-collected. It features a comprehensive standard library. "
    "The language is often described as batteries included due to this comprehensive library. "
    "Python consistently ranks as one of the most popular programming languages worldwide.",

    "CPython is the reference implementation of Python. When people refer to Python they often mean CPython. "
    "Other implementations include PyPy, Jython, and IronPython. "
    "CPython is an interpreter that compiles Python to bytecode before executing it. "
    "The GIL in CPython prevents true parallel execution of Python threads.",

    "Python 3 was released in 2008 and is incompatible with Python 2 in several ways. "
    "Python 2 reached end-of-life on January 1, 2020. "
    "The transition from Python 2 to Python 3 took the community over a decade to complete. "
    "Most major libraries have since dropped Python 2 support.",
]

QUERY = "How does CPython execute Python code?"

if __name__ == "__main__":
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    workflow = create_workflow()
    config = {"configurable": {"client": client, "model": "gpt-4o-mini"}}

    result = workflow.invoke({
        "chunks": SAMPLE_CHUNKS,
        "query": QUERY,
        "ratio": 0.4,
        "original_tokens": 0,
        "compressed_context": "",
        "compressed_tokens": 0,
        "answer": "",
    }, config=config)

    reduction = round((1 - result["compressed_tokens"] / result["original_tokens"]) * 100)
    print(f"Query: {QUERY}\n")
    print(f"Tokens: {result['original_tokens']} -> {result['compressed_tokens']} ({reduction}% reduction)\n")
    print(f"Answer: {result['answer']}")
