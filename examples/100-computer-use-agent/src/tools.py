MODEL = "claude-3-5-sonnet-20241022"
MAX_STEPS = 10

# bash + text_editor run without a display — same action-loop pattern as full computer use.
# Add "computer_20241022" + display config for mouse/keyboard control in a Docker+Xvfb env.
CU_TOOLS = [
    {"type": "bash_20241022",        "name": "bash"},
    {"type": "text_editor_20241022", "name": "str_replace_editor"},
]

TASK = (
    "Write a Python script called /tmp/fib.py that prints the first 10 Fibonacci numbers, "
    "one per line. Run it and show me the output."
)
