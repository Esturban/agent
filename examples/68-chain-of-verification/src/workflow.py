from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.tools import ClaimList, ClaimVerification


class CoVeState(TypedDict):
    question: str
    initial_answer: str
    claims: list[str]
    verifications: list[dict]
    revised_answer: str


def create_workflow():
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    claim_extractor = llm.with_structured_output(ClaimList)
    claim_verifier = llm.with_structured_output(ClaimVerification)

    def generate(state: CoVeState) -> dict:
        answer = llm.invoke([HumanMessage(content=state["question"])]).content.strip()
        return {"initial_answer": answer}

    def plan_verification(state: CoVeState) -> dict:
        prompt = f"Extract all specific, verifiable factual claims from this answer:\n{state['initial_answer']}"
        result: ClaimList = claim_extractor.invoke([HumanMessage(content=prompt)])
        return {"claims": result.claims}

    def execute_verification(state: CoVeState) -> dict:
        verifications = []
        for claim in state["claims"]:
            result: ClaimVerification = claim_verifier.invoke([
                SystemMessage(content="You are a fact-checker. Verify the following claim using your knowledge."),
                HumanMessage(content=f"Claim: {claim}"),
            ])
            verifications.append(result.model_dump())
        return {"verifications": verifications}

    def revise(state: CoVeState) -> dict:
        failed = [v for v in state["verifications"] if not v["correct"]]
        if not failed:
            return {"revised_answer": state["initial_answer"]}
        corrections = "\n".join(f"- Wrong: '{v['claim']}' → Correct: {v['correction']}" for v in failed)
        prompt = (
            f"Revise this answer to fix the following factual errors:\n\nOriginal:\n{state['initial_answer']}\n\nErrors:\n{corrections}"
        )
        revised = llm.invoke([HumanMessage(content=prompt)]).content.strip()
        return {"revised_answer": revised}

    graph = StateGraph(CoVeState)
    graph.add_node("generate", generate)
    graph.add_node("plan_verification", plan_verification)
    graph.add_node("execute_verification", execute_verification)
    graph.add_node("revise", revise)
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "plan_verification")
    graph.add_edge("plan_verification", "execute_verification")
    graph.add_edge("execute_verification", "revise")
    graph.add_edge("revise", END)
    return graph.compile()
