# Case study: Operations dashboard with a dense, sortable, selectable orders table

A bad-to-good calibration case for a web-app data table. The task rewards desktop
density: an operations user scans hundreds of orders per shift, sorts by columns,
multi-selects rows, and runs bulk actions. The weak answer flattens this into a
phone-style card list and ignores keyboard, contrast, and async-state work. The
strong answer exploits the desktop grid, native semantics, and WCAG 2.2 AA while
staying buildable.

## Prompt

```text
We run a B2B logistics tool. Operators live in the "Orders" screen all day on
1440px laptops. They need to:
- See ~50 rows at once: order ID, customer, status, destination, items, total, SLA due.
- Sort by any column (most often SLA due and total).
- Select many rows and run bulk actions: "Mark shipped", "Assign carrier", "Export CSV".
- Filter by status without losing their place.

It must be fast (thousands of orders), keyboard-friendly for power users, and meet
WCAG 2.2 AA. Give me the layout, the table interaction model, the states, and the
key CSS/markup decisions. Mobile matters less but it can't be unusable at 320px.
```

## Weak response

```md
Here's a clean Orders dashboard.

**Layout:** A top bar with the logo and a search box. Below it, the orders shown
as cards in a responsive grid so it looks good on every screen. Each card shows
the order ID in bold, the customer, a colored status dot (green = shipped, red =
late), and the total.

**Sorting:** Add a dropdown above the cards: "Sort by total / date / customer".
When the user picks one, re-order the cards.

**Selection:** Put a small checkbox in the corner of each card. A floating button
in the bottom-right opens the bulk-actions menu when something is selected.

**Filtering:** Status pills at the top (All / Open / Shipped / Late). Tapping one
filters the list.

**Styling:** 14px text to fit more in, lots of whitespace, subtle gray borders,
status shown by color so it's scannable at a glance. Hover changes the card
background. Use a spinner while data loads.

**Mobile:** Because it's already cards, it just reflows to one column at 320px.

That gives you a modern, friendly dashboard that works everywhere.
```

## Why this is weak

- Attention path & hierarchy (2/5): a card grid destroys column alignment, so the
  operator cannot scan one variable (SLA due, total) down a straight edge. Cards
  optimize for browsing a few rich items, not comparing 50 homogeneous records.
  Nielsen's "match between system and the real world" and "flexibility and efficiency
  of use" both point to a tabular layout for this task.
- Density & rhythm (1/5): the task explicitly rewards density on a 1440px laptop,
  yet the answer flattens desktop to a phone layout. It wastes horizontal space and
  shows far fewer than the requested ~50 rows per viewport.
- Color/state & contrast (1/5): status is conveyed by a colored dot alone, failing
  WCAG 1.4.1 Use of Color. "14px text" violates the 16px body floor and is at risk
  on 1.4.3 contrast if paired with gray. No focus-visible, loading skeleton, empty,
  error, or partial-failure states beyond a bare spinner.
- Interaction polish & motion (2/5): a floating button for bulk actions is the wrong
  pattern for a dense web tool and is a banned approach here; bulk actions belong in
  a contextual action bar tied to the selection. A sort dropdown hides the current
  sort key and direction instead of putting them in the column headers.
- Production readiness (1/5): "thousands of orders" with no virtualization will jank
  INP and scrolling. No keyboard model (2.1.1), no aria-sort, no row-selection
  semantics, no aria-live for async, no sticky header, no URL-as-state for sort/filter.
  Spinner-only loading risks layout shift (CLS) when content swaps in.
- Typography craft (2/5): "lots of whitespace" contradicts the density goal and is
  unspecified; no type scale, no tabular numerals for the numeric columns.

## Strong response

```md
This is a comparison-and-action task, so use a real data table, not cards. Exploit
the 1440px width; degrade gracefully, don't design phone-first.

## Layout (12-col desktop grid)

- header[role=banner]: product nav + global search. Skip link <a href="#orders">
  first in tab order.
- main#orders: a toolbar region above one <table>.
  - Left of toolbar: status filter as a segmented control of native <button>s
    (All / Open / Shipped / Late), aria-pressed reflecting state.
  - Right: density toggle (Comfortable 48px / Compact 36px rows), column-visibility menu.
- Container max-width ~1440px; table fills it. The ~65ch reading-column rule is for
  prose, not tables — let columns breathe, but right-align and tabular-align numbers.

## The table

Native semantics so the browser and assistive tech do the heavy lifting:

​```html
<table aria-describedby="orders-summary">
  <caption id="orders-summary" class="sr-only">
    Orders, sorted by SLA due ascending. 2,418 results, 3 selected.
  </caption>
  <thead>
    <tr>
      <th scope="col">
        <input type="checkbox" aria-label="Select all on this page" />
      </th>
      <th scope="col" aria-sort="ascending">
        <button type="button">SLA due <span aria-hidden="true">▲</span></button>
      </th>
      <th scope="col" aria-sort="none">
        <button type="button">Total</button>
      </th>
      <!-- … -->
    </tr>
  </thead>
  <tbody><!-- virtualized rows --></tbody>
</table>
​```

- Sort lives in the header: each sortable <th> wraps a <button> and carries
  aria-sort="ascending|descending|none". The arrow is a visible glyph AND the
  aria-sort value, so sort state is never conveyed by color or icon alone (1.4.1).
  Click or Enter/Space cycles asc → desc → none. Sort key + direction live in the
  URL (?sort=sla_due&dir=asc) so it is shareable and survives back/forward.
- Selection: a real <input type=checkbox> per row (<td> with aria-label naming the
  order). Header checkbox = select-all-on-page with an indeterminate state for
  partial selection. Shift-click selects a range; the same range op is reachable by
  keyboard (Space to toggle the focused row, Shift+Space to extend).
- Status column is text + a shape-bearing badge, never a bare dot: the "Late" badge
  has a warning glyph and a label; color reinforces but does not carry meaning
  (1.4.1). Badge border and text meet 1.4.11 non-text 3:1 and 1.4.3 text 4.5:1.
- Numbers: font-variant-numeric: tabular-nums, right-aligned Total and SLA, so
  digits line up for fast vertical scanning.

## Density, type, spacing

- Body 16px (1rem) minimum; data cells font-size: clamp(0.875rem, 0.8rem + 0.2vw, 1rem)
  with a rem term — but page chrome and any prose stay >=16px.
- Row heights from the 4px scale: Compact 36px, Comfortable 48px. Cell padding
  12px/16px. line-height 1.5 for wrapped cells, 1.2-1.35 for headings.
- Sticky thead (position: sticky; top: 0) so headers persist while scrolling 50+
  rows. Sticky select + Order ID columns (position: sticky; left: 0) on horizontal
  scroll.

## Selection → bulk actions (contextual action bar, not a floating button)

When selectedCount > 0, reveal an action bar pinned under the toolbar (not floating):
"3 selected · Mark shipped · Assign carrier · Export CSV · Clear". It is in the DOM
in source order, fully keyboard reachable, and aria-live="polite" announces "3
selected". Targets are >=24px (2.5.8); the primary "Mark shipped" is a 44px button
(2.5.5 AAA) given heavy use.

## States (web)

- Loading: skeleton rows that reserve the exact row height via aspect-ratio / fixed
  height, so swapping in data causes no layout shift (CLS <= 0.1). No bare spinner.
- Empty (filter matches nothing): "No orders match these filters" + a "Clear
  filters" button, not a dead grid.
- Error / partial failure: inline banner with retry; if one bulk-action row fails,
  show a per-row error state and keep the rest. role="alert" for the failure.
- Disabled bulk action when nothing selected (visually + disabled), plus
  session-expired and offline handled with a re-auth / retry banner.

## Keyboard & focus (2.1.1, 2.4.11)

- Tab order: skip link → search → filters → density → table. Inside tbody, Arrow
  keys move row focus (roving tabindex), Space toggles selection, Enter opens the
  order. Header buttons are normal tab stops.
- :focus-visible ring on every interactive element, 3:1 against its background
  (1.4.11); the sticky header must not obscure the focused row (2.4.11) —
  scroll-margin keeps the active row clear of the sticky chrome.
- Any row-detail overlay uses <dialog>: focus trap, ESC to close, scroll-lock, focus
  restored to the triggering row.

## Performance & responsive

- Virtualize tbody (windowed rows) so thousands of orders keep INP <= 200ms and
  smooth scroll; keep the real <table> semantics for the rendered window.
- font-display: swap + preload the table font; fallback metrics tuned to avoid CLS.
- Reflow (1.4.10): above 768px, full table. Below 640px, collapse to a stacked
  "label: value" list per order via a container query on the table wrapper — still a
  <table> semantically, restyled — usable and not horizontally clipped at 320px.
- Resize to 200% (1.4.4) and text-spacing (1.4.12) overrides: no clipping, no loss
  of rows or actions.

Target quality: 4/5 across the eight dimensions — strong and shippable.
```

## Why this is stronger

- Attention path & hierarchy (4/5): one <table> with aligned columns, a sticky
  header, and a single dominant sort indicator lets the eye scan one variable down a
  straight edge. Honors Nielsen "visibility of system status" (sort state and
  selected count are always visible) and "recognition rather than recall".
- Density & rhythm (4/5): the answer exploits desktop width with a density toggle
  (36/48px rows on the 4px scale) and tabular numerals, fitting the requested ~50
  rows without flattening to a phone layout.
- Color/state & contrast (4/5): status uses text + a shape-bearing badge, satisfying
  1.4.1 Use of Color; text 4.5:1 (1.4.3), non-text and focus rings 3:1 (1.4.11);
  forced-colors / Windows High Contrast support comes through native controls plus
  glyphs. Full state matrix: loading skeleton, empty, error, partial failure,
  disabled, offline, session-expired.
- Interaction polish & motion (4/5): sort is in the header with aria-sort; bulk
  actions live in a contextual action bar tied to selection (no floating button);
  shift-click range select has a keyboard equivalent. Sort/filter live in the URL for
  shareable, back/forward-safe state.
- Production readiness (4/5): virtualized rows protect INP <= 200ms; skeletons
  reserve space for CLS <= 0.1; LCP <= 2.5s aided by font preload + swap. Keyboard
  model (2.1.1), roving tabindex, focus not obscured (2.4.11), aria-live for async,
  <dialog> for detail overlays — all named and buildable.
- Typography craft (4/5): 16px floor for chrome/prose, fluid clamp() with a rem term
  for data cells, tabular-nums, line-height 1.5 with headings 1.2-1.35.

## Regression checks

- A future answer MUST keep a real <table> (or ARIA grid) for this comparison task
  and MUST NOT replace it with a card grid for the primary dense view.
- Status MUST NOT be conveyed by color alone: text plus a shape/label badge is
  required (WCAG 1.4.1). A bare colored dot is a regression.
- Bulk actions MUST live in a contextual action bar tied to selection; a floating
  button is banned here and is an automatic fail.
- Sort state MUST be exposed in the header via aria-sort and a visible glyph, not a
  hidden dropdown, and SHOULD persist in the URL for back/forward.
- Keyboard operability MUST be specified: tab order, roving tabindex inside tbody,
  :focus-visible, focus not obscured by the sticky header (2.4.11), ESC-to-close on
  any <dialog> overlay.
- Body/chrome text MUST stay >=16px (1rem); thousands of rows MUST be virtualized so
  INP <= 200ms, and loading MUST use space-reserving skeletons to hold CLS <= 0.1.
- Boundary: this is a SYNTHETIC calibration fixture for the skill and is not
  validation against a shipped, real product; the "4/5" rating is an authoring
  target, not a measured score from usability testing.
