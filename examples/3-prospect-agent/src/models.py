# models.py - Data structures and schemas

from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class State(TypedDict):
    messages: Annotated[list, add_messages]


class ProspectMetadata(BaseModel):
    first_name: str
    last_name: str
    company: str
    position: str


class ResearchOutput(BaseModel):
    search_query: str = Field(..., description="Generated search query")
    search_results: str = Field(..., description="Raw search results from tool")


class OutputSchema(BaseModel):
    generated_message: str = Field(..., description="Personalized outreach message")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    source_summary: str = Field(..., description="Concise summary of sources used")


class AgentState(TypedDict):
    prospect: ProspectMetadata
    research: ResearchOutput | None
    output: OutputSchema | None
