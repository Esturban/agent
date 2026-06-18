"""SWE-agent workflow: ReAct agent with file-editing tools iterates until tests pass.

Key insight from Yang et al. 2024: a well-designed ACI (agent-computer interface)
with view/edit/run tools lets an LLM solve real bugs without human intervention.
create_react_agent handles the loop — the model keeps calling tools until it decides
all tests pass and emits a final text response.
"""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .tools import SWE_TOOLS

SYSTEM = (
    "You are a software engineer fixing bugs in a Python codebase.\n"
    "Workflow:\n"
    "  1. view_file the test file to understand expected behaviour.\n"
    "  2. view_file the implementation to find the bugs.\n"
    "  3. edit_file to apply targeted fixes (one at a time).\n"
    "  4. run_tests to verify — repeat until all tests pass.\n"
    "Be methodical. Fix one bug at a time and verify after each edit."
)


def create_workflow():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # create_react_agent compiles a ReAct loop: LLM → tool call → result → LLM → …
    # It stops when the model emits a response with no tool calls (tests pass).
    return create_react_agent(llm, SWE_TOOLS, state_modifier=SYSTEM)
