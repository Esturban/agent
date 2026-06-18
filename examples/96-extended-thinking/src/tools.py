MODEL = "claude-3-7-sonnet-20250219"
THINKING_BUDGET = 8000  # private scratchpad tokens; counts toward max_tokens

# Three problems chosen to expose where private reasoning changes the answer.
# CRT and Wordplay catch naive pattern-matching. Modular math needs real work.
PUZZLES = [
    {
        "label": "Modular Math",
        "prompt": "What is the last digit of 7^77? Show your reasoning step by step.",
    },
    {
        "label": "Wordplay",
        "prompt": (
            "I have exactly two coins that add up to 30 cents. "
            "One of them is not a nickel. What are the two coins?"
        ),
    },
    {
        "label": "CRT (Cognitive Reflection)",
        "prompt": (
            "A bat and a ball together cost $1.10. "
            "The bat costs exactly $1.00 more than the ball. "
            "How much does the ball cost? Give your answer in cents."
        ),
    },
]
