# Patterns Catalog

This is the largest reference in the web-design skill. It catalogs the
interaction patterns you reach for when designing responsive web, marketing
and landing pages, and web applications. Each pattern is written as a
decision matrix so that you can pick deliberately, not by habit, and so that
reviewers can check a build against an explicit violation list.

## How to use this document

Every pattern entry uses the same five-field meta-structure. Read the fields
in order; the first two tell you whether the pattern even applies before you
spend time on the mechanics.

- **Use-when** — the conditions that make this pattern the right answer.
- **Avoid-when** — the conditions under which it is the wrong answer, even
  though it is tempting or conventional.
- **Mechanism** — how it works: the markup, the platform primitives, the
  state it owns, and the accessibility contract it must satisfy.
- **Failure mode** — how it breaks in production, so you can recognize the
  smell before users do.
- **Red flags** — a concrete checklist of violations. These are the lines a
  Mode D review reads aloud against the artifact. If any red flag is true,
  the pattern is implemented wrong.

Where a pattern maps to the WAI-ARIA Authoring Practices Guide (APG), the
entry names the APG pattern. Use the APG keyboard and roles spec as the
contract; do not invent ad-hoc roles when a named pattern exists.

These web physics are assumed everywhere and are not repeated per pattern:

- Body text at a minimum of `16px` / `1rem`; fluid type via `clamp()`; line
  length held near a `65ch` measure.
- Spacing drawn from the `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64` px scale.
- WCAG 2.2 AA: 1.4.3 text contrast `4.5:1` (`3:1` for large text), 1.4.11
  non-text contrast `3:1`, 1.4.10 reflow at `320px` with no loss of content
  or function, 2.5.8 target size `24px` minimum (`44px` is the 2.5.5 AAA
  bar), 2.4.11 focus appearance not obscured, and `forced-colors` support.
- Full keyboard operability: logical tab order, visible `:focus-visible`
  rings, focus trap plus restore for modal surfaces, skip links, and ESC to
  dismiss transient layers.
- Core Web Vitals budgets: LCP `<= 2.5s`, INP `<= 200ms`, CLS `<= 0.1`.

When a pattern conflicts with these physics, the physics win.

## 1. Primary navigation (top-nav / sidebar / mega-menu / breadcrumb / footer)

Navigation is the spine of a web product. The decisive question is the shape
of the information space, not the screen size. Pick the structure first, then
decide how it degrades down the breakpoint ladder (section 10).

### Decision matrix: which navigation structure

| Structure | Use-when | Avoid-when |
| --- | --- | --- |
| Top horizontal nav | 3–7 flat top-level destinations; marketing sites and shallow apps; you want the content column full-width | More than ~7 destinations; deep hierarchies; dense application chrome |
| Sidebar (vertical) nav | Application shells with many destinations or sections; persistent context (workspace, project); deep but navigable trees | Marketing pages where the sidebar steals the measure; fewer than 4 destinations |
| Mega-menu | A top-nav site with broad catalog/structure (commerce, large content sites) where users browse categories | Apps; small sites; any case where a flat menu or search would be faster |
| Breadcrumb | Deep hierarchical content where users need to know "where am I" and jump up levels | Flat sites; flows with no real hierarchy; as a substitute for primary nav |
| Footer nav | Secondary, comprehensive, low-frequency links (legal, support, sitemap, locale) | As the only home for a destination users need mid-task |

These coexist. A typical commerce site has top-nav + mega-menu +
breadcrumb + footer. A typical web app has sidebar + breadcrumb. Treat
them as a system, not alternatives.

### Top horizontal nav

- **Use-when**: 3–7 top-level destinations; you want maximum content width;
  the brand and primary actions sit on one row.
- **Avoid-when**: the destination count is growing past what fits without
  crowding; the product is a dense app shell that benefits from a persistent
  vertical rail.
- **Mechanism**: a `<nav aria-label="Primary">` containing a list of links
  (`<ul><li><a>`). It is a set of links, not a widget — do **not** apply
  `role="menubar"`. The current destination carries `aria-current="page"`.
  Each link is a real URL so it is shareable, mid-clickable, and indexable.
- **Breakpoint**: show the inline nav only from the width where every label
  fits on one line, measured by the rendered-QA width sweep, not guessed from
  the ladder. Labels carry `white-space: nowrap`; below that width the nav
  collapses to a disclosure button (`<button aria-expanded>`) with a text
  label. The breakpoint absorbs the overflow, not shrinking type.
- **Failure mode**: the link count outgrows the row, items wrap or get
  hidden behind an unlabeled icon, and the active state is lost. On small
  viewports it silently becomes an inaccessible icon toggle.
- **Red flags**:
  - `role="menubar"` / `role="menuitem"` on what are really page links.
  - No `aria-current` on the active destination.
  - The "current page" relies on color alone (fails 1.4.1 / 1.4.3).
  - A label wraps to two lines at a mid width (between ladder rungs).
  - Nav items are `<div onclick>` instead of `<a href>` — no real URL, no
    keyboard, no middle-click, no right-click "open in new tab".

### Sidebar (vertical) nav

- **Use-when**: an application shell with many sections, persistent context,
  or a navigable tree; users return to the same destinations repeatedly.
- **Avoid-when**: a marketing or content page where it eats the reading
  measure; fewer than ~4 destinations.
- **Mechanism**: `<nav aria-label="Sections">` with a link list; collapsible
  groups are disclosure buttons (`aria-expanded`), not menus. A collapsed
  icon-only rail still exposes accessible names (visible label, `title`, or
  `aria-label`) and a tooltip on hover/focus. Persist collapsed/expanded
  state. Below the breakpoint where it no longer fits, it converts to an
  off-canvas drawer (section 2, section 10) — deliberately, not by overflow.
- **Failure mode**: the collapsed icon rail becomes a guessing game (no
  labels), or the sidebar and content both try to scroll and trap the user.
- **Red flags**:
  - Icon-only items with no accessible name.
  - Tree/disclosure expansion not keyboard-operable or missing
    `aria-expanded`.
  - Sidebar overlaps content at narrow widths instead of converting to a
    drawer; reflow at `320px` breaks.

### Mega-menu

- **Use-when**: a broad catalog or large content taxonomy under a top-nav;
  users benefit from seeing a category's structure at a glance.
- **Avoid-when**: an app; a small site; when search gets users there faster.
- **Mechanism**: a disclosure pattern, not a `menu` widget. The trigger is a
  `<button aria-expanded>` (or a link with an associated panel) that reveals
  a panel of grouped **links**. Open on click/Enter/Space; ESC closes and
  returns focus to the trigger; clicking outside closes. Do not open on hover
  only — hover-only panels are unreachable by keyboard and flaky on touch.
  Reference: APG **Disclosure** pattern for the show/hide contract.
- **Failure mode**: a hover-only mega-menu that snaps shut when the pointer
  crosses a gap, is impossible to keyboard through, and overlays content the
  user wanted to click.
- **Red flags**:
  - Opens on hover with no click/keyboard equivalent.
  - No ESC-to-close, no focus return to trigger.
  - Treated as `role="menu"` with arrow-key roving when it is really a panel
    of links and form controls.
  - Panel content is not in the DOM until hover (invisible to assistive tech
    and search).

### Breadcrumb

- **Use-when**: deep hierarchical content; users need orientation and a fast
  way up the tree.
- **Avoid-when**: flat structures; as a stand-in for primary navigation.
- **Mechanism**: `<nav aria-label="Breadcrumb">` wrapping an ordered list of
  links; the final item is the current page and is marked with
  `aria-current="page"` (and is typically not a link). Separators are
  decorative (CSS or `aria-hidden`), never read out.
- **Failure mode**: breadcrumbs that don't reflect the real path (e.g. show
  the click path instead of the hierarchy) and mislead the user's mental map.
- **Red flags**:
  - Separators announced by a screen reader.
  - Current page is a link to itself with no `aria-current`.
  - Used as the only navigation on the page.

### Footer nav

- **Use-when**: comprehensive secondary links — legal, support, locale,
  sitemap, social — that users seek out intentionally.
- **Avoid-when**: hiding a primary, in-task destination only in the footer.
- **Mechanism**: a `<footer>` with grouped link lists, each group under a
  heading. Real links; keyboard reachable in logical order.
- **Failure mode**: the "everything bucket" — a wall of links with no
  grouping or headings, impossible to scan.
- **Red flags**: ungrouped link soup; a critical task link reachable only
  here; contrast of muted footer text below `4.5:1`.

### Routing, URL, and history contract (applies to all of the above)

This is non-negotiable for web navigation and is where single-page apps most
often regress versus plain documents.

- **History API**: client-side navigation must call `pushState` /
  `replaceState` so the URL changes, and must handle `popstate` so
  back/forward restore the right view. Use `pushState` for new destinations,
  `replaceState` for in-place state (e.g. applying a filter).
- **URL as shareable state**: the URL is the canonical, shareable, bookmarkable
  description of the view. Filters, tabs, search query, sort, and pagination
  belong in the query string (section 8) — not in component state that
  vanishes on reload.
- **Back/forward**: every meaningful state the user can reach forward must be
  reachable backward. Back must not skip past or replay destructive actions.
- **`beforeunload`**: register a `beforeunload` warning **only** when there is
  unsaved work to lose, and remove it the instant the form is clean. A blanket
  "are you sure you want to leave" on every page is a dark pattern and harms
  back/forward.
- **Scroll restoration**: set `history.scrollRestoration = 'manual'` and
  manage scroll yourself in SPAs (restore prior scroll on back, scroll to top
  on a new route, scroll to the target for in-page anchors). Default browser
  restoration fights client routing and causes jumps that read as CLS.

## 2. Overlays (dialog / popover / off-canvas / side sheet)

An overlay is layered UI that sits above the page. The first decision is
whether you need an overlay at all — inline disclosure is almost always
calmer. The second is whether it is **modal** (blocks the page beneath) or
**non-modal** (the page stays live).

### Decision matrix: which overlay

| Overlay | Modal? | Use-when | Avoid-when |
| --- | --- | --- | --- |
| Native `<dialog>` | Modal (`showModal`) | Focused, blocking task: confirm, edit, sign-in; you need the page beneath inert | Content that belongs in the page flow; anything users want to keep visible while working |
| Popover API | Non-modal (light dismiss) | Transient, anchored UI: menus, tooltips, small pickers, action lists | Long forms; content needing a focus trap; anything blocking |
| Off-canvas / side sheet | Either | Secondary nav drawer (collapsed sidebar at narrow widths), filters, detail panel beside a list | Primary content; when a popover or inline panel suffices |
| Inline disclosure | Non-modal | "Show more", accordions, expandable rows — keep context, no layer | When the content truly must interrupt and block |

Default bias: **inline > popover > side sheet > modal dialog**. Reach for a
modal only when blocking is the point.

### Native `<dialog>` (modal)

- **Use-when**: a blocking, focused task — confirmation, a short edit, a
  sign-in — where the rest of the page must wait.
- **Avoid-when**: content that wants to coexist with the page; long or
  multi-step flows better served by a dedicated route/page.
- **Mechanism**: open with `dialog.showModal()`. This gives you, for free:
  the top layer (above all stacking contexts), the `::backdrop`, `inert` on
  the rest of the document, ESC-to-close, and an accessible modal semantics
  baseline. You still must: set an accessible name (`aria-labelledby` to the
  title); move focus to the first sensible control or the dialog itself on
  open; **restore focus to the invoking trigger on close**; and lock body
  scroll so the page behind does not scroll. This is the APG **Dialog
  (Modal)** pattern — focus is trapped within the dialog, Tab/Shift+Tab
  cycle inside it, ESC dismisses.
- **Failure mode**: a hand-rolled `<div role="dialog">` overlay with **no
  focus trap** — Tab walks out the back of the modal into the inert page,
  the keyboard user is lost behind the backdrop, and ESC does nothing. This
  is the single most common overlay bug.
- **Red flags**:
  - Built from `<div>` + z-index instead of `<dialog>`/`showModal` with no
    equivalent of the top layer and `inert`.
  - **No focus trap**: Tab escapes to the page behind.
  - Focus not moved into the dialog on open.
  - Focus not restored to the trigger on close.
  - No ESC-to-close.
  - Body scrolls behind the modal (no scroll lock).
  - Missing `aria-labelledby` / accessible name; missing `aria-modal` when
    not using native modal semantics.
  - Close affordance is only the backdrop click, with no visible button.

### Popover API (non-modal, anchored)

- **Use-when**: transient, anchored, non-blocking UI — an action menu, a
  date picker, a small filter, a tooltip-like panel.
- **Avoid-when**: anything that needs to block the page or trap focus; long
  forms.
- **Mechanism**: native `popover` attribute with `popovertarget` triggers
  gives top-layer rendering and **light dismiss** (`popover="auto"`: ESC and
  outside-click close it, and only one auto popover is open at a time).
  Anchor positioning ties it to its trigger. Focus is *not* trapped — that is
  correct for non-modal. If the popover is a menu of commands, layer the APG
  **Menu Button** keyboard model on top (arrow-key roving, Enter/Space to
  activate, ESC returns focus to the button).
- **Failure mode**: a popover that never closes on outside click or ESC and
  stacks up; or one used as a modal (blocking) without the trap, leaving an
  ambiguous, escapable layer.
- **Red flags**:
  - Used for blocking/critical decisions (should be a modal dialog).
  - No light-dismiss (ESC / outside click).
  - Positioned off-screen at narrow widths because anchor/collision handling
    is missing — fails reflow at `320px`.
  - Command menu without keyboard roving or focus return.

### Off-canvas / side sheet

- **Use-when**: a drawer for navigation (the narrow-width form of a sidebar),
  filters, or a detail panel that slides in beside or over content.
- **Avoid-when**: it would hide primary content the user needs to act on; a
  popover or inline panel would do.
- **Mechanism**: a panel that translates in from an edge. As a navigation
  drawer at narrow widths it is **modal**: scrim/backdrop, scroll lock, focus
  trap, ESC, and focus restore to the hamburger trigger — same contract as a
  dialog. As a wide-screen detail panel beside a list it may be **non-modal**
  and persistent. Animate `transform` (compositor-friendly), respect
  `prefers-reduced-motion`.
- **Failure mode**: the drawer opens but the body keeps scrolling behind it,
  or it traps focus yet has no visible close and no ESC, stranding the user.
- **Red flags**:
  - Modal drawer with no scroll lock or no focus trap.
  - No focus restore to the toggle on close.
  - Animates `left`/`width` (layout thrash) instead of `transform`.
  - Ignores `prefers-reduced-motion`.

### Inline disclosure / accordion

- **Use-when**: progressive disclosure that should keep the user in place —
  "show more", FAQ accordions, expandable table rows.
- **Avoid-when**: the content must interrupt and block.
- **Mechanism**: APG **Disclosure** (single show/hide) or
  **Accordion** pattern. A `<button aria-expanded>` controls a region via
  `aria-controls`; content is in the DOM. No focus trap, no scrim.
- **Failure mode**: animating `height: auto` causes layout shift (CLS) and
  janky open/close.
- **Red flags**: toggle is a non-button element; missing `aria-expanded`;
  content removed from DOM (lost to search and assistive tech) instead of
  hidden.

## 3. Content display (list / grid / card / data table)

How you present a collection should follow the data's shape and the user's
task, not a default template. The big web-specific decision is recognizing
when the answer is a **real data table** — and resisting the urge to flatten
it into phone-style cards on desktop.

### Decision matrix: which collection layout

| Layout | Use-when | Avoid-when |
| --- | --- | --- |
| List (vertical) | One primary attribute per item; ordered or scannable text; feeds | Multi-attribute records users compare/sort |
| Grid / gallery | Visual items where the thumbnail is the content (photos, products) | Text-dense records; data that needs alignment and comparison |
| Card collection | Mixed media + text "objects" with a few attributes and per-item actions | Many rows of comparable numeric/text fields (use a table) |
| Data table | Records with multiple comparable columns; sorting, scanning, bulk ops | A single attribute per item; purely visual content |

### List

- **Use-when**: items reduce to one main line (plus minor metadata);
  notifications, activity feeds, simple results.
- **Avoid-when**: users need to compare several attributes across items.
- **Mechanism**: semantic `<ul>`/`<ol>`; each row a link or has a clear
  primary action; consistent left-aligned start so the eye scans one column.
- **Failure mode**: stuffing five attributes per row until it is a bad,
  unaligned table.
- **Red flags**: rows that are really records pretending to be a list;
  non-semantic `<div>` rows with no list semantics.

### Grid / gallery

- **Use-when**: the image *is* the information; product/photo/media browsing.
- **Avoid-when**: text-heavy records needing column alignment.
- **Mechanism**: CSS Grid with `minmax()` + `auto-fill`/`auto-fit` so columns
  reflow by available width (often better than breakpoint hops); reserve
  aspect-ratio boxes for images to prevent CLS; lazy-load below the fold.
- **Failure mode**: images without reserved dimensions reflow the grid as
  they load (CLS); too-small tap/click targets in dense grids.
- **Red flags**: no `width`/`height` or `aspect-ratio` on media (CLS);
  interactive cells below `24px`; decorative images with no empty `alt`.

### Card collection

- **Use-when**: heterogeneous objects with image + title + a few fields and
  one or two per-item actions.
- **Avoid-when**: a wall of comparable rows — that is a table. Do not pick
  cards just because they look modern.
- **Mechanism**: each card is a self-contained unit; one clear primary
  target (the whole card may be the link, with nested actions handled so they
  don't nest interactive controls illegally). **Equal height across a row**:
  peer cards in the same row share one height so their top *and* bottom edges
  resolve on the same line — the row then reads as one group (Gestalt
  similarity + continuity). Make each card a direct grid or flex child and
  keep the default `align-items: stretch` (grid rows and flex rows already
  stretch children to the tallest sibling); do not override a peer row to
  `align-items: flex-start`. When body copy varies in length, lay the card
  out as `display: flex; flex-direction: column` and push the footer row
  (CTA, price, "Learn more") down with `margin-top: auto`, so those controls
  align across cards even when the text above them does not. Emphasis on one
  card (a recommended plan, a featured tile) is carried by color, border,
  badge, or a deliberate equal-amount scale/elevation — never by letting it
  size raggedly to its own content. **Align the content inside, too**: equal
  card height is not enough — the internal rows must line up across siblings,
  so every card's title, body, and footer sit on shared baselines even when
  one title wraps to two lines and the next to one. Make the card row a grid
  with shared row tracks (e.g. `grid-template-rows: auto 1fr auto` for
  title / body / footer) and let each card adopt them with `display: grid;
  grid-template-rows: subgrid; grid-row: span 3` (subgrid, Baseline since
  2023). The tallest title then sets one shared track, the bodies start on
  one line, and the CTAs land on one baseline across the row. Where subgrid
  is outside the browser/engine scope, fall back to `flex-direction: column`
  + `margin-top: auto` — which pins only the footer, not the title/body
  boundary — or a uniform per-section `min-height`, and name the limitation.
- **Failure mode**: nested interactive elements (a button inside a card that
  is itself a link) producing invalid, unpredictable activation; or peer
  cards in a row sizing to their own content so bottom edges and footer CTAs
  are ragged and the row reads as unfinished rather than as one set.
- **Red flags**: a clickable card wrapping a link/button (nested
  interactives); inconsistent card affordances; using cards where a sortable
  table is what the task wants; peer cards in a row with mismatched heights
  and ragged bottom edges because each sizes to its own content (auto height,
  or `align-items: flex-start` on the row) instead of stretching to a shared
  height; footer CTAs/links not sitting on a common baseline across sibling
  cards; titles, descriptions, or CTAs that don't line up across sibling
  cards because one title wraps to a different number of lines, so each
  card's body and button start at a different height (use subgrid / shared
  row tracks, not only `margin-top: auto`).

### Data table (first-class)

Data tables are a primary web pattern, not an afterthought. On the desktop
web you have density, a pointer, and width — **use them**. Real tabular data
deserves a real `<table>`.

- **Use-when**: records with multiple comparable columns that users scan,
  sort, filter, compare, and act on in bulk — the core surface of most
  admin, analytics, and operational tools.
- **Avoid-when**: a single attribute per item (use a list); purely visual
  content (use a grid). Do **not** force tabular layout on non-tabular data.
- **Mechanism**:
  - Semantic `<table>` with `<thead>`, `<tbody>`, `<th scope="col">` /
    `<th scope="row">`, and a `<caption>`. This gives row/column association
    to assistive tech for free; ARIA `grid` roles are only for editable,
    spreadsheet-like grids with their own keyboard model — most tables are
    plain tables.
  - **Sortable columns**: the header is a `<button>`; the sorted column's
    `<th>` carries `aria-sort="ascending|descending"`; sort state lives in
    the URL so it is shareable and survives reload.
  - **Sticky header**: `position: sticky` on `<thead>` so column labels stay
    while the body scrolls.
  - **Keyboard row navigation**: arrow keys move between rows/cells where the
    table is interactive; Enter opens the row; the row action set is fully
    keyboard reachable (do not hide actions behind hover only — see below).
  - **Row select + bulk actions**: a select-all header checkbox (with an
    indeterminate state) plus per-row checkboxes; selecting rows reveals a
    bulk action bar; selection count is announced via a live region.
  - **Virtualization**: for large sets (thousands of rows), render only
    visible rows (windowing) to keep INP and memory in budget; preserve
    correct semantics and keyboard paging for the virtualized rows.
  - **Density toggle**: offer comfortable/compact row heights; persist the
    choice. Compact density is a desktop advantage, not a defect.
  - **Hover row actions**: per-row actions may appear on hover on pointer
    devices for cleanliness — but they must **also** be reachable via
    keyboard focus and present for touch/assistive-tech users (never
    hover-only).
  - **Responsive collapse to cards**: at narrow widths a table may transform
    into a stacked card-per-row view (section 10) — but this is a deliberate
    transformation at a chosen breakpoint, **not** the default rendering.
- **Exploit desktop density — do not flatten**: the anti-pattern is taking a
  rich desktop table and shipping phone-style one-card-per-row stacks on
  large screens "to be safe". That is responsive flattening: it throws away
  comparison, alignment, sort, and bulk selection — the entire reason a table
  exists. On wide viewports, ship the real table, multi-pane layouts, and
  hover affordances. Collapse to cards **only** below the width where columns
  genuinely stop fitting.
- **Failure mode**: a `<div>`-based fake table (no row/column semantics, no
  `aria-sort`, broken keyboard); or a desktop table pre-flattened into cards
  so users can no longer compare or sort; or virtualization that breaks
  Find-in-page and tab order.
- **Red flags**:
  - Built from `<div>`/`<span>` instead of `<table>` semantics.
  - Sort controls that are not buttons / missing `aria-sort`.
  - Sort/filter/page state not reflected in the URL.
  - Sticky header overlaps and obscures focused rows (fails 2.4.11).
  - Bulk-select with no announced count and no indeterminate "select all".
  - Row actions available only on hover (lost to keyboard and touch).
  - Desktop renders cards by default when a table fits — responsive
    flattening.
  - Virtualized rows that break keyboard order or Find-in-page.

## 4. Actions and primary action placement

Every view should make the one most important action obvious and everything
else quieter. Hierarchy is communicated by weight, not by scattering buttons.

### Button hierarchy

- **Use-when**: any view with actions — i.e. almost all of them.
- **Avoid-when**: never skip the hierarchy; "everything is primary" means
  nothing is.
- **Mechanism**: three tiers.
  - **Primary** (filled, high contrast): the single most likely/important
    action. **One primary action per view.**
  - **Secondary** (outlined or tonal): alternative actions of real weight.
  - **Tertiary** (text/ghost link-like): low-stakes or escape actions
    (Cancel, "Learn more").
  All are real `<button>` (for actions) or `<a>` (for navigation). Hit area
  meets `24px` minimum (`44px` AAA), visible `:focus-visible`, accessible
  name not reliant on color or icon alone.
- **Failure mode**: two or three competing filled buttons so the user can't
  tell what the view wants them to do.
- **Red flags**:
  - More than one primary button in a view.
  - `<div onclick>` used as a button (no role, no keyboard).
  - Icon-only buttons with no accessible name.
  - Disabled primary with no explanation of why or how to enable it.
  - Targets below `24px`.

### Primary action placement

- **Use-when**: deciding where the commit action lives.
- **Avoid-when**: burying the primary action below the fold with no anchor.
- **Mechanism**: in dialogs and forms, the primary action sits at the
  end of the natural reading/tab order (typically bottom-right of an action
  row in left-to-right locales), with secondary/cancel beside it. For **long
  forms**, use a **sticky footer action bar** so Save/Submit is always
  reachable without scrolling to the bottom — and so it does not cover the
  field being edited. There is **no floating circular action button** in this
  web pattern set; primary actions live in the page, toolbar, or sticky
  footer, not as a detached round overlay.
- **Failure mode**: the submit button scrolls off a tall form; or a sticky
  bar covers the last input.
- **Red flags**:
  - Long form whose submit is only reachable at the very bottom.
  - Sticky action bar overlapping inputs or the focused field (2.4.11).
  - Primary action order inconsistent across the product.

### Destructive-action confirmation

- **Use-when**: irreversible or hard-to-undo actions (delete, remove access,
  purge).
- **Avoid-when**: reversible actions — prefer **undo** (a toast with Undo)
  over a confirm dialog, which is faster and less fatiguing.
- **Mechanism**: a modal dialog (section 2) that names exactly what will
  happen, labels its confirm button with the verb ("Delete 3 projects", not
  "OK"), styles it as destructive, and does **not** auto-focus the
  destructive button. For high-stakes deletes, require typing the resource
  name to enable confirm. Provide undo where feasible.
- **Failure mode**: confirm-fatigue dialogs on trivial reversible actions, so
  users reflexively confirm the dangerous ones too.
- **Red flags**: destructive confirm with a generic "OK"; destructive button
  auto-focused; confirming reversible actions that should just be undoable;
  no undo offered anywhere.

## 5. Input and forms

Forms are where users do the real work and where most abandonment happens.
The guidance here follows the GOV.UK Design System and Luke Wroblewski's
*Web Form Design*: ask only what you need, one thing per line, label
everything, and fail gracefully.

### Field construction

- **Use-when**: any data entry.
- **Avoid-when**: collecting data you don't need — every field is a cost.
- **Mechanism**:
  - **Label every field** with a real `<label for>` (or wrapping label).
    Placeholders are **not** labels — they vanish on input and fail contrast.
  - Set `autocomplete` tokens (`name`, `email`, `street-address`,
    `postal-code`, `cc-number`, etc.) so browsers and password managers fill
    correctly — this is WCAG 1.3.5.
  - Set `inputmode` and the right `type` (`email`, `tel`, `url`, `number`,
    `date`) so the correct virtual keyboard and validation apply.
  - Group related fields in `<fieldset><legend>`; mark required fields in
    text, not by color or asterisk alone; describe constraints up front with
    `aria-describedby`, not only after an error.
- **Failure mode**: placeholder-as-label forms that look clean empty and
  become unlabeled and unusable once filled.
- **Red flags**: inputs with no associated label; placeholder used as the
  only label; missing `autocomplete` on personal-data fields; wrong/no
  `type`/`inputmode`; required-ness signaled by color only.

### Validation and errors

- **Use-when**: any form that can be submitted wrong.
- **Avoid-when**: validating aggressively on every keystroke before the user
  has finished a field (premature, noisy errors).
- **Mechanism**:
  - **Inline validation** on blur / on a meaningful change; the error sits
    beside its field, is tied via `aria-describedby`, and the field gets
    `aria-invalid="true"`.
  - On submit, render an **error summary** at the top: a list of every error,
    each linking to its field, with focus moved to the summary so assistive
    tech announces it (the GOV.UK pattern). Messages say what's wrong **and**
    how to fix it.
  - Never clear the user's entered values on error.
- **Failure mode**: a single generic "form has errors" with no field
  associations; or all-red-on-load before the user has typed anything.
- **Red flags**: error text conveyed by color only (no icon/text); errors not
  programmatically tied to fields; no top-of-form summary on multi-error
  submit; focus not managed to the first error; values wiped on error.

### Form length and resumability

- **Use-when**: choosing single-page vs multi-step.
- **Avoid-when**: splitting a short form into needless wizard steps, or
  cramming a genuinely long/branching flow onto one overwhelming page.
- **Mechanism**: prefer **one thing per page/step** for long or complex
  flows (GOV.UK), with a visible step indicator and a real URL per step so
  back/forward and deep-linking work. Use **single-page** for short forms.
  For anything long, provide **save-and-resume** (persist draft state, keyed
  to the user/session) so progress survives interruption. Guard real unsaved
  work with `beforeunload` (section 1), and clear that guard once saved.
- **Failure mode**: a long single-page form with no save; the user loses
  everything to a refresh, a session timeout, or a back-button.
- **Red flags**: multi-step flow with no URL per step (back/forward broken);
  no save-and-resume on a long form; step state lost on reload; needless
  wizardization of a 3-field form.

## 6. Feedback and status

Feedback tells the user that something happened, where, and how important it
is. Match the channel to the message's scope and urgency.

### Decision matrix: which feedback channel

| Channel | Use-when | Avoid-when |
| --- | --- | --- |
| Inline (next to the element) | Feedback about a specific field/row/control | System-wide or page-wide messages |
| Toast / snackbar | Transient confirmation of a completed action; offers Undo | Critical errors that must not be missed; anything needing a decision |
| Banner / alert region | Persistent, page-level status (outage, plan limit, validation summary) | Per-field feedback; throwaway confirmations |
| `aria-live` region | Programmatic announcement of dynamic changes to assistive tech | As a substitute for a visible message — pair it with one |

### Inline feedback

- **Use-when**: the message is about one element (a field, a row, a toggle).
- **Avoid-when**: it's a global condition.
- **Mechanism**: rendered adjacent to the element, associated via
  `aria-describedby`/`aria-invalid`; persists until resolved.
- **Failure mode**: a global toast used for a field error the user must then
  hunt for.
- **Red flags**: field-level feedback delivered only as a transient toast;
  color-only signaling.

### Toast / snackbar

- **Use-when**: confirming a completed, non-critical action — often with
  **Undo**.
- **Avoid-when**: errors or messages that must not be missed, or that require
  a choice (use a banner or dialog).
- **Mechanism**: brief, auto-dismissing, non-modal; never steals focus.
  Announce via an `aria-live="polite"` region (or `role="status"`). If it
  carries an action (Undo), give enough dwell time and a keyboard-reachable
  control; pause auto-dismiss on hover/focus.
- **Failure mode**: a critical error shown as a 3-second toast the user
  misses; or a toast that grabs focus and interrupts typing.
- **Red flags**: critical/blocking info in a toast; toast steals focus;
  auto-dismiss too fast for an action; not announced to assistive tech;
  stacking toasts that cover content.

### Banner / alert

- **Use-when**: persistent page-level status (degraded service, trial
  expiring, account warning) or a form-level error summary.
- **Avoid-when**: transient per-element confirmations.
- **Mechanism**: a visible region near the top of the relevant scope;
  `role="alert"` (assertive) for urgent, `role="status"` (polite) otherwise;
  dismissible only if truly transient.
- **Failure mode**: stacking banners that push content down and cause CLS, or
  an undismissable banner that permanently steals space.
- **Red flags**: assertive `role="alert"` overused for non-urgent info;
  banner injected without reserved space (CLS); critical banner that color
  alone distinguishes.

### `aria-live` regions

- **Use-when**: content updates without a page load (results count, save
  status, validation, async loading done) and a screen reader must hear it.
- **Avoid-when**: as the *only* feedback — always pair with something visible.
- **Mechanism**: a region present in the DOM at load with
  `aria-live="polite"` or `assertive` (or `role="status"`/`role="alert"`);
  update its text content to trigger announcement. Don't toggle the whole
  region in/out — keep it mounted.
- **Failure mode**: announcements that never fire (region added after the
  update) or that flood the user (assertive on every keystroke).
- **Red flags**: dynamic updates with no live region; assertive used where
  polite belongs; region mounted only at update time.

### Optimistic UI and loading

- **Use-when**: high-probability mutations where instant feedback matters and
  rollback is cheap (likes, reorder, toggles).
- **Avoid-when**: irreversible or high-stakes mutations — show real pending
  state instead.
- **Mechanism**: reflect the change immediately, reconcile when the server
  responds, and **roll back visibly with an explanation** on failure.
- **Loading skeletons**: for content fetches, show skeletons that match the
  final layout's dimensions so there is **no layout shift** when real content
  arrives (protects CLS); use them for perceived-performance gains, not as an
  excuse for slow responses. Distinguish skeleton (structure-known) from
  spinner (indeterminate, short waits).
- **Failure mode**: optimistic update that silently diverges from server
  truth on failure; or a skeleton whose size doesn't match real content, so
  arrival shifts the layout.
- **Red flags**: optimistic UI on irreversible actions; failed mutation with
  no rollback/notice; skeletons that don't reserve the real dimensions
  (causes CLS); spinner-only for multi-second content loads.

### Full-page preloader / splash

- **Use-when**: a heavy client-rendered experience (WebGL scene, video-led
  story) cannot paint anything meaningful until assets arrive.
- **Avoid-when**: the page is static HTML/CSS with images and no video. The
  hero is already painted when a preloader would cover it, so the preloader
  only delays LCP; the browser's own progress indicator is the loading state.
- **Mechanism**: when a client asks for one, state the LCP cost in
  milliseconds before building it and offer the alternative: no preloader,
  or a skeleton of the real layout. If it ships, it is inline CSS in the
  first HTML bytes (a JS-injected preloader appears after the browser's own
  blank or spinner frame) and it never outlasts `DOMContentLoaded` plus the
  hero image.
- **Red flags**: preloader on a page under a few MB; minimum display time;
  a preloader that hides content already rendered.

## 7. States

A component is not "done" until every state it can enter is designed. Missing
states are where polish — and accessibility — quietly fail.

### Interaction states (per control)

- **Use-when**: every interactive element.
- **Avoid-when**: never skip; an unstyled state is an undesigned state.
- **Mechanism**: design and implement, at minimum:
  - **default**, **hover** (pointer only — never the sole affordance),
    **`:focus-visible`** (a clearly visible ring meeting `3:1` non-text
    contrast and not obscured — 2.4.11), **active/pressed**, **loading**
    (control shows pending and is non-resubmittable), **disabled** (and a way
    to learn *why*).
  - Distinguish each state by more than color; honor `forced-colors` so states
    survive high-contrast modes.
- **Failure mode**: focus removed (`outline: none`) with no replacement —
  keyboard users navigate blind.
- **Red flags**: `outline: none` without a visible `:focus-visible`
  substitute; hover-only affordances; states distinguished by color alone;
  disabled with no rationale; double-submit possible during loading.

### Content / page states

- **Use-when**: any view that loads data or can be reached in an unusual
  condition.
- **Avoid-when**: never assume the happy path is the only path.
- **Mechanism**: design the full set:
  - **empty** (first-run / no-data): explain what goes here and the action to
    populate it — not a blank panel.
  - **error** (request failed): say what failed and offer retry.
  - **success**: confirm completion.
  - **404** (not found): orient and offer a way back/search.
  - **500** (server error): apologize plainly, preserve nav, offer retry/
    support — never a raw stack trace.
  - **offline**: detect connectivity loss and tell the user; queue or block
    actions clearly. Offline support is **conditional**, not a default: a
    PWA / service worker is justified only when offline use is a real
    requirement. When you do add one, treat offline as **one error state
    among** 404/500/session-expired — handle it consistently with them, not
    as a separate magic layer.
  - **session-expired**: detect expiry, explain it, and re-authenticate
    **without** destroying the user's in-progress work (section 9).
- **Failure mode**: shipping only the loaded state; blank screens on empty,
  white screens on error, lost work on session expiry, raw 500s.
- **Red flags**:
  - Empty state is a blank area with no guidance.
  - Error state with no retry and no explanation.
  - Custom 404/500 missing (raw server pages, stack traces leaked).
  - Service worker shipped as a default with no actual offline requirement.
  - Offline/session-expired handled inconsistently with other error states.
  - Session expiry discards unsaved work.

## 8. Search

Search is a navigation method. The decisions are when results appear, how the
query is suggested, how results are filtered, and how all of that lives in the
URL.

### Instant vs submit

- **Use-when**: **instant** (search-as-you-type) for fast, local, or cheap
  datasets where immediacy aids discovery; **submit** when each query is
  expensive, when the result is a full navigation, or when precision matters
  more than speed.
- **Avoid-when**: instant search that fires an unthrottled request per
  keystroke and races; or submit-only where instant would obviously help.
- **Mechanism**: a real `<form role="search">` with a labeled input
  (`type="search"`). For instant, **debounce** input, cancel stale requests
  (last-write-wins), and announce the result count via an `aria-live` region.
- **Failure mode**: out-of-order responses paint stale results; or every
  keystroke hammers the server, blowing INP.
- **Red flags**: unlabeled search input; instant search with no debounce or
  no stale-request cancellation; result count not announced.

### Autosuggest (combobox)

- **Use-when**: helping users form a query or jump straight to a known item.
- **Avoid-when**: there is nothing meaningful to suggest.
- **Mechanism**: the APG **Combobox** pattern with a listbox popup —
  `role="combobox"` on the input, `aria-expanded`, `aria-controls` to the
  listbox, `aria-activedescendant` to track the highlighted option; Down/Up
  move through options, Enter selects, ESC closes. Suggestions are keyboard
  navigable and announced.
- **Failure mode**: a suggestion dropdown that is mouse-only — keyboard users
  can't reach it, screen readers don't know it exists.
- **Red flags**: suggestions not built on the combobox roles; arrow keys
  don't move through options; `aria-activedescendant`/`aria-expanded`
  missing; dropdown not dismissible with ESC.

### Faceted filters

- **Use-when**: large result sets users narrow by attributes (category,
  price, tags, status).
- **Avoid-when**: small result sets where filtering is overkill.
- **Mechanism**: filters are controls (checkboxes, ranges) whose state is
  **encoded in the URL query string** so the filtered view is shareable,
  bookmarkable, and survives reload/back. Show active filters as removable
  chips and a result count; provide "clear all". On narrow viewports the
  facet panel becomes an off-canvas sheet (section 2).
- **Failure mode**: filter state held only in memory — share the link and the
  recipient sees the unfiltered page; back-button loses the user's facets.
- **Red flags**: filter/sort/page state not in the URL; no result count; no
  visible active-filter chips or "clear all"; facet panel unreachable at
  `320px`.

### Empty / zero-results

- **Use-when**: a query returns nothing.
- **Avoid-when**: never leave it blank.
- **Mechanism**: state plainly that nothing matched **this** query, echo the
  query, and offer next steps — relax a filter, fix spelling, suggested
  queries, or clear filters.
- **Failure mode**: a bare "No results" that doesn't say why or what to do.
- **Red flags**: zero-results with no query echo and no recovery path;
  indistinguishable from a loading or error state.

### Pagination vs infinite scroll vs load-more

- **Use-when**: **pagination** when users need addressable, comparable pages
  (results you cite, jump to, or return to), and for predictable, accessible
  navigation; **load-more** (explicit button) when you want continuous
  browsing without losing the footer or keyboard control; **infinite scroll**
  only for exploratory, low-commitment feeds.
- **Avoid-when**: infinite scroll on anything users must return to, deep-link,
  or where it buries the footer and breaks "back to where I was".
- **Mechanism**: pagination uses real, linkable page URLs (`?page=`),
  `<nav aria-label="Pagination">`, `aria-current` on the current page.
  Load-more is a `<button>` that appends results and moves focus to the first
  new item, announcing the new count. Infinite scroll must still expose a
  keyboard/`load-more` fallback and a reachable footer, and must restore
  position on back.
- **Failure mode**: infinite scroll that loses scroll position on back,
  strands the footer, leaks memory, and is unreachable by keyboard.
- **Red flags**: page state not in the URL; infinite scroll with no
  keyboard/load-more fallback; footer permanently pushed away; scroll
  position not restored on back; focus not moved to newly loaded items.

## 9. Authentication (WebAuthn / OAuth / SSO)

Authentication is a high-stakes flow where small mistakes block users
entirely. Favor strong, low-friction methods and let the browser and password
managers do their job.

### Method decision matrix

| Method | Use-when | Avoid-when |
| --- | --- | --- |
| Passkeys (WebAuthn) | You want phishing-resistant, passwordless sign-in; modern baseline | Environments with no platform/authenticator support and no fallback |
| OAuth / social / SSO | Delegating identity to a provider; enterprise SSO requirements | When users expect a local account and you add only friction |
| Password | Fallback or where mandated | As the *only* option when passkeys are feasible; ever storing weakly |
| OTP / one-time code | Step-up, recovery, or passwordless email/phone codes | As a primary factor where passkeys would be smoother |

### Passkeys / WebAuthn

- **Use-when**: you want phishing-resistant, passwordless auth as the primary
  or first-class path.
- **Avoid-when**: no authenticator is available and you offer no fallback.
- **Mechanism**: WebAuthn creates a public-key credential bound to the origin;
  the browser/authenticator handles the user gesture. Offer passkey creation
  after first sign-in, surface passkey autofill on the sign-in field, and
  **always** keep a fallback (password or OTP) for new or unsupported
  devices.
- **Failure mode**: a passkey-only flow that locks out users on a device with
  no synced credential and no recovery.
- **Red flags**: no fallback path; no account-recovery route; passkey UI not
  keyboard/assistive-tech operable.

### OAuth / SSO

- **Use-when**: delegating to an identity provider, or enterprise SSO.
- **Avoid-when**: it merely adds a step over a simple local account users
  expect.
- **Mechanism**: standard OAuth/OIDC redirect or popup; preserve the user's
  intended destination across the redirect (return to where they were);
  handle provider errors and "account already exists with another method"
  gracefully.
- **Failure mode**: post-login lands on a generic home page, losing the deep
  link the user started from; duplicate-account confusion.
- **Red flags**: intended destination not preserved across redirect; no
  handling of linked-account collisions; provider error dumped raw.

### Password fields

- **Use-when**: fallback or mandated credentials.
- **Avoid-when**: as the only method when passkeys are viable; rolling your
  own crypto.
- **Mechanism**: a real `<input type="password">` with the correct
  autocomplete token: **`autocomplete="current-password"`** on sign-in and
  **`autocomplete="new-password"`** on create/change (so managers offer to
  save/generate correctly). Provide a show/hide toggle with an accessible
  name; never block paste; state rules up front, not only on error.
- **Failure mode**: wrong/missing autocomplete tokens break password-manager
  autofill, pushing users to weak, reused passwords.
- **Red flags**: missing/incorrect `current-password`/`new-password` tokens;
  paste blocked; rules hidden until rejection; password echoed insecurely.

### One-time codes (OTP)

- **Use-when**: email/SMS verification, step-up, or passwordless codes.
- **Avoid-when**: as a primary factor where a passkey would be smoother.
- **Mechanism**: an input with **`autocomplete="one-time-code"`** and
  `inputmode="numeric"` so the platform can offer the code automatically;
  accept paste of the full code across split inputs; show clear expiry and a
  resend control with a cooldown.
- **Failure mode**: split single-digit boxes that reject paste and lack the
  autocomplete token, so the platform can't autofill and users mistype.
- **Red flags**: missing `one-time-code` autocomplete; paste of the full code
  rejected; no resend / no expiry feedback; wrong `inputmode`.

### Session expiry

- **Use-when**: every authenticated app.
- **Avoid-when**: never silently drop a session mid-task.
- **Mechanism**: detect expiry, warn before forced logout where possible, and
  on re-auth **restore the user to their place with their in-progress work
  intact** (re-authenticate inline or in a dialog, then resume) — tie this to
  the `session-expired` content state (section 7).
- **Failure mode**: a 401 mid-form silently redirects to login and discards
  everything the user had typed.
- **Red flags**: session expiry destroys unsaved work; no warning; re-auth
  dumps the user on a generic landing page instead of their task.

## 10. Responsive / breakpoint divergence

Responsive design is not "the same layout, smaller". Across the breakpoint
ladder, patterns should **change behavior deliberately**, not merely reflow
visually. The reference ladder:

`320 / 360 / 480 / 640 / 768 / 1024 / 1280 / 1440 / 1920` px.

- **Use-when**: always — every layout must work across this range, and must
  reflow at `320px` with no loss of content or function (WCAG 1.4.10).
- **Avoid-when**: never treat one viewport as canonical and the rest as
  squeezed copies; never let a layout require horizontal scrolling of content
  at `320px` (data tables are the allowed two-dimensional exception).
- **Mechanism**:
  - **Prefer intrinsic/fluid layout** (`clamp()` type, `minmax()` grids,
    flexbox wrap) so the design adapts continuously; reserve explicit
    breakpoints for **behavioral** changes, not cosmetic nudges.
  - **Container queries** size a component to **its own container**, not the
    viewport — so a card, table, or panel can adapt correctly whether it sits
    in a wide main column or a narrow sidebar. Prefer container queries for
    reusable components; reserve media queries for page-level structure.
  - **Change behavior at thresholds, deliberately:**
    - Persistent **sidebar → off-canvas drawer** when the rail no longer fits
      (section 1, section 2): a modal drawer with focus trap, ESC, scroll
      lock, restore.
    - **Data table → stacked cards** *only* below the width where columns stop
      fitting (section 3) — and exploit full table density above it; do not
      pre-flatten on desktop.
    - **Mega-menu / multi-column nav → disclosure-driven menu** behind a
      hamburger at narrow widths, with full keyboard support.
    - **Multi-pane (list + detail) → single pane with navigation** between
      list and detail on narrow viewports.
    - **Faceted filter rail → off-canvas filter sheet** (section 8).
  - Honor `prefers-reduced-motion` for any transition introduced at these
    transitions; keep targets at `24px`+ at every width; keep the `65ch`
    measure by capping content width, not by shrinking type below `16px`.
- **Failure mode**: a desktop layout that merely squashes — a sidebar that
  overlaps content, a table that forces horizontal scrolling of the whole
  page, a mega-menu unreachable on narrow widths, a multi-pane view crushed
  into an unusable double-scroll. Content or function is lost at `320px`.
- **Red flags**:
  - Content (other than a data table) requires horizontal scroll at `320px`
    (fails 1.4.10).
  - Patterns reflow visually but keep desktop-only behaviors (hover-only
    actions, sidebar overlap) at narrow widths.
  - Sidebar/table/nav don't transform at their thresholds — they just shrink.
  - Reusable components keyed to viewport width instead of container width,
    so they break inside a narrow column.
  - Type shrinks below `16px` or measure blows past `~65ch` to "make it fit".
  - Desktop pre-flattened to phone-style cards (responsive flattening).
  - Breakpoint transitions animate without honoring `prefers-reduced-motion`.
