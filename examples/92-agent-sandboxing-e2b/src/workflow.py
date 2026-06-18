from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

# E2B Sandbox (e2b.dev) — safe code execution for LLM agents
#
# Why sandboxing matters:
#   - Raw exec() or subprocess runs on YOUR host with YOUR permissions
#   - A buggy (or adversarial) agent can delete files, exfiltrate data, or crash
#     the host process
#   - E2B spins up an ephemeral cloud microVM per execution: completely isolated
#   - stdout/stderr/errors returned as structured data — no side effects on host
#   - Enforced timeout; VM is destroyed after execution
#
# Pattern: generate_code → execute_in_sandbox → interpret_result
# The sandbox node is the safety gate — no generated code touches the host.
#
# Setup: pip install e2b-code-interpreter
#        Set E2B_API_KEY in .env (free tier at e2b.dev)

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class SandboxState(TypedDict):
    task: str           # natural language description of what to compute
    code: str           # LLM-generated Python — NOT yet executed
    stdout: str         # captured from sandbox execution
    stderr: str         # errors captured from sandbox (not host)
    interpretation: str  # LLM explanation of what the execution produced


def generate_code(state: SandboxState) -> dict:
    """Generate Python code for the task. Code is NOT executed here.

    This separation is important: generation and execution are distinct nodes.
    It lets you inspect, log, or modify the code before it runs in the sandbox.
    """
    prompt = (
        "Write clean, working Python code to accomplish this task. "
        "Output ONLY the raw Python code — no markdown fences, no explanation.\n\n"
        f"Task: {state['task']}"
    )
    code = _llm.invoke([HumanMessage(content=prompt)]).content.strip()
    # Strip markdown fences if the model adds them despite the instruction.
    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1])  # remove first and last fence lines
    return {"code": code}


def execute_in_sandbox(state: SandboxState) -> dict:
    """Run the generated code inside an E2B cloud sandbox.

    Sandbox() creates an ephemeral microVM — the context manager ensures it is
    destroyed after execution even if an exception occurs.

    execution.logs.stdout — list of stdout lines
    execution.logs.stderr — list of stderr lines
    execution.error       — structured exception info if code raised an error
    """
    from e2b_code_interpreter import Sandbox  # lazy import — optional dep

    with Sandbox() as sandbox:
        execution = sandbox.run_code(state["code"])
        stdout = "\n".join(execution.logs.stdout) if execution.logs.stdout else ""
        stderr = "\n".join(execution.logs.stderr) if execution.logs.stderr else ""
        # execution.error captures exceptions without crashing the agent —
        # this is the key safety property vs. bare exec().
        if execution.error:
            stderr = f"{stderr}\n{execution.error.name}: {execution.error.value}".strip()
    return {"stdout": stdout, "stderr": stderr}


def interpret_result(state: SandboxState) -> dict:
    """Interpret the sandbox output — explain what happened in plain English.

    This node closes the loop: the agent can now reason about the execution
    result and decide whether to retry, report, or continue the task.
    """
    output_block = (
        f"STDOUT:\n{state['stdout'] or '(empty)'}\n"
        f"STDERR:\n{state['stderr'] or '(none)'}"
    )
    prompt = (
        f"Task: {state['task']}\n\n"
        f"Code run in sandbox:\n{state['code']}\n\n"
        f"Execution output:\n{output_block}\n\n"
        "Explain what the code did, whether it succeeded, and what the output means. "
        "Be concise."
    )
    interpretation = _llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return {"interpretation": interpretation}


def create_workflow():
    builder = StateGraph(SandboxState)
    builder.add_node("generate_code", generate_code)
    builder.add_node("execute_in_sandbox", execute_in_sandbox)
    builder.add_node("interpret_result", interpret_result)
    builder.add_edge(START, "generate_code")
    builder.add_edge("generate_code", "execute_in_sandbox")
    builder.add_edge("execute_in_sandbox", "interpret_result")
    builder.add_edge("interpret_result", END)
    return builder.compile()
