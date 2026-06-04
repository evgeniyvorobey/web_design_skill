# Case study: Faceted search results that survive sharing, reload, and the back button

This is a SYNTHETIC calibration fixture: a hand-written bad-to-good example for the skill, not an evaluation of any shipped feature. It does not measure a live product; do not read the scores as field metrics.

## Prompt

```text
We run a marketplace for used cameras. The category listing page needs proper
faceted search. Users filter by brand, price, condition, lens mount, and
megapixels, then sort by price or "newest". Results paginate ~30 per page.

Right now the filters are a wall of checkboxes, sorting reloads the whole page
and loses your place, and you can't share a filtered link with a friend — the
URL is always just /cameras. Marketing also complains the filtered pages don't
rank because every combination looks like the same page to crawlers.

Design the results layout, the filter panel, sort, and pagination. Tell me how
state lives in the URL, what happens on slow networks, and how a keyboard- or
screen-reader user gets through it. Desktop is our main traffic but ~45% is
phones. Give me concrete markup and CSS values, not vibes.
```

## Weak response

```md
Here's a clean faceted search layout.

**Layout**
- Left sidebar (~280px) holds all the filters. Main area on the right shows a
  responsive grid of result cards.
- On mobile, hide the sidebar and show a "Filters" button that opens it.

**Filters**
- Group filters by attribute: Brand, Price, Condition, Mount, Megapixels.
- Each group is a list of checkboxes. Price is a dual-handle range slider.
- Apply filters when the user clicks an "Apply" button at the bottom so we
  don't hammer the server.

**Sort**
- A dropdown in the top-right with "Price: Low to High", "Price: High to Low",
  and "Newest". Changing it re-runs the search with AJAX so the page doesn't
  fully reload.

**Pagination**
- Numbered pages at the bottom (1, 2, 3 … Next). 30 results per page.

**Cards**
- Photo, title, price, condition badge. Hover to lift the card with a shadow
  and show a "Quick view" link.

**Styling**
.card { padding: 16px; border-radius: 8px; transition: 0.2s; }
.card:hover { box-shadow: 0 8px 24px rgba(0,0,0,.15); }
.badge.mint { color: #19c37d; }
.filters { width: 280px; font-size: 14px; }

For SEO, add a meta description and make sure each card links to the product
page. The grid uses repeat(auto-fill, minmax(240px, 1fr)) so it reflows on its
own.
```

## Why this is weak

- **URL state is missing entirely (the core ask).** The prompt explicitly wants shareable filtered links, crawlable combinations, and a working back button — the weak answer never touches the URL, so `/cameras?brand=...` never exists. This fails the shareable-state requirement and the SEO/crawl concern, and it breaks **Nielsen heuristic #3 (user control and freedom)** because Back cannot undo a filter.
- **AJAX sort with no History API = a broken back button.** "Re-runs with AJAX so the page doesn't fully reload" sounds modern but silently discards browser history. After three sort/filter changes, Back jumps to the previous *page*, not the previous *state* — a violation of **heuristic #4 (consistency and standards)** with the platform.
- **No async state model.** There is no loading, empty, or error state for the results region, and nothing announced to assistive tech. A screen-reader user clicks a filter and hears nothing change — fails **WCAG 4.1.3 Status Messages** (no `aria-live` for "showing 42 results") and ignores the prompt's explicit "slow network" question.
- **"Apply" button contradicts the live model and hides the result count.** Batching behind Apply means users cannot see how each facet narrows results, removing the single most useful signal in faceted search (the running count). Weak on *attention path & hierarchy* — decisions are starved of feedback.
- **Contrast and color-only signaling fail.** `.badge.mint { color: #19c37d }` is green text that, on white, lands near 1.9:1 — far below the **WCAG 1.4.3** floor of 4.5:1 — and condition is conveyed by color alone, failing **1.4.1 Use of Color**. Weak on *color/state & contrast*.
- **Type below the floor and a fragile grid.** `font-size: 14px` on filters is under the 16px / 1rem body minimum and risks problems under **1.4.4 Resize text**. `minmax(240px, 1fr)` overflows a 320px viewport (240px + gap + padding > 320), failing **1.4.10 Reflow**. Weak on *typography craft* and *production readiness*.
- **Hover-only affordances exclude touch and keyboard.** "Quick view" appears on hover only — invisible to touch and to `:focus-visible`, and the card lift has no `prefers-reduced-motion` guard. Weak on *interaction polish & motion* and fails **2.1.1 Keyboard** for the hidden control.
- **Off-canvas filter panel with no dialog semantics.** "Hide the sidebar, show a Filters button" with no focus trap, no ESC, no scroll-lock, no return focus — the phone path is unusable by keyboard and strands screen-reader users behind page content.

## Strong response

```md
## Layout and grid

Two-pane on >= 1024px, single column below it.

- Container max-width 1280px, side padding clamp(16px, 4vw, 32px).
- Desktop: CSS grid `grid-template-columns: 280px minmax(0, 1fr)` with 32px gap.
  Left column is the filter panel as a sticky `<aside>` (top: 16px); right
  column is the results region.
- The results grid uses a container query, not the viewport, so it stays
  correct inside the narrowed column:

.results { container-type: inline-size; }
.results__grid {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr;            /* 320px reflow floor: 1 card */
}
@container (min-width: 480px)  { .results__grid { grid-template-columns: repeat(2, 1fr); } }
@container (min-width: 720px)  { .results__grid { grid-template-columns: repeat(3, 1fr); } }
@container (min-width: 1080px) { .results__grid { grid-template-columns: repeat(4, 1fr); } }

Cards reserve image space to protect CLS (<= 0.1):

.card__media { aspect-ratio: 4 / 3; }   /* no layout shift on image load */
.card__media img { width: 100%; height: 100%; object-fit: cover; }
.card { padding: 16px; border: 1px solid var(--border); border-radius: 12px; }
.card__title { font-size: 1rem; line-height: 1.35; }   /* 16px floor */

Body type: `font-size: clamp(1rem, 0.95rem + 0.3vw, 1.125rem)`, line-height 1.5,
result copy capped at ~65ch. Filter labels are 1rem, never below 16px.

## Semantics and landmarks

<main>
  <h1>Used cameras</h1>
  <div class="layout">
    <aside aria-labelledby="filters-h" id="filter-panel">
      <h2 id="filters-h">Filters</h2>
      <!-- one <fieldset> per facet -->
    </aside>

    <section aria-labelledby="results-h">
      <div class="results__bar">
        <h2 id="results-h" aria-live="polite">42 cameras</h2>
        <!-- sort control -->
      </div>
      <ol class="results__grid"> … </ol>
      <nav aria-label="Search results pages"> … </nav>
    </section>
  </div>
</main>

One `<h1>`, no skipped levels; each facet group is a `<fieldset>` with a
`<legend>`. The live count in `#results-h` is `aria-live="polite"` so every
filter change announces "42 cameras" without moving focus — satisfies
WCAG 4.1.3 Status Messages.

## Filters: live, counted, never color-only

- Each option shows its post-filter count and stays operable when it would
  return zero, but is visibly de-emphasized: `Sony (18)`, `Hasselblad (0)`.
- Apply filters ON CHANGE (debounced 250ms), not behind an Apply button, so the
  running count gives immediate feedback. Provide a persistent "Clear all" and
  per-chip removal.
- Active facets render as a removable chip row above the grid; each chip is a
  `<button>` ("Brand: Sony ✕", target >= 24x24px) and updates the URL on remove.
- Price is a numeric MIN/MAX INPUT PAIR first (typeable, keyboard-native), with
  the dual slider as a `pointer: coarse` enhancement layered on top — never the
  only control, so it passes 2.1.1 Keyboard.
- Condition badges pair a shape/text token with color so meaning never rides on
  hue alone (1.4.1 Use of Color): `● Mint`, `◐ Good`, `○ Fair`, each token also
  reaching 4.5:1 against its background (1.4.3) and 3:1 for the dot itself
  (1.4.11 Non-text Contrast).

## Sort

A native `<select>` labelled "Sort", four options (Newest, Price low→high,
Price high→low, Best match). On change it patches the URL and re-fetches — no
custom listbox, so keyboard, screen reader, and forced-colors mode work for
free. Default `?sort=newest` is omitted from the URL to keep links clean.

## URL as the single source of truth (the spine of the feature)

Every facet, the sort, and the page live in the query string. The URL *is* the
state; the DOM is rendered from it.

/cameras/mirrorless?brand=sony,fujifilm&condition=mint,good&price=200-900&mp=24-&sort=price_asc&page=2

- On a filter/sort/page change, build the next URL and call
  `history.pushState(state, '', nextUrl)`, then fetch and swap the results
  region only. `popstate` (Back/Forward) re-reads the query and re-renders —
  Back undoes exactly one facet change (heuristic #3, user control).
- Removing the last value of a facet drops the param entirely; arrays are
  comma-joined and sorted for stable, cache-friendly, canonical URLs.
- `<link rel="canonical">` points at the normalized URL; thin/duplicate
  combinations get `<meta name="robots" content="noindex,follow">` so crawlers
  index the valuable facet pages (brand, category) without combinatorial bloat.
- Pagination uses real `<a href>` links so crawlers and middle-click work; JS
  intercepts them to pushState + fetch as a progressive enhancement.

## Async states for the results region

Default, loading, empty, error — all scoped to the results region; page chrome
and filters stay interactive.

- LOADING: render N skeleton cards matching the card's `aspect-ratio` box so
  there is zero layout shift; set `aria-busy="true"` on the grid. Keep the old
  results visible but dimmed for < 300ms to avoid flashing on fast networks.
- EMPTY: "No cameras match these filters." plus a one-tap "Clear all filters"
  and the two most-restrictive active chips to remove.
- ERROR / OFFLINE: "Couldn't load results." with a Retry button (the request is
  idempotent — a GET — so retry is safe) and an `aria-live="assertive"`
  announcement. Session-expired falls back to a full navigation.
- INP budget: change handlers do URL + optimistic count synchronously, network
  off the main thread; target INP <= 200ms, LCP <= 2.5s on the first card image
  (preloaded, `fetchpriority="high"`).

## Filter panel under 1024px: a real dialog

Trigger button "Filters (3)" opens a `<dialog>` (or off-canvas side-sheet) with
proper modal semantics:

- `dialog.showModal()` traps focus, ESC closes, focus returns to the trigger,
  background scroll is locked, `aria-modal="true"`.
- A sticky footer holds "Show 42 results" (primary) and "Clear all"; the live
  count updates as facets toggle so the CTA always reflects reality. A standard
  sticky action bar, not an overlay button that floats over content.

## Interaction and motion

.card { transition: box-shadow 150ms ease, transform 150ms ease; }
.card:hover, .card:focus-within { box-shadow: 0 8px 24px rgb(0 0 0 / 0.12); }
:where(a, button, input, select, summary):focus-visible {
  outline: 2px solid var(--focus); outline-offset: 2px;   /* 2.4.7 / 2.4.11 */
}
@media (prefers-reduced-motion: reduce) { .card { transition: none; } }
@media (pointer: fine)  { .card__quickview { opacity: 0; }
  .card:hover .card__quickview, .card:focus-within .card__quickview { opacity: 1; } }
@media (pointer: coarse){ .card__quickview { opacity: 1; } }  /* always shown on touch */

"Quick view" is a real `<button>` present in the DOM for everyone; only its
*reveal animation* is hover-gated, and it is always visible on touch and on
keyboard focus. Focus is never obscured by the sticky bar (2.4.11).

This lands at 4/5: shareable/crawlable URL state, live counted facets, a genuine
dialog on the phone breakpoint, full async states, and AA contrast — strong and
shippable. The fifth point would need real ranking/relevance tuning and field
CWV data.
```

## Why this is stronger

- **The URL becomes the state machine**, directly answering the prompt's three hardest asks at once — shareable links, crawlable facet pages (canonical + selective `noindex,follow`), and a correct Back button via `pushState`/`popstate`. This closes the weak answer's largest gap and aligns with **heuristic #3 (user control & freedom)** and **#4 (consistency with the platform)**. Big lift on *production readiness*.
- **Live, counted facets with per-option result counts** turn filtering into a guided narrowing task instead of guesswork; the running "42 cameras" count plus visible-but-de-emphasized zero options is textbook *attention path & hierarchy* and **heuristic #1 (visibility of system status)**.
- **Every async state is designed and announced.** Skeletons that match `aspect-ratio` protect **CLS <= 0.1**; `aria-live` regions satisfy **WCAG 4.1.3**; an idempotent GET makes Retry safe. This answers the "slow network" question the weak version ignored — strong *interaction polish* and *production readiness*.
- **Accessibility is structural, not bolted on.** `<fieldset>`/`<legend>` per facet, a native `<select>` for sort, a native `<dialog>` with focus trap + ESC + restore on the phone breakpoint, and typeable price inputs before any slider — all satisfy **2.1.1 Keyboard**, **2.4.3 Focus Order**, and **2.4.11 Focus Not Obscured**, and they survive forced-colors mode.
- **Contrast and non-color signaling are correct.** Condition uses shape + text + color and hits **1.4.3 (4.5:1)**, **1.4.11 (3:1 non-text)**, and **1.4.1 (Use of Color)** — the precise trio the weak `#19c37d` badge failed. Solid *color/state & contrast*.
- **Layout is robust by construction.** Container queries (not the viewport) keep the grid correct inside the narrowed results column; a single-column floor passes **1.4.10 Reflow** at 320px; the 16px / 1rem minimum and `clamp()` fluid scaling respect **1.4.4 Resize text**. Strong *composition & spacing*, *density & rhythm*, and *typography craft*.
- **Touch, mouse, and keyboard are first-class together** via `@media (pointer: coarse|fine)` and `:focus-within`, so "Quick view" exists for everyone and only its animation is hover-gated — fixing the weak answer's hover-only trap and honoring `prefers-reduced-motion`.

## Regression checks

A future revision of this answer must still pass every one of these:

- Changing a filter, sort, or page updates the query string via `history.pushState`, and Back/Forward (`popstate`) restores the exact prior result state — a shared link reproduces the same filtered, sorted, paginated view.
- The result count is exposed in an `aria-live="polite"` region and updates on every facet change, so a non-sighted user is told "N cameras" without a focus jump (WCAG 4.1.3).
- The results region defines all four async states — loading (skeletons sized to `aspect-ratio`, `aria-busy`), empty (with Clear-all), and error/offline (idempotent Retry) — with no cumulative layout shift above CLS 0.1.
- Condition and any other status never rely on color alone: each carries a shape or text token AND meets 4.5:1 text contrast (1.4.3) and 3:1 non-text contrast (1.4.11 / 1.4.1).
- Body and filter type stay at 16px / 1rem or above, and the grid reflows to a single column at 320px without horizontal scroll (1.4.10 / 1.4.4); the results grid keys off a container query, not the viewport.
- The phone-breakpoint filter panel is a true modal (`<dialog>` / side-sheet) with focus trap, ESC to close, scroll-lock, and focus restored to the trigger — no keyboard trap, focus never obscured by the sticky action bar (2.1.1 / 2.4.11).
- Sort is a native `<select>` (or an APG-conformant listbox), pagination uses real `<a href>` links, and price has a typeable min/max input pair before any slider enhancement.
