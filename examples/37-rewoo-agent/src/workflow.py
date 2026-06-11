import json

from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import PLANNER_PROMPT, SOLVER_PROMPT, TOOL_DESCRIPTIONS, ReWOOState, llm


def planner(state: ReWOOState) -> dict:
    prompt = PLANNER_PROMPT.format(task=state["task"])
    result = llm.invoke([HumanMessage(content=prompt)])
    try:
        # Strip markdown fences if present
        text = result.content.strip()
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:-1])
        plans = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        plans = []
    print(f"  Plan: {len(plans)} steps")
    return {"plans": plans, "evidence": {}}


def executor(state: ReWOOState) -> dict:
    evidence = dict(state["evidence"])
    for step in state["plans"]:
        tool = step.get("tool", "analyze")
        raw_args = step.get("args", "")
        # Resolve variable references
        args = raw_args
        for var, val in evidence.items():
            args = args.replace(var, val[:200] if isinstance(val, str) else str(val))
        desc = TOOL_DESCRIPTIONS.get(tool, "process")
        prompt = f"Tool: {tool} ({desc})\nInput: {args}\nProvide a detailed result in 3-5 sentences."
        result = llm.invoke([HumanMessage(content=prompt)])
        output_var = step.get("output_var", f"$E{len(evidence)+1}")
        evidence[output_var] = result.content
        print(f"  ✓ {tool}({args[:40]}...) → {output_var}")
    return {"evidence": evidence}


def solver(state: ReWOOState) -> dict:
    evidence_text = "\n".join(f"{k}: {v}" for k, v in state["evidence"].items())
    prompt = SOLVER_PROMPT.format(task=state["task"], evidence=evidence_text)
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"final_answer": result.content}


def create_workflow():
    graph = StateGraph(ReWOOState)
    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_node("solver", solver)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "solver")
    graph.add_edge("solver", END)
    return graph.compile()
