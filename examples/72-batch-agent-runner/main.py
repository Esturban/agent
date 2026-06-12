import asyncio

from dotenv import load_dotenv

load_dotenv()

from src.tools import BATCH_SIZE, SAMPLE_TASKS  # noqa: E402
from src.workflow import run_batch_agent  # noqa: E402


async def main() -> None:
    print(f"Running {len(SAMPLE_TASKS)} tasks in batches of {BATCH_SIZE}\n")
    results = await run_batch_agent(SAMPLE_TASKS)

    ok = [r for r in results if r["status"] == "ok"]
    errors = [r for r in results if r["status"] != "ok"]
    print(f"\nCompleted: {len(ok)}/{len(results)} ok, {len(errors)} errors\n")
    for r in results:
        status = "OK" if r["status"] == "ok" else r["status"]
        print(f"  [{r['index'] + 1:02d}] {status}  {r['answer'][:80]}")


if __name__ == "__main__":
    asyncio.run(main())
