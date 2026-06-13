from typing import Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import BUDGET_LIMIT, RESEARCH_TOPIC, count_tokens


class BudgetState(TypedDict):
    topic: str
    steps: list[str]
    current_step: int
    notes: list[str]
    tokens_used: int
    token_log: list[dict]
    budget_exceeded: bool
    final_answer: str


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    system = SystemMessage(content=f"You are a researcher summarizing: {RESEARCH_TOPIC}")

    def research_step(state: BudgetState) -> dict:
        step_idx = state["current_step"]
        if step_idx >= len(state["steps"]):
            return {}
        step_prompt = state["steps"][step_idx]
        prompt_tokens = count_tokens(step_prompt)
        response = llm.invoke([system, HumanMessage(content=step_prompt)])
        content = response.content.strip()
        completion_tokens = count_tokens(content)
        step_tokens = prompt_tokens + completion_tokens
        new_total = state["tokens_used"] + step_tokens
        log_entry = {"step": step_idx + 1, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total": step_tokens}
        return {
            "notes": state["notes"] + [content],
            "current_step": step_idx + 1,
            "tokens_used": new_total,
            "token_log": state["token_log"] + [log_entry],
        }

    def check_budget(state: BudgetState) -> dict:
        if state["tokens_used"] >= BUDGET_LIMIT:
            partial = "\n\n".join(f"Step {i + 1}: {n}" for i, n in enumerate(state["notes"]))
            return {
                "budget_exceeded": True,
                "final_answer": f"[BUDGET EXCEEDED at {state['tokens_used']} tokens]\nPartial research:\n{partial}",
            }
        return {"budget_exceeded": False}

    def route(state: BudgetState) -> Literal["research_step", "synthesize", "__end__"]:
        if state["budget_exceeded"]:
            return END
        if state["current_step"] >= len(state["steps"]):
            return "synthesize"
        return "research_step"

    def synthesize(state: BudgetState) -> dict:
        combined = "\n\n".join(f"Step {i + 1}: {n}" for i, n in enumerate(state["notes"]))
        answer = llm.invoke([
            system,
            HumanMessage(content=f"Synthesize these research notes into a coherent summary:\n{combined}"),
        ]).content.strip()
        return {"final_answer": answer}

    graph = StateGraph(BudgetState)
    graph.add_node("research_step", research_step)
    graph.add_node("check_budget", check_budget)
    graph.add_node("synthesize", synthesize)
    graph.add_edge(START, "research_step")
    graph.add_edge("research_step", "check_budget")
    graph.add_conditional_edges("check_budget", route)
    graph.add_edge("synthesize", END)
    return graph.compile()
