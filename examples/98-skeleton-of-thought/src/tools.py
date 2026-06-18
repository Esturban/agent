# Two questions that produce 4-5 skeleton points — enough to show meaningful parallelism.
QUESTIONS = [
    "What are the key differences between supervised, unsupervised, and reinforcement learning?",
    "How does a transformer neural network work?",
]

SKELETON_PROMPT = """\
Generate a numbered skeleton outline for a clear answer to the question below.
Output ONLY the skeleton: one numbered point per line, no elaboration, 4-5 points.

Question: {question}"""

# Each expand call receives only its own point — parallel calls have no shared context.
EXPAND_PROMPT = """\
Expand the following skeleton point into 2-3 concise, informative sentences.
Stay focused on this point only.

Question context: {question}
Point: {point}"""
