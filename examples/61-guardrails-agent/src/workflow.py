from typing import Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import MAX_ANSWER_WORDS, InputGuard, OutputGuard


class GuardrailsState(TypedDict):
    query: str
    input_decision: dict
    answer: str
    output_decision: dict
    blocked: bool
    block_reason: str


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    input_checker = llm.with_structured_output(InputGuard)
    output_checker = llm.with_structured_output(OutputGuard)

    def validate_input(state: GuardrailsState) -> dict:
        guard: InputGuard = input_checker.invoke([
            SystemMessage(content="You are a content policy classifier."),
            HumanMessage(content=f"Classify this query:\n{state['query']}"),
        ])
        blocked = not guard.is_on_topic or guard.contains_pii
        return {
            "input_decision": guard.model_dump(),
            "blocked": blocked,
            "block_reason": guard.reason if blocked else "",
        }

    def route_after_input(state: GuardrailsState) -> Literal["agent", "blocked"]:
        return "blocked" if state["blocked"] else "agent"

    def agent(state: GuardrailsState) -> dict:
        answer = llm.invoke([
            SystemMessage(content="You are a coding assistant. Be concise and accurate."),
            HumanMessage(content=state["query"]),
        ]).content.strip()
        return {"answer": answer}

    def validate_output(state: GuardrailsState) -> dict:
        guard: OutputGuard = output_checker.invoke([
            SystemMessage(content="You are an output safety validator."),
            HumanMessage(
                content=f"Validate this response (max {MAX_ANSWER_WORDS} words, must be factual, no untrusted URLs):\n{state['answer']}"
            ),
        ])
        return {"output_decision": guard.model_dump()}

    def blocked_node(state: GuardrailsState) -> dict:
        return {"answer": f"[BLOCKED] {state['block_reason']}"}

    graph = StateGraph(GuardrailsState)
    graph.add_node("validate_input", validate_input)
    graph.add_node("agent", agent)
    graph.add_node("validate_output", validate_output)
    graph.add_node("blocked", blocked_node)
    graph.add_edge(START, "validate_input")
    graph.add_conditional_edges("validate_input", route_after_input)
    graph.add_edge("agent", "validate_output")
    graph.add_edge("validate_output", END)
    graph.add_edge("blocked", END)
    return graph.compile()
