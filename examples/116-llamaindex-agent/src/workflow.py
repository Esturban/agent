"""
ReAct agent workflow for example 116 — LlamaIndex Agent.

Builds a ReActAgent backed by 3 QueryEngineTool instances (science,
history, technology) and runs multi-hop questions that require
routing across tools.
"""

from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

from src.tools import build_query_engine_tools, ask_agent, SCIENCE_DOCS, HISTORY_DOCS, TECHNOLOGY_DOCS


MULTI_HOP_QUESTIONS = [
    (
        "What physical principle makes quantum computing fundamentally different "
        "from classical computing, and when was that principle first described?",
        "Requires: technology_tool (quantum computing) + science_tool (quantum mechanics history)",
    ),
    (
        "The Industrial Revolution depended on a specific energy conversion device. "
        "What is the biological process that originally captured the energy stored "
        "in the coal it burned?",
        "Requires: history_tool (Industrial Revolution coal) + science_tool (photosynthesis)",
    ),
    (
        "Bitcoin was introduced in 2008. What percentage of the global population "
        "was online at that time versus today, and what technology underpins both "
        "blockchain and the internet?",
        "Requires: technology_tool (blockchain/internet) + cross-tool synthesis",
    ),
]


def create_workflow() -> tuple[ReActAgent, list[tuple[str, str]]]:
    """
    Build a LlamaIndex ReActAgent with 3 QueryEngineTool instances.

    Returns:
        (agent, questions) where questions is the list of multi-hop questions
        with routing notes.
    """
    llm = OpenAI(model="gpt-4o-mini", temperature=0)

    tools = build_query_engine_tools(SCIENCE_DOCS, HISTORY_DOCS, TECHNOLOGY_DOCS)

    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=False,
        max_iterations=8,
    )

    return agent, MULTI_HOP_QUESTIONS


def run_questions(agent: ReActAgent, questions: list[tuple[str, str]]) -> list[dict]:
    """
    Run each multi-hop question through the agent.

    Returns:
        List of dicts: {question, routing_note, answer}
    """
    results = []
    for question, routing_note in questions:
        answer = ask_agent(agent, question)
        results.append(
            {
                "question": question,
                "routing_note": routing_note,
                "answer": answer,
            }
        )
    return results
