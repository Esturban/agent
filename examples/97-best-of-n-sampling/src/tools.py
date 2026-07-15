N_SAMPLES = 4  # reasoning chains to generate per question

# Problems where reasoning quality varies — good test bed for a process reward judge.
PROBLEMS = [
    {
        "label": "Rate Problem",
        "question": (
            "A train travels 120 miles in 90 minutes. "
            "How many miles will it travel in 2.5 hours at the same speed?"
        ),
    },
    {
        "label": "Constraint Logic",
        "question": (
            "Alice, Bob, and Carol each own exactly one pet: a cat, a dog, or a fish. "
            "Alice does not own the cat or the fish. Bob does not own the fish. Carol does not own the dog. "
            "Who owns the cat?"
        ),
    },
]

# Instructs the judge to score reasoning quality, not just correctness.
# Process reward: intermediate steps matter as much as the final answer.
JUDGE_PROMPT = """\
You are a process reward model. Score this reasoning chain on 3 criteria:
  1. Step clarity   — each step is labeled and easy to follow
  2. Logical rigor  — no skipped deductions or unjustified leaps
  3. Correct answer — the final answer is right

Question: {question}

Reasoning chain:
{reasoning}

Respond with ONLY valid JSON (no markdown):
{{"score": <integer 1-10>, "critique": "<one sentence>"}}"""
