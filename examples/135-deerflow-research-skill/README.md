# 135 — DeerFlow Research Skill

Upload course notes into a DeerFlow thread, activate a custom `@course-research` skill, and watch subagents produce a structured report artifact.

## How to run

```bash
# 1. Start DeerFlow with skills enabled — see runtime/README.md
# 2. Copy runtime/skills/ into your deer-flow checkout root
DEERFLOW_BASE_URL=http://localhost:8000 python main.py
```

## What it demonstrates

- `runtime/skills/custom/course-research/SKILL.md`: DeerFlow prompt module — trigger, section instructions, subagent delegation
- `ResearchRun`: uploads source files, streams a skill-activated run with `plan_mode=True` + `subagent_enabled=True`
- Skill vs subagent split: skill owns report structure; subagents draft individual sections
- Contrast with 134: 134 drives DeerFlow as a generic chat API; 135 uses it as a configured skill runtime
