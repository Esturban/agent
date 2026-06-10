# models.py - Simple data structures for idea generation

from typing import Annotated, Optional, TypedDict

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class State(TypedDict):
    messages: Annotated[list, add_messages]


class FreeTool(BaseModel):
    name: str
    category: str
    description: str
    free_tier: str
    url: Optional[str] = None


class ParsedContent(BaseModel):
    tools: list[FreeTool]
    categories: list[str]
    summary: str


class IdeaConcept(BaseModel):
    title: str
    description: str
    target_tools: list[str]
    value_proposition: str
    effort_level: str  # "low", "medium", "high"
    implementation_complexity: str  # "simple", "moderate", "complex"


class IdeaOutput(BaseModel):
    idea_concept: IdeaConcept
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    reasoning: str = Field(..., description="Explanation of why this idea is valuable")
    next_steps: list[str] = Field(..., description="Recommended next steps")


class AgentState(TypedDict):
    parsed_content: ParsedContent | None
    ideas: list[IdeaOutput] | None
