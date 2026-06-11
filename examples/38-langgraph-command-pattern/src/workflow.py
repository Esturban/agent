from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.types import Command

from .tools import (
    CODE_PROMPT,
    CREATIVE_PROMPT,
    EXPLAIN_PROMPT,
    MATH_PROMPT,
    ROUTER_PROMPT,
    CommandState,
    llm,
)

VALID_ROUTES = {"code", "explain", "math", "creative"}


def router(state: CommandState) -> Command:
    prompt = ROUTER_PROMPT.format(task=state["task"])
    result = llm.invoke([HumanMessage(content=prompt)])
    route = result.content.strip().lower()
    if route not in VALID_ROUTES:
        route = "explain"
    print(f"  Route: {route}")
    return Command(goto=route, update={"route": route})


def code_handler(state: CommandState) -> dict:
    result = llm.invoke([SystemMessage(content=CODE_PROMPT.format(task=state["task"]))])
    return {"result": result.content}


def explain_handler(state: CommandState) -> dict:
    result = llm.invoke([SystemMessage(content=EXPLAIN_PROMPT.format(task=state["task"]))])
    return {"result": result.content}


def math_handler(state: CommandState) -> dict:
    result = llm.invoke([SystemMessage(content=MATH_PROMPT.format(task=state["task"]))])
    return {"result": result.content}


def creative_handler(state: CommandState) -> dict:
    result = llm.invoke([SystemMessage(content=CREATIVE_PROMPT.format(task=state["task"]))])
    return {"result": result.content}


def create_workflow():
    graph = StateGraph(CommandState)
    graph.add_node("router", router)
    graph.add_node("code", code_handler)
    graph.add_node("explain", explain_handler)
    graph.add_node("math", math_handler)
    graph.add_node("creative", creative_handler)
    graph.set_entry_point("router")
    # No conditional_edges needed — Command(goto=...) routes directly
    for node in ("code", "explain", "math", "creative"):
        graph.add_edge(node, END)
    return graph.compile()
