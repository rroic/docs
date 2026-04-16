---
template: slide_with_bullets
---

# Slide Header

overhead-title: Agents Development Life Cycle
slide-title-main: New roles.
slide-title-accent: New ownership.

# Bullets (up to 6 — leave a title/body pair blank to hide that bullet)

bullet-1-title: Prompt Engineer
bullet-1-body: The system prompt is the agent's primary behavior specification. The prompt engineer authors, versions, and iterates it. They own the Build phase the way a software engineer owns the codebase.

bullet-2-title: HITL Designer
bullet-2-body: Not a UX role — an architecture role. The HITL designer maps every agent action to a control level and designs the checkpoints where humans stay in the loop. They own the Define HITL phase.

bullet-3-title: Agent Architect
bullet-3-body: Designs the agent's cognitive architecture — model selection, memory, tools, skills, subagents — before any code is written. They own the Design Harness phase and enforce the boundary between framework and use-case logic.

bullet-4-title: Evaluation Engineer
bullet-4-body: The evaluation engineer builds test datasets, defines scoring rubrics, and runs the agent against them before it ever touches production. Agent outputs are probabilistic — "it works" has to mean something measurable. They own the Evaluate phase.
