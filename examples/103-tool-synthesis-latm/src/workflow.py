"""LATM graph: dispatch → (synthesize?) → execute.

On the first call for a task type the dispatcher returns 'synthesize';
the tool-maker writes Python code, we exec() it and register it.
On subsequent similar tasks the dispatcher picks the cached tool directly.

Safety note: exec() is fine for a self-contained demo.
For production pair with E2B sandboxing (see example 92).
"""

import re
from typing import Callable, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph

from .tools import TOOLMAKER_SYSTEM, dispatcher, tool_maker

# Shared registry — persists across all tasks run in the same process.
_registry: dict[str, Callable] = {}


class LATMState(TypedDict):
    task: str
    chosen_tool: str
    tool_result: str


def dispatch(state: LATMState) -> dict:
    available = list(_registry) or ["(none yet)"]
    reply = dispatcher.invoke([HumanMessage(
        content=(
            f"Available tools: {available}\n"
            f"Task: {state['task']}\n"
            "Reply with an existing tool name if it fits this task, "
            "else reply exactly: synthesize"
        )
    )]).content.strip().strip("'\"")
    return {"chosen_tool": reply}


def route(state: LATMState) -> str:
    return "synthesize" if state["chosen_tool"] not in _registry else "execute"


def synthesize(state: LATMState) -> dict:
    # Tool-maker generates a Python function; exec registers it in the shared registry.
    code = tool_maker.invoke([
        SystemMessage(content=TOOLMAKER_SYSTEM),
        HumanMessage(content=f"Task: {state['task']}"),
    ]).content.strip()
    m = re.search(r"def (\w+)\(", code)
    name = m.group(1) if m else "generated_tool"
    ns: dict = {}
    exec(code, ns)  # noqa: S102 — demo only, pair with E2B in production
    _registry[name] = ns[name]
    print(f"  [LATM] synthesized '{name}()' — registry: {list(_registry)}")
    return {"chosen_tool": name}


def execute(state: LATMState) -> dict:
    fn = _registry[state["chosen_tool"]]
    try:
        result = str(fn(state["task"]))
    except Exception as e:
        result = f"Error in {state['chosen_tool']}: {e}"
    return {"tool_result": result}


def create_workflow():
    g = StateGraph(LATMState)
    g.add_node("dispatch", dispatch)
    g.add_node("synthesize", synthesize)
    g.add_node("execute", execute)
    g.add_edge(START, "dispatch")
    g.add_conditional_edges("dispatch", route, {"synthesize": "synthesize", "execute": "execute"})
    g.add_edge("synthesize", "execute")
    g.add_edge("execute", END)
    return g.compile()
