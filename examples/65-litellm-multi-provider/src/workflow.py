"""LangGraph workflow for the LiteLLM multi-provider example.

Graph: START → pick_model → call_llm → END

pick_model uses smart_completion logic to select the cheapest model that
fits the budget stored in state["budget_usd"].  call_llm executes the
call through ChatLiteLLM (LangChain drop-in) and writes the answer.
"""

import os

from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

import litellm

from .tools import PROVIDERS, compare_providers


class ProviderState(TypedDict):
    prompt: str
    budget_usd: float
    chosen_model: str
    answer: str
    comparison: list


def pick_model(state: ProviderState) -> ProviderState:
    """Choose the cheapest available model whose estimated cost fits budget."""
    preferred = "openai/gpt-4o"
    fallback = "openai/gpt-4o-mini"
    estimated_input = int(len(state["prompt"].split()) * 1.3)
    assumed_output = 80
    input_cost, output_cost = litellm.cost_per_token(
        model=preferred,
        prompt_tokens=estimated_input,
        completion_tokens=assumed_output,
    )
    chosen = preferred if (input_cost + output_cost) <= state["budget_usd"] else fallback
    return {**state, "chosen_model": chosen}


def call_llm(state: ProviderState) -> ProviderState:
    """Call the chosen model via ChatLiteLLM and store the answer."""
    llm = ChatLiteLLM(model=state["chosen_model"], max_tokens=80)
    response = llm.invoke([HumanMessage(content=state["prompt"])])
    results = compare_providers(state["prompt"])
    return {**state, "answer": response.content, "comparison": results}


def create_workflow():
    """Build and compile the provider-selection LangGraph workflow."""
    graph = StateGraph(ProviderState)
    graph.add_node("pick_model", pick_model)
    graph.add_node("call_llm", call_llm)
    graph.add_edge(START, "pick_model")
    graph.add_edge("pick_model", "call_llm")
    graph.add_edge("call_llm", END)
    return graph.compile()
