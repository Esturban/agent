# workflow.py - Workflow graph definition and related functions

from langgraph.graph import END, START, StateGraph

from .agent import copywriter_agent, researcher_agent
from .models import AgentState


def create_workflow(researcher_llm, copywriter_llm, search_tool):
    """Create the decoupled two-agent workflow"""

    def run_researcher(state: AgentState) -> dict:
        return researcher_agent(state, researcher_llm, search_tool)

    def run_copywriter(state: AgentState) -> dict:
        return copywriter_agent(state, copywriter_llm)

    workflow = StateGraph(AgentState)

    # Add agent nodes
    workflow.add_node("researcher", run_researcher)
    workflow.add_node("copywriter", run_copywriter)

    # Define the flow: START → researcher → copywriter → END
    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "copywriter")
    workflow.add_edge("copywriter", END)

    # No checkpointer needed for batch processing - each prospect is independent
    return workflow.compile()
