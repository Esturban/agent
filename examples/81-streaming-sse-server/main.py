from dotenv import load_dotenv
load_dotenv()

import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn
from src.tools import DEMO_QUESTION, create_langchain_app

app = FastAPI()


@app.get("/stream")
async def stream_graph(q: str = DEMO_QUESTION):
    graph = create_langchain_app()

    async def event_generator():
        async for event in graph.astream_events(
            {"question": q, "answer": ""},
            version="v2",
        ):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"].content
                if chunk:
                    yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    print(f"Server starting at http://localhost:8000")
    print(f"Test with: curl 'http://localhost:8000/stream?q={DEMO_QUESTION[:30]}...'")
    print(f"Or: curl 'http://localhost:8000/stream'")
    uvicorn.run(app, host="0.0.0.0", port=8000)
