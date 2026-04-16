---
template: slide_with_bullets
---

# Slide Header

overhead-title: Agents Development Life Cycle
slide-title-main: Six phases.
slide-title-accent: Every one earns its place.

# Bullets (up to 6 — leave a title/body pair blank to hide that bullet)

bullet-1-title: 1. Conceptualize
bullet-1-body: Is an agent actually the right solution? Define success criteria before you start. Output: agent brief — problem statement, scope, and a go/no-go decision.

bullet-2-title: 2. Design the Harness
bullet-2-body: Architecture before code. Brain (model + system prompt), memory, tools, skills, subagents, orchestrator. Output: architecture diagram and tool list.

bullet-3-title: 3. Build
bullet-3-body: Implement the harness. Register tools — narrow and composable, not broad and monolithic. Write the system prompt as you would write code: with intention, under version control, with peer review. Expect to revise it.

bullet-4-title: 4. Define HITL
bullet-4-body: Map every agent action: auto, approve, or audit. Irreversible actions always need an approval gate. This is an engineering decision, not a product one.

bullet-5-title: 5. Evaluate
bullet-5-body: Two modes. Offline: build a controlled dataset and score the agent against it before shipping. Online: sample live interactions in production and monitor loop quality continuously. Both are required — neither replaces the other. A well-built eval suite also becomes a safety net for model upgrades — when a better model is available, you can adopt it with confidence instead of guesswork.

bullet-6-title: 6. Integrate
bullet-6-body: Connect to UI, backend, and other agents. The main challenge is state sync — the UI must stay coherent while the agent is mid-run, retrying, or paused at a HITL gate waiting for a human signal. Observability is non-negotiable from day one.
