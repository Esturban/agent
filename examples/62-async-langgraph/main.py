import asyncio
import time

from dotenv import load_dotenv

from src.workflow import create_workflow

load_dotenv()


async def main():
    app = create_workflow()

    print("Running briefing graph (4 concurrent async tools + 1 LLM call)...")
    t0 = time.perf_counter()
    result = await app.ainvoke({"context": "", "summary": ""})
    elapsed = time.perf_counter() - t0

    print(f"Context : {result['context']}")
    print(f"Summary : {result['summary']}")
    print(f"Time    : {elapsed:.2f}s  (4 tools concurrently via asyncio.gather)")

    print()
    print("Streaming tokens with astream_events():")
    print("Response: ", end="", flush=True)
    async for event in app.astream_events({"context": "", "summary": ""}, version="v2"):
        if event["event"] == "on_chat_model_stream":
            chunk = event["data"]["chunk"].content
            if chunk:
                print(chunk, end="", flush=True)
    print()
    print("[stream complete]")


if __name__ == "__main__":
    asyncio.run(main())
