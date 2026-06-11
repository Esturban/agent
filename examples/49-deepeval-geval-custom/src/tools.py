import json
from typing import TypedDict
from langchain_openai import ChatOpenAI

TEST_CASES = [
    {
        "input": "Explain what an API is in one sentence.",
        "concise_output": "An API is an interface that lets software systems communicate with each other.",
        "verbose_output": "Well, an API, which stands for Application Programming Interface, is essentially a set of rules and protocols that allows different software applications to communicate and interact with each other, enabling them to share data and functionality in a standardized way, which is really quite fundamental to modern software development.",
    },
    {
        "input": "List the top 3 benefits of using TypeScript.",
        "correct_format": "1. Static typing catches errors at compile time\n2. Better IDE support and autocomplete\n3. Improved code maintainability",
        "wrong_format": "TypeScript has static typing, which is good. Also IDE support is nice. And it helps with code that is easier to maintain over time.",
    },
    {
        "input": "What year was Python released?",
        "correct_output": "Python was first released in 1991.",
        "wrong_output": "Python was released in 2001.",  # wrong year
    },
]

JSON_OUTPUTS = [
    '{"name": "Alice", "age": 30, "role": "engineer"}',   # valid
    '{"name": "Bob", "age": "thirty"}',                    # age should be int
    'name: Charlie, age: 25',                               # not valid JSON
]


class EvalState(TypedDict):
    input: str
    output: str
    score: float


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
