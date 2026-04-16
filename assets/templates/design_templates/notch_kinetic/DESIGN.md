```markdown
# Design System Strategy: The Kinetic Architect

## 1. Overview & Creative North Star
This design system is built to transform corporate storytelling from static slides into a fluid, editorial experience. The Creative North Star for this system is **"The Kinetic Architect."** 

Unlike traditional "corporate" templates that rely on rigid boxes and heavy borders, this system uses **Structural Asymmetry** and **Tonal Depth** to create a sense of movement and professional sophistication. We treat the PowerPoint canvas not as a flat page, but as a three-dimensional workspace where ideas are layered. By utilizing high-contrast typography scales and overlapping surface tiers, we break the "template" look in favor of a bespoke, agency-level aesthetic.

---

## 2. Colors & Surface Logic
The palette is anchored by the deep, authoritative `#36454F` (Secondary) and the vibrant, high-energy `#2CC295` (Primary). To maintain a premium feel, we prioritize whitespace and subtle tonal shifts.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders to section content. Boundaries must be defined solely through background color shifts or the spacing scale. Use `surface-container-low` for large section blocks sitting on a `surface` background to create natural separation without visual clutter.

### Surface Hierarchy & Nesting
Treat the slide as a series of physical layers. 
- **Base Layer:** `surface` (#f5faff).
- **Secondary Layer:** `surface-container-low` (#e9f5ff) for content grouping.
- **Top Layer:** `surface-container-lowest` (#ffffff) for high-priority "cards" or callouts.
This "nested" approach creates a soft, tactile depth that feels organized and modern.

### The "Glass & Gradient" Rule
To move beyond a "standard" feel, use semi-transparent surface colors (60-80% opacity) with a Backdrop Blur (10pt - 20pt) for floating UI elements or navigation overlays. For main CTAs and hero headers, utilize a subtle linear gradient transitioning from `primary` (#006c50) to `primary_container` (#2cc295) at a 135° angle.

---

## 3. Typography: Editorial Authority
We utilize a pairing of **Plus Jakarta Sans** for high-impact displays and **Manrope** (as a high-end alternative to Rethink Sans) for functional reading.

*   **Display (Plus Jakarta Sans):** Used for "Big Idea" slides and section headers. The `display-lg` (3.5rem) scale is designed to be intentionally oversized to create a focal point.
*   **Headlines (Plus Jakarta Sans):** Used for slide titles. Use `headline-lg` (2rem) with tight letter-spacing (-2%) for a modern, compressed look.
*   **Body (Manrope):** `body-lg` (1rem) is the workhorse. It provides a clean, technical contrast to the expressive display face.
*   **Labels (Manrope):** Use `label-md` (0.75rem) in ALL CAPS with increased letter-spacing (+5%) for metadata, categories, or slide numbering to mimic architectural blueprints.

---

## 4. Elevation & Depth
Depth in this system is achieved through **Tonal Layering** rather than traditional structural lines.

*   **The Layering Principle:** Place a `surface-container-lowest` card on a `surface-container-low` section. This creates a "lift" that is felt rather than seen.
*   **Ambient Shadows:** For floating elements, use a "Cloud Shadow." Color: `on_surface` (#0e1d26) at 6% opacity. Blur: 40px. Offset: Y=10px. This mimics natural ambient light.
*   **The "Ghost Border" Fallback:** If a container requires a border for accessibility, use the `outline_variant` (#bbcac1) at **15% opacity**. High-contrast, 100% opaque borders are strictly forbidden.
*   **Glassmorphism:** Apply a blur effect to any element using the `inverse_surface` (#23323c) at 80% opacity to create a "Dark Glass" mode for sophisticated interstitial slides.

---

## 5. Components

### Buttons
- **Primary:** Gradient fill (`primary` to `primary_container`), `xl` roundedness (1.5rem), `label-md` text in `on_primary`.
- **Secondary:** `surface-container-highest` fill, no border, `secondary` text.
- **Tertiary:** No fill, `primary` text, underlined only on hover/interaction.

### Cards & Layout Modules
- **Rule:** Forbid divider lines. Use `spacing-8` (2.75rem) to separate vertical content.
- **Style:** Use `lg` roundedness (1rem). Ensure content within cards follows the `spacing-4` (1.4rem) internal padding.

### Chips
- **Selection Chips:** `primary_container` fill with `on_primary_container` text. Use `full` roundedness (pill shape).
- **Data Chips:** `surface-variant` fill with `secondary` text for low-priority metadata.

### Input Fields (for interactive decks)
- Fill: `surface-container-low`.
- Bottom-only Border: `outline_variant` at 20% opacity.
- Focus State: Border transitions to `primary` (#006c50) at 2px thickness.

### Key Performance Indicators (KPIs)
- Value: `display-md` in `on_surface`.
- Label: `label-sm` in `secondary` above the value.
- Accent: A 4px vertical "notch" (bar) of `primary` color to the left of the group.

---

## 6. Do’s and Don'ts

### Do:
- **Do** use intentional asymmetry. Align a title to the far left and the body text to a mid-right column to create dynamic tension.
- **Do** use the "Notch" accent: a single, small square or line in `primary` (#2CC295) to draw the eye to the most important data point on a slide.
- **Do** maximize whitespace. If a slide feels "full," move content to a second slide.

### Don't:
- **Don't** use black (#000000). Use `on_surface` (#0e1d26) for text and `inverse_surface` (#23323c) for dark backgrounds to keep the palette sophisticated.
- **Don't** use standard PowerPoint bullet points. Use the `primary` color for custom bullet shapes (small squares or "notches") or use spacing to separate list items.
- **Don't** stretch images. Use "Cover" fills within containers using the `md` or `lg` roundedness scale.

---

## 7. Spacing & Grid
This system operates on a **12-column Grid** but encourages "Bleed Layouts."
- **Outer Margin:** Always use `spacing-12` (4rem) for the safe zone.
- **Gutter:** Use `spacing-4` (1.4rem).
- **Vertical Rhythm:** Use `spacing-6` (2rem) between headlines and body text to ensure the layout "breathes."```