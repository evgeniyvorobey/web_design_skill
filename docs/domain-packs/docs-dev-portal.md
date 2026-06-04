# Documentation And Developer Portal Domain Pack

A playbook for reference docs, API explorers, search, code samples, and versioned content. Developer portals are read in two modes at once: deep linear learning (guides, tutorials) and high-frequency lookup (signatures, parameters, error codes). The design job is to keep both fast, scannable, and trustworthy across versions and runtimes.

## When To Use

Use this pack when the surface is a place developers go to *do their job* with your product:

- API reference (endpoints, methods, parameters, return shapes, error tables).
- SDK and library docs with installable code samples per language/runtime.
- Conceptual guides, quickstarts, tutorials, and "how-to" recipes.
- Changelogs, migration guides, and versioned/long-term-support documentation.
- Interactive consoles: API explorers, request builders, embedded playgrounds.
- Search-first portals where the landing experience is the search box, not marketing.

Do not use this pack for the marketing site that wraps the docs (use the landing/marketing pack), for in-product onboarding, or for status pages. Those have different trust language and conversion goals.

## Primary User Jobs

Design around these recurring tasks, ranked by frequency:

1. **Lookup under pressure.** A developer mid-task wants one signature, one parameter default, or one error meaning. They arrive from a search engine or in-page search, scan, copy, and leave. Optimize the path from query to copyable answer in under 10 seconds.
2. **Copy a working snippet.** They want a code block they can paste and run, correct for *their* language and *their* version. The copy button and language tab selection are load-bearing UI.
3. **Authenticate and make a first call.** Quickstart success ("hello world returns 200") is the activation metric. Reduce steps between "I have a key" and "I got a response."
4. **Understand a concept once.** Linear reading of a guide. Needs a stable heading outline, "on this page" rail, and prev/next pagination.
5. **Migrate across a version.** Find what changed, what broke, and the exact replacement. Migration guides and changelogs carry this.
6. **Self-rescue from an error.** Paste an error string into search and land on a page that names it and gives the fix.

## Trust And Safety Risks

Developers extend trust slowly and revoke it instantly. The fastest way to lose a docs reader is to show them something that does not run.

- **Stale or wrong samples.** A snippet that 404s, uses a deprecated method, or omits required setup destroys credibility. Version-stamp every example and tie it to a tested source where possible.
- **Version ambiguity.** If the reader cannot tell which version a page describes, every fact is suspect. Always show the active version in the chrome, in the URL (`/v2/...`), and on deprecated pages.
- **Secret leakage in copy paths.** Quickstarts that hardcode keys teach insecure habits. Use placeholders like `YOUR_API_KEY`, never a real-looking token, and warn against committing secrets.
- **Silent breaking changes.** Migration guides that omit a removed field send readers into production failures. Make removals and renames explicit with before/after.
- **Untrustworthy search.** A search that returns marketing pages, the wrong version, or nothing for a known term feels broken. Scope, rank, and filter search by version and section.
- **Destructive console actions.** Embedded API explorers can hit *live* endpoints. Distinguish sandbox from production, confirm writes/deletes, and never auto-send a mutating request.
- **AI-generated answer drift.** If you ship an "ask the docs" assistant, it must cite the source page and version; an unattributed wrong answer is worse than no answer.

## Common Web Surfaces

- **Three-pane reference layout:** left section/version navigation, center content (~65ch reading column), right "On this page" anchor rail.
- **Global search:** command-palette overlay (Cmd/Ctrl-K), instant results, keyboard-navigable, scoped to version.
- **Code blocks:** language tabs, copy button, line highlighting, optional "run" affordance, filename label.
- **API endpoint cards:** method badge (GET/POST/DELETE), path, collapsible parameter tables, response schema, status-code table.
- **Version switcher:** dropdown in the header that re-resolves the current page in the target version (or routes to the nearest equivalent).
- **Tabs/callouts:** Note / Warning / Deprecated admonitions; per-runtime tabbed content (npm/pnpm/yarn, curl/Python/Node).
- **Changelog / migration timeline:** reverse-chronological entries with version anchors and "breaking" labels.
- **Interactive explorer:** request builder with auth field, parameter inputs, live response panel, copy-as-curl.
- **Feedback widget:** "Was this helpful?" with a comment path that does not block the page.

## Hierarchy Guidance

The reading column owns attention; navigation supports it. Build the page outline so a scanner wins before a reader does.

- **One `h1` per page** = the page subject (the method name, the concept). No skipped heading levels; the right rail mirrors the `h2`/`h3` outline exactly.
- **Signature first.** On a reference page, the method signature and a minimal working example appear above the fold, before prose. Lookup users need the shape immediately.
- **Type scale:** body 1rem (16px) minimum, fluid headings via `clamp()` with a `rem` term, e.g. `h1 { font-size: clamp(1.75rem, 1.5rem + 1.2vw, 2.5rem); }`. Body `line-height: 1.5`; headings 1.2–1.35. Code uses a monospace stack at ~0.9375rem with `line-height: 1.55` for dense scanning.
- **Spacing rhythm** on the 4px scale: 8px inside table cells, 16px between paragraphs, 24px above `h3`, 32–48px above `h2`. Code blocks get 16px internal padding and 24px vertical separation so they read as distinct objects.
- **Density where it pays.** Parameter and status-code tables are first-class: dense rows (8–12px vertical padding), sticky table header on long tables, monospace for names/types, a plain-language description column, and a "Required" indicator that is *not color alone* (use a label or asterisk with legend).
- **Persistent wayfinding:** breadcrumb (Section / Page) at top, version in the header, prev/next pagination at the bottom of guides, and the section tree always reflecting the current location (expanded ancestors, marked current item with `aria-current="page"`).
- **De-emphasize chrome.** Navigation and the anchor rail use smaller type and lower contrast than body; the content column carries the strongest hierarchy.

## State And Recovery Requirements

Cover every state a developer can hit, including the ones that only show up in someone else's network conditions.

- **Default / loading:** stream content fast; show skeletons for search results and explorer responses, never a spinner that blocks reading. Reserve space for code blocks and images with `aspect-ratio`/explicit dimensions to keep CLS ≤ 0.1.
- **Empty search:** "No results for *term*" with spelling/synonym suggestions, scope reset ("searching v2 — search all versions?"), and links to top sections. Never a blank panel.
- **Copy feedback:** the copy button confirms with a transient "Copied" label and `aria-live="polite"` announcement; failure (clipboard blocked) falls back to selecting the text.
- **Deprecated page:** a persistent warning banner naming the version it was removed/changed in and a link to the replacement. Do not hide deprecated pages from search; redirect-with-notice is better than a 404 for a bookmarked link.
- **Explorer error states:** surface the real HTTP status, the response body, and a human hint ("401 — check your API key"). Distinguish network failure (offline), auth failure (401/403), validation (400 with field-level messages), and rate limit (429 with retry timing).
- **404 / 410:** a docs-specific not-found page with search, the section tree, and "this may have moved in v3" guidance — not a generic site 404.
- **500 / offline:** if content is served from a cache or service worker, indicate stale-but-readable; otherwise a retry affordance. Session-expired in an authenticated console should preserve the unsent request and re-auth in place.
- **Version mismatch:** if a user lands on a page that does not exist in their pinned version, offer the nearest match rather than dead-ending.

## Accessibility Notes

Target WCAG 2.2 AA across the portal; treat code and tables as the hard cases.

- **Contrast (1.4.3 / 1.4.11):** body text 4.5:1, large text 3:1, and — critically — **syntax-highlighting tokens must each clear 4.5:1** against the code background. Many themes fail on comments and punctuation; verify every token color. UI borders, focus rings, and method badges meet 3:1 (1.4.11).
- **Use of color (1.4.1):** "Required" params, "Breaking" changelog entries, and added/removed diff lines must carry a text label or symbol, not just red/green. Diff blocks use `+`/`−` glyphs and `aria` text, not color alone.
- **Keyboard operability (2.1.1):** the Cmd/Ctrl-K search opens, traps focus, is fully arrow-navigable, and restores focus on close (ESC). Language tabs follow the WAI-ARIA APG Tabs pattern (arrow keys move, `tab` exits). Copy buttons are real `<button>`s, reachable and labeled ("Copy code"). No keyboard trap in the embedded explorer.
- **Focus visibility (2.4.7 / 2.4.11):** a `:focus-visible` ring that is not obscured by the sticky header or anchor rail; use `scroll-margin-top` so anchored headings are not hidden under the sticky top bar.
- **Semantics & landmarks:** `header` / `nav` (labeled "Documentation sections") / `main` / `footer`; the anchor rail is a labeled `nav` with `aria-current="location"` on the in-view heading. Code blocks are `<pre><code>`; tables use real `<th scope>` headers so screen readers announce parameter rows correctly.
- **Skip link** to main content, since the section tree is long. Live regions (`aria-live`) for async search results and explorer responses.
- **Target size (2.5.8):** copy buttons, tab triggers, and version switcher hit at least 24×24px (prefer 44px for the copy button, which is tapped often). Spacing keeps adjacent controls from overlapping targets.
- **Resize & spacing (1.4.4 / 1.4.10 / 1.4.12):** content reflows to a single column at 320px with no horizontal scroll except *inside* code blocks (which may scroll-x); usable at 200% zoom; tolerant of user text-spacing overrides. Respect `prefers-reduced-motion` for tab/accordion transitions and `forced-colors` (Windows High Contrast) so badges, focus, and diff markers stay visible.

## Responsive And Browser Notes

Mobile-first ladder, with the three-pane layout collapsing predictably.

- **320–480px (reflow floor):** single column. Section tree becomes an off-canvas drawer behind a labeled toggle (ESC to close, scroll-lock, focus trap). The right anchor rail collapses into a `<details>` "On this page" disclosure above the content. Code blocks scroll horizontally inside their own container; the rest of the page never does.
- **640–768px (tablet):** content plus a slide-in section drawer; anchor rail still inline/disclosed. Language tabs may overflow into a scrollable tab strip with edge fades.
- **1024px+:** two panes (section tree + content). **1280px+:** full three panes with persistent anchor rail. Cap the reading column near ~65ch even on 1440/1920 wide screens — let the side panels and gutters absorb extra width rather than stretching prose.
- **Container queries** for components (code block, endpoint card) so a card in a narrow embed collapses its language tabs independently of the viewport.
- **Browser/engine considerations:** test `position: sticky` headers and `scroll-margin-top` across Blink (Chrome/Edge), Gecko (Firefox), and WebKit (Safari) — sticky plus anchor-scroll offset behavior differs subtly. The Clipboard API requires a secure context and a user gesture; provide the select-text fallback for older or restricted browsers. Use `:focus-visible` with a fallback so focus rings still appear where the pseudo-class is unsupported. Verify `prefers-reduced-motion`, `forced-colors`, and font-loading (`font-display: swap`, preload the above-the-fold body font, set fallback metrics) so version switches and search overlays do not cause layout shift. Honor `prefers-color-scheme` for the dark/light code theme and persist the user's explicit choice.

## Evidence And Compliance Boundaries

This pack is a set of **recommendations**, not **proof** of **compliance**, safety, or business performance. Treat it as synthetic calibration material, not real-product validation.

- Following this guidance does not constitute **proof** that a portal meets WCAG 2.2 AA, any accessibility statute, or any security standard. Named criteria (1.4.3, 2.1.1, 2.5.8, and the rest) are design targets; claiming **compliance** requires real audits — automated checks plus manual keyboard and screen-reader testing — against your actual rendered pages.
- Performance figures (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1) are budgets to design toward, not measured results. Verify with field data (RUM/CrUX) and lab runs on representative content and devices.
- No claim here is evidence of usability, conversion, activation, or developer satisfaction. Inspiration galleries and award sites are *never* evidence of accessibility, performance, or correctness; validate with your own users and instrumentation.
- Security guidance (secret handling, sandbox vs. production, confirmation on destructive calls) is directional and does not replace a security review of your specific implementation.

## Design-Quality Traps

Common ways docs portals score below 4/5 on the quality dimensions:

- **Low-contrast syntax themes.** The single most common failure: comment and punctuation tokens below 4.5:1. Audit each token, not just body text.
- **Marketing prose on reference pages.** Burying the signature under three paragraphs of value-prop. Lookup users bounce. Lead with the answer.
- **Color-only status.** Required/optional, breaking/non-breaking, added/removed conveyed only by hue. Add labels and glyphs.
- **Anchor headings hidden under the sticky header.** Clicking an anchor scrolls the target *behind* the top bar. Fix with `scroll-margin-top`.
- **Copy button that lies.** No confirmation, or it copies the prompt (`$`) and line numbers along with the command. Strip non-copyable decoration from the copied text.
- **Unscoped search.** Returning v1 and v3 results intermixed with no version filter, or surfacing the marketing site. Scope and label results.
- **Tabs that reset per page.** A reader who picks "Python" should keep it across pages; losing the selection on every navigation is friction. Persist the language choice.
- **Over-wide prose.** Stretching the reading column to 1440px because the layout allows it. Cap near 65ch.
- **Motion-heavy transitions.** Animated accordions and tab fades that ignore `prefers-reduced-motion`.

## Handoff Checks

Before shipping a docs/portal surface, confirm:

- [ ] One `h1` per page; heading outline has no skipped levels; right rail mirrors it; `aria-current` marks the current nav item and in-view heading.
- [ ] Every code block: language label, working copy button with "Copied" `aria-live` feedback, copied text excludes prompts/line numbers, horizontal scroll contained.
- [ ] Language/runtime tab selection persists across navigation and follows the APG Tabs keyboard pattern.
- [ ] Search opens via Cmd/Ctrl-K and a visible control, is keyboard-navigable, version-scoped, traps and restores focus, and has a defined empty state.
- [ ] Version switcher present in chrome and URL; deprecated pages show a banner naming the change and linking the replacement; no bookmarked URL dead-ends without guidance.
- [ ] Parameter and status-code tables use `<th scope>`; "Required" shown with label/symbol, not color alone; sticky header on long tables.
- [ ] Syntax tokens, badges, borders, and focus rings pass contrast (4.5:1 text, 3:1 non-text); verified in light and dark themes and under `forced-colors`.
- [ ] States built: default, loading/skeleton, empty search, copy success/failure, deprecated, explorer 400/401/429, 404/410, 500/offline, session-expired.
- [ ] Embedded explorer distinguishes sandbox from production, confirms destructive calls, never auto-sends mutations, and uses `YOUR_API_KEY` placeholders.
- [ ] Reflows to one column at 320px with no page-level horizontal scroll; usable at 200% zoom and under text-spacing overrides; reading column capped ~65ch.
- [ ] Skip link present; landmarks labeled; `:focus-visible` rings unobscured by sticky chrome (`scroll-margin-top` applied to anchor targets).
- [ ] CWV budgets checked (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1) with media space reserved and `font-display: swap` + preload + fallback metrics; `prefers-reduced-motion` and `prefers-color-scheme` honored and the theme choice persisted.
