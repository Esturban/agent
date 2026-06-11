from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import (
    EXECUTOR_PROMPT,
    PLANNER_PROMPT,
    SYNTHESIZER_PROMPT,
    A2AState,
    llm,
    planner_llm,
)


def planner_agent(state: A2AState) -> dict:
    """Agent A: plans the task and creates structured AgentTask handoff."""
    prompt = PLANNER_PROMPT.format(request=state["original_request"])
    task = planner_llm.invoke([HumanMessage(content=prompt)])
    print(f"  Planner created task: {task.task_id} ({task.task_type})")
    print(f"  Instruction: {task.instruction[:80]}...")
    return {"task_dict": task.model_dump()}


def executor_agent(state: A2AState) -> dict:
    """Agent B: receives structured task and executes it."""
    task = state["task_dict"]
    prompt = EXECUTOR_PROMPT.format(
        instruction=task["instruction"],
        context=task["context"],
        expected_output=task["expected_output"],
    )
    result = llm.invoke([HumanMessage(content=prompt)])
    print(f"  Executor completed task: {len(result.content)} chars")
    return {"execution_result": result.content}


def synthesizer_agent(state: A2AState) -> dict:
    """Agent A synthesizes executor output into final answer."""
    task = state["task_dict"]
    prompt = SYNTHESIZER_PROMPT.format(
        original_request=state["original_request"],
        task_instruction=task["instruction"],
        execution_result=state["execution_result"],
    )
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"final_synthesis": result.content}


def create_workflow():
    graph = StateGraph(A2AState)
    graph.add_node("planner", planner_agent)
    graph.add_node("executor", executor_agent)
    graph.add_node("synthesizer", synthesizer_agent)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "synthesizer")
    graph.add_edge("synthesizer", END)
    return graph.compile()
