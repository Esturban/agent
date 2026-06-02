from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from src.tools import search_web


class EntityProfile(BaseModel):
    name: str = Field(description="Full name of the entity")
    summary: str = Field(description="2-3 sentence overview")
    key_facts: list[str] = Field(description="3-5 notable facts")
    confidence: str = Field(description="high | medium | low based on source quality")


class ProfileState(TypedDict):
    subject: str
    raw_results: str
    profile: dict


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano")

    def search_node(state: ProfileState) -> dict:
        return {"raw_results": search_web(state["subject"])}

    def extract_node(state: ProfileState) -> dict:
        structured_llm = llm.with_structured_output(EntityProfile)
        profile = structured_llm.invoke([
            SystemMessage(f"Extract a structured profile for: {state['subject']}"),
            HumanMessage(f"Use these search results:\n{state['raw_results']}"),
        ])
        return {"profile": profile.model_dump()}

    graph = StateGraph(ProfileState)
    graph.add_node("search", search_node)
    graph.add_node("extract", extract_node)
    graph.add_edge(START, "search")
    graph.add_edge("search", "extract")
    graph.add_edge("extract", END)
    return graph.compile()
