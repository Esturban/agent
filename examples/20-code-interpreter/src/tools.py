import subprocess
import sys

MAX_ITERATIONS = 3
TIMEOUT = 10  # seconds

SAMPLE_TASKS = [
    "Write a function that returns the first N Fibonacci numbers and print the first 10.",
    "Sort a list of tuples by the second element in descending order. Use: [(3, 1), (1, 4), (2, 2), (4, 3)]",
    "Write a function to check if a string is a palindrome and test it with 'racecar' and 'hello'.",
]


def execute_code(code: str) -> dict:
    """Run Python code in a subprocess sandbox with a hard timeout."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"Execution timed out after {TIMEOUT} seconds.",
            "returncode": -1,
        }
