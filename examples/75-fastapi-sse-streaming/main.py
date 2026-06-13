import json

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

load_dotenv()

from src.workflow import create_graph  # noqa: E402

app = FastAPI(title="LangGraph SSE Stream")
graph = create_graph()


class AskRequest(BaseModel):
    question: str


async def event_stream(question: str):
    async for event in graph.astream_events(
        {"question": question, "answer": ""},
        version="v2",
    ):
        kind = event.get("event", "")
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"].content
            if chunk:
                yield f"data: {json.dumps({'token': chunk})}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/ask")
async def ask(req: AskRequest) -> StreamingResponse:
    return StreamingResponse(
        event_stream(req.question),
        media_type="text/event-stream",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
