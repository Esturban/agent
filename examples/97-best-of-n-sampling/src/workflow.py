import json
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from .tools import N_SAMPLES, JUDGE_PROMPT

# High temp → diverse chains; zero temp → stable reward signal.
_gen   = ChatOpenAI(model="gpt-5.4-nano", temperature=0.8)
_judge = ChatOpenAI(model="gpt-5.4-nano", temperature=0)


class BonState(TypedDict):
    question: str
    candidates: Annotated[list[dict], operator.add]  # accumulates from N parallel generate calls
    scored:     list[dict]   # full scored list, set once by score_all
    best:       str          # winning chain's answer


class GenState(TypedDict):
    question: str


def dispatch(state: BonState) -> list[Send]:
    """Fan out N independent generate calls — same question, different temperature seeds."""
    return [Send("generate", {"question": state["question"]}) for _ in range(N_SAMPLES)]


def generate(state: GenState) -> dict:
    """Produce one chain-of-thought solution. High temp → diverse reasoning paths."""
    reply = _gen.invoke([
        {"role": "system", "content": "Solve step by step. End your response with 'Answer: <answer>'"},
        {"role": "user",   "content": state["question"]},
    ])
    text = reply.content.strip()
    # Extract declared answer; fall back to the last non-empty line.
    answer = next(
        (l.split("Answer:")[-1].strip() for l in text.splitlines() if "Answer:" in l),
        text.splitlines()[-1] if text.splitlines() else "",
    )
    return {"candidates": [{"reasoning": text, "answer": answer}]}


def score_all(state: BonState) -> dict:
    """Score every candidate with the LLM judge; pick highest-scoring chain."""
    scored = []
    for c in state["candidates"]:
        raw = _judge.invoke([
            {"role": "user", "content": JUDGE_PROMPT.format(
                question=state["question"], reasoning=c["reasoning"]
            )}
        ]).content
        s, e = raw.find("{"), raw.rfind("}") + 1
        try:
            data = json.loads(raw[s:e])
            score, critique = int(data.get("score", 5)), data.get("critique", "")
        except (TypeError, ValueError, json.JSONDecodeError):
            score, critique = 1, "Invalid judge response."
        score = min(10, max(1, score))
        scored.append({**c, "score": score, "critique": critique})

    best = max(scored, key=lambda c: c["score"])
    return {"scored": scored, "best": best["answer"]}

def create_workflow():
    g = StateGraph(BonState)
    g.add_node("generate",  generate)
    g.add_node("score_all", score_all)
    g.add_conditional_edges(START, dispatch, ["generate"])
    g.add_edge("generate",  "score_all")
    g.add_edge("score_all", END)
    return g.compile()
