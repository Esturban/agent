# workflow.py - Simple workflow for parsing and idea generation

from langgraph.graph import END, START, StateGraph

from .agent import idea_generation_agent, parser_agent
from .models import AgentState


def create_workflow(parser_llm, idea_llm, tools):
    """Create the two-agent workflow for parsing and idea generation"""

    def run_parser(state: AgentState) -> dict:
        return parser_agent(state, parser_llm, tools)

    def run_idea_generator(state: AgentState) -> dict:
        return idea_generation_agent(state, idea_llm, tools)

    workflow = StateGraph(AgentState)

    # Add agent nodes
    workflow.add_node("parser", run_parser)
    workflow.add_node("idea_generator", run_idea_generator)

    # Define the flow: START → parser → idea_generator → END
    workflow.add_edge(START, "parser")
    workflow.add_edge("parser", "idea_generator")
    workflow.add_edge("idea_generator", END)

    # No checkpointer needed for batch processing
    return workflow.compile()
