from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

# Analogical Prompting (Webb et al. 2023 — nature.com/articles/s41562-023-01659-w)
#
# Key insight: asking the LLM to RECALL its own analogous problems before solving
# outperforms providing human-curated few-shot examples on many benchmarks.
#
# Why it works: the model retrieves problems that activate the right reasoning
# schema — like a worked example that "primes the pump." Human-curated examples
# may not align with the model's internal representations.
#
# Contrast with few-shot prompting:
#   Few-shot:  YOU provide examples → they may not match what the model needs
#   Analogical: MODEL generates its own examples → activates its own schema
#
# Two-node graph: generate_analogies → solve
# The analogies are passed as context to the solve node — no in-context examples
# needed from the human at all.

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class ARState(TypedDict):
    problem: str
    analogies: str   # self-generated similar solved problems (plain text block)
    answer: str


def generate_analogies(state: ARState) -> dict:
    """Ask the model to recall 3 similar problems it already knows how to solve.

    The key prompt instruction is 'recall' rather than 'invent' — we want the
    model to retrieve problems from training, not fabricate toy problems.
    Each recalled problem should include a step-by-step solution so it functions
    as a worked example in the next node.
    """
    prompt = (
        "Before solving the target problem, recall 3 similar problems you know "
        "from mathematics, logic, or puzzles. For each, show the full step-by-step "
        "solution. These examples should activate the right reasoning approach.\n\n"
        f"Target problem: {state['problem']}\n\n"
        "List 3 analogous problems with solutions. Be specific and rigorous."
    )
    analogies = _llm.invoke([HumanMessage(content=prompt)]).content
    return {"analogies": analogies}


def solve(state: ARState) -> dict:
    """Use the self-generated analogies as context to solve the target problem.

    By placing the analogies before the target problem, the model is guided
    toward the same reasoning pattern it just demonstrated in the examples.
    This is in-context learning driven by the model's own retrieved knowledge.
    """
    prompt = (
        "Here are similar solved problems for reference:\n\n"
        f"{state['analogies']}\n\n"
        "---\n\n"
        f"Now solve this problem step by step:\n{state['problem']}\n\n"
        "Show your reasoning clearly, then state the final answer."
    )
    answer = _llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return {"answer": answer}


def create_workflow():
    builder = StateGraph(ARState)
    builder.add_node("generate_analogies", generate_analogies)
    builder.add_node("solve", solve)
    builder.add_edge(START, "generate_analogies")
    builder.add_edge("generate_analogies", "solve")
    builder.add_edge("solve", END)
    return builder.compile()
