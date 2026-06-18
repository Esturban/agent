import os
import subprocess
import anthropic
from .tools import MODEL, CU_TOOLS, MAX_STEPS


def _run_bash(command: str) -> str:
    """Execute a shell command; return stdout or a formatted error."""
    try:
        r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
        return r.stdout or (f"[exit {r.returncode}] {r.stderr.strip()}" if r.returncode else "(no output)")
    except Exception as e:
        return f"Error: {e}"


def _run_editor(params: dict) -> str:
    """Minimal text_editor_20241022 executor: create, view, str_replace."""
    cmd, path = params.get("command", "view"), params.get("path", "")
    if cmd == "create":
        with open(path, "w") as f:
            f.write(params.get("file_text", ""))
        return f"Created {path}"
    if cmd == "view":
        try:
            return open(path).read()
        except FileNotFoundError:
            return f"Not found: {path}"
    if cmd == "str_replace":
        content = open(path).read()
        open(path, "w").write(content.replace(params.get("old_str", ""), params.get("new_str", "")))
        return "Done"
    return "Unknown editor command"


def run_agent(task: str) -> list[dict]:
    """Action loop: send task → receive ToolUseBlocks → execute → feed results → repeat.

    Each iteration the model sees previous tool outputs and decides the next action.
    Stops on stop_reason='end_turn' or when no tool calls remain.
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": task}]
    steps: list[dict] = []

    for _ in range(MAX_STEPS):
        resp = client.beta.messages.create(
            model=MODEL, max_tokens=4096,
            tools=CU_TOOLS, messages=messages,
            betas=["computer-use-2024-10-22"],
        )

        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        for b in resp.content:
            if b.type == "text" and b.text.strip():
                steps.append({"type": "text", "content": b.text.strip()})

        if resp.stop_reason == "end_turn" or not tool_uses:
            break

        results = []
        for tu in tool_uses:
            output = _run_bash(tu.input.get("command", "")) if tu.name == "bash" else _run_editor(tu.input)
            steps.append({"type": "action", "tool": tu.name, "input": tu.input, "output": output})
            results.append({"type": "tool_result", "tool_use_id": tu.id, "content": output})

        messages += [{"role": "assistant", "content": resp.content},
                     {"role": "user",      "content": results}]

    return steps
