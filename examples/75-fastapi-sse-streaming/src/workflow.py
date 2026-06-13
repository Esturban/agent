from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from src.tools import MODEL, AgentState


async def answer_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model=MODEL, temperature=0, streaming=True)
    response = await llm.ainvoke([HumanMessage(content=state["question"])])
    return {"question": state["question"], "answer": response.content}


def create_graph():
    graph = StateGraph(AgentState)
    graph.add_node("answer", answer_node)
    graph.set_entry_point("answer")
    graph.add_edge("answer", END)
    return graph.compile()
