# Visual review fixture: Billing dashboard with dense invoices data table (desktop 1440px)

Synthetic fixture only. This file is a text stand-in for a screenshot or Figma frame. It exists to calibrate Mode D visual reviews: a strong reviewer reading only the prose below should surface the issues in `## Expected critique` and avoid the claims in `## Prohibited critique`. Do not claim anything about pixels, rendered output, or runtime behavior that is not stated here.

## Review setup

- Artifact type: static description of one rendered screen plus a second viewport note.
- Product: "Ledgerline", a B2B invoicing/billing web app. The screen is the **Invoices** index inside an authenticated app shell.
- Primary user task: scan a high-volume invoice list, sort and filter it, multi-select rows, and run bulk actions (send reminder, mark paid, export).
- What the reviewer is given: this fixture only. No live DOM, no design tokens file, no contrast audit output, no axe report.
- Review mode: Mode D (synthetic visual review). Score against the 8 design-quality dimensions; cite WCAG 2.2 success criteria by number and Nielsen heuristics by name.

## Page description

A desktop web app at 1440px wide. Fixed left sidebar navigation (240px) holds the primary nav; a top bar (64px tall) spans the remaining width with global search, a notifications bell, and an account menu. The main content region is a billing dashboard whose centerpiece is a dense, sortable **invoices data table** showing 50 rows per page out of 3,120 total.

Above the table sits a summary strip of four KPI stat cards (Outstanding, Overdue, Paid this month, Draft). Below the stat cards is a toolbar: a search input, three filter dropdowns (Status, Customer, Date range), a density toggle, and a "Columns" button. When one or more rows are selected, a bulk-action bar replaces the toolbar caption area and shows the selection count plus action buttons.

The table has a sticky header row. Columns: a select-all checkbox, Invoice # (monospace), Customer, Status (pill), Issued date, Due date, Amount (right-aligned, tabular numerals), and a trailing actions cell (kebab menu). The footer of the table holds pagination (Prev / page numbers / Next) and a "rows per page" selector. There is no global page `<footer>` landmark below the app shell.

The 390px mobile-web viewport is described in `## Viewport specs` so the reviewer can reason about reflow, but the primary artifact under review is the 1440px desktop screen.

## Viewport specs

Desktop (primary artifact):
- Viewport width 1440px; app shell uses a fixed 240px sidebar + fluid main region.
- Main content max width 1200px, left-aligned in the fluid region with 32px gutters; this leaves a wide empty band on the right at 1440px.
- 12-column grid inside the content region, 24px column gap.
- Stat cards: 4 across, each spanning 3 columns, 16px internal padding, 24px gap between cards.
- Data table spans the full 12 columns (1136px usable). Default row height 44px in "comfortable" density; 32px in "compact" density.
- Sidebar nav items: 40px tall rows, 16px horizontal padding.

Mobile-web (secondary, reflow note only):
- Viewport width 390px. Sidebar collapses behind a hamburger menu in the top bar.
- The data table is set to `overflow-x: auto` inside a 390px container; the table keeps its intrinsic ~1136px width, so it scrolls horizontally. The sticky header remains sticky vertically.
- Stat cards stack 1-per-row.
- Reflow target per WCAG 1.4.10 is 320px; this fixture only describes behavior down to 390px and does not state what happens at 320px.

## Visible hierarchy

1. h1 "Invoices" (top of main content, 28px).
2. KPI stat strip: four cards, each with a small caps label and a large number. The label and number are the same hue at different lightness; "Overdue" card uses red text for its number.
3. Toolbar (search + filters + density + columns).
4. Data table (the visual and functional centerpiece; ~70% of vertical space).
5. Table footer: pagination + rows-per-page.

The four stat-card numbers (32px each) compete with the h1 (28px) for first fixation; the largest type on the screen is in the stat cards, not the page title, so the eye lands on "Outstanding $482,910" before "Invoices".

## Components

- **App shell**: fixed sidebar (`<nav aria-label="Primary">`) + top bar. Sidebar links are `<a>` with an active state. Top bar search is an `<input type="search">`.
- **KPI stat cards**: static `<div>` cards; not interactive, not links.
- **Toolbar**:
  - Search `<input type="search" inputmode="search">`, 320px wide.
  - Status / Customer / Date-range filters: custom dropdowns (`<button aria-haspopup="listbox">` + a div popover). They are NOT native `<select>`.
  - Density toggle: a two-option segmented control (Comfortable / Compact).
  - "Columns" button opens a popover of column checkboxes.
- **Data table**: `<table>` with `<thead>` sticky, `<tbody>` of 50 `<tr>`. Header sort controls are `<button>` inside `<th>` with `aria-sort` on the active column. Row checkboxes are native `<input type="checkbox">`. Status pills are colored `<span>` (Paid green, Overdue red, Draft gray, Sent blue). Trailing kebab is a `<button aria-haspopup="menu">` opening a menu.
- **Bulk-action bar**: appears on selection; shows "N selected" + buttons (Send reminder, Mark paid, Export, Clear). Rendered in place of the toolbar's left caption; it is a visual swap, and the fixture does not state that the selection count is announced to assistive tech.
- **Pagination**: Prev / 1 2 3 … 63 / Next as `<button>`s; current page marked by background color only.
- **Row actions kebab target**: the clickable kebab hit area is stated as 20px x 20px.

## Typography

Font family: "Inter", system-ui fallback. Tabular numerals enabled on the Amount column and stat-card numbers.

- Body / table cell text: 14px (0.875rem), line-height 1.45.
- Table header labels: 12px (0.75rem), uppercase, letter-spacing 0.04em, weight 600.
- h1 "Invoices": 28px (1.75rem), line-height 1.25, weight 700.
- Stat-card label: 11px (0.6875rem) uppercase.
- Stat-card number: 32px (2rem), weight 700, line-height 1.2.
- Status pill text: 12px (0.75rem), weight 600.
- Secondary metadata (e.g., "Issued 12 days ago" under the date): 12px (0.75rem), color is a light gray.
- Pagination numbers: 13px (0.8125rem).
- Fluid type: none. All sizes are fixed px; no `clamp()` is used, so type does not scale between breakpoints.

Body text minimum: the densest readable content (table cells) is 14px, below the 16px (1rem) body-minimum bar for primary reading content; the 11px stat label and 12px metadata are well below it.

## Color and state notes

Palette and declared contrast pairs (foreground on background):

- Table cell text `#3A3F47` on white `#FFFFFF`: contrast ratio 9.8:1. Passes 1.4.3.
- Table header label `#6B7280` on white `#FFFFFF`: 4.83:1. Passes 1.4.3 for the 12px size.
- Secondary metadata `#9AA1AC` on white `#FFFFFF`: 2.6:1. FAILS 1.4.3 (needs 4.5:1 at 12px).
- Status pill "Sent" — text `#2563EB` on fill `#DBEAFE`: 3.1:1. FAILS 1.4.3 for 12px pill text (needs 4.5:1).
- Status pill "Paid" — text `#15803D` on fill `#DCFCE7`: 4.9:1. Passes.
- Status pill "Overdue" — text `#B91C1C` on fill `#FEE2E2`: 5.2:1. Passes.
- Status is conveyed by the pill's fill color and its text label, so status is not color-alone. Good for 1.4.1.
- Overdue stat-card number uses red `#DC2626` on white as the ONLY signal that the number is "bad"; there is no icon or text qualifier, only color. This is color-alone for that semantic and risks 1.4.1.
- Active sort indicator: the sorted column header changes background tint only (no arrow glyph stated). Sort direction is therefore conveyed by a subtle background, plus `aria-sort` for AT. Sighted-but-non-AT users get a weak visual signal.
- Current pagination page: indicated by a filled background `#2563EB` with white text; no underline, bold, or `aria-current` stated, so the "you are here" cue is background-color-only visually.
- Focus indicator: a 2px outline `#2563EB` at 3:1 against white is stated for buttons and links, but the fixture does NOT state a visible focus style for the native row checkboxes or for the sticky-header sort buttons specifically.
- Row hover: background shifts to `#F3F4F6`. No hover affordance is stated for keyboard users (no equivalent row focus highlight described).

## Interaction states

- Default: as described.
- Hover: rows highlight `#F3F4F6`; buttons darken. Stat cards do not react (correct; they are not interactive).
- Focus-visible: stated for top-bar controls, toolbar buttons, pagination, and links. NOT stated for row checkboxes or sort buttons.
- Active/pressed: buttons show a darker fill.
- Loading: when sorting or paginating, the table body shows a skeleton of 8 shimmer rows; the rest of the page stays put. Stat cards do not re-skeleton on table sort (correct scope). No `aria-live` / `aria-busy` announcement of the loading or completed state is stated.
- Empty: when filters match nothing, the table body shows an empty state ("No invoices match these filters") with a "Clear filters" button. Stated.
- Error: a failed fetch shows an inline error row spanning the table with a "Retry" button. Stated.
- Success: after "Mark paid" bulk action, a toast appears bottom-center ("12 invoices marked paid"). The toast auto-dismisses in 4s; no pause-on-hover or persistent affordance is stated, and it is not stated whether the toast is an `aria-live` region.
- Disabled: bulk-action buttons are disabled (and stated as such) until at least one row is selected.
- Density toggle: switching to "compact" sets row height to 32px and cell padding to 4px vertical.
- Selection: clicking the header checkbox selects all 50 rows on the current page; there is a "Select all 3,120" link offered after select-all. Good.

## Known constraints

- This is a desktop-first internal tool; the 1440px desktop experience is the priority, mobile-web is "supported, not optimized".
- The team intends to keep the table dense (this is a density-rewarding task — exploit desktop density, do not flatten to a phone layout). Compact mode at 32px rows is intentional.
- The 50-rows-per-page choice with server pagination is intentional; virtualization is out of scope this iteration.
- The right-side empty band at 1440px (content capped at 1200px) is a known layout decision and is acceptable as a deliberate max-width, though the reviewer may comment on whether the table specifically should be allowed to widen.

## Expected critique

A strong reviewer SHOULD surface these, with severity:

1. **Table cell text is 14px, below the 16px body minimum** for primary reading content; combined with 12px/11px metadata, the densest text is small. Flag against the body-min bar and WCAG 1.4.4 (resize) headroom. Severity 2. (Defensible as intentional density, so not a 3.)
2. **Secondary metadata `#9AA1AC` on white at 2.6:1 fails WCAG 1.4.3** (needs 4.5:1 at 12px). Severity 3.
3. **"Sent" status pill `#2563EB` on `#DBEAFE` at 3.1:1 fails WCAG 1.4.3** for 12px text. Severity 3.
4. **Overdue stat-card number relies on color alone** (red, no icon/text qualifier) to signal "bad" — WCAG 1.4.1 risk. Severity 2.
5. **Active sort and current-page are conveyed by background tint / fill color only** with no glyph, underline, or `aria-current` stated for the page indicator — weak non-AT visual cue and a 1.4.1 use-of-color concern; also `aria-current="page"` missing for pagination. Severity 2.
6. **No visible focus style stated for row checkboxes and sticky-header sort buttons** — WCAG 2.4.7 / 2.4.11 (focus not obscured) gap, especially since the sticky header could overlap focused content while scrolling. Severity 3.
7. **Kebab row-action target is 20px x 20px, below the 24px minimum** of WCAG 2.5.8 (target size minimum). Severity 3.
8. **Async table updates (sort, paginate, bulk action) have no `aria-live`/`aria-busy` announcement** and the selection-count swap is not stated as announced — screen-reader users get silent state changes (4.1.3 status messages). Severity 3.
9. **Attention path is inverted**: the largest type on screen is the stat-card numbers (32px) over the h1 (28px), pulling first fixation to "Outstanding" rather than the page title/table — hierarchy critique (Nielsen: match between system and the real world; visual hierarchy). Severity 1-2.
10. **No `clamp()` / fluid type**: fixed px sizes mean type does not scale across the breakpoint ladder; note as a production-readiness / typography-craft gap, not a hard failure. Severity 1.
11. **Toast success message** auto-dismisses in 4s with no pause/persist and unstated `aria-live` — possible 2.2.1 (timing adjustable) / 4.1.3 concern for confirming a state-changing bulk action. Severity 2.
12. **Missing global `<footer>` landmark** below the app shell — minor landmark/semantics gap. Severity 1.

## Prohibited critique

A reviewer must NOT make these claims from this text alone:

- Do not claim the status is conveyed by color alone — the pills carry a text label; 1.4.1 is satisfied for status pills (only the Overdue stat-card NUMBER is color-alone).
- Do not claim table cell text fails contrast — `#3A3F47` on white is 9.8:1 and passes.
- Do not claim the table lacks a sticky header or that it is unsortable — both are stated present (`aria-sort`, sticky `<thead>`).
- Do not claim there is no empty or error state — both are explicitly stated.
- Do not claim there is no keyboard support for sorting — sort controls are `<button>`s with `aria-sort`; operability is present even though their focus *style* is unstated.
- Do not claim a corner-anchored circular overlay action button exists — there is none; actions live in a toolbar and bulk-action bar.
- Do not invent specific INP/LCP/CLS millisecond numbers, font-file weights, or bundle sizes — no performance telemetry is provided here.
- Do not claim the 1440px right-side empty band is a bug — it is a stated deliberate max-width decision (you may still argue the table should widen, but not call it broken).
- Do not claim reflow fails at 320px — this fixture only describes 390px behavior and does not state the 320px result; treat 320px as unverified, not failed.
- Do not assert exact pixel positions, z-index values, or animation easing curves — none are given.

## Severity expectations

Nielsen 0-4 severity scale (0 = not a problem, 1 = cosmetic, 2 = minor, 3 = major, 4 = catastrophe):

- Metadata contrast fail (2.6:1), "Sent" pill contrast fail (3.1:1), 20px kebab target, missing focus on checkboxes/sort buttons, silent async/status-message gap: **3 (major)** — real barriers for low-vision and AT users on a data-heavy screen.
- 14px body text below minimum, color-alone overdue number, sort/page color-only cue, toast timing: **2 (minor)** — defensible-but-should-fix.
- Inverted type-size hierarchy: **2** trending **1** depending on whether the stat strip is judged a deliberate focal point.
- No fluid type, missing `<footer>` landmark: **1 (cosmetic)**.
- No issue here rises to **4 (catastrophe)**: the screen is operable, has empty/error/loading states, and most content passes contrast.

## Rubric score expectation

Scores are per the 8 design-quality dimensions (1-5), with an overall read.

- Attention path & hierarchy: **3** (inverted type sizing pulls focus off the table/title; otherwise clean).
- Composition & spacing: **4** (12-col grid, consistent 4px-based spacing, deliberate max-width; minor: wide right band).
- Typography craft: **3** (clean scale and tabular numerals, but sub-16px body, no fluid type, tiny 11px label).
- Color/state & contrast: **2** (multiple 1.4.3 fails and color-alone cues drag this down).
- Density & rhythm: **4** (density is appropriate and rewarded by the task; compact mode is a real asset).
- Interaction polish & motion: **3** (good empty/error/loading/skeleton coverage; gaps in focus styling, status announcements, toast timing).
- Context & brand fit: **4** (reads as a credible, restrained B2B billing tool).
- Production readiness: **3** (semantic table, real states, but accessibility fails and missing announcements block a clean handoff).

Expected current overall: **3 / 5** (strong skeleton, accessibility and contrast gaps keep it from shipping clean).
Projected after addressing the Severity-3 items (contrast fixes, 24px targets, focus styles, `aria-live` / `aria-current`): **4 / 5** (strong and shippable).

Synthetic fixture only — these scores are the calibration target for Mode D reviews of this fixture, not a claim about any real product.
