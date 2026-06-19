import asyncio
from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from .tools import fetch_calendar, fetch_news, fetch_stock, fetch_weather


class BriefingState(TypedDict):
    context: str
    summary: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def gather_context_node(state: BriefingState) -> dict:
    """Concurrently fire all I/O tools with asyncio.gather() — ~1 s total."""
    weather, news, calendar, stock = await asyncio.gather(
        fetch_weather(),
        fetch_news(),
        fetch_calendar(),
        fetch_stock(),
    )
    return {
        "context": f"Weather: {weather}. News: {news}. Calendar: {calendar}. Stock: {stock}."
    }


async def summarise_node(state: BriefingState) -> dict:
    """Call the LLM once to produce a one-sentence morning briefing."""
    prompt = f"Give a one-sentence morning briefing from: {state['context']}"
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"summary": response.content}


def create_workflow():
    """Build and compile the async briefing graph."""
    builder = StateGraph(BriefingState)
    builder.add_node("gather", gather_context_node)
    builder.add_node("summarise", summarise_node)
    builder.add_edge(START, "gather")
    builder.add_edge("gather", "summarise")
    builder.add_edge("summarise", END)
    return builder.compile()
