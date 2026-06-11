from typing import TypedDict

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

SAMPLE_TASKS = [
    "Research the key differences between LangGraph and LangChain, then summarize in 3 bullet points.",
    "Find the top 3 use cases for LangGraph agents and explain why each is a good fit.",
]

PLANNER_PROMPT = """You are a planner for a ReWOO agent. Given a task, output a plan as a list of tool steps.
Each step has:
  - tool: one of "search", "summarize", "analyze"
  - args: what to search for or analyze
  - output_var: variable name like $E1, $E2 to store this result

Output JSON only. Example:
[
  {{"tool": "search", "args": "LangGraph vs LangChain", "output_var": "$E1"}},
  {{"tool": "summarize", "args": "$E1", "output_var": "$E2"}}
]

Task: {task}"""

SOLVER_PROMPT = """Given the task and all tool outputs, write a final answer.

Task: {task}

Tool outputs:
{evidence}

Final answer:"""

TOOL_DESCRIPTIONS = {
    "search": "Retrieve information about a topic",
    "summarize": "Condense text into key points",
    "analyze": "Break down and interpret information",
}


class ToolPlan(BaseModel):
    tool: str
    args: str
    output_var: str


class ReWOOState(TypedDict):
    task: str
    plans: list[dict]  # list of {tool, args, output_var}
    evidence: dict  # output_var -> result
    final_answer: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
