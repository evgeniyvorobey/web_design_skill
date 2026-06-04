# Worked example: Rationale / handoff (Mode F)

## Example prompt

```text
Use the web-design-skill.

Prepare the design rationale and engineering handoff for a primary-navigation redesign:
replacing a hamburger-only nav with a persistent top nav + mega-menu on desktop and an
accessible off-canvas drawer on mobile-web.

Inputs:
- Product: a content-heavy marketing + docs site
- Breakpoints: mobile-web through wide desktop
- Browsers: evergreen engines
- Constraints: many top-level sections, SEO matters, accessibility-sensitive, existing tokens
```

## Example output

```md
Mode: Prepare design rationale / handoff
Responsive/breakpoint scope: Mobile-web (320px) through wide desktop
Browser/engine scope: Evergreen Chromium / WebKit / Gecko
Assumptions:
- The information architecture (top-level sections and children) is already settled.
- Nav links are real `<a>` elements with server-rendered hrefs (SEO + no-JS fallback).
- The design system provides menu, disclosure, and overlay primitives.

## Design objective
Make the site's breadth discoverable on desktop and keep it operable and fast on mobile-web, without hiding primary navigation behind a single hamburger on large screens.

## Target users and context
First-time visitors scanning for the right section, and returning readers jumping to docs — across phones, tablets, and wide monitors, frequently via search-engine deep links.

## Key design decisions
- Persistent top nav on desktop — alternative considered: keep the hamburger everywhere — chosen because hiding primary nav on desktop reduces discoverability and section traffic, and the viewport has room.
- Mega-menu for sections with many children — alternative considered: simple dropdown lists — chosen because grouped, scannable columns fit the breadth and match user expectations for content sites.
- Off-canvas drawer on mobile-web — alternative considered: a full-screen takeover — chosen because the drawer preserves context and is simpler to make focus-safe.

## Pattern choices and why
- Top nav with mega-menu over a sidebar because the content is browse-first and horizontal space is plentiful on desktop.
- Native `<a>` links with a disclosure pattern over a re-implemented ARIA `menubar`, because site navigation is a set of links, not an application menu — the APG advises against forcing menubar semantics on link navigation.
- Off-canvas drawer over an inline accordion on mobile-web because it keeps the page uncluttered and gives a single, trappable focus context.

## Design quality rationale
- Quality target: 4/5 — discoverable, operable, and fast; 5/5 needs validated localization of the mega-menu and a measured CWV pass.
- Mega-menu grouping — mechanism: 12-col alignment, 24px column gutters, 600-weight group headings — so breadth reads as structured columns, not a wall of links.
- Drawer affordance — mechanism: 44px target rows, 16px spacing, `:focus-visible` ring — so it is comfortable on coarse pointers and operable by keyboard.
- Restraint — mechanism: a single brand accent on the active item only, semantic color elsewhere — so the nav supports wayfinding without competing with content.

## Responsive and browser alignment
### Breakpoint behavior
- < 768px: hamburger button toggles the off-canvas drawer; mega-menu content becomes nested disclosures inside the drawer.
- 768–1023px: condensed top nav, mega-menu opens as a single scrollable panel.
- 1024px+: full top nav with multi-column mega-menus on hover-intent and on focus/click; verified 320px reflow on the small end.
### Browser/engine notes
- Open the mega-menu on hover-intent (delay) and on click/focus so it is operable without a pointer; gate any `:has()`-based CSS against Baseline and provide a JS fallback for older builds.

## Accessibility and usability considerations
- Keyboard operability: top-level items are tabbable; a mega-menu opens with Enter/Space and closes on ESC, returning focus to its trigger; the drawer traps focus and restores it on close.
- Hover is never the only way to open a menu — focus and click do too — and a short close-delay prevents accidental dismissal.
- Semantics: `<nav aria-label>`, disclosure buttons with `aria-expanded`/`aria-controls`, `aria-current="page"` on the active link; a skip link bypasses the nav.
- Contrast ≥ 4.5:1 for links and 3:1 for the focus ring and active indicator; the active state uses an underline plus color, not color alone.

## States and edge cases
- Default / hover / focus-visible / active / open / disabled for each nav control.
- Long section names wrap or truncate with a title; very tall mega-menus scroll within a max-height.
- No-JS fallback: links still navigate; the mega-menu degrades to a plain section index page.

## Implementation notes
- Server-render hrefs for SEO and no-JS; hydrate disclosure behavior progressively.
- Manage focus in JS on drawer open/close and on mega-menu open; expose `prefers-reduced-motion` to disable the drawer slide.
- Budget the nav's JS so it does not block LCP; the mega-menu content can be lazy-rendered on first open.

## Open questions
- Should the mega-menu show on hover-intent on desktop, or click-only, for the analytics-heavy audience?
- Does the active-trail indicator need to reflect docs sub-navigation as well as top-level?

## Validation plan / recommended testing focus
- Run an axe pass and a full keyboard pass (open/close, focus trap, focus restore) on the drawer and mega-menu.
- Verify 320px reflow and 200% zoom; measure nav JS impact on LCP/INP via Lighthouse.
- Screen-reader test the disclosure `aria-expanded` announcements in two engines.

## Next actions
- Confirm hover-intent vs click-only with a quick analytics-informed decision.
- Build the disclosure primitive and verify focus restoration before wiring the mega-menu content.
- Add the no-JS section-index fallback pages.
```
