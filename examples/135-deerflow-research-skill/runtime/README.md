# DeerFlow Runtime Setup — Research Skill (Example 135)

This extends [example 134's runtime setup](../../134-deerflow-embedded-client/runtime/README.md).
Follow those steps first, then come back here for the skill-specific additions.

## Additional steps for the research skill

**1.** Copy `config.sample.yaml` → `conf/config.yaml` in your deer-flow checkout:

```bash
cp examples/135-deerflow-research-skill/runtime/config.sample.yaml \
   ../deer-flow/conf/config.yaml
```

**2.** Copy the custom skill into the deer-flow root:

```bash
cp -r examples/135-deerflow-research-skill/runtime/skills ../deer-flow/
```

**3.** Confirm paths in `conf/config.yaml`:

```yaml
subagent:
  enabled: true

skills:
  custom:
    - path: "skills/custom/course-research"
      name: "course-research"
```

**4.** Restart DeerFlow so it loads the skill registry:

```bash
cd ../deer-flow && make dev
```

## Run the example

```bash
cd /path/to/py/agent
DEERFLOW_BASE_URL=http://localhost:8000 python examples/135-deerflow-research-skill/main.py
```

## How the skill works

DeerFlow reads `SKILL.md`, registers `@course-research` as an activatable prompt module, and when triggered with `subagent_enabled=True`:
- Subagent A summarises patterns from uploaded files
- Subagent B drafts the comparison table
- The supervisor merges and writes `research-report.md` as a thread artifact
