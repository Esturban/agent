# Self-consistency requires problems with clear, verifiable answers so the
# majority vote is observable. Math and logic problems work best because
# correct reasoning paths converge on the same final answer.

# N_PATHS: how many independent CoT samples to generate.
# Wang et al. 2022 found accuracy gains plateau near N=40 on hard tasks;
# N=5 is enough to demonstrate the clustering effect without burning tokens.
N_PATHS = 5

SAMPLE_PROBLEMS = [
    {
        "question": (
            "A train travels 120 miles in 2 hours, then 90 miles in 1.5 hours. "
            "What is the average speed over the entire journey?"
        ),
        "answer": "60 mph",
    },
    {
        "question": (
            "A store marks items up by 40% and then offers a 20% discount. "
            "What is the net percentage change from the original price?"
        ),
        "answer": "12% increase",
    },
    {
        "question": (
            "How many integers between 100 and 999 inclusive are divisible by both 4 and 6?"
        ),
        "answer": "75",
    },
]
