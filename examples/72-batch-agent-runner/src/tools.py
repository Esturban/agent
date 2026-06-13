import asyncio

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

BATCH_SIZE = 3
MAX_RETRIES = 3
RETRY_DELAY = 1.0

SAMPLE_TASKS = [
    "What is photosynthesis? Answer in one sentence.",
    "What is the capital of Japan? Answer in one sentence.",
    "What is Newton's first law? Answer in one sentence.",
    "What is DNA? Answer in one sentence.",
    "What is the speed of light? Answer in one sentence.",
    "What is machine learning? Answer in one sentence.",
    "What is blockchain? Answer in one sentence.",
    "What is quantum computing? Answer in one sentence.",
    "What is the Pythagorean theorem? Answer in one sentence.",
]


async def process_task(llm: ChatOpenAI, task: str, index: int) -> dict:
    for attempt in range(MAX_RETRIES):
        try:
            response = await llm.ainvoke([HumanMessage(content=task)])
            return {"index": index, "task": task, "answer": response.content.strip(), "status": "ok", "attempts": attempt + 1}
        except Exception as exc:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (2**attempt))
            else:
                return {"index": index, "task": task, "answer": "", "status": f"error: {exc}", "attempts": attempt + 1}
    return {"index": index, "task": task, "answer": "", "status": "error", "attempts": MAX_RETRIES}
