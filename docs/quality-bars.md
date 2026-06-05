# Quality Bars

These are the concrete numeric thresholds the skill checks a web design against. They are floors and reference ranges, not style opinions. When a recommendation cannot meet a bar, say so and explain the tradeoff; do not silently relax it.

All values are in CSS reference pixels (`px`) and `rem` (1rem = the user's root font size, 16px by default). Never anchor type or spacing to device pixels, points, or viewport-locked magic numbers. Respect the user's root size — size in `rem` for anything that should scale with browser text settings.

---

## Typography

- **Body text baseline: 16px (1rem) minimum.** Below 16px, mobile browsers zoom on focus and reading speed drops. Long-form reading bodies run 18–20px (1.125–1.25rem).
- **Fluid type with `clamp()`** so size tracks the viewport without media-query steps: `font-size: clamp(1rem, 0.93rem + 0.35vw, 1.125rem);`. Always include a `rem` term in the middle so zoom still works (never a pure `vw` size).
- **Measure (line length): 45–75 characters, target ~65ch** for body copy. Cap with `max-width: 65ch` rather than a fixed pixel width.
- **Line-height: 1.5 for body, 1.2–1.35 for headings.** Tighter than 1.4 on body copy fails comfortable reading; tighter than 1.2 on large headings causes descender collisions.
- **Type scale ratio:** 1.2 (minor third) for dense app UI, 1.25–1.333 for editorial/marketing. Define roles, not ad-hoc sizes.
- **WCAG 1.4.12 Text Spacing (AA) must survive user overrides** with no clipping or overlap: line-height ≥ 1.5×, paragraph spacing ≥ 2× font size, letter-spacing ≥ 0.12em, word-spacing ≥ 0.16em.
- **Font loading:** prefer `font-display: swap` (accept FOUT) over invisible text (FOIT); `<link rel="preload">` the one or two fonts used above the fold; set `size-adjust` / fallback face metrics to keep the swap from shifting layout (protects CLS).

## Targets and pointer

- **WCAG 2.5.8 Target Size (Minimum, AA): 24 × 24 CSS px**, or a smaller target with a 24px-diameter undisturbed spacing circle, or an equivalent inline/UA exception.
- **WCAG 2.5.5 Target Size (Enhanced, AAA): 44 × 44 CSS px.** Use 44px for primary and touch-first actions.
- **Pointer-aware sizing:** treat input as simultaneous, not exclusive. Bump hit areas on coarse pointers and allow denser fine-pointer targets:
  - `@media (pointer: coarse) { /* ≥ 44px targets, larger spacing */ }`
  - `@media (pointer: fine) { /* 24–32px targets acceptable, hover affordances allowed */ }`
- **Spacing between adjacent targets: ≥ 8px**; for coarse pointers prefer the full 24px undisturbed circle.
- **Fitts's Law on web** is governed by cursor travel and screen edges/corners (infinitely deep edges), not a thumb arc. Place high-frequency actions near the pointer's resting area, the active element, or a screen edge.

## Color and contrast (WCAG 2.2 AA)

- **Text contrast (1.4.3): 4.5:1** for normal text; **3:1 for large text** (≥ 24px, or ≥ 18.66px bold).
- **Non-text contrast (1.4.11): 3:1** for UI component boundaries, states, focus indicators, and meaningful graphics.
- **Use of color (1.4.1):** never encode meaning by color alone — pair with text, icon, underline, or pattern.
- **Focus indicator:** visible `:focus-visible` outline ≥ 2px with ≥ 3:1 contrast against adjacent colors; honor 2.4.11 Focus Not Obscured (Minimum) — sticky headers/footers must not hide the focused element.
- **`prefers-color-scheme`:** supply a real dark theme (not an inverted filter); re-check every contrast pair in dark mode.
- **`forced-colors` / Windows High Contrast:** do not suppress outlines or rely on box-shadow for state; map to system colors and test that focus and selection survive.
- AAA reference when requested: 7:1 text (1.4.6).

## Motion and reduced motion

- **Durations:** 100–250ms for state/hover/press feedback (the smallest direct-manipulation changes — a toggle or checkbox — land near ~100ms), 200–400ms for entrances/overlays; avoid > 500ms for functional transitions.
- **`prefers-reduced-motion: reduce`** must remove parallax, large translate/scale transitions, auto-advancing carousels, and scroll-jacking; replace with instant or opacity-only changes. Never gate content behind motion.
- **No content flashing more than 3 times per second (2.3.1).**
- **Scroll-triggered motion** is decoration: content must be fully present and readable with motion off and with JavaScript reveal-on-scroll disabled.
- For the canonical duration scale, the full easing palette (cubic-bezier tokens), the spring-vs-tween rule, the CSS → WAAPI → View Transitions → library build ladder, and the appropriateness gate (animate only where it earns its place), see [`motion-and-animation.md`](motion-and-animation.md).

## Spacing, grid and breakpoints

- **Spacing scale (4px base):** 4, 8, 12, 16, 24, 32, 48, 64, 96 px (0.25–6rem). Pick from the scale; no ad-hoc gaps.
- **Breakpoint ladder (min-width, mobile-first):** ~320 (smallest supported, reflow floor) → 360/480 → 640 → 768 (tablet) → 1024 → 1280 (desktop) → 1440 → 1920+ (wide). Treat these as content-driven, not device-named.
- **Container queries** (Baseline since 2023) for component-level adaptation (a card that reflows by its own width, independent of the viewport); media queries for page-level layout.
- **Max content width:** cap reading and form columns (~640–760px / 65ch); cap full app shells ~1200–1440px with fluid gutters beyond that.
- **Grid:** 12 columns on desktop with 24–32px gutters; 8 columns tablet; 4 columns / single-column mobile. Whitespace scales up with viewport — desktop earns generous margins, not stretched line lengths.

## Performance (Core Web Vitals)

Field "good" thresholds at the 75th percentile:

- **LCP (Largest Contentful Paint) ≤ 2.5s** (needs-improvement 2.5–4s; poor > 4s).
- **INP (Interaction to Next Paint) ≤ 200ms** (needs-improvement 200–500ms; poor > 500ms).
- **CLS (Cumulative Layout Shift) ≤ 0.1** (needs-improvement 0.1–0.25; poor > 0.25).
- Supporting: TTFB ≈ ≤ 0.8s, FCP ≤ 1.8s.
- **Prevent CLS:** reserve media space with `width`/`height` or `aspect-ratio`; never inject content above existing content after load; reserve ad/embeds slots.
- **Protect LCP:** the hero text/image is the LCP candidate — preload it, avoid render-blocking webfonts on it, don't lazy-load it.
- **Protect INP:** keep main-thread tasks short; defer non-critical JS; debounce expensive handlers; show optimistic/loading feedback within 100ms.
- Treat these as quality bars and as a Mode D review lens, not vanity metrics.

## Forms and input

- **Every field has a visible, programmatically associated `<label>`** (placeholder is not a label).
- **`autocomplete` tokens** on identity/address/payment fields; `autocomplete="one-time-code"` + `inputmode` for OTP.
- **`type` / `inputmode`** chosen for the data (`email`, `tel`, `numeric`, `decimal`) so the right soft keyboard appears — this is the web meaning of "keyboard": input *type*, kept separate from keyboard *operability*.
- **Input font-size ≥ 16px** to prevent mobile browsers (notably Safari/WebKit) from zooming the viewport on focus.
- **Errors:** inline, specific, tied to the field via `aria-describedby`; set `aria-invalid`; move focus to the first error on submit; never clear entered data on a validation failure.
- **Target/spacing:** controls meet the target-size bar above; grouped controls (radios, checkboxes) have ≥ 8px separation.

## States

Every interactive surface defines, at minimum: **default, hover, focus-visible, active/pressed, loading, empty, error, success, disabled.** Web-specific system states to cover where relevant: **404, 500, offline / network-lost, and session-expired** (see [`sources.md`](sources.md) and the patterns catalog). Skeletons or spinners must appear within ~100ms of an action; never leave a control inert with no feedback.

## Accessibility specifics (keyboard, focus, reflow)

- **Keyboard operability (2.1.1):** every action reachable and operable by keyboard; logical tab order matching visual order; no keyboard trap (2.1.2); ESC closes overlays.
- **Focus management:** on route change or overlay open, move focus deliberately (to the dialog / new heading); **trap focus inside modal dialogs and restore it** to the trigger on close; provide a **skip link** to main content; consider a command palette for power users.
- **Semantic structure:** one `<h1>` per page, a logical heading outline (no skipped levels), landmark regions (`header`/`nav`/`main`/`footer`), and `aria-live` for async updates.
- **Reflow (1.4.10):** content reflows without two-dimensional scrolling at a width equivalent to **320 CSS px** for vertically-scrolling content, or a height of **256 CSS px** for horizontally-scrolling content (e.g. vertical writing modes); data tables and code are the only sanctioned exceptions.
- **Resize text (1.4.4):** usable at **200% zoom** with no loss of content or function.
- **Text spacing (1.4.12)** and **forced-colors** as above.

---

These bars are referenced by [`design-quality.md`](design-quality.md), [`design-quality-rubric.md`](design-quality-rubric.md), [`patterns-catalog.md`](patterns-catalog.md), and the Mode D review lenses in [`workflow.md`](workflow.md). When a number here changes, update the worked examples and the rubric bands together.
