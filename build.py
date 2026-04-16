#!/usr/bin/env python3
"""Presentation build script."""
import re
import shutil
from pathlib import Path

BASE = Path(__file__).parent
SLIDES_DIR = BASE / "slides"
TEMPLATES_DIR = BASE / "assets/templates/design_templates"
OUTPUT_DIR = BASE / "output"
IMAGES_SRC = BASE / "assets/images"


# ── HTML helpers ──────────────────────────────────────────────────────────────

def md_links_to_html(text):
    """Convert markdown [label](url) links to HTML <a> tags."""
    return re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        lambda m: f'<a href="{m.group(2)}" target="_blank" style="color:#2CC295;text-decoration:underline;">{m.group(1)}</a>',
        text
    )


def parse_md(filepath):
    """Return dict of key: value pairs from a content MD file.

    Continuation lines after a key:value are appended to that key's value:
    - Blank lines become a paragraph break (<br><br>) in the output.
    - Lines starting with '* ' are appended with a single <br>.
    - Any other plain text line is also appended (with <br> or <br><br>
      depending on whether a blank line preceded it).
    Markdown links [label](url) are converted to <a> tags throughout.
    """
    fields = {}
    last_key = None
    pending_break = False
    content = Path(filepath).read_text(encoding="utf-8")
    # strip YAML frontmatter
    content = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL)
    for line in content.splitlines():
        s = line.strip()
        if not s:
            if last_key:
                pending_break = True
            continue
        if s.startswith("#"):
            continue
        m = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)", s)
        if m:
            last_key = m.group(1).strip()
            fields[last_key] = md_links_to_html(m.group(2).strip())
            pending_break = False
        elif last_key:
            sep = "<br><br>" if pending_break else "<br>"
            item = md_links_to_html(s[2:].strip() if s.startswith("* ") else s)
            fields[last_key] = fields[last_key] + sep + item
            pending_break = False
    return fields


def read_template(name):
    return (TEMPLATES_DIR / name / "code.html").read_text(encoding="utf-8")


def get_slide_template(filepath):
    """Read the template name from YAML frontmatter (---...---) of a slide file."""
    content = Path(filepath).read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", content, flags=re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            tm = re.match(r"^template:\s*(\S+)", line.strip())
            if tm:
                return tm.group(1).strip()
    return "slide_with_bullets"


def set_inner(html, eid, value):
    """Replace innerHTML of first element whose id=eid."""
    pat = rf'<(\w+)(?:\s[^<>]*)?\bid="{re.escape(eid)}"[^<>]*>'
    m = re.search(pat, html)
    if not m:
        return html
    tag = m.group(1)
    start = m.end()
    depth, pos = 1, start
    while depth > 0 and pos < len(html):
        nopen = re.search(rf"<{re.escape(tag)}[\s>/]", html[pos:])
        nclose = re.search(rf"</{re.escape(tag)}>", html[pos:])
        if nopen and (not nclose or nopen.start() < nclose.start()):
            ts = pos + nopen.start()
            te = re.search(r">", html[ts:])
            if te and not html[ts: ts + te.end()].endswith("/>"):
                depth += 1
            pos = pos + nopen.end()
        elif nclose:
            depth -= 1
            if depth == 0:
                return html[:start] + value + html[pos + nclose.start():]
            pos = pos + nclose.end()
        else:
            break
    return html


def set_href(html, eid, href):
    pat = rf'(<[^<>]+\bid="{re.escape(eid)}"[^<>]*)href="[^"]*"'
    r = re.sub(pat, lambda m: m.group(1) + f'href="{href}"', html, count=1)
    if r == html:
        r = re.sub(rf'(<[^<>]+\bid="{re.escape(eid)}")',
                   lambda m: m.group(1) + f' href="{href}"', html, count=1)
    return r


def set_img_attrs(html, eid, src, alt):
    pat = rf'(<img\b[^<>]*\bid="{re.escape(eid)}"[^<>]*)(/>|>)'
    def rep(m):
        tag = m.group(1)
        tag = re.sub(r'src="[^"]*"', f'src="{src}"', tag) if 'src=' in tag else tag + f' src="{src}"'
        tag = re.sub(r'alt="[^"]*"', f'alt="{alt}"', tag) if 'alt=' in tag else tag + f' alt="{alt}"'
        return tag + m.group(2)
    return re.sub(pat, rep, html, count=1)


def hide_by_id(html, eid):
    pat = rf'(<[^<>]+\bid="{re.escape(eid)}"[^<>]*)(>)'
    def rep(m):
        tag = m.group(1)
        if 'style=' in tag:
            tag = re.sub(r'style="([^"]*)"', lambda s: f'style="{s.group(1)};display:none"', tag)
        else:
            tag += ' style="display:none"'
        return tag + m.group(2)
    return re.sub(pat, rep, html, count=1)


def wrap_div_link(html, div_id, href):
    """Wrap <div id=div_id>…</div> with <a href=href>."""
    pat = rf'<div(\s[^<>]*)?id="{re.escape(div_id)}"([^<>]*)>'
    m = re.search(pat, html)
    if not m:
        return html
    start, pos, depth = m.start(), m.end(), 1
    while depth > 0 and pos < len(html):
        nopen = html.find("<div", pos)
        nclose = html.find("</div>", pos)
        if nopen != -1 and (nclose == -1 or nopen < nclose):
            depth += 1
            pos = nopen + 4
        elif nclose != -1:
            depth -= 1
            if depth == 0:
                end = nclose + 6
                block = html[start:end]
                wrapped = (f'<a href="{href}" style="display:block;'
                           f'text-decoration:none;color:inherit;">{block}</a>')
                return html[:start] + wrapped + html[end:]
            pos = nclose + 6
        else:
            break
    return html


def set_title_tag(html, title):
    return re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", html, count=1)


def inject_section_config(html, nn, total_minutes, is_intro):
    """Inject window.NOTCH_SECTION config before </head>."""
    is_intro_js = "true" if is_intro else "false"
    script = (f'<script>window.NOTCH_SECTION='
              f'{{nn:"{nn}",totalMinutes:{total_minutes},isIntro:{is_intro_js}}};</script>')
    return html.replace('</head>', script + '\n</head>', 1)


_KEYBOARD_NAV = (
    '<script>(function(){'
    'document.addEventListener("keydown",function(e){'
    'var id=e.key==="ArrowRight"||e.key==="ArrowDown"?"nav-next":'
    'e.key==="ArrowLeft"||e.key==="ArrowUp"?"nav-prev":null;'
    'if(!id)return;'
    'var a=document.getElementById(id);'
    'if(a&&a.getAttribute("href")!=="#")location.href=a.href;'
    '});'
    '})();</script>'
)


def write_file(rel_path, html):
    html = html.replace('</body>', _KEYBOARD_NAV + '\n</body>', 1)
    full = OUTPUT_DIR / rel_path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(html, encoding="utf-8")
    print(f"  ✓  {rel_path}")


# ── Step 0: Clear output ──────────────────────────────────────────────────────
print("Step 0: Clearing output folder…")
if OUTPUT_DIR.exists():
    for item in OUTPUT_DIR.iterdir():
        shutil.rmtree(item) if item.is_dir() else item.unlink()


# ── Step 1: Discover & classify ───────────────────────────────────────────────
print("Step 1: Discovering content files…")
content_files = sorted(
    f for f in SLIDES_DIR.glob("*.md")
    if f.name != "AGENT_INSTRUCTIONS.md" and not f.name.startswith("template-")
)

cover_file = None
section_files = {}   # "01" -> Path
topic_files = {}     # "01" -> [("01", Path), …]

for f in content_files:
    stem = f.stem
    if stem == "00-title":
        cover_file = f
    elif re.match(r"^\d{2}-\d{2}-", stem):
        m = re.match(r"^(\d{2})-(\d{2})-", stem)
        nn, mm = m.group(1), m.group(2)
        topic_files.setdefault(nn, []).append((mm, f))
    elif re.match(r"^\d{2}-", stem):
        nn = re.match(r"^(\d{2})-", stem).group(1)
        section_files[nn] = f

for nn in topic_files:
    topic_files[nn].sort(key=lambda x: x[0])

section_nns = sorted(section_files.keys())

# ordered slide list per section: [(Path, output_rel_path), …]
section_slides = {}
for nn in section_nns:
    sf = section_files[nn]
    slides = [(sf, f"{sf.stem}/index.html")]
    for _mm, tf in topic_files.get(nn, []):
        slides.append((tf, f"{tf.stem}/index.html"))
    section_slides[nn] = slides

print(f"  Cover: {cover_file.name}")
print(f"  Sections: {', '.join(section_nns)}")
for nn in section_nns:
    n_topics = len(topic_files.get(nn, []))
    print(f"    {nn}: {section_files[nn].name}  +{n_topics} topic slide(s)")

# Pre-compute total minutes per section (for timer injection)
section_minutes = {}
for nn in section_nns:
    sf = parse_md(section_files[nn])
    dur = sf.get("agenda-duration", "")
    m = re.match(r"(\d+)", dur)
    section_minutes[nn] = int(m.group(1)) if m else 0


# ── Step 2: Nav resolver ──────────────────────────────────────────────────────
def nav_for(nn, pos):
    slides = section_slides[nn]
    total = len(slides)
    agenda = "../index.html"
    prev = "../index.html" if pos == 0 else f"../{slides[pos-1][1]}"
    if pos == total - 1:
        idx = section_nns.index(nn)
        nxt = f"../{section_slides[section_nns[idx+1]][0][1]}" if idx + 1 < len(section_nns) else "#"
    else:
        nxt = f"../{slides[pos+1][1]}"
    counter = f"{pos+1} / {total}"
    return agenda, prev, nxt, counter


# ── Step 3: Build HTML files ───────────────────────────────────────────────────
print("\nStep 3: Building HTML files…")

# Cover
print("  [cover]")
f = parse_md(cover_file)
html = read_template("presentation_first_slide")
label   = f.get("presentation-label", "")
t_main  = f.get("presentation-title-main", "")
t_acc   = f.get("presentation-title-accent", "")

html = set_title_tag(html, f"{label} — {t_main} {t_acc}")
html = set_inner(html, "presentation-label", label)
html = set_inner(html, "presentation-title",
    f'{t_main} <span id="presentation-title-accent" class="text-brand-mint">{t_acc}</span>')
html = set_inner(html, "presentation-subtitle", f.get("presentation-subtitle", ""))

# Auto-calculate total duration from section agenda-duration fields
total_minutes = 0
for nn in section_nns:
    sf = parse_md(section_files[nn])
    dur = sf.get("agenda-duration", "")
    m = re.match(r"(\d+)", dur)
    if m:
        total_minutes += int(m.group(1))
html = set_inner(html, "presentation-duration", f"{total_minutes} Minutes")

for i, nn in enumerate(section_nns[:8], 1):
    sf = parse_md(section_files[nn])
    sec_out = section_slides[nn][0][1]
    html = set_inner(html, f"agenda-title-{i}", sf.get("agenda-title", ""))
    html = set_inner(html, f"agenda-subtitle-{i}", sf.get("agenda-subtitle", ""))
    html = set_inner(html, f"agenda-duration-{i}", sf.get("agenda-duration", ""))
    html = wrap_div_link(html, f"agenda-item-{i}", sec_out)

for i in range(len(section_nns) + 1, 9):
    html = hide_by_id(html, f"agenda-item-{i}")

write_file("index.html", html)

# Section intros
print("  [section intros]")
for nn in section_nns:
    f = parse_md(section_files[nn])
    agenda, prev, nxt, counter = nav_for(nn, 0)
    out_path = section_slides[nn][0][1]
    t_main = f.get("slide-title-main", "")
    t_acc  = f.get("slide-title-accent", "")

    html = read_template("section_intro_slide")
    html = inject_section_config(html, nn, section_minutes[nn], is_intro=True)
    html = set_title_tag(html, f"ALL HANDS AI — {t_main} {t_acc}")
    html = set_inner(html, "overhead-title",  f.get("overhead-title", ""))
    html = set_inner(html, "slide-title-main", t_main)
    html = set_inner(html, "slide-title-accent", t_acc)
    html = set_inner(html, "slide-intro",     f.get("slide-intro", ""))
    html = set_inner(html, "author-name",     f.get("author-name", ""))
    html = set_href(html, "nav-agenda", agenda)
    html = set_href(html, "nav-prev",   prev)
    html = set_href(html, "nav-next",   nxt)
    html = set_inner(html, "slide-counter", counter)

    img_val = f.get("section-image", "")
    if img_val and (IMAGES_SRC.parent / img_val).exists():
        html = set_img_attrs(html, "section-image",
                             f"../assets/images/{Path(img_val).name}",
                             f.get("section-image-alt", ""))
    else:
        html = hide_by_id(html, "section-image-container")

    write_file(out_path, html)

# Topic slides
print("  [topic slides]")
for nn in section_nns:
    slides = section_slides[nn]
    for pos, (tf, out_path) in enumerate(slides[1:], 1):
        f = parse_md(tf)
        tmpl = get_slide_template(tf)
        agenda, prev, nxt, counter = nav_for(nn, pos)
        t_main = f.get("slide-title-main", "")
        t_acc  = f.get("slide-title-accent", "")

        html = read_template(tmpl)
        html = inject_section_config(html, nn, section_minutes[nn], is_intro=False)
        html = set_title_tag(html, f"ALL HANDS AI — {t_main} {t_acc}")
        html = set_inner(html, "overhead-title",    f.get("overhead-title", ""))
        html = set_inner(html, "slide-title-main",  t_main)
        html = set_inner(html, "slide-title-accent", t_acc)
        html = set_href(html, "nav-agenda", agenda)
        html = set_href(html, "nav-prev",   prev)
        html = set_href(html, "nav-next",   nxt)
        html = set_inner(html, "slide-counter", counter)

        if tmpl == "slide_with_bullets":
            for i in range(1, 7):
                bt = f.get(f"bullet-{i}-title", "")
                bb = f.get(f"bullet-{i}-body", "")
                if bt or bb:
                    html = set_inner(html, f"bullet-{i}-title", bt)
                    html = set_inner(html, f"bullet-{i}-body",  bb)
                else:
                    html = hide_by_id(html, f"bullet-item-{i}")

        elif tmpl == "slide_with_text_and_image":
            html = set_inner(html, "content-heading", f.get("content-heading", ""))
            html = set_inner(html, "content-body",    f.get("content-body", ""))
            for i in range(1, 5):
                bt = f.get(f"bullet-{i}-title", "")
                bb = f.get(f"bullet-{i}-body", "")
                if bt or bb:
                    html = set_inner(html, f"bullet-{i}-title", bt)
                    html = set_inner(html, f"bullet-{i}-body",  bb)
                else:
                    html = hide_by_id(html, f"bullet-item-{i}")
            has_boxes = any(f.get(f"{b}-{k}", "") for b in ("box1", "box2") for k in ("title", "number", "subtext"))
            if has_boxes:
                for b in ("box1", "box2"):
                    html = set_inner(html, f"{b}-title",   f.get(f"{b}-title", ""))
                    html = set_inner(html, f"{b}-number",  f.get(f"{b}-number", ""))
                    html = set_inner(html, f"{b}-subtext", f.get(f"{b}-subtext", ""))
            else:
                html = hide_by_id(html, "boxes-container")
            img_val = f.get("slide-image", "")
            if img_val and (IMAGES_SRC.parent / img_val).exists():
                html = set_img_attrs(html, "slide-image",
                                     f"../assets/images/{Path(img_val).name}",
                                     f.get("slide-image-alt", ""))

        elif tmpl == "slide_with_image":
            img_val = f.get("slide-image", "")
            if img_val and (IMAGES_SRC.parent / img_val).exists():
                html = set_img_attrs(html, "slide-image",
                                     f"../assets/images/{Path(img_val).name}",
                                     f.get("slide-image-alt", ""))
            has_boxes = any(f.get(f"{b}-{k}", "") for b in ("box1", "box2") for k in ("title", "number", "subtext"))
            if has_boxes:
                for b in ("box1", "box2"):
                    html = set_inner(html, f"{b}-title",   f.get(f"{b}-title", ""))
                    html = set_inner(html, f"{b}-number",  f.get(f"{b}-number", ""))
                    html = set_inner(html, f"{b}-subtext", f.get(f"{b}-subtext", ""))
            else:
                html = hide_by_id(html, "boxes-container")

        elif tmpl == "slide_punchline":
            html = set_inner(html, "punchline-main",   f.get("punchline-main", ""))
            html = set_inner(html, "punchline-accent",  f.get("punchline-accent", ""))
            pst = f.get("punchline-subtext", "")
            html = set_inner(html, "punchline-subtext", pst) if pst else hide_by_id(html, "punchline-subtext")

        write_file(out_path, html)


# ── Step 4: Copy images ───────────────────────────────────────────────────────
print("\nStep 4: Copying images…")
dst = OUTPUT_DIR / "assets/images"
dst.mkdir(parents=True, exist_ok=True)
if IMAGES_SRC.exists():
    shutil.rmtree(dst)
    shutil.copytree(IMAGES_SRC, dst)
    imgs = list(dst.iterdir())
    print(f"  Copied {len(imgs)} image(s) → output/assets/images/")
else:
    print("  No source images folder found — output/assets/images/ created empty.")


# ── Step 5: Verify ────────────────────────────────────────────────────────────
print("\nStep 5: Verifying output…")
errors = []
expected = ["index.html"] + [p for nn in section_nns for _, p in section_slides[nn]]
for p in expected:
    if not (OUTPUT_DIR / p).exists():
        errors.append(f"MISSING: {p}")

PLACEHOLDERS = ["Overhead Title", "Topic 1", "Topic 2", "Subtitle 1",
                "Adrian Thorne", "Author Name", "Main title text"]
for p in expected:
    full = OUTPUT_DIR / p
    if full.exists():
        txt = full.read_text()
        for ph in PLACEHOLDERS:
            if ph in txt:
                errors.append(f"Placeholder '{ph}' still present in {p}")

if errors:
    print("  WARNINGS:")
    for e in errors:
        print(f"    ⚠  {e}")
else:
    print("  All checks passed ✓")

total = len(expected)
print(f"\nBuild complete — {total} HTML files written to output/")
print("(Do not commit or push.)")
