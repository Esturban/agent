import io
from typing import Literal, TypedDict

import pandas as pd
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import MAX_ITERATIONS, QUERY_PROMPT, SAMPLE_CSV


class TabularState(TypedDict):
    question: str
    schema: str
    query_code: str
    result: str
    error: str
    iterations: int


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    df = pd.read_csv(io.StringIO(SAMPLE_CSV))
    schema = f"columns: {list(df.columns)}, dtypes: {df.dtypes.to_dict()}"
    sample = df.head(3).to_string(index=False)

    def load_table(state: TabularState) -> dict:
        return {"schema": schema, "error": "", "iterations": 0}

    def write_query(state: TabularState) -> dict:
        prompt = QUERY_PROMPT.format(
            columns=list(df.columns),
            sample=sample,
            question=state["question"],
        )
        if state["error"]:
            prompt += f"\n\nPrevious expression raised: {state['error']}\nFix it."
        code = llm.invoke([HumanMessage(content=prompt)]).content.strip()
        return {"query_code": code, "iterations": state["iterations"] + 1}

    def execute_query(state: TabularState) -> dict:
        try:
            result = eval(state["query_code"], {"df": df, "pd": pd})  # noqa: S307
            return {"result": str(result), "error": ""}
        except Exception as exc:
            return {"result": "", "error": str(exc)}

    def route(state: TabularState) -> Literal["write_query", "__end__"]:
        if state["error"] and state["iterations"] < MAX_ITERATIONS:
            return "write_query"
        return END

    graph = StateGraph(TabularState)
    graph.add_node("load_table", load_table)
    graph.add_node("write_query", write_query)
    graph.add_node("execute_query", execute_query)
    graph.add_edge(START, "load_table")
    graph.add_edge("load_table", "write_query")
    graph.add_edge("write_query", "execute_query")
    graph.add_conditional_edges("execute_query", route)
    return graph.compile()
