from typing import Optional

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

SAMPLE_REQUESTS = [
    "Research the key benefits of vector databases and write a summary.",
    "Explain the CAP theorem and its practical implications.",
]


class AgentTask(BaseModel):
    """Structured handoff from Planner to Executor."""

    task_id: str = Field(description="Unique identifier for this task")
    task_type: str = Field(description="Type: research, analysis, or synthesis")
    instruction: str = Field(description="Clear instruction for the executor")
    context: str = Field(description="Background context to help executor")
    expected_output: str = Field(description="What the executor should produce")


class A2AState(TypedDict):
    original_request: str
    task_dict: Optional[dict]  # serialized AgentTask
    execution_result: str
    final_synthesis: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
planner_llm = llm.with_structured_output(AgentTask)

PLANNER_PROMPT = """You are a planning agent. Given a request, create a structured task for an executor agent.

Request: {request}

Create a task with: task_id (short slug), task_type (research/analysis/synthesis), instruction (clear directive), context (relevant background), expected_output (what executor should return)."""

EXECUTOR_PROMPT = """You are an executor agent. Complete the task below thoroughly.

Task: {instruction}
Context: {context}
Expected Output: {expected_output}

Provide a clear, well-structured response."""

SYNTHESIZER_PROMPT = """You are a planning agent finalizing a request.

Original Request: {original_request}
Task Created: {task_instruction}
Executor Result: {execution_result}

Synthesize a polished final answer that addresses the original request."""
