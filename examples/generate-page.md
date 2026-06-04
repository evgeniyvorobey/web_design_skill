# Worked example: Generate web page concept (Mode A)

## Example prompt

```text
Use the web-design-skill.

Design a web page concept for a "Project overview" page in a SaaS project-management web app.

Inputs:
- User goal: understand a project's status at a glance and act on what is blocked
- Breakpoints: desktop-first, must work down to 320px
- Browsers: evergreen Chromium/WebKit/Gecko
- Audience: project managers and contributors, frequent return users
- Constraints: dense status data, keyboard-operable, existing design-system tokens, accessibility-sensitive
```

## Example output

```md
Mode: Generate web page concept
Responsive/breakpoint scope: Desktop-first, working down to 320px (mobile-web), tablet, wide
Browser/engine scope: Evergreen Chromium / WebKit / Gecko
Assumptions:
- The user is authenticated and already inside a selected project.
- "Blocked" status is computed server-side; this page reads it, it does not edit workflow rules.
- The design system provides table, badge, button, and avatar components with tokens.

## Page goal
Let a returning PM grasp project health in one glance and jump straight to whatever is blocked or overdue.

## Primary user task
Find what needs attention now and act on it (open the blocked item, reassign, or unblock).

## Information hierarchy
1. Project name + health summary (on-track / at-risk / blocked) — first glance
2. Blocked and overdue items — the action zone
3. Progress by milestone and recent activity
4. Team and supporting metadata

## Recommended layout structure
- Header / global nav: project switcher, breadcrumb (Workspace › Project), primary action "New task"
- Above-the-fold summary band: health status, % complete, due date, owner
- Main content (desktop two-column): left = "Needs attention" list (blocked/overdue); right = milestone progress
- Secondary: recent activity feed and team panel below the fold
- Footer: help, keyboard-shortcuts link

## Suggested components
- Status badge (semantic color + text + icon) — non-color-dependent health
- Data table for "Needs attention" with sortable columns and row actions — exploits desktop density
- Milestone progress bars with labels — quick scan of completion
- Avatar group for assignees — recognition over recall

## Interaction notes
- Row hover reveals quick actions (open, reassign); the same actions are reachable by keyboard via a row menu button.
- Sorting and filtering update the URL query so a filtered view is shareable and survives back/forward.
- Optimistic UI on "reassign" with an undo toast; revert on failure.

## Empty / loading / error states
- Empty: "No blocked items — nice." with a link to all tasks, not a dead end.
- Loading: skeleton rows for the table and summary band within ~100ms.
- Error: inline panel with retry if the status service fails; preserve any filter state. Plus 404 (project not found) and session-expired re-auth handling.

## Responsive and browser behavior
### Breakpoint behavior
- 320–767 (mobile-web): single column; summary band stacks; the table collapses to status-led cards; nav becomes an off-canvas drawer.
- 768–1023 (tablet): summary band in a row; single main column with the attention list first.
- 1024+ (desktop/wide): two-column layout; full data table with sticky header; whitespace scales up, measure stays capped.
### Browser/engine notes
- Use native `<dialog>` for the reassign modal; it is Baseline across the named engines. Provide a focus-trap fallback for older builds.

## Accessibility considerations
- One h1 (project name); logical heading outline for summary, attention, milestones, activity; landmark regions.
- Full keyboard operability: tab order matches visual order, visible `:focus-visible`, row menus reachable, ESC closes the reassign dialog with focus restored to the trigger; a skip link to main content.
- Status conveyed by text + icon + color (never color alone); contrast ≥ 4.5:1 for text and 3:1 for badges/borders; `aria-live="polite"` announces reassignment results.

## Design quality calibration
- Quality target: 4/5 — strong, shippable; 5/5 needs validated reduced-motion and localization passes.
- Attention path: health summary → blocked/overdue list → act.
- Composition and spacing: 12-col desktop grid, 24px gutters, 16px (1rem) base rhythm, summary band separated by 32px; reading/metadata columns capped ~65ch.
- Typography: role scale with fluid `clamp()`; 16px/1rem body, 1.5 line-height; numeric metrics in a tabular-figures style.
- Color and state: semantic status roles, real dark theme, forced-colors keeps badge borders; hover/focus/active/loading states defined.
- Interaction polish: 150–250ms feedback, optimistic reassign with undo, reduced-motion removes row transitions.
- Production checks: tokens for spacing/color/type; table/badge/dialog components mapped; CWV budget (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1); axe-clean and keyboard-pass expected; 320px reflow verified.

## Rationale for major choices
- A real data table (not cards) on desktop because PMs scan and compare many rows; density is the job here.
- "Needs attention" placed above milestones because acting on blockers beats admiring progress (goal-gradient + task priority).
- URL-encoded filters because returning users share and bookmark views; this respects back/forward (Jakob's Law).

## Alternatives considered
- Kanban board as the overview — rejected because the question is "what's blocked", not "move cards"; a board buries status under columns.
- Cards instead of a table on desktop — rejected because it wastes desktop density and slows row-to-row comparison.
- A single tall feed — rejected because it makes the at-risk items compete with low-priority activity for first glance.

## Next actions
- Confirm the exact "at-risk" computation and whether PMs can override it from this page.
- Validate the table's keyboard row-navigation and reassign dialog focus flow with an axe + keyboard pass.
- Define the dark-theme and forced-colors token values for the status badge set.
```
