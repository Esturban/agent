import dspy

DOCS = [
    "DSPy was created by Stanford NLP and released in 2023.",
    "DSPy replaces hand-crafted prompts with compiled, auto-optimized signatures.",
    "DSPy Signatures define typed input and output fields using Python class syntax.",
    "DSPy ChainOfThought adds step-by-step reasoning before producing the final answer.",
    "DSPy BootstrapFewShot automatically selects few-shot examples from a labeled trainset.",
    "MIPROv2 is a DSPy optimizer that jointly tunes instructions and few-shot examples.",
    "DSPy modules are composable Python classes that inherit from dspy.Module.",
    "LangGraph was created by LangChain Inc. and released in January 2024.",
    "LangChain LCEL uses the | pipe operator to chain prompts, models, and parsers.",
    "LangGraph StateGraph compiles into a runnable that can be invoked or streamed.",
]

TRAINSET = [
    dspy.Example(question="Who created DSPy?", answer="Stanford NLP").with_inputs("question"),
    dspy.Example(
        question="What does DSPy ChainOfThought do?",
        answer="adds step-by-step reasoning before the final answer",
    ).with_inputs("question"),
    dspy.Example(question="When was LangGraph released?", answer="January 2024").with_inputs(
        "question"
    ),
    dspy.Example(
        question="What is BootstrapFewShot?",
        answer="selects few-shot examples automatically from a trainset",
    ).with_inputs("question"),
]

SAMPLE_QUESTIONS = [
    "Who created DSPy and when?",
    "How does DSPy differ from LangChain LCEL?",
    "What is the role of MIPROv2 in DSPy?",
]


class GenerateAnswer(dspy.Signature):
    """Answer a question given relevant context from a knowledge base."""

    context: str = dspy.InputField(desc="relevant facts from the knowledge base")
    question: str = dspy.InputField()
    answer: str = dspy.OutputField(desc="1-2 sentences, factual and concise")


def keyword_retrieve(question: str, k: int = 3) -> str:
    words = set(question.lower().split())
    scored = [(sum(w in d.lower() for w in words), d) for d in DOCS]
    scored.sort(reverse=True)
    top = [d for _, d in scored[:k] if _ > 0] or DOCS[:k]
    return "\n".join(top)
