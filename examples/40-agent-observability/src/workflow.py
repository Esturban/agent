from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import ObservabilityCallback, ObservabilityState, llm


def create_workflow(callback: ObservabilityCallback | None = None):
    graph = StateGraph(ObservabilityState)

    def node(state):
        result = llm.invoke(
            [HumanMessage(content=state["task"])],
            config={"callbacks": [callback]} if callback else {},
        )
        return {"response": result.content}

    graph.add_node("llm", node)
    graph.set_entry_point("llm")
    graph.add_edge("llm", END)
    return graph.compile()
