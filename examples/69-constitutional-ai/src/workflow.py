from typing import Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import CONSTITUTION, MAX_REVISIONS, Critique


class CAIState(TypedDict):
    prompt: str
    response: str
    critiques: list[dict]
    revision_count: int
    violations: list[str]


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    critiquer = llm.with_structured_output(Critique)

    def generate(state: CAIState) -> dict:
        response = llm.invoke([HumanMessage(content=state["prompt"])]).content.strip()
        return {"response": response, "revision_count": 0}

    def critique(state: CAIState) -> dict:
        critiques = []
        violations = []
        for principle in CONSTITUTION:
            result: Critique = critiquer.invoke([
                SystemMessage(content="You are a constitutional AI evaluator."),
                HumanMessage(content=f"Principle: {principle}\n\nResponse to evaluate:\n{state['response']}"),
            ])
            critiques.append(result.model_dump())
            if result.violated:
                violations.append(f"{principle} — {result.reason}")
        return {"critiques": critiques, "violations": violations}

    def revise(state: CAIState) -> dict:
        violation_text = "\n".join(f"- {v}" for v in state["violations"])
        response = llm.invoke([
            SystemMessage(content="You are revising a response to comply with principles."),
            HumanMessage(
                content=f"Revise this response to fix all violations:\n\nResponse:\n{state['response']}\n\nViolations:\n{violation_text}"
            ),
        ]).content.strip()
        return {"response": response, "revision_count": state["revision_count"] + 1}

    def route(state: CAIState) -> Literal["critique", "__end__"]:
        if not state["violations"] or state["revision_count"] >= MAX_REVISIONS:
            return END
        return "critique"

    graph = StateGraph(CAIState)
    graph.add_node("generate", generate)
    graph.add_node("critique", critique)
    graph.add_node("revise", revise)
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "critique")
    graph.add_conditional_edges("critique", route)
    graph.add_edge("revise", "critique")
    return graph.compile()
