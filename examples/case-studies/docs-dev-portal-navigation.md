# Case study: Docs / dev portal navigation that survives deep links and version switches

A bad-to-good calibration fixture for a developer documentation portal: a persistent left sidebar tree, global search, breadcrumbs, and a version switcher. The hard part is not drawing the chrome — it is keeping orientation, scope, and history coherent when a reader lands cold on a deep URL, switches the documented version, and drives the whole thing from the keyboard.

## Prompt

```text
We're building the docs site for our API platform (think hundreds of pages
across Guides, API Reference, SDKs, and Changelog). We have v2 and v3 of the
product live at the same time, plus an unreleased "next" branch.

Design the navigation: the left sidebar that lists all the pages, the search,
the breadcrumbs at the top of each page, and the version switcher. People
arrive mostly from a search engine straight onto a deep page, so they land
without having clicked through the nav. Many of our readers live on the keyboard.

Give me concrete HTML/CSS/ARIA, responsive behavior down to phones, and the
states you'd build. Tell me what's easy to get wrong.
```

## Weak response

```md
Here's a clean docs navigation layout.

**Sidebar**
Put a fixed sidebar on the left, ~280px wide. List the sections (Guides, API
Reference, SDKs, Changelog) with the pages nested under each. Use a `<div>`
for each row and highlight the active page with a blue background. On phones,
hide the sidebar and show a hamburger that slides it in.

```html
<div class="sidebar">
  <div class="group">Guides</div>
  <div class="item active" onclick="go('/guides/auth')">Authentication</div>
  <div class="item" onclick="go('/guides/webhooks')">Webhooks</div>
</div>
```

**Search**
Add a search box at the top. On input, fetch results and show them in a
dropdown below the box. Clicking a result navigates to the page.

**Breadcrumbs**
Show the path at the top: `Guides > Authentication`. Use `>` between levels.

**Version switcher**
A `<select>` in the header with v2 / v3 / next. On change, reload the page
for the chosen version.

**Responsive**
Below 768px, collapse the sidebar behind a hamburger. The search and version
switcher stay in the header.

Use a blue accent for active items so people can see where they are. Keep it
minimal and it'll feel fast.
```

## Why this is weak

- Attention path & hierarchy: a reader arriving on a deep page from a search engine has no idea where they are in a tree of hundreds of pages. The sidebar never auto-expands to the active node or scrolls it into view, so the single most important orientation cue is missing. Active state is a blue background only — that fails WCAG 1.4.1 Use of Color (color is the sole channel) and provides no programmatic "current page" signal.
- Production readiness: rows are `<div onclick>`. They are not focusable, not in the tab order, give no `:focus-visible` ring, are invisible to assistive tech as links, and break Cmd/Ctrl-click, middle-click, and "copy link" — violating 2.1.1 Keyboard and 4.1.2 Name, Role, Value. This is the central defect; everything in a docs portal is a link and must be an `<a href>`.
- Color/state & contrast: "blue accent," "highlight," and "minimal" are asserted with no token values, no contrast ratios, and no non-color state. There is no evidence the active row clears 1.4.3 (4.5:1) or that the active indicator clears 1.4.11 Non-text Contrast (3:1).
- Interaction polish: the search dropdown is a plain div with no combobox semantics — no `role="combobox"`, no `aria-expanded`, no `aria-activedescendant`, no arrow-key traversal, no `aria-live` result count, no Escape to dismiss. It violates 2.1.1 and the WAI-ARIA APG Combobox pattern, and ignores Nielsen's "Visibility of system status."
- Context & brand fit: a native `<select>` version switcher silently reloads "the page for the chosen version." If `/v3/guides/webhooks` does not exist in v2, the reader is dumped on a 404 with no recovery — a "User control and freedom" failure. There is no warning that switching may move them, and no preserved anchor/scroll position.
- Density & rhythm / composition: "~280px" and "768px" are the only numbers. No spacing scale, no measure cap on the content column, no breakpoint ladder, no scroll containment, no sticky behavior for the sidebar or breadcrumbs. The layout cannot actually be built from this.
- Composition & reflow: "hide the sidebar, show a hamburger" is the entire small-screen story. No mention of 1.4.10 Reflow at 320px, focus management when the off-canvas panel opens, scroll lock, Escape, or focus restore — so the drawer is a keyboard trap waiting to happen.

## Strong response

```md
# Docs portal navigation — sidebar, search, breadcrumbs, versioning

## Layout shell and the orientation rule

Three landmarks plus the doc body, mobile-first. The non-negotiable rule that
the weak version misses: **on every page load the sidebar auto-expands the
ancestors of the current page, marks it `aria-current="page"`, and scrolls it
into view.** Deep-link readers must see "you are here" without a click.

Breakpoint ladder (min-width): 320 reflow floor / 360 / 480 / 640 /
768 sidebar becomes persistent / 1024 / 1280 three-column with right-hand
"On this page" / 1440. Spacing scale (px): 4, 8, 12, 16, 24, 32, 48, 64.

```html
<a class="skip-link" href="#doc">Skip to content</a>
<header class="topbar">
  <a class="brand" href="/">Acme&nbsp;Docs</a>
  <!-- combobox search lives here -->
  <div class="version"><!-- version switcher --></div>
</header>

<div class="shell">
  <nav id="sidenav" class="sidenav" aria-label="Documentation">
    <ul class="tree" role="tree">
      <li role="treeitem" aria-expanded="true">
        <a href="/v3/guides/">Guides</a>
        <ul role="group">
          <li role="treeitem">
            <a href="/v3/guides/auth" aria-current="page">Authentication</a>
          </li>
          <li role="treeitem"><a href="/v3/guides/webhooks">Webhooks</a></li>
        </ul>
      </li>
    </ul>
  </nav>

  <main id="doc" class="doc">
    <nav class="crumbs" aria-label="Breadcrumb"><!-- ol below --></nav>
    <article><h1>Authentication</h1><!-- one h1 per page --></article>
  </main>
</div>
```

```css
:root {
  --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-6: 24px;
  --fg: #1b1f24; --muted: #4a5158; --bg: #ffffff;
  --rail: #d7dce1;            /* 3.05:1 on white — clears 1.4.11 */
  --accent: #0b5cff;          /* 5.3:1 on white  — clears 1.4.3  */
  --accent-wash: #eef3ff;
}
.shell { display: grid; grid-template-columns: 1fr; }
.doc { padding: var(--space-6) var(--space-4); }
.doc article { max-width: 70ch; }      /* ~65ch reading measure */
body { font-size: 1rem; line-height: 1.5; color: var(--fg); }
h1 { font-size: clamp(1.75rem, 1.4rem + 1.6vw, 2.5rem); line-height: 1.25; }

@media (min-width: 768px) {
  .shell { grid-template-columns: 18rem minmax(0, 1fr); }
  .sidenav {
    position: sticky; top: 4rem; align-self: start;
    block-size: calc(100dvh - 4rem); overflow: auto; overscroll-behavior: contain;
    border-inline-end: 1px solid var(--rail);
  }
}
@media (min-width: 1280px) {
  .shell { grid-template-columns: 18rem minmax(0, 1fr) 16rem; }  /* + ToC */
}

/* Active row: 3 redundant channels, not color alone (1.4.1) */
.tree a[aria-current="page"] {
  background: var(--accent-wash);
  box-shadow: inset 3px 0 0 var(--accent);   /* left rail bar */
  font-weight: 600;
}
.tree a { display: block; min-block-size: 24px; padding: var(--space-2) var(--space-3); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

@media (forced-colors: active) {
  .tree a[aria-current="page"] { outline: 2px solid LinkText; }
  :focus-visible { outline: 2px solid Highlight; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
```

Every row is a real `<a href>`: Cmd/Ctrl-click, middle-click, and "copy link
address" all work; crawlers and assistive tech see links. `aria-current="page"`
is the programmatic current-page signal; the inset rail bar + weight + wash are
the three visible channels that satisfy 1.4.1.

## Sidebar tree: collapse, keyboard, scroll

- Disclosure triangles are `<button aria-expanded>` siblings of the link (a
  target inside a link is invalid). Min target 24px (2.5.8); 44px at
  `@media (pointer: coarse)` per 2.5.5 AAA.
- Tree keyboard model (WAI-ARIA APG Tree View): Up/Down move between visible
  rows via roving `tabindex`, Right expands or steps in, Left collapses or
  steps to parent, Home/End jump to first/last, Enter activates the link.
- Persist expand/collapse in `localStorage` so a reader's open sections survive
  navigation; always re-expand the active branch on load regardless.
- `scrollIntoView({ block: "nearest" })` on the active row after expansion, but
  only when it is outside the viewport, so deep-link readers see context.

## Search: APG combobox, not a div

```html
<div class="search">
  <label for="q" class="vh">Search docs</label>
  <input id="q" type="search" role="combobox" autocomplete="off"
         aria-expanded="false" aria-controls="q-list"
         aria-activedescendant="" placeholder="Search   /   Ctrl-K" />
  <ul id="q-list" role="listbox" aria-label="Results" hidden></ul>
  <p id="q-count" class="vh" aria-live="polite"></p>
</div>
```

- Global `/` and `Cmd/Ctrl-K` focus the input (a documented dev-portal idiom).
- ArrowDown/Up move `aria-activedescendant` across `role="option"` rows without
  moving DOM focus; Enter follows the highlighted result; Escape clears then
  closes; the input keeps `inputmode="search"`.
- `#q-count` announces "12 results" via `aria-live="polite"` (1.4.1 status,
  Nielsen "Visibility of system status"); a zero-result branch shows an empty
  state with a "Browse Guides" fallback link, never a dead end.
- Debounce 150ms, abort stale `fetch` with `AbortController`, cap the listbox
  height and let it scroll, reserve its box so opening it causes no layout
  shift (CLS budget <= 0.1). Each result row shows section + version chip so
  a reader knows *which* tree the hit lives in.

## Breadcrumbs: ordered, current, truncation-safe

```html
<nav aria-label="Breadcrumb">
  <ol class="crumbs">
    <li><a href="/v3/">v3</a></li>
    <li><a href="/v3/guides/">Guides</a></li>
    <li><a href="/v3/guides/auth" aria-current="page">Authentication</a></li>
  </ol>
</nav>
```

- `<ol>` for real order; the leaf carries `aria-current="page"` and is not a
  link away from itself. The separators are CSS `::before` (`content: "/"`) so
  they are decorative, never read aloud or copied.
- On narrow viewports collapse the middle to a `…` disclosure rather than
  wrapping to three lines; first and current crumb always stay visible.

## Version switcher: a menu, with a safe-landing contract

Not a bare `<select>` that blind-reloads. A `<button aria-haspopup="menu">` +
`role="menu"` (APG Menu Button) whose items are links:

```html
<button id="ver" aria-haspopup="menu" aria-expanded="false">
  v3 <span aria-hidden="true">▾</span>
</button>
<ul role="menu" aria-labelledby="ver" hidden>
  <li role="none"><a role="menuitem" href="/v2/guides/auth">v2 (maintenance)</a></li>
  <li role="none"><a role="menuitem" href="/v3/guides/auth" aria-current="true">v3 (current)</a></li>
  <li role="none"><a role="menuitem" href="/next/guides/auth">next (preview)</a></li>
</ul>
```

- **Equivalent-page contract:** the server resolves the *same logical page* in
  the target version. If `/v2/guides/auth` exists, go there and preserve the
  `#anchor`; if it does not, redirect to the nearest ancestor that does and
  show a dismissible banner — "This page is new in v3; showing the v2 Guides
  index" — so a switch never dumps the reader on a 404 ("User control and
  freedom," "Help users recognize, diagnose, and recover from errors").
- Each version carries a status word (current / maintenance / preview), never
  color alone (1.4.1). A `next (preview)` page renders a persistent notice.
- Menu keyboard model: Arrow keys move between items, Escape closes and
  restores focus to the trigger, focus stays within the menu while open.

## Small-screen off-canvas (1.4.10 Reflow at 320px)

Below 768px the sidebar is an off-canvas panel opened by a labeled
`<button aria-expanded aria-controls="sidenav">` ("Menu") — not an unlabeled
glyph. On open: move focus into the panel, trap focus, lock body scroll
(`overflow: hidden` + `overscroll-behavior`), Escape closes, and on close
**restore focus to the toggle**. At 320px the doc column reflows to one column
with no horizontal scroll; code blocks scroll inside their own box. Verify the
whole portal at 200% zoom (1.4.4) and with a text-spacing override (1.4.12).

## States to build

default · hover · `:focus-visible` · active/`aria-current` · expanded/collapsed
· search-loading (skeleton rows) · search-empty (fallback link) ·
search-error (retry) · version-mismatch banner · offline (cached pages note) ·
404 (search box + "popular pages") · forced-colors.
```

## Why this is stronger

- Production readiness: every navigable element is an `<a href>` (or a real
  `<button>` for disclosure/menu triggers), fixing the core 2.1.1 / 4.1.2
  defect and restoring Cmd-click, middle-click, copy-link, and crawlability —
  the things a docs portal lives or dies on.
- Attention path & hierarchy: the auto-expand + `aria-current="page"` +
  scroll-into-view rule directly serves the brief's "land cold on a deep URL"
  reader; orientation is the product, and it is now guaranteed on load.
- Color/state & contrast: named tokens with stated ratios (`--accent` 5.3:1 for
  1.4.3, `--rail` 3.05:1 for 1.4.11) and a three-channel active state (rail bar
  + weight + wash) satisfy 1.4.1; `forced-colors` and reduced-motion are handled.
- Interaction polish & motion: search is a real APG Combobox with
  `aria-activedescendant`, `aria-live` counts, debounce, `AbortController`, and
  a reserved box for CLS; the version switcher is an APG Menu Button with a
  safe-landing contract that respects "User control and freedom."
- Composition, density & rhythm: explicit breakpoint ladder, 4px spacing scale,
  sticky self-scrolling sidebar with `overscroll-behavior: contain`, a ~65ch
  reading measure, and a three-column desktop layout that exploits width with a
  right-hand "On this page" rather than flattening to a phone layout.
- Context & brand fit: `/` and `Cmd/Ctrl-K` to focus search, per-result section
  + version chips, and version status words are the idioms developer readers
  expect — this lands strong and shippable at the 4/5 target.

This is a SYNTHETIC fixture for calibration; the ratios, tokens, and contract
above are illustrative and have not been validated against any shipping
product — do not treat them as audited numbers.

## Regression checks

- Every sidebar, breadcrumb, search-result, and version-menu row is a real
  `<a href>` (or a `<button>` for disclosure/menu triggers) — never a
  `<div onclick>` — so keyboard (2.1.1), `:focus-visible`, Cmd/Ctrl-click,
  middle-click, "copy link," and crawlers all work.
- On any deep-link load the sidebar auto-expands the active page's ancestors,
  sets `aria-current="page"`, and scrolls the active row into view when it is
  off-screen; the active state uses at least two non-color channels (1.4.1).
- The active indicator and section rails clear the named contrast bars —
  text 4.5:1 (1.4.3) and the rail/border 3:1 (1.4.11) — with the ratios stated,
  not asserted.
- Search exposes `role="combobox"` + `role="listbox"`/`option`,
  `aria-activedescendant` arrow traversal, an `aria-live` result count, Escape
  to dismiss, and a non-dead-end empty state (WAI-ARIA APG Combobox).
- Switching version resolves the equivalent page or redirects to the nearest
  existing ancestor with a dismissible banner — it never lands the reader on a
  404, and it preserves the URL anchor.
- At 320px the layout reflows to one column with no horizontal scroll (1.4.10),
  the off-canvas sidebar traps focus, locks scroll, closes on Escape, and
  restores focus to its toggle; the portal survives 200% zoom (1.4.4) and a
  text-spacing override (1.4.12).
