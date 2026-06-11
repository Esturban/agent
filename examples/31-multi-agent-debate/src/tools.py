from typing import TypedDict

from langchain_openai import ChatOpenAI

MAX_ROUNDS = 2

TOPIC = "Is specialization or generalization better for a software engineer's career?"

SOLVER_A_SYSTEM = (
    "You are a career expert arguing FOR SPECIALIZATION in software engineering. "
    "Make compelling, evidence-based arguments in 3-4 sentences. "
    "If given a critique, acknowledge its strongest point then reinforce your position."
)

SOLVER_B_SYSTEM = (
    "You are a career expert arguing FOR GENERALIZATION (being a full-stack or T-shaped engineer). "
    "Make compelling, evidence-based arguments in 3-4 sentences. "
    "If given a critique, acknowledge its strongest point then reinforce your position."
)

JUDGE_SYSTEM = (
    "You are an impartial judge evaluating a structured debate. "
    "Read both final positions and select the stronger argument. "
    "Explain your reasoning in 2-3 sentences, then end with exactly: WINNER: [SPECIALIZATION or GENERALIZATION]"
)


class DebateState(TypedDict):
    topic: str
    position_a: str
    position_b: str
    critique_a: str  # B's critique of A (A must respond to this)
    critique_b: str  # A's critique of B (B must respond to this)
    round: int
    verdict: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
