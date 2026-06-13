from langchain_core.messages import HumanMessage
from langsmith import traceable
from langgraph.graph import END, StateGraph

from src.tools import TraceState, get_llm


@traceable(name="answer-node")
def answer(state: TraceState) -> TraceState:
    llm = get_llm()
    response = llm.invoke([HumanMessage(content=state["question"])])
    return {"question": state["question"], "answer": response.content.strip()}


def create_workflow() -> StateGraph:
    graph = StateGraph(TraceState)
    graph.add_node("answer", answer)
    graph.set_entry_point("answer")
    graph.add_edge("answer", END)
    return graph.compile()
