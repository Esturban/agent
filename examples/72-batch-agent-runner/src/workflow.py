import asyncio

from langchain_openai import ChatOpenAI

from src.tools import BATCH_SIZE, process_task


async def run_batch_agent(tasks: list[str]) -> list[dict]:
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    results: list[dict] = []
    batches = [tasks[i:i + BATCH_SIZE] for i in range(0, len(tasks), BATCH_SIZE)]

    for batch_idx, batch in enumerate(batches):
        print(f"  Running batch {batch_idx + 1}/{len(batches)} ({len(batch)} tasks)...")
        batch_results = await asyncio.gather(
            *[process_task(llm, task, i + batch_idx * BATCH_SIZE) for i, task in enumerate(batch)]
        )
        results.extend(batch_results)

    return results
