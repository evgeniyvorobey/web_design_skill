# Golden example: Developer documentation portal

A compact calibration example showing a strong (4/5) web answer for a developer
documentation portal: a persistent sidebar tree, instant search, copy-able code
blocks, and an on-page table of contents that tracks the reading position.

## Prompt

```text
We're building the public docs site for our API platform. I need the
docs-article layout: left sidebar with the section tree, a center column for
the article, and a right-hand "On this page" table of contents.

Requirements:
- Header search (Cmd/Ctrl-K) that opens a results dialog.
- Code blocks need a copy button and a language label.
- TOC on the right should highlight the current heading as I scroll.
- Has to work down to a phone width and be keyboard- and screen-reader-friendly.

Give me the layout structure, the key CSS (grid, type, breakpoints), the
component states, and the accessibility behavior I have to get right.
```

## Golden output

```md
# Docs portal — article layout

## Layout model

Three regions inside a centered shell (max-width 1440px), driven by one CSS
grid that collapses mobile-first:

- **Sidebar** (section tree) — `<nav aria-label="Docs">`, sticky, own scroll.
- **Article** (`<main id="content">`, single `<h1>`) — reading column ~65ch.
- **On this page** TOC — `<nav aria-label="On this page">`, sticky.

Landmarks: `<header>` (search + product nav) / `<nav>` / `<main>` / `<aside>` /
`<footer>`. A skip link (`<a href="#content">`, visible on focus) jumps past
the sidebar — WCAG 2.4.1 Bypass Blocks.

​```html
<a class="skip-link" href="#content">Skip to content</a>
<header class="site-header">…search, product switcher…</header>
<div class="docs-shell">
  <nav class="sidebar" aria-label="Docs">…tree…</nav>
  <main id="content" tabindex="-1">
    <article>
      <h1>Authentication</h1>
      …h2 / h3 sections…
    </article>
  </main>
  <nav class="toc" aria-label="On this page">…</nav>
</div>
​```

## Grid + breakpoints (mobile-first)

​```css
:root {
  --space-1: .25rem; --space-2: .5rem;  --space-3: .75rem;
  --space-4: 1rem;   --space-6: 1.5rem; --space-8: 2rem;
  --line: #d3d7e0; --focus: #2b59ff;
  --measure: 68ch;
}

/* Base (320px floor → small screens): single column, rails off-canvas */
.docs-shell { display: block; }
.sidebar, .toc { display: none; }     /* surfaced via header toggles < 1024px */

main { padding: var(--space-6) var(--space-4); }
.prose { max-width: var(--measure); margin-inline: auto; }

/* Tablet: bring the sidebar in as a fixed rail */
@media (min-width: 768px) {
  .docs-shell {
    display: grid;
    grid-template-columns: 17rem minmax(0, 1fr);
    gap: var(--space-8);
  }
  .sidebar { display: block; position: sticky; top: 4rem;
             max-height: calc(100dvh - 4rem); overflow: auto; }
}

/* Desktop: add the TOC as a third column */
@media (min-width: 1024px) {
  .docs-shell {
    grid-template-columns: 17rem minmax(0, 1fr) 14rem;
  }
  .toc { display: block; position: sticky; top: 4rem; }
}

@media (min-width: 1280px) {
  .docs-shell { grid-template-columns: 18rem minmax(0, 1fr) 16rem; }
}
​```

Reflow holds at 320px (WCAG 1.4.10): both rails leave the grid and open as
off-canvas dialogs behind header toggles — no horizontal scroll, no clipped
content at 400% zoom (1.4.4). Text-spacing overrides (1.4.12) don't clip.

## Typography

​```css
body { font-size: 1rem; line-height: 1.5; }           /* 16px floor */
h1 { font-size: clamp(1.75rem, 1.4rem + 1.6vw, 2.5rem); line-height: 1.2; }
h2 { font-size: clamp(1.375rem, 1.2rem + .8vw, 1.75rem); line-height: 1.25; }
h3 { font-size: 1.125rem; line-height: 1.3; }
.prose { font-size: 1.0625rem; }   /* 17px reading size, still resizable */
code, pre { font-family: ui-monospace, SFMono-Regular, monospace;
            font-size: .9375rem; }
​```

Headings follow a strict outline — one `h1`, no skipped levels — so the TOC and
assistive tech share the same structure. The body font loads with
`font-display: swap`, is preloaded above the fold, and pairs with a
metric-matched fallback to avoid CLS.

## Component specs + states

### Sidebar tree

Native disclosure per group via `<button aria-expanded>` controlling a nested
`<ul>`; the current page link carries `aria-current="page"`. State styling never
relies on color alone (WCAG 1.4.1): the active item gets a 3px accent **border**
plus a tint, and expanded groups show a rotated chevron.

States: default · hover (row tint) · `:focus-visible` (2px `--focus` outline,
2px offset) · current (`aria-current` border + weight) · expanded/collapsed.

### Search (Cmd/Ctrl-K)

A header `<button>` opens a `<dialog>` combobox (WAI-ARIA APG Combobox): the
input is `role="combobox" aria-expanded aria-controls` over a `role="listbox"`;
results are `role="option"`; `aria-activedescendant` tracks the highlighted row
so focus stays in the input. ArrowUp/Down move, Enter navigates, **Esc closes**,
focus is **trapped** while open and **restored** to the trigger on close
(2.4.3 Focus Order, 2.1.2 No Keyboard Trap). An `aria-live="polite"` node
announces "N results". States: idle · loading (skeleton rows) · results ·
**empty** ("No matches for *term*") · error ("Search is unavailable — retry").
Hit targets are ≥ 24px (2.5.8); the shortcut is also a visible, clickable
control, not keyboard-only.

### Code block

​```html
<figure class="code">
  <figcaption>
    <span class="lang">TypeScript</span>
    <button class="copy" aria-label="Copy code">Copy</button>
  </figcaption>
  <pre tabindex="0"><code>…</code></pre>
</figure>
​```

`<pre tabindex="0">` is focusable so keyboard users can scroll long samples.
The copy button swaps its label to "Copied" and fires an `aria-live="polite"`
confirmation — never icon-and-color only. Code/background contrast meets 4.5:1;
the language label is text, not a color swatch.

### On-this-page TOC (scroll-spy)

Links to each `h2`/`h3`. The active entry is set with `IntersectionObserver`
(not scroll math) and marked `aria-current="true"` plus a left accent bar, so
the cue is structural, not color-only. Respects `prefers-reduced-motion`:
smooth scroll and the highlight transition drop to instant.

## Color, contrast, focus

- Body text ≥ 4.5:1, large headings ≥ 3:1 (1.4.3); links carry an underline or
  a ≥ 3:1 non-text cue, not hue alone (1.4.1).
- Focus indicators meet 3:1 against adjacent colors (1.4.11) and are never
  hidden under the sticky header — `scroll-margin-top: 4.5rem` on headings and
  focus targets keeps them clear (2.4.11 Focus Not Obscured).
- `@media (forced-colors: active)` preserves borders/outlines via `CanvasText`
  and `Highlight`; the active-item accent falls back to a system color.
- `:focus-visible` everywhere; `:focus:not(:focus-visible)` stays quiet for
  mouse users. `@media (pointer: coarse)` bumps tree rows to a ≥ 44px target.
```

## Behavior + performance

These notes sit outside the code sample to keep the inner Markdown clean.

- URL is shareable state: deep links to `#heading` open the right section and
  the TOC reflects it; History API plus scroll restoration on back/forward.
- Off-canvas rails on small screens are a `<dialog>` with scroll-lock, Esc, and
  a focus trap that restores focus to the toggle on close.
- Budgets: LCP ≤ 2.5s (preload the hero font, no render-blocking webfont),
  INP ≤ 200ms (search is debounced, results virtualized past ~50 rows),
  CLS ≤ 0.1 (reserved rail widths, sized images via `aspect-ratio`).

## Design-quality notes

This is a strong, shippable answer — it earns 4/5 on the dimensions that matter
for a docs layout, and it is honest about what would push it to 5/5.

**Quality target: 4/5**

- **Attention path & hierarchy (4/5)** — One `h1`, a strict heading outline, and
  three clearly-labeled landmarks give a single obvious reading path; the TOC
  mirrors that outline rather than inventing a second structure. The skip link
  and `aria-current` keep "where am I" answerable at every width.
- **Composition & spacing (4/5)** — A single grid drives all breakpoints with a
  real 4px-based token scale (`--space-*`), a ~65ch measure, and sticky rails
  that own their own scroll. The mobile-first collapse (rails leave the grid, no
  orphaned content behind `display:none`) is concrete and buildable.
- **Typography craft (4/5)** — 16px floor, `clamp()` headings with a rem term,
  1.5 body line-height, tightened heading leading, and a CLS-safe font strategy
  (swap + preload + metric fallback). Resizes to 200% without breaking measure.
- **Color/state & contrast (4/5)** — Named criteria are applied, not just cited:
  1.4.3, 1.4.11, and especially 1.4.1 (every state has a non-color cue — border,
  weight, underline, chevron). Forced-colors support is addressed explicitly.
- **Interaction polish & motion (4/5)** — The search dialog follows the APG
  Combobox pattern with `aria-activedescendant`, Esc-to-close, focus trap +
  restore, and a full state set (idle/loading/empty/error). Scroll-spy uses
  `IntersectionObserver` and honors `prefers-reduced-motion`.
- **Production readiness (4/5)** — Shareable URL state, History API, scroll
  restoration, virtualized results, and explicit Core Web Vitals budgets make
  this a spec an engineer can implement without guessing.

**What would push it to 5/5:** ship the actual token values (color hex with
measured contrast ratios and the metric-override numbers for the fallback font),
specify the sidebar tree's roving-`tabindex` keyboard model for arrow-key
navigation between items, define a density/compact toggle for power users, and
add the offline and session-expired states for the authenticated "try it" panels
referenced by the API docs. Those move it from "clearly correct" to "nothing
left to decide."
