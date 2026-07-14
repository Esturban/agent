from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import STEP_BACK_PROMPT, build_vectorstore


class StepBackState(TypedDict):
    query: str
    abstract_query: str
    documents: list[str]
    answer: str


def create_workflow():
    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    vs = build_vectorstore()

    def step_back(state: StepBackState) -> dict:
        msgs = [SystemMessage(content=STEP_BACK_PROMPT), HumanMessage(content=state["query"])]
        return {"abstract_query": llm.invoke(msgs).content.strip()}

    def retrieve(state: StepBackState) -> dict:
        docs = vs.similarity_search(state["abstract_query"], k=3)
        return {"documents": [d.page_content for d in docs]}

    def answer(state: StepBackState) -> dict:
        context = "\n".join(state["documents"])
        prompt = (
            f"Background context (retrieved using an abstracted query):\n{context}\n\n"
            f"Original question: {state['query']}\n"
            "Answer the original question using only the background context."
        )
        return {"answer": llm.invoke([HumanMessage(content=prompt)]).content}

    graph = StateGraph(StepBackState)
    graph.add_node("step_back", step_back)
    graph.add_node("retrieve", retrieve)
    graph.add_node("answer", answer)
    graph.add_edge(START, "step_back")
    graph.add_edge("step_back", "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)
    return graph.compile()
