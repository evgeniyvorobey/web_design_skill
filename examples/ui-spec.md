# Worked example: Create responsive UI spec (Mode C)

## Example prompt

```text
Use the web-design-skill.

Turn this into a responsive UI spec: an admin "Users" page with a searchable, sortable, selectable
data table and bulk actions.

Inputs:
- User goal: find users, sort/filter, and apply a bulk action (deactivate, change role)
- Breakpoints: desktop-first, usable on mobile-web
- Browsers: evergreen engines
- Constraints: thousands of rows, keyboard power-users, existing design-system tokens, accessibility-sensitive
```

## Example output

```md
Mode: Create responsive UI spec
Responsive/breakpoint scope: Desktop-first, usable down to 320px (mobile-web), tablet, wide
Browser/engine scope: Evergreen Chromium / WebKit / Gecko
Assumptions:
- The list is server-paginated and server-sorted; the client requests pages by URL query.
- Roles are a fixed enum; bulk role change targets a single new role.
- The design system provides table, checkbox, menu, toolbar, and toast components.

## Screen or flow scope
A single admin "Users" page: search + filter toolbar, a virtualized data table with row selection, and a bulk-action bar that appears on selection.

## Structural zones
- Header / global nav: breadcrumb (Admin › Users), page title, "Invite user" primary action
- Toolbar: search input, role filter, status filter, density toggle, column settings
- Main: data table (sticky header) with row checkboxes
- Contextual bulk-action bar: appears above the table when ≥ 1 row is selected
- Footer: pagination + total count

## Components by section
### Toolbar
- Search input (`type=search`, debounced 250ms, query synced to URL)
- Role + status filter menus (multi-select)
- Density toggle (comfortable / compact)

### Table
- Header row with sortable column buttons and a "select all on page" checkbox
- Body rows: checkbox, name + email, role badge, status badge, last-active, row menu
- Bulk-action bar: count, "Change role", "Deactivate", "Clear selection"

## State definitions
- Default: paginated rows
- Hover / focus-visible / active: row highlight; visible focus ring on every interactive cell
- Loading: skeleton rows on first load; inline row spinner during a bulk action
- Empty: "No users match these filters" with a clear-filters link
- Error: toolbar-level error banner with retry; a failed bulk action rolls back optimistic changes
- Success: toast confirming the bulk action with an undo affordance
- Disabled: bulk actions disabled until a selection exists
- System: 403 (insufficient admin rights) and session-expired re-auth

## Behavior rules
- If a sort column is clicked, then update the URL `sort` param and refetch; show the sort direction with an icon + `aria-sort`.
- If "select all on page" is checked, then offer "select all N across pages" as an explicit secondary action.
- If a bulk action is confirmed, then apply optimistically, show a toast with undo, and reconcile on the server response.
- If the viewport is < 768px, then the table collapses to stacked cards and bulk selection moves into a per-card checkbox.

## Content guidance
- Column headers are nouns; the row menu uses verb-first labels ("Deactivate user").
- Empty and error copy name the cause and the next step, never a dead end.
- Destructive labels say what is affected ("Deactivate 4 users").

## Spacing and layout notes
- 12-column desktop grid, 24px gutters; table cell padding 12px vertical / 16px horizontal in comfortable, 8px / 12px in compact.
- Toolbar separated from the table by 16px (1rem); bulk-action bar height 48px; page max width 1440px with fluid margins beyond.
- Spacing from the 4px scale (space-1 = 4px … space-6 = 32px); no ad-hoc gaps.

## Typography rules
- Table body: 14px / 0.875rem, line-height 1.4; column header label: 13px uppercase tracking; page title (h1): fluid `clamp(1.5rem, 1.3rem + 1vw, 2rem)`.
- Numeric/last-active columns use tabular figures; email truncates with a title tooltip, never wraps mid-token.

## Accessibility requirements
- The table uses real `<table>` semantics with `<th scope>` and `aria-sort` on sortable headers.
- Full keyboard operability: arrow-key cell navigation, Space toggles a row checkbox, the row menu opens with Enter and closes on ESC with focus restored; a skip link bypasses the toolbar.
- Selection count and bulk-action results are announced via `aria-live`; status/role badges use text + icon + color, never color alone; contrast ≥ 4.5:1 (text) and 3:1 (badges, focus ring).
- Targets meet 24px minimum (44px on coarse pointers); the density toggle never drops a target below 24px.

## Design quality requirements
- Quality target: 4/5 — dense, operable, shippable; 5/5 adds validated virtualization performance and localization.
- Attention path: search/filter → scan rows → select → bulk act.
- Composition and spacing: sticky header, aligned columns, consistent 4px rhythm, capped page width.
- Typography: tabular figures, truncation rules, role-based header style.
- Color and state: semantic role/status colors, dark theme, forced-colors keeps badge borders and focus ring.
- Interaction polish: optimistic bulk action with undo; 150–250ms feedback; reduced-motion removes row transitions.
- Production checks: tokens for spacing/type/color; table/menu/toast components mapped; CWV budget with INP ≤ 200ms under interaction; axe-clean and keyboard-pass; verified 320px reflow to the card layout.

## Responsive and browser implementation notes
### Breakpoint behavior
- 320–767: table → stacked cards; toolbar filters move into a "Filters" off-canvas sheet; bulk bar sticks to the bottom.
- 768–1023: table with horizontal scroll for overflow columns and a frozen first column.
- 1024+: full table, sticky header, density toggle enabled; virtualization for large pages.
### Browser/engine notes
- Use CSS `position: sticky` for the header (Baseline); test sticky + virtualization scroll in WebKit. Provide a non-virtualized fallback if `content-visibility` is unavailable.

## Key decision tradeoffs
- A real data table chosen over a card grid because admins compare and sort many rows; cards lose column alignment and slow scanning.
- Server pagination chosen over infinite scroll because admins need stable, shareable, deep-linkable pages and predictable counts.
- Optimistic bulk actions chosen over a blocking modal-per-action because throughput matters; an undo toast covers mistakes.

## Next actions
- Confirm the "select all across pages" semantics and the server's bulk-action limits.
- Verify virtualized-table keyboard navigation and `aria-sort` announcements with a screen reader.
- Define compact-density token values and the frozen-first-column behavior on tablet.
```
