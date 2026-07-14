from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt


class ApprovalState(TypedDict):
    action: str
    risk: str
    approved: bool
    result: str


def propose_action(state: ApprovalState) -> dict:
    return {"action": state["action"], "risk": state["risk"]}


def await_approval(state: ApprovalState) -> dict:
    decision = interrupt(
        {
            "action": state["action"],
            "risk": state["risk"],
            "question": "Approve this action?",
        }
    )
    if decision:
        return {"approved": True, "result": f"EXECUTED: {state['action']}"}
    return {"approved": False, "result": f"REJECTED: {state['action']}"}


def create_workflow():
    graph = StateGraph(ApprovalState)
    graph.add_node("propose_action", propose_action)
    graph.add_node("await_approval", await_approval)
    graph.add_edge(START, "propose_action")
    graph.add_edge("propose_action", "await_approval")
    graph.add_edge("await_approval", END)
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)
