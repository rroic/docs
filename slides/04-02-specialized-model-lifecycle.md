---
template: slide_with_bullets
---

# Slide Header

overhead-title: Models Development Life Cycle
slide-title-main: Specialized models.
slide-title-accent: When you own everything.

# Bullets (up to 6 — leave a title/body pair blank to hide that bullet)

bullet-1-title: Foundation models — you integrate, not train
bullet-1-body: For reasoning, generation, and open-ended tasks, foundation models are the starting point. You select, evaluate, and configure them — prompt engineering, system design, monitoring provider changes. The development work is real, but the model itself is not yours.

bullet-2-title: Start with the problem, not the model
bullet-2-body: Narrow scope, clear success criteria, confirmed data availability — these come before any training decisions. Being able to write the evaluation rubric is a good signal you are ready to start.

bullet-3-title: Data quality sets the ceiling
bullet-3-body: Labeling is slow, expensive, and consistently underestimated. The quality of your data is the upper bound on your model's quality. Investing here early pays off throughout the lifecycle.

bullet-4-title: Small models win on narrow tasks
bullet-4-body: A fine-tuned classifier often beats a frontier model on cost, latency, and accuracy — when the task is well-defined. OCR, guardrails, intent classification. These are not GPT-4 problems.

bullet-5-title: Evaluation before you ship
bullet-5-body: Precision, recall, F1 — defined against what matters to your users. A held-out test set gives you real confidence the model is ready before it reaches production.

bullet-6-title: Production data shifts — and that is normal
bullet-6-body: Retraining over time is regular maintenance, not a sign something went wrong. Models benefit from the same versioning discipline as the rest of your code.
