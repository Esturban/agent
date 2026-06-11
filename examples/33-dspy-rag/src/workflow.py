import dspy
from dspy.teleprompt import BootstrapFewShot

from .tools import TRAINSET, GenerateAnswer, keyword_retrieve


class RAG(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question: str):
        context = keyword_retrieve(question)
        return self.generate(context=context, question=question)


def _validate(example, pred, trace=None) -> bool:
    return bool(pred.answer and len(pred.answer.strip()) > 10)


def create_pipeline() -> tuple[RAG, RAG]:
    """Return (base_rag, compiled_rag) — compiled has auto-bootstrapped few-shots."""
    base = RAG()
    compiler = BootstrapFewShot(metric=_validate, max_bootstrapped_demos=2, max_labeled_demos=2)
    compiled = compiler.compile(RAG(), trainset=TRAINSET)
    return base, compiled
