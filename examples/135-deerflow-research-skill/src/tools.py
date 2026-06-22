SOURCE_FILES = {
    "01-state-graph.md": """\
# State Graph Pattern
Explicit directed graph. Nodes process state; edges route flow.
Use when: pipeline has well-defined stages with predictable transitions.
Trade-offs: verbose setup; great for auditability and replay.
""",
    "02-reactive-loop.md": """\
# Reactive Loop Pattern
Agent calls tools in a loop until a stop condition is met.
Use when: task is open-ended; number of steps is unknown upfront.
Trade-offs: harder to debug; powerful for code generation and research.
""",
    "03-multi-agent.md": """\
# Multi-Agent Pattern
Supervisor delegates sub-tasks to specialist worker agents.
Use when: task can be parallelised or needs diverse domain expertise.
Trade-offs: coordination overhead; scales well for deep research tasks.
""",
}

# Skill activation prompts — use these as the message body to trigger the skill.
REPORT_PROMPT = (
    "@course-research Summarise the uploaded notes into a short report."
)
REPORT_PROMPT_DEEP = (
    "@course-research Generate a structured research report: executive summary, "
    "pattern comparison table, implementation notes, and next-step recommendations."
)

SKILL_NAME = "course-research"
