"""
123 — Agent Cost Tracking
Workflow: 3-node LangGraph agent with per-node cost instrumentation and budget enforcement.
"""

from typing import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from .tools import CostTracker, count_tokens

MODEL = "gpt-4o-mini"


class AgentState(TypedDict):
    task: str
    plan: str
    result: str
    summary: str
    tracker: CostTracker
    budget_exceeded: bool


def _call_llm(system: str, user: str, tracker: CostTracker, node_name: str) -> str:
    """Call LLM, count tokens via tiktoken, record cost."""
    llm = ChatOpenAI(model=MODEL, temperature=0)
    input_text = system + user
    input_tokens = count_tokens(input_text, MODEL)
    response = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
    output = response.content
    output_tokens = count_tokens(output, MODEL)
    cost = tracker.record(node_name, input_tokens, output_tokens)
    print(f"  [{node_name}] {input_tokens} in / {output_tokens} out / ${cost:.6f}")
    return output


def planner_node(state: AgentState) -> AgentState:
    plan = _call_llm(
        "You are a task planner. Break the given task into 3 numbered steps.",
        f"Task: {state['task']}",
        state["tracker"],
        "planner",
    )
    return {**state, "plan": plan}


def executor_node(state: AgentState) -> AgentState:
    result = _call_llm(
        "You are a task executor. Execute the given plan and provide results.",
        f"Plan:\n{state['plan']}\n\nTask: {state['task']}",
        state["tracker"],
        "executor",
    )
    return {**state, "result": result}


def summarizer_node(state: AgentState) -> AgentState:
    summary = _call_llm(
        "You are a summarizer. Write a 2-sentence summary of the execution result.",
        f"Result:\n{state['result']}",
        state["tracker"],
        "summarizer",
    )
    return {**state, "summary": summary}


def budget_check(state: AgentState) -> str:
    """Route to budget_exceeded node if cost is too high."""
    return "budget_exceeded" if state.get("budget_exceeded") else "executor"


def budget_exceeded_node(state: AgentState) -> AgentState:
    print("  [BUDGET] Budget exceeded — stopping agent.")
    return {**state, "summary": "Stopped: budget limit reached."}


def create_workflow(max_budget_usd: float = 0.05) -> dict:
    """Create and run a 3-node LangGraph agent with cost tracking."""
    tracker = CostTracker()

    task = "Research and explain the key differences between RAG and fine-tuning for production LLM applications."

    initial_state: AgentState = {
        "task": task,
        "plan": "",
        "result": "",
        "summary": "",
        "tracker": tracker,
        "budget_exceeded": False,
    }

    # Build graph
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("budget_exceeded", budget_exceeded_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "summarizer")
    graph.add_edge("summarizer", END)
    graph.add_edge("budget_exceeded", END)

    app = graph.compile()

    print(f"Task: {task[:60]}...\n")
    print(f"Budget limit: ${max_budget_usd:.4f}\n")

    final_state = app.invoke(initial_state)
    report = tracker.report()

    print(f"\n--- Cost Report ---")
    print(f"Total: ${report['total_cost_usd']:.6f} (budget: ${max_budget_usd:.4f})")
    print(f"Most expensive node: {report['most_expensive_node']}")
    for node, cost in report["per_node"].items():
        print(f"  {node}: ${cost:.6f}")
    print(f"Total tokens: {report['total_input_tokens']} in / {report['total_output_tokens']} out")

    if report["total_cost_usd"] > max_budget_usd:
        print(f"\nWARNING: Exceeded budget by ${report['total_cost_usd'] - max_budget_usd:.6f}")
    else:
        print(f"\nWithin budget: ${max_budget_usd - report['total_cost_usd']:.6f} remaining")

    return {
        "summary": final_state["summary"],
        "cost_report": report,
    }
