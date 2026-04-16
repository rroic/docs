# Agent Instructions — Presentation Build System

## Overview

This document tells the agent how to build a complete web-based presentation from content files and HTML templates. The presentation is a folder of static HTML files that link to each other via navigation buttons.

---

## Paths

| Resource | Path |
|---|---|
| Content files (MD) | `slides/` |
| HTML templates | `assets/templates/design_templates/` |
| Image assets (source) | `assets/images/` |
| Output folder | `output/` |
| Output images (copied) | `output/assets/images/` |

---

## File Naming Convention

| File pattern | Template used | Output path | Purpose |
|---|---|---|---|
| `00-title.md` | `presentation_first_slide` | `output/index.html` | Cover + agenda slide |
| `NN-name.md` | `section_intro_slide` | `output/NN-name/index.html` | First slide of a section |
| `NN-MM-name.md` | declared in frontmatter | `output/NN-MM-name/index.html` | Individual slides within a section |

- `NN` = two-digit section number (01, 02, 03…)
- `MM` = two-digit slide number within the section (01, 02, 03…)
- Sections are ordered by `NN`. Slides within a section are ordered by `MM`.

**The agent derives template, output path, section number, section slug, navigation, and slide counter directly from the filename — no frontmatter needed for `00-title.md` or `NN-name.md` files.**

Derivation rules:
- `00-title.md` → template: `presentation_first_slide`, output: `output/index.html`
- `NN-name.md` → template: `section_intro_slide`, output: `output/NN-name/index.html`, section number: `NN`, section slug: `name`
- `NN-MM-name.md` → output: `output/NN-MM-name/index.html`; template is declared in the file's frontmatter (`template:` field) since topic slides can use different templates

For `NN-MM-name.md` files, the **only** frontmatter field is `template:`. Fields `output`, `section`, `section-slug`, `slide`, `nav-agenda`, `nav-prev`, `nav-next`, and `slide-counter` must not appear in these files — the agent derives all of them from the filename and the section's file list.

---

## Templates

### 1. `presentation_first_slide` — Cover / Agenda

**Output file:** `output/index.html`

**Fields read from `00-title.md`:**

| ID | Field in `00-title.md` |
|---|---|
| `presentation-label` | `presentation-label` |
| `presentation-title` | Reconstruct h1 as: `{presentation-title-main} <span id="presentation-title-accent">{presentation-title-accent}</span>` |
| `presentation-subtitle` | `presentation-subtitle` |
| `presentation-duration` | Auto-calculated — sum all `agenda-duration` values from section files (parse the leading integer, e.g. `"15 MIN"` → 15). Format result as `"{total} Minutes"`. Do not read this field from `00-title.md`. |

**Agenda items — fully auto-resolved from section files:**

`00-title.md` contains no agenda fields at all. The agent builds the agenda entirely by scanning section files.

For each `NN-name.md` file, sorted by `NN` (mapping to agenda slot N = 1, 2, 3…):
- Read `agenda-title` from the section file → set `agenda-title-N` innerHTML
- Read `agenda-subtitle` from the section file → set `agenda-subtitle-N` innerHTML
- Read `agenda-duration` from the section file → set `agenda-duration-N` innerHTML
- Derive output path from filename: `NN-name.md` → `NN-name/index.html` → wrap `<div id="agenda-item-N">` in `<a href="NN-name/index.html" style="display:block;text-decoration:none;color:inherit;">`

Rules:
- Fewer than 8 sections → hide remaining `agenda-item-N` cards with `style="display:none"`
- More than 8 sections → log a warning; only the first 8 are shown

---

### 2. `section_intro_slide` — Section Introduction

**Output file:** derived from filename — `NN-name.md` → `output/NN-name/index.html`
No frontmatter needed. Template, output path, section number, and slug are all derived from the filename.

**Fields read but NOT rendered on this slide (used only for the cover agenda):**

| Field | Purpose |
|---|---|
| `agenda-title` | Section title as it appears on the cover agenda card |
| `agenda-subtitle` | Section subtitle as it appears on the cover agenda card |
| `agenda-duration` | Duration badge on the cover agenda card |

**IDs to populate:**

| ID | Field in MD |
|---|---|
| `overhead-title` | `overhead-title` |
| `slide-title-main` | Plain text part of title |
| `slide-title-accent` | Mint-colored part of title |
| `slide-intro` | `slide-intro` |
| `author-name` | `author-name` |
| `section-image` (`<img>` src) | `section-image` |
| `section-image` (`<img>` alt) | `section-image-alt` |
| `nav-agenda` (href) | `nav-agenda` |
| `nav-prev` (href) | Always `../index.html` (cover) |
| `nav-next` (href) | Output path of the first `NN-01-name.md` in this section, or `../index.html` if no topic slides exist |
| `slide-counter` | `01 / {total}` where total = 1 (section intro) + count of `NN-MM-name.md` files for this `NN` |

If `section-image` is blank or the file does not exist in `assets/images/`, add `style="display:none"` to `id="section-image-container"` so the layout does not break.

Image paths in MD files are relative to `assets/` (e.g. `images/photo.jpg`). Rewrite `src` to be relative to the output file's location (`../assets/images/photo.jpg`).

---

### 3. `slide_with_image` — Image Slide

**Output file:** `output/{section-slug}/{slide-slug}/index.html`

**IDs to populate:**

| ID | Field in MD |
|---|---|
| `overhead-title` | `overhead-title` |
| `slide-title-main` | Plain text part of title |
| `slide-title-accent` | Mint-colored part of title |
| `nav-agenda` (href) | `nav-agenda` |
| `nav-prev` (href) | Resolved from section slides list |
| `nav-next` (href) | Resolved from section slides list — if last slide, point to next section's `index.html` |
| `slide-counter` | Format: `{position} / {total}` |
| `<img>` src | `slide-image` |
| `<img>` alt | `slide-image-alt` |
| `box1-title` | `box1-title` |
| `box1-number` | `box1-number` |
| `box1-subtext` | `box1-subtext` |
| `box2-title` | `box2-title` |
| `box2-number` | `box2-number` |
| `box2-subtext` | `box2-subtext` |

---

### 4. `slide_with_text_and_image` — Text Slide

**Output file:** `output/{section-slug}/{slide-slug}/index.html`

**IDs to populate:**

| ID | Field in MD |
|---|---|
| `overhead-title` | `overhead-title` |
| `slide-title-main` | Plain text part of title |
| `slide-title-accent` | Mint-colored part of title |
| `nav-agenda` (href) | `nav-agenda` |
| `nav-prev` (href) | Resolved from section slides list |
| `nav-next` (href) | Resolved from section slides list |
| `slide-counter` | Format: `{position} / {total}` |
| `h2` in key insight card | `content-heading` |
| `p` body in key insight card | `content-body` |
| Bullet 1 `h4` / `p` | `bullet-1-title` / `bullet-1-body` |
| Bullet 2 `h4` / `p` | `bullet-2-title` / `bullet-2-body` |
| Bullet 3 `h4` / `p` | `bullet-3-title` / `bullet-3-body` |
| Bullet 4 `h4` / `p` | `bullet-4-title` / `bullet-4-body` |
| `box1-title` | `box1-title` |
| `box1-number` | `box1-number` |
| `box1-subtext` | `box1-subtext` |
| `box2-title` | `box2-title` |
| `box2-number` | `box2-number` |
| `box2-subtext` | `box2-subtext` |

---

### 5. `slide_with_bullets` — Bullet List Slide

**Output file:** `output/{NN-MM-name}/index.html`

**IDs to populate:**

| ID | Field in MD |
|---|---|
| `overhead-title` | `overhead-title` |
| `slide-title-main` | Plain text part of title |
| `slide-title-accent` | Mint-colored part of title |
| `nav-agenda` (href) | Resolved from file discovery |
| `nav-prev` (href) | Resolved from section slides list |
| `nav-next` (href) | Resolved from section slides list |
| `slide-counter` | Format: `{position} / {total}` |
| `bullet-1-title` / `bullet-1-body` | `bullet-1-title` / `bullet-1-body` |
| `bullet-2-title` / `bullet-2-body` | `bullet-2-title` / `bullet-2-body` |
| `bullet-3-title` / `bullet-3-body` | `bullet-3-title` / `bullet-3-body` |
| `bullet-4-title` / `bullet-4-body` | `bullet-4-title` / `bullet-4-body` |
| `bullet-5-title` / `bullet-5-body` | `bullet-5-title` / `bullet-5-body` |
| `bullet-6-title` / `bullet-6-body` | `bullet-6-title` / `bullet-6-body` |

If fewer than 6 bullets are provided, hide unused `bullet-item-N` wrapper divs with `style="display:none"`.

---

### 6. `slide_punchline` — Punchline Slide

**Output file:** `output/{NN-MM-name}/index.html`

**IDs to populate:**

| ID | Field in MD |
|---|---|
| `overhead-title` | `overhead-title` |
| `punchline-main` | Plain text part of punchline |
| `punchline-accent` | Mint-colored part of punchline |
| `punchline-subtext` | `punchline-subtext` |
| `nav-agenda` (href) | Resolved from file discovery |
| `nav-prev` (href) | Resolved from section slides list |
| `nav-next` (href) | Resolved from section slides list |
| `slide-counter` | Format: `{position} / {total}` |

If `punchline-subtext` is empty, hide the `<p id="punchline-subtext">` element with `style="display:none"`.

---

## Images

Authors place image files in:
```
assets/images/your-image.jpg
```

In the MD file, reference images with a path relative to the `assets/` folder:
```
slide-image: images/your-image.jpg
```

At build time the agent must:
1. Copy the entire `assets/images/` folder to `output/assets/images/`
2. Rewrite the `src` attribute in the output HTML to `../assets/images/your-image.jpg` (relative to the output file's location — adjust `../` depth based on how deep the output file sits in the output folder)

**Depth reference:**
- `output/index.html` → images are at `assets/images/file.jpg`
- `output/01-strategy/index.html` → images are at `../assets/images/file.jpg`
- `output/01-01-topic-name/index.html` → images are at `../assets/images/file.jpg`

If a `slide-image` value is blank or the file does not exist in `assets/images/`, leave the `<img>` src as an empty string and add `style="display:none"` to the image container so the layout does not break.

---

## Build Process — Step by Step

### Step -1: Spell Check (runs before every build)

**Purpose:** Catch pure spelling errors in slide content before publishing. This step is interactive — it must complete before the build continues.

**Exceptions file:** `spelling-exceptions.txt` in the project root.
- Each line is one word or phrase the user has confirmed is intentionally correct.
- Read this file at the start of every spell-check. Any word listed here must be silently skipped — never flagged again.
- If the file does not exist, treat it as empty (do not create it until the first word is added).

**What to check:**
- Scan all content MD files (same set as Step 1 — exclude `AGENT_INSTRUCTIONS.md` and any `template-*` files).
- Check only **field values** — the text after the `:` on each `key: value` line, and any plain text paragraphs. Never flag field keys, frontmatter keys, filenames, URLs, or comment lines (lines starting with `#`).
- Flag **pure spelling mistakes only** — incorrect letter sequences that produce a non-word or a clearly wrong word. Do NOT flag: stylistic choices, unconventional capitalisation, intentional fragments, jargon, proper nouns, abbreviations (e.g. "SDLC", "ADLC", "MDLC"), acronyms, or branded terms.
- Each flagged item must include: the file it appears in, the field key, the misspelled word in context (surrounding phrase), and one suggested correction.

**Interaction flow:**
1. Collect all spelling issues across all files first, deduplicating by (word, suggested correction) pairs.
2. Present issues one at a time, in this format:

```
Spelling issue [N of M]
File:       01-strategy.md
Field:      slide-intro
Context:    "...expanding into a multiveres of..."
Mistake:    multiveres
Suggestion: multiverse

[A] Accept — apply correction   [D] Decline — never flag this word again
```

3. Wait for the user to type A or D before showing the next issue.
4. **Accept:** Apply the correction directly to the source MD file. Update the file immediately — do not batch changes.
5. **Decline:** Append the word exactly as written (the misspelled form, lowercased) to `spelling-exceptions.txt`, one word per line. Do not add duplicates.
6. After all issues are resolved (or if there are none), confirm the outcome and proceed automatically to Step 0.

**If there are no spelling issues:** Print `Spell check complete — no issues found.` and continue to Step 0 without waiting for input.

---

### Step 0: Clear the output folder

Delete the entire contents of the `output/` folder before starting the build. This ensures no stale files from a previous build remain. Do not delete the `output/` folder itself — only its contents.

### Step 1: Discover all content files
Read the slides folder. Sort files alphabetically — this gives the correct presentation order.

**Ignore the following files entirely — do not process or build output for them:**
- `AGENT_INSTRUCTIONS.md`
- Any file whose name begins with `template-` (these are starter templates for authors, not content slides)

Classify each remaining file:
- `00-title.md` → cover
- Files matching `NN-name.md` (no second number, NN is 01–99) → section intros
- Files matching `NN-MM-name.md` (two numbers) → topic slides

Group topic slides under their parent section by matching the leading `NN` of their filename.

For each section, the ordered slide list is:
1. The section intro (`NN-name.md`) — always first
2. All topic slides matching `NN-MM-name.md` with the same `NN`, sorted by `MM`

This list is computed entirely from filenames — section files contain no `slides:` list. Do not look for one.

Build the **section index** — an ordered list of all section intro files sorted by `NN`. This is used to auto-wire the cover agenda and cross-section navigation.

### Step 2: Resolve navigation for every slide

All navigation values (`nav-agenda`, `nav-prev`, `nav-next`, `slide-counter`) are computed entirely from the file discovery in Step 1. No MD file contains or needs navigation fields.

**nav-agenda** — always `../index.html` from any section or topic slide (one level up reaches the cover).

**nav-prev / nav-next** — computed from the full ordered slide list per section:
1. Section intro (`NN-name.md`) — always position 1
2. Topic slides (`NN-MM-name.md`) — sorted by `MM`, positions 2, 3, 4…

For each slide at position P of total T in the section:
- `nav-prev` = output path of the slide at P-1, or `../index.html` (cover) if P = 1
- `nav-next` = output path of the slide at P+1, or the next section's `index.html` if P = T (last section gets `#`)

**slide-counter** — format `P / T` where P = position in section, T = total slides in section.

Output paths are always derived from filenames:
- `NN-name.md` → `NN-name/index.html`
- `NN-MM-name.md` → `NN-MM-name/index.html`

All nav `href` values are relative to the output file's own folder (one level deep), so always prefix with `../` when pointing to another folder.

### Step 3: Build each HTML file

For each content file:
1. Copy the correct template's `code.html` to the output path defined in `output:` frontmatter.
2. Inject the section timer config block into `<head>` (see **Section Timer** below).
3. Parse all `key: value` fields from the MD file.
4. For each ID in the template, find the matching key and replace the element's `innerHTML` with the value.
5. For `nav-prev`, `nav-next`, `nav-agenda` — set the element's `href` attribute.
6. For the image `<img>` tag — set `src` and `alt` attributes.
7. For the title with two spans (`slide-title-main` + `slide-title-accent`) — set each span's `innerHTML` independently.

#### Section Timer

Every non-cover slide must have the following injected immediately before `</head>`:

```html
<script>window.NOTCH_SECTION={nn:"NN",totalMinutes:MM,isIntro:BOOL};</script>
```

- `nn` — two-digit section number string (e.g. `"01"`)
- `totalMinutes` — integer parsed from the section's `agenda-duration` field (e.g. `15` from `"15 MIN"`)
- `isIntro` — `true` for `NN-name.md` section intro slides, `false` for `NN-MM-name.md` topic slides

The cover slide (`index.html`) gets no config block — the `presentation_first_slide` template already contains a script that clears the timer from `sessionStorage` on load.

The timer UI (`id="section-timer-wrap"`) and JS are already embedded in all section and topic slide templates. The build script only needs to inject the per-slide config.

### Step 4: Copy image assets
Copy the entire `assets/images/` folder to `output/assets/images/`. This must always happen — even if no slide currently references an image. Then for every `<img>` element populated in Step 3, rewrite the `src` attribute to be relative to the output file's location:
- Files one level deep (`output/NN-name/index.html`, `output/NN-MM-name/index.html`) → `../assets/images/filename.ext`
- `output/index.html` → `assets/images/filename.ext`

If a referenced image file does not exist in `assets/images/`, set `src=""` and add `style="display:none"` to the image's container element.

### Step 5: Verify output
After building, check that:
- Every `href` in nav buttons resolves to an existing output file.
- No template placeholder text (e.g. "Topic 1", "Overhead Title", "00") remains in any output file.
- The cover `index.html` links to all section intros.
- The `output/assets/images/` folder exists and contains all images referenced by any slide.

### Step 6: Stop — never commit or push unless asked

**The agent must NEVER run `git add`, `git commit`, `git push`, or any other git write command after a build — unless the user directly and explicitly asks for it.**

The build is complete when the output files are written and verified. Inform the user the build is done. Only perform git operations if the user explicitly requests them.

---

## Output Folder Structure

```
output/
├── index.html                        ← built from 00-title.md
├── 01-strategy/
│   ├── index.html                    ← built from 01-strategy.md
│   ├── 01-topic-name/
│   │   └── index.html                ← built from 01-01-topic-name.md
│   └── 02-topic-name/
│       └── index.html                ← built from 01-02-topic-name.md
├── 02-SDLC/
│   ├── index.html
│   └── ...
└── ...
```

---

## Notes

- The `slide-title-main` / `slide-title-accent` split is intentional: the accent span keeps the mint gradient styling. If the title has no two-part split, put the full title in `slide-title-main` and leave `slide-title-accent` empty.
- Image paths in MD files are relative to `assets/` (e.g. `images/photo.jpg`). At build time, copy `assets/images/` to `output/assets/images/` and rewrite `src` attributes to be relative to each output file's location.
- Agenda item links on the cover slide are **always auto-resolved** from the section index — never from fields in `00-title.md`. The MD only provides the displayed content (title, subtitle, duration) for each agenda item.
- Unused agenda items in the cover slide should be hidden, not removed, so the template structure stays intact.
- The `<title>` tag in each HTML file should be set to: `{presentation-label} — {slide-title-main} {slide-title-accent}`.
