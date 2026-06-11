import operator
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI

N_BRANCHES = 3

SAMPLE_PROBLEMS = [
    "Design a system to recommend personalized learning paths for software engineers.",
    "How should a startup prioritize features when resources are limited?",
]


class BranchState(TypedDict):
    """State for a single thought branch."""
    problem: str
    branch_id: int
    thought: str
    score: int


class ToTState(TypedDict):
    """Root state for the Tree of Thoughts graph."""
    problem: str
    branches: Annotated[list[dict], operator.add]   # reducer: accumulate all branch results
    best_thought: str
    final_answer: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)   # higher temp for branch diversity
judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)  # low temp for consistent scoring

BRANCH_PROMPT = """You are exploring solution path {branch_id} of {n_branches} for this problem.
Approach it from a DIFFERENT angle than typical solutions.

Problem: {problem}

Generate a creative, well-reasoned thought (3-5 sentences). Be specific and concrete."""

SCORE_PROMPT = """Rate this thought on a scale of 0-10 for solving the problem.
Criteria: relevance (0-4), creativity (0-3), feasibility (0-3).

Problem: {problem}
Thought: {thought}

Respond with ONLY a number 0-10."""

SYNTHESIS_PROMPT = """You selected the best thought from a tree search. Now expand it into a complete answer.

Problem: {problem}
Best Thought: {thought}
(This was scored highest of {n} candidate thoughts)

Write a thorough, actionable response."""
