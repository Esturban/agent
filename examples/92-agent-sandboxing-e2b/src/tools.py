# Tasks that generate interesting, verifiable Python — chosen to demonstrate
# that the sandbox captures real output (stdout, errors) without touching
# the host machine's filesystem, processes, or network.

CODING_TASKS = [
    "Write Python to calculate and print the first 10 Fibonacci numbers.",
    (
        "Write Python to simulate rolling two dice 1000 times. "
        "Print the most common sum and its frequency."
    ),
    (
        "Write Python to count the frequency of each letter (case-insensitive) "
        "in 'Hello World' and print the top 3 letters with their counts."
    ),
    (
        "Write Python with a deliberate ZeroDivisionError to demonstrate "
        "that sandbox errors are captured without crashing the agent."
    ),
]
