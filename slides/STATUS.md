# Presentation Status — All Hands AI 2026

Quick-startup context for resuming work. Read this first, then AGENT_INSTRUCTIONS.md for build mechanics.

---

## What this is

An all-hands presentation for a software company's AI transformation moment. Title: **Strategic inflection point 2026**. ~76 minutes total. Delivered by section authors to the whole company.

**Build system:** Edit `.md` files here → run `build.py` from the project root → static HTML lands in `output/`.

```
python3 build.py
```

---

## Sections and authors

| # | Section slug | Title | Author | Duration | Topic slides |
|---|---|---|---|---|---|
| 01 | `01-strategy` | Strategy — Exploding into a multiverse of opts | Roko Roić | 5 MIN | 3 built ✓ |
| 02 | `02-sdlc` | SDLC — The all new way to develop software | Darko Špoljarić | 15 MIN | none yet |
| 03 | `03-adlc` | ADLC — Agents development life cycle | Vedran Pugar | 10 MIN | none yet |
| 04 | `04-mdlc` | MDLC — Models development life cycle | Marco Hrlić | 10 MIN | none yet |
| 05 | `05-uxax` | UX/AX — New and updated interactions | Aida Malkić | 10 MIN | none yet |
| 06 | `06-discovery` | Discovery — Discovery and customer success | Aida Malkić | 10 MIN | none yet |
| 07 | `07-gtm` | GTM — Sales and marketing | Hrvoje Fijucek | 10 MIN | none yet |
| 08 | `08-cto` | Support — How we plan to tackle the curve | Marko Štefančić | 6 MIN | none yet |

---

## Current slide inventory

**Built (12 HTML files):**
- `00-title.md` — Cover + auto-generated agenda
- `01-strategy.md` — Section intro
- `01-01-strategy-main.md` — "Where we are right now" (slide_with_text_and_image)
- `01-02-Engineering.md` — "A warm welcome to our new stars" (slide_with_bullets)
- `01-03-New life cycles.md` — "What changed for us" (slide_with_bullets)
- `02-sdlc.md` through `08-cto.md` — Section intros only

**Remaining work:** Topic slides for sections 02–08. Each section currently has only its intro slide.

---

## Key content decisions already made

- Brand accent color: mint green (`text-brand-mint` spans)
- Slide title split: `slide-title-main` (plain) + `slide-title-accent` (mint colored)
- Single image in use: `images/inflection-point.png` (used as section image on all sections so far)
- Template `slide_with_text_and_image` has 4 bullets + key insight card + 2 stat boxes
- Template `slide_with_bullets` has up to 6 bullets (hide unused ones)
- Navigation is fully auto-wired from filenames — never put nav fields in .md files
- Section timer config auto-injected at build time — no manual timer fields needed

---

## How to add a new slide

1. Pick a template (see `template-nn-nn-*.md` starters)
2. Name the file `NN-MM-descriptive-name.md` (e.g. `02-01-new-sdlc-overview.md`)
3. Fill in the fields — only content fields, no nav/counter fields
4. Run `python3 build.py` from project root

---

## What NOT to do

- Never put `nav-agenda`, `nav-prev`, `nav-next`, or `slide-counter` in .md files
- Never run git commands (build system is local-only by design)
- Never edit files in `output/` — always edit the source `.md` and rebuild
