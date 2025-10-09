# models.py - Simple data structures for idea generation

from typing import Annotated, TypedDict, List, Optional
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

class FreeTool(BaseModel):
    name: str
    category: str
    description: str
    free_tier: str
    url: Optional[str] = None

class ParsedContent(BaseModel):
    tools: List[FreeTool]
    categories: List[str]
    summary: str

class IdeaConcept(BaseModel):
    title: str
    description: str
    target_tools: List[str]
    value_proposition: str
    effort_level: str  # "low", "medium", "high"
    implementation_complexity: str  # "simple", "moderate", "complex"

class IdeaOutput(BaseModel):
    idea_concept: IdeaConcept
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    reasoning: str = Field(..., description="Explanation of why this idea is valuable")
    next_steps: List[str] = Field(..., description="Recommended next steps")

class AgentState(TypedDict):
    parsed_content: ParsedContent | None
    ideas: List[IdeaOutput] | None
