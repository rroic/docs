---
template: slide_with_bullets
---

# Slide Header

overhead-title: Agents Development Life Cycle
slide-title-main: Agents are
slide-title-accent: not software.

# Bullets (up to 6 — leave a title/body pair blank to hide that bullet)

bullet-1-title: The system prompt is code
bullet-1-body: It is the agent's constitution — the primary way you shape its behavior. It needs version control, peer review, and iteration. Treating it as a config file is the first mistake.

bullet-2-title: You cannot unit test an agent
bullet-2-body: Outputs are probabilistic. You cannot assert an answer. Instead, you define what good looks like in advance — evaluation datasets, scoring rubrics, loop quality metrics — and run the agent against them. Different discipline entirely.

bullet-3-title: HITL is architecture, not afterthought
bullet-3-body: Where humans intervene must be designed into the system before a line of code is written. Think of it as access control for autonomous actions — the same discipline you already apply to permissions, now applied to behavior.

bullet-4-title: The feedback loop never closes
bullet-4-body: Once in production, agents keep improving from real use. Model updates, new edge cases, and user feedback all feed back into the system. Engineers who care about quality already live this way — ADLC just makes it explicit.
