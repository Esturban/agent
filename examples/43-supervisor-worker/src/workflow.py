from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from .tools import WORKER_PROMPTS, SupervisorState, llm, router_llm

SUPERVISOR_PROMPT = (
    "You are a supervisor. Classify this task to the best worker: "
    "researcher (needs facts/research), summarizer (needs condensed info), "
    "analyst (needs structured analysis). Task: {task}"
)


def supervisor(state: SupervisorState) -> dict:
    result = router_llm.invoke([HumanMessage(content=SUPERVISOR_PROMPT.format(task=state["task"]))])
    print(f"  Supervisor → {result.worker} ({result.rationale[:60]})")
    return {"worker_type": result.worker, "rationale": result.rationale}


def make_worker(worker_type: str):
    def worker(state: SupervisorState) -> dict:
        prompt = WORKER_PROMPTS[worker_type].format(task=state["task"])
        result = llm.invoke([SystemMessage(content=prompt)])
        return {"worker_result": result.content}

    worker.__name__ = f"{worker_type}_worker"
    return worker


def route(state: SupervisorState) -> str:
    return state["worker_type"]


def create_workflow():
    graph = StateGraph(SupervisorState)
    graph.add_node("supervisor", supervisor)
    for wt in WORKER_PROMPTS:
        graph.add_node(wt, make_worker(wt))
        graph.add_edge(wt, END)
    graph.set_entry_point("supervisor")
    graph.add_conditional_edges("supervisor", route, {wt: wt for wt in WORKER_PROMPTS})
    return graph.compile()
