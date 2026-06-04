# Golden: Analytics web-app dashboard (dense data table)

A compact calibration example of a strong, shippable (4/5) web answer for an
analytics dashboard whose workhorse view is a dense, filterable table of
thousands of campaigns — the screen power users live in all day.

## Prompt

```text
We're building the "Campaigns" screen for our marketing analytics web app.
It's a dense table of ~2,000 campaigns: name, channel, status, spend,
impressions, CTR, conversions, CPA. Above it a filter bar (search, channel,
status, date range) and bulk actions (pause, archive, export). Power users
live here on 1440px monitors; PMs also open it on a laptop and sometimes a
tablet. Give me the layout, the table interaction model, the filter/state
design, and the accessibility + performance details an engineer can build
from. Tailwind + React, token-driven. Don't flatten the desktop into a phone.
```

## Golden output

```md
# Campaigns

Three landmarks, no surprises: a `<header>` (64px: product nav, account menu),
a `<main>` split into a 240px collapsible `<nav>` sidebar plus a fluid content
column, and a `<footer>`. One `<h1>` ("Campaigns"); the content column caps at
`max-inline-size: 1440px` and stays left-aligned so the eye anchors at the same
x on every load instead of re-centering as the window grows.

## Layout & responsive behavior

- Content stack: page title row -> sticky filter bar -> results-meta /
  bulk-action bar -> table -> pagination footer.
- Spacing on the 4px scale: 16px gutters inside the filter bar, 24px between the
  filter bar and table, 8px vertical cell padding at default density. Body text
  1rem / line-height 1.5; numeric cells use
  `font-variant-numeric: tabular-nums` so digits align down each column.
- Breakpoint ladder (min-width, mobile-first):
  - 320–767 (down to the 1.4.10 reflow floor): single column; the sidebar
    becomes an off-canvas drawer (`<dialog>` with ESC, scroll-lock, focus trap),
    and the table reflows to a stacked card list — each row an `<article>` of
    label/value pairs. No horizontal scroll on the page itself.
  - 768–1023 (tablet): sidebar collapses to a 56px icon rail; the table keeps
    its grid but drops Impressions behind a "+2 more" column toggle.
  - 1024 / 1280 / 1440+: full sidebar, all columns, desktop density. This is
    where the power user works, so we EXPLOIT density rather than padding it out.
- A container query on the table wrapper (`@container (min-width: 60rem)`) lets
  the same component behave correctly inside the narrower drawer preview too.

## Filter bar (sticky, URL-as-state)

`position: sticky; top: 0` on an elevated surface token with a 1px bottom border
so it reads as a layer over the scrolling table. Controls, left to right:

- Search `<input type="search">`, 320px, leading icon, `inputmode="search"`,
  debounced 300ms; label is visually hidden but present.
- Channel `<select>` (or a listbox combobox per the WAI-ARIA APG combobox
  pattern when multi-select is needed).
- Status segmented control built as a `radiogroup` — each option pairs a text
  label with a status dot AND a shape/icon, never color alone (WCAG 1.4.1).
- Date-range `<button aria-haspopup="dialog">` opening a calendar popover.

Every filter writes to the query string
(`?channel=email&status=active&sort=cpa.asc&page=2`). The view is shareable,
survives reload, and back/forward restore exact state via the History API. A
"Clear all" `<button>` resets to the canonical URL. Applied filters render as
removable chips with a live count — `247 of 1,983 campaigns` — announced via an
`aria-live="polite"` region so the result change is heard, not just seen.

## The table (the main event)

A semantic `<table>` with real `<thead>` / `<tbody>` — not a div grid — so
assistive tech gets row and column semantics for free.

- Sticky header: `<thead>` cells `position: sticky; top: <filter-bar-height>` so
  column titles stay visible through long scrolls, with a bottom shadow that
  appears only once scrolled rather than a permanent heavy line.
- Sortable columns: each sortable `<th>` holds a `<button>` with
  `aria-sort="ascending|descending|none"`; direction shows as an arrow glyph
  (not color), the active column gets a subtle tint, and sort persists to the URL.
- Selection + bulk actions: a leading checkbox column; the header checkbox is
  tri-state (`indeterminate`) for partial selection. With >= 1 row selected the
  results-meta row swaps to a bulk bar — `3 selected — Pause / Archive /
  Export / Clear` — that is `aria-live` so the count is announced. Destructive
  actions route through a confirmation `<dialog>`.
- Keyboard row navigation: roving `tabindex` so Up/Down move between rows, Space
  toggles the row checkbox, Enter opens the campaign, and Tab moves OUT of the
  grid to the next landmark (composite-widget pattern) so keyboard users are not
  trapped tabbing 2,000 rows (WCAG 2.1.2).
- Density toggle: Comfortable (48px row) / Compact (36px row), persisted to
  localStorage; even Compact keeps the row hit target >= 24px (WCAG 2.5.8).
- Virtualization: render ~30 visible rows plus overscan via a windowing list to
  hold INP <= 200ms with 2,000 rows; reserve row height so scrolling causes no
  layout shift (CLS <= 0.1). The sticky header lives outside the virtualized
  body so it never unmounts.
- Status and threshold cells: status is dot + text label; CPA over target is
  tinted AND flagged with a small "high" badge, never color alone.

## States (web reality, all of them)

- Loading: skeleton rows sized to the final row height — no spinner jump.
- Empty (cold start): centered illustration, one-line explainer, primary
  "Create campaign" button.
- Empty (filters match nothing): distinct copy — "No campaigns match these
  filters" + a "Clear filters" button — separate from the cold-start state.
- Error (fetch failed): inline `role="alert"` banner with Retry; the last good
  data stays visible where possible instead of blanking.
- Stale: if a background refresh fails, a quiet "Showing data from 2:14 PM ·
  Refresh" affordance.
- Session-expired: a 401 opens a non-destructive re-auth modal without losing
  the current URL state.
- Per control: default / hover / `:focus-visible` / active / disabled, all
  token-driven.

## Accessibility checklist (named, not vibes)

- 1.4.3 contrast: body text >= 4.5:1, large headings >= 3:1, against every
  surface token (default, hover, selected-row, sticky-header).
- 1.4.11 non-text contrast: checkbox borders, sort arrows, focus ring, and
  status dots all >= 3:1 against their background.
- 1.4.1 use of color: status, sort, and threshold flags always pair color with
  text or shape.
- 2.4.7 / `:focus-visible`: a 2px token-colored ring with offset, visible on
  light and dark rows; 2.4.11 ensures the sticky header never obscures the
  focused row (scroll it into the clear area on focus).
- 1.4.10 reflow at 320px, 1.4.4 resize to 200%, and 1.4.12 text-spacing override
  all verified without clipping cells.
- `forced-colors: active`: status dots and the focus ring fall back to system
  colors; borders use `currentColor` so the grid survives Windows High Contrast.
- Skip link to `<main>`; one `<h1>`, no skipped heading levels.

## Tokens & performance

```css
:root {
  --space-2: 0.5rem;   /* 8px  */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --row-h-compact: 2.25rem;   /* 36px */
  --row-h-comfort: 3rem;      /* 48px */
  --fs-body: 1rem;            /* 16px floor */
  --fs-table: clamp(0.875rem, 0.8rem + 0.3vw, 1rem);
  --lh-body: 1.5;
  --focus-ring: 0 0 0 2px var(--surface), 0 0 0 4px var(--accent-600);
}
```

- LCP <= 2.5s: server-render the shell + first page of rows; defer the
  virtualization JS.
- INP <= 200ms: debounce filters, virtualize rows, run sort/filter over the full
  2,000-row set off the main thread.
- CLS <= 0.1: reserve table, row, and skeleton heights; `font-display: swap`
  with a preloaded above-the-fold font and tuned fallback metrics so the header
  does not reflow.
```

## Design-quality notes

Quality target: 4/5

This response is strong and shippable across the dimensions that matter for a
dense data view, without over-reaching into a reference implementation.

- Attention path & hierarchy (4/5): the page funnels title -> filters ->
  results meta -> table, and the table sets a clear scan order (name first,
  money and threshold flags weighted). The sticky filter bar and sticky header
  keep the user oriented through long scrolls.
- Composition & spacing (4/5): consistent 4px-scale spacing, a 1440px content
  column anchored left, and a real breakpoint ladder that reflows to cards at
  320px instead of squashing the grid.
- Typography craft (4/5): 1rem body floor, fluid `clamp()` table type with a rem
  term, line-height 1.5, and `tabular-nums` for column alignment — the detail
  that makes a dense numeric table actually readable.
- Color/state & contrast (4/5): every status, sort, and threshold signal is
  color-plus-text-or-shape (WCAG 1.4.1), and contrast is named per surface
  token, including the often-missed selected-row and sticky-header backgrounds.
- Density & rhythm (4/5): it exploits desktop density (36px compact rows, a
  density toggle, all columns at 1280px+) rather than flattening to a phone
  layout, while keeping hit targets >= 24px.
- Interaction polish & motion (4/5): roving-tabindex row nav, tri-state
  select-all, a scroll-driven header shadow, and skeletons sized to final rows.
  Restrained and honest — no gratuitous motion.
- Production readiness (4/5): URL-as-state, virtualization tied to a Core Web
  Vitals budget, the full web state matrix (loading / two empties / error /
  stale / session-expired), and a token excerpt an engineer can paste in.

What would push it to 5/5: a worked contrast table with actual hex values and
measured ratios per surface (not just ">= 4.5:1"); a concrete virtualization
library choice with the overscan number justified against a measured INP trace;
a `prefers-reduced-motion` branch for the shimmer and the header shadow; and a
saved-views / column-config model (reorder, hide, pin, persist) since users on
this screen all day will want it. Those move it from clearly strong and
shippable to a reference implementation.
