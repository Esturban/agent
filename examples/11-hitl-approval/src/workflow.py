from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from src.tools import PENDING_ACTION


class HITLState(TypedDict):
    action: str
    approved: bool
    result: str


def create_workflow():
    def draft_action(state: HITLState) -> dict:
        return {"action": PENDING_ACTION}

    def await_approval(state: HITLState) -> dict:
        # interrupt() pauses here and surfaces a value to the caller.
        # On resume, the node re-runs from the top — so anything before
        # this line executes twice. Side effects must come AFTER.
        decision = interrupt({"action": state["action"], "question": "Approve this action?"})
        if decision:
            return {"approved": True, "result": f"EXECUTED: {state['action']}"}
        return {"approved": False, "result": f"CANCELLED: {state['action']}"}

    graph = StateGraph(HITLState)
    graph.add_node("draft_action", draft_action)
    graph.add_node("await_approval", await_approval)
    graph.add_edge(START, "draft_action")
    graph.add_edge("draft_action", "await_approval")
    graph.add_edge("await_approval", END)

    # checkpointer is mandatory -- without it the graph cannot save state
    # across the two .stream() calls and resume will fail.
    return graph.compile(checkpointer=MemorySaver())
