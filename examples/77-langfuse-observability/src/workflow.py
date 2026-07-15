from typing import Any, TypedDict

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


class TraceState(TypedDict):
    task: str
    answer: str
    trace_id: str


class SimpleTraceHandler(BaseCallbackHandler):
    """Callback handler that logs LLM start/end events -- mirrors the Langfuse handler interface."""

    def __init__(self, trace_id: str) -> None:
        super().__init__()
        self.trace_id = trace_id
        self.events: list[dict] = []

    def on_llm_start(self, serialized: dict, prompts: list[str], **kwargs: Any) -> None:
        self.events.append({"event": "llm_start", "trace_id": self.trace_id, "prompt": prompts[0][:80]})

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        text = response.generations[0][0].text if response.generations else ""
        self.events.append({"event": "llm_end", "trace_id": self.trace_id, "output": text[:80]})


def create_workflow(handler: SimpleTraceHandler):
    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0, callbacks=[handler])

    def ask_question(state: TraceState) -> TraceState:
        response = llm.invoke([HumanMessage(content=state["task"])])
        return {**state, "answer": response.content.strip()}

    def format_answer(state: TraceState) -> TraceState:
        formatted = f"[{state['trace_id']}] {state['answer']}"
        return {**state, "answer": formatted}

    graph = StateGraph(TraceState)
    graph.add_node("ask_question", ask_question)
    graph.add_node("format_answer", format_answer)
    graph.set_entry_point("ask_question")
    graph.add_edge("ask_question", "format_answer")
    graph.add_edge("format_answer", END)
    return graph.compile()
