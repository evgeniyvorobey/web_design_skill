# Web Apps And Dashboards Domain Pack

Synthetic calibration material for the web-design-skill. This pack shapes hierarchy, trust language, state coverage, responsive and browser behavior, and handoff checks for dense, data-driven web applications: analytics dashboards, admin consoles, observability views, CRMs, internal tools, and multi-pane operator surfaces. These are recommendations, not validation of any real product.

## When To Use

Reach for this pack when the surface is an authenticated, task-oriented web application rather than a marketing page. Signals that you are in dashboard territory:

- The primary content is **data the user returns to repeatedly**: metrics, tables, time series, queues, logs, records. Reading and acting beats first-impression persuasion.
- Density is a feature, not a defect. A power user on a 1440px or 1920px viewport wants to see 40 rows, three panes, and a filter rail at once, not a phone layout stretched wide.
- The user is **keyboard-resident**: they sort, filter, select ranges, trigger bulk actions, and navigate with shortcuts dozens of times per session. Mouse-only flows are a tax.
- Actions have **consequences and audit trails**: editing a record, deleting rows, changing a billing plan, deploying, or exporting regulated data.
- Sessions are long and stateful: filter state, sort, pagination, selected tabs, and split-pane sizes should survive reload and be shareable by URL.

Do not use this pack for landing pages, content marketing, blogs, or one-shot conversion funnels. If the job is "convince a stranger in 8 seconds," use the marketing pack instead. A dashboard's job is "let a returning expert get work done in 8 seconds."

## Primary User Jobs

Design the surface around these recurring jobs. Each should be reachable without a full-page reload.

1. **Scan for anomalies.** "Is anything wrong right now?" The user wants the worst or most-changed thing surfaced first: a red KPI, a spiking line, an overflowing queue. Hierarchy must answer this before the user reads a single label.
2. **Drill from summary to detail.** KPI tile to filtered table to single record. Each step keeps context (the filter that got them here) and is back-navigable via the browser Back button and breadcrumbs.
3. **Slice and filter.** Date range, segment, status, owner, free-text search. Filters compose, render in the URL as shareable state, and show an explicit "X active filters" affordance with one-click clear.
4. **Triage in bulk.** Select a range of rows (Shift-click, Shift-Arrow, header "select all on page" vs "select all matching"), then apply a bulk action: assign, resolve, export, delete. Show the count and a confirmation for destructive bulk ops.
5. **Edit a record in place.** Inline edit, side-sheet edit, or full detail route. Optimistic UI where safe; explicit save where money or permissions are involved.
6. **Export and report.** CSV export, scheduled reports, "copy link to this view." Long exports run async with progress and a notification, never a frozen tab.
7. **Configure and administer.** Settings, roles, integrations, API keys. Lower-frequency but high-consequence; favor clarity and confirmation over speed.

## Trust And Safety Risks

Dashboards carry operational and financial weight. The interface itself is a risk surface.

- **Stale data read as live.** A chart that silently shows cached numbers invites bad decisions. Always stamp freshness ("Updated 2 min ago" via `<time datetime>`), and degrade visibly when a fetch fails rather than showing old numbers as if current.
- **Destructive actions one click away.** Delete, archive, revoke, and "select all matching" (which may touch 50,000 rows, not the 25 on screen) need a confirmation that names the scope and count, plus undo where feasible. Never put a destructive control adjacent to a frequent one without differentiation.
- **Wrong-scope edits.** In multi-tenant or multi-environment tools, a clear, persistent environment/tenant indicator (and a guard on production actions) prevents the "I edited prod thinking it was staging" class of incident.
- **Number ambiguity.** Currency, timezone, units, and rounding must be unambiguous. Show the timezone on timestamps; label currency; never let a chart axis start at a non-zero baseline without saying so.
- **Permission leakage.** Hide or disable what a role cannot do, but also enforce server-side; a disabled button is UX, not security. Explain *why* a control is disabled ("Requires Admin role").
- **Color as the only signal.** Red/green status alone fails WCAG 1.4.1 and colorblind users. Pair color with an icon, label, or shape.

State plainly in copy what an action will do, to how many items, and whether it can be undone. Trust here is built by precise scope language, not reassurance adjectives.

## Common Web Surfaces

- **KPI / metric tile row.** 3 to 6 cards, value + delta + sparkline + trend direction. Container queries let a tile reflow its sparkline below the number when narrow.
- **Data table.** The centerpiece. Sortable columns, sticky header (and often sticky first column), keyboard row navigation, row selection with checkboxes, bulk-action toolbar that appears on selection, column show/hide and reorder, density toggle (comfortable 48px / compact 36px / condensed 32px row height), pagination or virtualization for large sets, and a responsive collapse strategy below 768px.
- **Charts and time series.** Line, area, bar, and stacked views with a legend, hover tooltip (with keyboard/focus equivalent), brush-to-zoom, and an accessible data-table fallback behind a toggle.
- **Filter rail / filter bar.** Faceted filters, date-range picker, saved views/segments. Collapsible to an off-canvas side-sheet on tablet and below.
- **Detail side-sheet / split pane.** Master-detail: list on the left, record on the right; or a side-sheet that slides in over the table. Resizable splitter with keyboard support.
- **Command palette.** Cmd/Ctrl-K to jump to any view, run an action, or search records. The keyboard power-user's front door.
- **Global chrome.** Top bar (environment, account, notifications), collapsible left sidebar nav, breadcrumb trail, and an inline notification/toast region.

## Hierarchy Guidance

The eye should land on **status, then the thing that changed, then the action**. Concretely:

- **One h1 per view** naming the dashboard or record; never skip heading levels. KPI tiles are typically an unordered list of labeled figures or h2-level regions, not a separate heading each.
- **Surface the exception.** Sort the table or order the tiles so the anomaly is top-left in the LTR reading path. A queue dashboard leads with "23 overdue," not an alphabetical list.
- **Quiet the chrome.** Navigation, filters, and toolbars are persistent furniture; render them in lower-contrast neutrals so the data carries the strongest contrast. The brightest ink belongs to live values and primary actions.
- **One primary action per region.** A single filled primary button (e.g., "Create"), secondary/tertiary actions as outline or ghost. No two competing primaries in the same toolbar.
- **Density with rhythm.** Use the 4px spacing scale (4, 8, 12, 16, 24, 32, 48, 64). Tighten *within* a table row to 8px gutters while keeping 24-32px between major regions so the page still has air. Right-align numerics and use tabular figures (`font-variant-numeric: tabular-nums`) so columns scan vertically.
- **Type scale.** 16px (1rem) body minimum even in compact density; labels and table cells no smaller than 13-14px and only when contrast and spacing compensate. Fluid headings via `clamp(1.25rem, 1rem + 1vw, 1.75rem)`. Body line-height 1.5; tighten table-cell line-height to ~1.35 for density. Keep any prose column near 65ch.
- **Color encodes state, never identity alone.** Reserve saturated hues for status (success/warning/error/info) and always pair with text or icon.

## State And Recovery Requirements

Every data surface ships these states. Missing states are the most common dashboard defect.

- **Loading.** Skeleton rows/tiles that match final layout to keep CLS <= 0.1; reserve table height with `min-height` so the toolbar does not jump. Use `aria-busy="true"` on the region. Avoid spinner-only for content areas.
- **Empty (first-run).** "No data yet" with the reason and a next step ("Connect a source"), not a blank grid. Distinguish from filtered-empty.
- **Filtered-empty.** "No results match these filters" with a one-click "Clear filters" and an echo of the active filters so the user understands why.
- **Partial / degraded.** Some panels load, one fails: show a per-panel error with retry, not a whole-page failure. Stamp which data is stale.
- **Error.** Inline, scoped, actionable: what failed, a retry button, and a correlation/request ID to quote in support. Announce via `role="alert"` / `aria-live="assertive"`.
- **Success / confirmation.** Toast or inline confirmation naming the result and count ("Resolved 12 alerts"); offer **undo** for reversible bulk actions for ~5-10s.
- **Disabled.** Visibly distinct (>= 3:1 against background per 1.4.11) with an explanation on hover/focus and via `aria-disabled` semantics.
- **Optimistic + rollback.** When applying optimistic updates, reconcile on server response and roll back visibly with an error toast if it fails.
- **App-level fallbacks.** 404 (unknown route/record), 403 (no permission, with who to ask), 500 (with request ID), **session-expired** (re-auth without losing in-progress edits), and **offline** (banner via the `online`/`offline` events, queue or block writes). Long async jobs report progress and survive navigation.

## Accessibility Notes

Target WCAG 2.2 AA across the surface.

- **Operable by keyboard (2.1.1, 2.4.3).** Logical tab order; no keyboard traps. Tables support arrow-key cell/row navigation (APG grid pattern), Home/End, Page Up/Down; row selection via Space; Shift-Arrow to extend. A skip link jumps past nav to `main`.
- **Visible focus (2.4.7, 2.4.11).** `:focus-visible` rings with >= 3:1 contrast (1.4.11) and at least 2px offset; ensure the ring is never clipped by sticky headers or overflow containers (2.4.11 focus not obscured).
- **Focus management.** On route change move focus to the new view's h1 or a heading; for side-sheets and dialogs use a focus trap, ESC to close, scroll-lock, and restore focus to the trigger. Prefer native `<dialog>`.
- **Semantics and landmarks.** `header`/`nav`/`main`/`footer`; data tables use real `<table>`/`<th scope>`/`<caption>`, not div grids, unless implementing the ARIA grid pattern deliberately. Sortable headers expose `aria-sort`.
- **Live regions (4.1.3).** Async results, save confirmations, and row-count changes after filtering announce via `aria-live="polite"`; errors via `assertive`.
- **Contrast and color (1.4.3, 1.4.11, 1.4.1).** 4.5:1 text, 3:1 large text and non-text/UI; status never by color alone, pair with icon/label/text.
- **Reflow and zoom (1.4.10, 1.4.4, 1.4.12).** Usable at 320px width with no loss of content (tables collapse, not horizontal-scroll-only); usable at 200% zoom; survive the text-spacing override.
- **Targets (2.5.8).** Interactive controls (sort handles, row checkboxes, icon buttons) >= 24x24px hit area, with spacing; 44px is the AAA (2.5.5) comfort target for touch.
- **Forced colors.** Test the `forced-colors: active` / Windows High Contrast mode: do not convey state purely via `background-color`; keep borders and focus visible.

## Responsive And Browser Notes

**Breakpoint behavior (mobile-first min-width ladder):** 320 / 360 / 480 / 640 / 768 / 1024 / 1280 / 1440 / 1920+.

- **320-480 (reflow floor):** Single column. Tables collapse to stacked "cards" (each row becomes a labeled key/value list) or expose only 2-3 priority columns with a detail tap-through. Filters move to an off-canvas side-sheet behind a "Filters (3)" button. KPI tiles stack 1-up or 2-up. No content is lost, only reorganized.
- **640-768 (tablet):** 2-column tile grids; sidebar nav becomes a collapsible drawer; tables show more columns with horizontal scroll *plus* a sticky first column so context is never lost. Filter rail can be a collapsible top bar.
- **1024-1280 (desktop):** Persistent left sidebar, multi-pane master-detail, full table density with all columns, KPI row 4-6 across. This is the design center for a dashboard.
- **1440-1920+ (wide):** Cap page content at ~1440px or use the extra width for a third pane / wider charts rather than ballooning line lengths. Keep any reading column near 65ch; let tables and charts consume the rest. Do not center a narrow column in an ocean of whitespace on operator screens.
- Use **container queries** for components (a KPI tile, a chart card) so they reflow by their own width inside any pane, independent of the viewport. Reserve a 12-column grid for page-level layout.

**Browser and engine considerations:**

- Test current Chromium (Blink), Firefox (Gecko), and Safari (WebKit). `position: sticky` inside scroll containers behaves differently across engines; verify sticky table headers and sticky first columns in WebKit and Gecko specifically.
- `<dialog>` and the Popover API are broadly supported in current engines; provide a focus-trap fallback for older WebKit. `scrollbar-gutter: stable` prevents layout shift when scrollbars appear/disappear (notably between overlay-scrollbar and classic-scrollbar platforms).
- Honor `prefers-reduced-motion`: disable chart animation, row-expand transitions, and auto-scroll for users who request it; keep state changes instant and legible.
- Virtualized tables must keep content reachable to find-in-page expectations and screen readers; announce that results are virtualized and provide a non-virtual export.
- Font loading: `font-display: swap`, preload the primary above-the-fold font, and set fallback metrics (`size-adjust` / `ascent-override`) to avoid CLS as numeric tables reflow. Mind tabular-figure availability in fallback fonts.

## Evidence And Compliance Boundaries

This pack is **synthetic calibration material, not real-product validation.** It encodes defensible defaults for dense web applications; it is not a measurement of any shipped dashboard.

- The guidance is **recommendations, not proof.** Following it does not constitute proof of compliance with WCAG 2.2, nor proof of safety, accuracy, or business performance. Conformance is established by audit against the actual built artifact, not by citing this document.
- Inspiration galleries (Awwwards, Land-book, Mobbin Web) are **never evidence** for usability, accessibility, performance, or compliance. They show surface aesthetics, not measured outcomes. Treat them as mood, not proof.
- Real validation requires testing the running product: automated and manual accessibility audits with assistive technology, field Core Web Vitals (LCP/INP/CLS) from real users, usability sessions with the actual operator persona, and security/permission review of server-side enforcement.
- Numeric and regulatory claims (financial accuracy, data residency, audit logging) are out of scope here and must be verified by the responsible engineering, legal, and compliance functions. This pack cannot and does not certify them.

Where this pack and a verified measurement disagree, the measurement wins.

## Design-Quality Traps

Calibrated against the 8 design-quality dimensions; each trap drops a dimension below the 4/5 shippable bar.

- **Phone-flattening the desktop.** Stretching a single-column small-screen layout to 1920px wastes the density the operator wants. *(density & rhythm)*
- **No exception surfacing.** An alphabetical, undifferentiated table where the on-fire row looks like every other row. *(attention path & hierarchy)*
- **Color-only status.** Green/red dots with no icon or label; fails 1.4.1 and colorblind users. *(color/state & contrast)*
- **Missing states.** Shipping only the happy path; no skeleton, filtered-empty, partial-failure, or session-expired handling. *(production readiness)*
- **Mouse-only tables.** No keyboard row nav, no sort via keyboard, checkboxes too small to hit. *(interaction polish, accessibility)*
- **Layout shift on load.** Tiles and tables that jump as data arrives, blowing the CLS <= 0.1 budget. *(production readiness)*
- **Cramped numerics.** Proportional figures and left-aligned numbers that fail to scan down a column. *(typography craft)*
- **Competing primaries.** Two filled primary buttons per toolbar so nothing reads as the main action. *(attention path & hierarchy)*
- **Decorative chart chrome.** Heavy gridlines, 3D bars, and non-zero baselines that distort the data story. *(composition & spacing, trust)*
- **Generic chrome with no domain voice.** A console that could be any product; labels and empty states with no operator-specific guidance. *(context & brand fit)*

## Handoff Checks

Before this surface is "done," confirm:

- [ ] One h1 per view; heading outline has no skipped levels; landmarks (`header`/`nav`/`main`/`footer`) present.
- [ ] Body text >= 16px; table cells >= 13-14px with sufficient contrast; numerics use `tabular-nums` and right-align.
- [ ] Spacing uses the 4px scale; major regions separated by >= 24px; table density toggle behaves at each level.
- [ ] All states delivered: default, loading (skeleton, no CLS), empty, filtered-empty, partial/degraded, error (with request ID), success (+undo for bulk), disabled, plus 404 / 403 / 500 / session-expired / offline.
- [ ] Table is keyboard-operable (arrow nav, Space select, Shift-extend, sort via keyboard) and sortable headers expose `aria-sort`.
- [ ] `:focus-visible` ring >= 3:1, never clipped by sticky headers (2.4.11); focus moves to heading on route change; dialogs trap focus, ESC closes, focus restores.
- [ ] Filter/sort/pagination/selected-tab state is in the URL and survives reload; browser Back/Forward and scroll restoration work; `beforeunload` guards unsaved edits.
- [ ] Status uses icon/label, never color alone (1.4.1); contrast meets 4.5:1 / 3:1 (1.4.3, 1.4.11); usable in forced-colors mode.
- [ ] Reflows usable at 320px with no content loss; works at 200% zoom; passes text spacing (1.4.12).
- [ ] Targets >= 24px (2.5.8); destructive/bulk actions confirm scope and count and offer undo where reversible.
- [ ] Container queries drive component reflow; page grid is 12-col; content capped ~1200-1440px; reading column ~65ch.
- [ ] CWV budgets met (LCP <= 2.5s, INP <= 200ms, CLS <= 0.1); fonts use `font-display: swap` + preload + fallback metrics; media reserve space via `aspect-ratio` or width/height.
- [ ] `prefers-reduced-motion` honored; long async jobs show progress, survive navigation, and notify on completion.
- [ ] Verified in current Chromium, Firefox, and Safari, including sticky headers and `<dialog>`/popover behavior.
