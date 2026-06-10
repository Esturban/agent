from typing import Literal, TypedDict

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import MAX_ITERATIONS, execute_code


class CodeInterpreterState(TypedDict):
    task: str
    code: str
    output: str
    error: str
    iterations: int


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano")

    def write_code(state: CodeInterpreterState) -> dict:
        if state["error"]:
            prompt = (
                f"Task: {state['task']}\n\n"
                f"Your previous code:\n```python\n{state['code']}\n```\n\n"
                f"Error:\n{state['error']}\n\n"
                "Fix the code. Output ONLY raw Python — no markdown fences, no explanation."
            )
        else:
            prompt = (
                f"Task: {state['task']}\n\n"
                "Write a complete, runnable Python script to solve this task. "
                "Output ONLY raw Python — no markdown fences, no explanation."
            )
        response = llm.invoke([
            SystemMessage(content="You are an expert Python programmer."),
            HumanMessage(content=prompt),
        ])
        return {"code": response.content.strip(), "iterations": state["iterations"] + 1}

    def run_code(state: CodeInterpreterState) -> dict:
        result = execute_code(state["code"])
        if result["returncode"] == 0:
            return {"output": result["stdout"], "error": ""}
        return {"output": "", "error": result["stderr"] or result["stdout"]}

    def route(state: CodeInterpreterState) -> Literal["write_code", "__end__"]:
        if not state["error"] or state["iterations"] >= MAX_ITERATIONS:
            return END
        return "write_code"

    graph = StateGraph(CodeInterpreterState)
    graph.add_node("write_code", write_code)
    graph.add_node("run_code", run_code)

    graph.add_edge(START, "write_code")
    graph.add_edge("write_code", "run_code")
    graph.add_conditional_edges("run_code", route)

    return graph.compile()
