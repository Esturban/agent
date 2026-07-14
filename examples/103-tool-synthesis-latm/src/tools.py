"""Tool registry and LLM clients for LATM (LLMs as Tool Makers).

Cai et al. 2023 "Large Language Models as Tool Makers" (arxiv.org/abs/2305.17126):
a dispatcher LLM selects tools; a tool-maker LLM generates Python code for new ones.
Synthesized tools are cached — amortizing generation cost across future calls.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

MODEL = "gpt-5.4-nano"

# Tasks designed to trigger synthesis on the first occurrence, then reuse on repeats.
# The tool-maker is instructed to call zero-auth public APIs (wttr.in, numbersapi.com).
DEMO_TASKS = [
    "What is the current weather in Paris?",
    "What is the current weather in Tokyo?",   # reuses synthesized weather tool
    "Give me a fun fact about the number 42.",
    "Give me a fun fact about the number 7.",  # reuses synthesized fact tool
    "How many vowels are in the word 'extraordinary'?",
]

TOOLMAKER_SYSTEM = """\
You write Python functions. Given a task, produce ONE function that solves it.
Rules:
- Name in snake_case; accept exactly one str argument (the full task description)
- Extract any needed values from the argument with string parsing or regex
- Return a plain string result
- Use only Python stdlib + requests (already installed)
- For live data use ONLY zero-auth free APIs:
    weather  → https://wttr.in/{city}?format=3
    numbers  → http://numbersapi.com/{n}
    anything else → prefer stdlib over external calls
- Put ALL imports inside the function body
Output ONLY the raw function definition. No markdown. No explanation.\
"""

# Dispatcher picks an existing tool or says 'synthesize'.
dispatcher = ChatOpenAI(model=MODEL, temperature=0)
# Tool-maker generates Python code; higher temperature for creative function naming.
tool_maker = ChatOpenAI(model=MODEL, temperature=0.2)
