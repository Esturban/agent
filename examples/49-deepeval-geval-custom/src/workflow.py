from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import EvalState, llm

GENERATE_PROMPT = """Answer the following question clearly and concisely.

Question: {query}

Answer:"""


def generate(state: EvalState) -> dict:
    prompt = GENERATE_PROMPT.format(query=state["input"])
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"output": result.content}


def create_workflow():
    graph = StateGraph(EvalState)
    graph.add_node("generate", generate)
    graph.set_entry_point("generate")
    graph.add_edge("generate", END)
    return graph.compile()
