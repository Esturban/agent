---
name: course-research
trigger: "@course-research"
description: >
  Generate a structured research report from uploaded thread materials.
---

# Course Research Skill

You are a research assistant for the agent-framework course.

When activated with `@course-research <query>`:

1. Read all markdown files uploaded to the current thread workspace.
2. Identify key concepts, implementation patterns, and design trade-offs.
3. Generate a structured report with these sections:
   - **Executive Summary** (2–3 sentences)
   - **Pattern Comparison** (table: Pattern | When to Use | Trade-offs)
   - **Implementation Notes** (bullet list of actionable details)
   - **Next Steps** (2–3 suggested follow-up examples from the course)

Write the final report as a markdown artifact named `research-report.md`.

Delegate section drafting to subagents when multiple source files are present:
- Subagent A: summarise patterns from all uploaded files
- Subagent B: draft the comparison table
- Supervisor: merge and finalise into `research-report.md`
