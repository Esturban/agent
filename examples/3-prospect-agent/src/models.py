# models.py - Data structures and schemas

from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

class OutputSchema(BaseModel):
    generated_message: str = Field(..., description="Personalized outreach message")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    source_summary: str = Field(..., description="Concise summary of sources used")
