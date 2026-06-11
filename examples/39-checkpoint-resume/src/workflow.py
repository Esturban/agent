from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from .tools import DB_PATH, STEP_PROMPTS, CheckpointState, llm


def step_node(state: CheckpointState) -> dict:
    step = state["step"]
    if step >= len(STEP_PROMPTS):
        return {"done": True}
    prompt = STEP_PROMPTS[step].format(task=state["task"])
    result = llm.invoke([HumanMessage(content=prompt)])
    print(f"  Step {step + 1}/{len(STEP_PROMPTS)} complete")
    return {
        "outputs": state["outputs"] + [result.content],
        "step": step + 1,
        "done": step + 1 >= len(STEP_PROMPTS),
    }


def should_continue(state: CheckpointState) -> str:
    return END if state["done"] else "step"


def create_workflow():
    graph = StateGraph(CheckpointState)
    graph.add_node("step", step_node)
    graph.set_entry_point("step")
    graph.add_conditional_edges("step", should_continue, {"step": "step", END: END})
    saver = SqliteSaver.from_conn_string(DB_PATH)
    return graph.compile(checkpointer=saver)
