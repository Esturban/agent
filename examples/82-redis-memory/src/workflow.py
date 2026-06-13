import json
from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import get_redis_client

_llm = ChatOpenAI(model="gpt-5-nano", temperature=0)


class RedisState(TypedDict):
    user_id: str
    query: str
    history: list[dict]
    answer: str


def load_history(state: RedisState) -> dict:
    r = get_redis_client()
    key = f"history:{state['user_id']}"
    raw = r.lrange(key, 0, -1)
    history = [json.loads(item) for item in raw]
    return {"history": history}


def respond(state: RedisState) -> dict:
    context = "\n".join(
        f"[{m['role']}] {m['content']}" for m in state["history"]
    )
    prompt = (
        f"Prior conversation history:\n{context or '(none yet)'}\n\n"
        f"User: {state['query']}\n"
        "Answer using the history if relevant."
    )
    response = _llm.invoke([HumanMessage(content=prompt)])
    return {"answer": response.content}


def save_history(state: RedisState) -> dict:
    r = get_redis_client()
    key = f"history:{state['user_id']}"
    r.rpush(key, json.dumps({"role": "user", "content": state["query"]}))
    r.rpush(key, json.dumps({"role": "assistant", "content": state["answer"]}))
    return {}


def create_workflow():
    builder = StateGraph(RedisState)
    builder.add_node("load_history", load_history)
    builder.add_node("respond", respond)
    builder.add_node("save_history", save_history)
    builder.add_edge(START, "load_history")
    builder.add_edge("load_history", "respond")
    builder.add_edge("respond", "save_history")
    builder.add_edge("save_history", END)
    return builder.compile()
