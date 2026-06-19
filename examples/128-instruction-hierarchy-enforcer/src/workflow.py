"""
LangGraph workflow: instruction → enforce → execute or block.

Graph: receive_instruction → enforce_node → (execute_node | block_node) → END

The enforcement node checks privilege and trust. If allowed, execute_node
sends the instruction to the actual LLM. If blocked, block_node returns a
safe refusal explaining the hierarchy violation.
"""

from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from .trust_levels import Instruction, TrustContext
from .enforcer import check_privilege

_executor = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class HierarchyState(TypedDict):
    instruction: Instruction
    context: TrustContext
    allowed: bool
    decision: str
    reasoning: str
    response: str


def enforce_node(state: HierarchyState) -> dict:
    allowed, decision, reasoning = check_privilege(state["instruction"], state["context"])
    return {"allowed": allowed, "decision": decision, "reasoning": reasoning}


def execute_node(state: HierarchyState) -> dict:
    system = f"System context: {state['context'].system_instruction}"
    response = _executor.invoke([
        SystemMessage(content=system),
        HumanMessage(content=state["instruction"].content),
    ]).content
    return {"response": response}


def block_node(state: HierarchyState) -> dict:
    level = state["instruction"].trust_level.name
    return {
        "response": (
            f"[BLOCKED by instruction hierarchy enforcer]\n"
            f"Source trust level: {level}\n"
            f"Reason: {state['reasoning']}\n"
            f"The {level}-level instruction conflicts with a higher-trust system directive."
        )
    }


def route_after_enforce(state: HierarchyState) -> str:
    return "execute_node" if state["allowed"] else "block_node"


def create_workflow():
    g = StateGraph(HierarchyState)
    g.add_node("enforce_node", enforce_node)
    g.add_node("execute_node", execute_node)
    g.add_node("block_node",   block_node)
    g.add_edge(START, "enforce_node")
    g.add_conditional_edges("enforce_node", route_after_enforce, ["execute_node", "block_node"])
    g.add_edge("execute_node", END)
    g.add_edge("block_node",   END)
    return g.compile()
