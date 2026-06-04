# Output Templates

Use these templates as the response skeleton for each mode.

Templates are structure, not quality. Before returning any filled template, run the known-weakness preflight from `docs/weaknesses.md` and the 1-5 design-quality rubric from `docs/design-quality-rubric.md`; do not expose the preflight as a separate output section unless the user explicitly asks for failure-mode analysis.

Every response carries two scope axes, never a single "platform":

- `Responsive/breakpoint scope:` — which viewports/breakpoints this answer targets (mobile-web, tablet, desktop, wide).
- `Browser/engine scope:` — which engines this answer targets (Chromium, WebKit, Gecko) and any Baseline/`caniuse` gating.

---

## Clarification-only template

Use this only when `docs/clarification-policy.md` says missing information blocks a reliable artifact.

```md
Mode: [best inferred mode]
Responsive/breakpoint scope: [known / unspecified / assumed]
Browser/engine scope: [known / unspecified / assumed]
Assumptions:
- [known fact or minimal assumption]
- [what cannot be safely assumed]

## Clarifying questions
1. [blocking question]
2. [blocking question if needed]
3. [blocking question if needed]

## Why this blocks
- [reason tied to task / breakpoint / browser / accessibility / safety / implementation]

## Fast path
- [smallest safe assumption for a provisional draft]

## Next actions
- [answer questions or confirm fast path]
- [share missing artifact/context if needed]
```

---

## Template A: Generate web page concept

```md
Mode: Generate web page concept
Responsive/breakpoint scope: [Mobile-web / Tablet / Desktop / Wide / Assumed]
Browser/engine scope: [Chromium / WebKit / Gecko / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Page goal
[what the page is for]

## Primary user task
[the main action the user needs to complete]

## Information hierarchy
1. [highest priority content/action — first glance]
2. [secondary content/action]
3. [supporting content/action]

## Recommended layout structure
- Header / global nav:
- Above-the-fold primary content:
- Main content column (measure capped ~65ch where text-heavy):
- Secondary / sidebar content:
- Footer:

## Suggested components
- [component] — [why; native element or named design-system component]
- [component] — [why]

## Interaction notes
- [behavior — hover/focus/click/keyboard, optimistic feedback]
- [behavior]

## Empty / loading / error states
- Empty:
- Loading (skeleton/spinner within ~100ms):
- Error (inline + retry; plus 404/500/offline/session-expired if relevant):

## Responsive and browser behavior
### Breakpoint behavior
- 320–767 (mobile-web): [reflow, stacked layout, off-canvas nav]
- 768–1023 (tablet): [columns, condensed nav]
- 1024+ (desktop/wide): [multi-column, exploit density where it helps]
### Browser/engine notes
- [engine-specific behavior or feature gated via Baseline/caniuse + fallback]

## Accessibility considerations
- [semantic structure: one h1, landmarks, heading outline]
- [keyboard operability: tab order, :focus-visible, skip link]
- [contrast / non-color cues / reduced-motion / forced-colors]

## Design quality calibration
- Quality target: [4/5 by default unless context blocks it]
- Attention path: [first → second → primary action]
- Composition and spacing: [grid, spacing-scale values, responsive placement]
- Typography: [roles, clamp() range, measure, line-height, font-loading]
- Color and state: [semantic roles, contrast, dark theme + forced-colors, state colors]
- Interaction polish: [feedback timing, motion budget, reduced-motion]
- Production checks: [tokens, states, breakpoints, semantic outline, CWV budget, axe/keyboard]

## Rationale for major choices
- [decision] because [reason]
- [decision] because [reason]

## Alternatives considered
- [alternative] — rejected because [reason tied to user goal, task, breakpoint, accessibility, or implementation]
- [alternative] — rejected because [reason]

## Next actions
- [action]
- [action]
```

---

## Template B: Design web user flow

```md
Mode: Design web user flow
Responsive/breakpoint scope: [Mobile-web / Tablet / Desktop / Wide / Assumed]
Browser/engine scope: [Chromium / WebKit / Gecko / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Flow goal
[what the flow needs to accomplish]

## Entry points
- [entry point — direct URL / deep link / referral / in-app]
- [entry point]

## Ordered steps / views
1. [route or view — what the user sees and can do]
2. [route or view]
3. [route or view]

## Decision points
- [condition] → [branch]
- [condition] → [branch]

## Back/forward and URL state
- [each step's URL is shareable/bookmarkable; History API push vs replace]
- [browser back/forward behavior; beforeunload guard on unsaved input; scroll restoration]

## Failure and recovery paths
- [failure case — network/validation/timeout/session-expired] → [recovery, data preserved]
- [failure case] → [recovery]

## Responsive and browser behavior
- [how the flow adapts across breakpoints — multi-pane on desktop, stepwise on mobile-web]
- [engine/browser considerations: autofill, passkeys, back-forward cache]

## Accessibility and usability risks
- [focus management on step/route change]
- [keyboard operability and aria-live status]
- [error clarity and recovery]

## Simplification opportunities
- [opportunity]
- [opportunity]

## Next actions
- [action]
- [action]
```

---

## Template C: Create responsive UI spec

```md
Mode: Create responsive UI spec
Responsive/breakpoint scope: [Mobile-web / Tablet / Desktop / Wide / Assumed]
Browser/engine scope: [Chromium / WebKit / Gecko / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Screen or flow scope
[scope]

## Structural zones
- Header / global nav:
- Main content area:
- Supporting / sidebar area:
- Footer / sticky action bar:

## Components by section
### Section 1
- [component — native element or design-system component]
- [component]

### Section 2
- [component]
- [component]

## State definitions
- Default:
- Hover / focus-visible / active:
- Loading:
- Empty:
- Error:
- Success:
- Disabled if applicable:
- System: 404 / 500 / offline / session-expired (where relevant)

## Behavior rules
- [If X, then Y]
- [rule]

## Content guidance
- [content principle, microcopy]
- [content principle]

## Spacing and layout notes
- [grid: 12-col desktop, gutters; spacing-scale values in px/rem, e.g. 24px / 1.5rem]
- [max content width / ~65ch measure; container queries where used]

## Typography rules
- [role] → [size in px/rem, line-height, clamp() range]
- [role] → [usage]

## Accessibility requirements
- [semantic structure + heading outline + landmarks]
- [keyboard operability: tab order, focus-visible, focus management, trap+restore]
- [contrast / target size 24px (2.5.8) / non-color cues / forced-colors]

## Design quality requirements
- Quality target: [4/5 by default unless context blocks it]
- Attention path:
- Composition and spacing:
- Typography:
- Color and state:
- Interaction polish:
- Production checks:

## Responsive and browser implementation notes
### Breakpoint behavior
- [how each zone reflows across 320 → 768 → 1024 → 1440+; 320px reflow verified]
### Browser/engine notes
- [feature support gated via Baseline/caniuse with fallback]

## Key decision tradeoffs
- [decision] chosen over [alternative] because [reason]
- [decision] chosen over [alternative] because [reason]

## Next actions
- [action]
- [action]
```

---

## Template D: Review page for usability/accessibility

```md
Mode: Review page for usability/accessibility
Responsive/breakpoint scope: [Mobile-web / Tablet / Desktop / Wide / Assumed]
Browser/engine scope: [Chromium / WebKit / Gecko / Assumed]
Sub-case: [D1 visual provided / D2 description only / D3 problem statement / D4 context change]
Assumptions:
- [assumption 1]
- [assumption 2]

## Quick summary
[one-paragraph assessment; for D3, lead with diagnosis hypothesis]

## Strengths
- [strength]
- [strength]

## Findings
> Each finding is one causal chain, ordered by severity. High-severity (3–4) findings use all fields. Low/cosmetic (0–2) may compress to Observation → Change → Severity. Never split an issue from its fix.

### F1 — [short title]
- Lens: [Usability / Accessibility / Keyboard operability / Hierarchy & readability / Design quality / Navigation & interaction / Performance (Core Web Vitals) / Responsive (breakpoints) / SEO & semantics / Forced-colors]
- Observation: [what is there now — evidence-bound; for D2, structure & behavior only, no visual assertions]
- Violated principle: [named — e.g. Nielsen #5 Error prevention · Hick's Law · WCAG 2.4.11 Focus Not Obscured · Gestalt proximity · Wroblewski form-design]
- User consequence: [the mechanism by which it hurts the user — not a restatement of the observation]
- Change: [the specific edit]
- Predicted effect: [directional + confidence — "should reduce mis-submits; confidence M (D2 text-only)". Never a fabricated %]
- Severity: [0–4, Nielsen] — [frequency × impact × persistence, one line]
- Moves: [dimension band→band, e.g. "Hierarchy 2→4"; + "lifts cap: …" if applicable]

### F2 — [short title]  (full form, repeat F1's fields)
- Lens:
- Observation:
- Violated principle:
- User consequence:
- Change:
- Predicted effect:
- Severity:
- Moves:

### F3 — [short title]  (compressed form for a cosmetic/severity-0–2 finding)
- Observation: [what is there now]
- Change: [the specific edit]
- Severity: [0–2, Nielsen] — [one-line reason]

## Design quality score (current → projected)
- Current: [1-5]/5 — [evidence-based reason; "provisional" for D2/D3]
- Projected: [1-5]/5 — the median of the assessable projected dimensions once the listed fixes land; conditional: requires F[..] AND [assumptions]. State a flat number, not "up to". [D2/D3: provisional — visual dimensions stay unassessable.]
- Ceiling note: with a visual pass confirming [x], the ceiling is [1-5]/5 (capped at 4/5 unless resilience is named). Visual dimensions are never projected upward from a text-only review.
- Primary lever(s): [the one or two findings that move the score most]

| Dimension | Now | Projected | Gated by (cap / ladder rung) | Confidence |
|-----------|-----|-----------|------------------------------|------------|
| Attention path & hierarchy | [n] | [n] | [cap / rung / —] | [verifiable / provisional / not-from-text] |
| Composition & spacing | [n] | [n] | | |
| Typography craft | [n] | [n] | | |
| Color, state & contrast | [n] | [n] | | |
| Density & rhythm | [n] | [n] | | |
| Interaction polish & motion | [n] | [n] | | |
| Context & brand fit | [n] | [n] | | |
| Production readiness | [n] | [n] | | |
- Projected overall = the median of the assessable (non-`n/v`) projected dimensions, lowered if a critical task dimension stays weak. It is NOT the sum of per-dimension gains, and it is NOT raised by a dimension the input cannot verify. A higher number reachable only after a visual pass belongs in `Ceiling note`, not here.

## Severity index
> A rollup for triage (0 = not a problem, omitted). Each finding already carries its severity inline.
- 4 (catastrophe): [F..]
- 3 (major): [F..]
- 2 (minor): [F..]
- 1 (cosmetic): [F..]

## Bold move (optional — omit unless the trigger is met)
> Use only when ALL hold: the page is already competent (current ≥3/5) but inert (loses no major points yet has no point of view); there is no unresolved severity-3 or severity-4 finding (fix those first); and there is a concrete UX upside. Allowed in D1/D3; D2 = structure/flow only; D4 = only if the new context unlocks it. This is NOT a fix and NOT required to ship. At most one (two only if genuinely distinct). If unsure, omit.

- The move: [one buildable sentence — a component/layout/flow/interaction change, not an adjective]
- Deviates from: [the product assumption / current direction / brand rule / web convention it contradicts]
- Job served (JTBD): [the job + one desired-outcome statement: minimize/increase [metric] of [object] when [context]]
- UX upside: [concrete, checkable benefit — tie to a named heuristic or quality bar]
- Risk / cost: [learnability, discoverability, accessibility exposure, or dev cost if this is wrong]
- De-risk / validate: [the cheap test before committing + kill criterion + the contrast / reduced-motion / keyboard / 320px-reflow checks it must still pass]
- Score impact: safe fixes alone → [X]/5; this move targets [Y]/5; it does NOT raise the score until validated.
- Conviction: [Speculative / Worth a spike / High-confidence]

## Platform-convention mismatches
> Web-platform and browser conventions (Jakob's Law): native control behavior, back/forward, link vs button semantics, engine-specific rendering.
- [mismatch]
- [mismatch]

## Unresolved assumptions
- [unknown]
- [unknown]

## Next actions
- [action]
- [action]
```

---

## Template E: Create typography, spacing and grid system

```md
Mode: Create typography, spacing and grid system
Responsive/breakpoint scope: [Mobile-web / Tablet / Desktop / Wide / Assumed]
Browser/engine scope: [Chromium / WebKit / Gecko / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Type roles
- Display:
- Page title (h1):
- Section title (h2/h3):
- Body:
- Secondary body:
- Label:
- Caption / helper:
- Button / action label:

## Size hierarchy
- [role] → [size in px/rem, e.g. 16px / 1rem; fluid clamp() range]
- [role] → [size guidance]

## Weight usage
- [weight] for [purpose]
- [weight] for [purpose]

## Line-height guidance
- Body → [1.5]
- Headings → [1.2–1.35]

## Spacing scale
- 4
- 8
- 12
- 16
- 24
- 32
- 48
- 64

## Density rules
- [comfortable vs compact presets; when to tighten one step for dense tables/dashboards]
- [rule]

## Visual rhythm rules
- Quality target: [4/5 by default unless context blocks it]
- [vertical rhythm: spacing multiples; baseline consistency across components]
- [measure cap ~65ch; section spacing on long-scroll pages]

## Pointer, target-size and input implications
- Minimum target size 24×24px (WCAG 2.5.8); 44×44px (2.5.5 AAA) for primary/touch-first actions
- Pointer-aware sizing: @media (pointer: coarse) bumps targets/spacing; (pointer: fine) allows denser targets
- Input font-size ≥ 16px to avoid mobile zoom-on-focus; ≥ 8px spacing between adjacent targets

## Accessibility considerations
- [text spacing 1.4.12 survives; 200% zoom; rem-based scaling honors user root size]
- [contrast; non-color cues; forced-colors]

## Usage examples
- Global header / nav:
- Content card / list row:
- Form field + label + help + error:
- Data table cell + header:
- Article body / long-form reading column:

## Next actions
- [action]
- [action]
```

---

## Template F: Prepare design rationale / handoff

```md
Mode: Prepare design rationale / handoff
Responsive/breakpoint scope: [Mobile-web / Tablet / Desktop / Wide / Assumed]
Browser/engine scope: [Chromium / WebKit / Gecko / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Design objective
[objective]

## Target users and context
[users and context]

## Key design decisions
- [decision] — alternative considered: [alternative] — chosen because [reason tied to user goal, task, breakpoint, accessibility, or implementation]
- [decision] — alternative considered: [alternative] — chosen because [reason]

## Pattern choices and why
- [pattern] over [alternative pattern] because [reason]
- [pattern] over [alternative pattern] because [reason]

## Design quality rationale
- Quality target: [4/5 by default unless context blocks it]
- [quality decision] — mechanism: [size/spacing/alignment/color role/density/motion/token] — [why it fits context]
- [quality decision] — mechanism: [mechanism] — [why]

## Responsive and browser alignment
### Breakpoint behavior
- [how the design holds across the breakpoint ladder; 320px reflow]
### Browser/engine notes
- [feature support / Baseline gating / fallbacks for the named engines]

## Accessibility and usability considerations
- [semantic structure + keyboard operability + focus management]
- [contrast / reduced-motion / forced-colors / target size]
- [error clarity and recovery]

## States and edge cases
- [state]
- [state]

## Implementation notes
- [tokens, component/state mapping, performance/CWV, analytics, focus management]
- [note]

## Open questions
- [question]
- [question]

## Validation plan / recommended testing focus
- [what to test, how — method, metric, acceptance: axe/keyboard pass, Lighthouse budget, 320px reflow]
- [test focus]

## Next actions
- [action]
- [action]
```

---

## Template G: Generate / critique a marketing landing page (conversion / CRO)

```md
Mode: Generate / critique a marketing landing page (conversion / CRO)
Responsive/breakpoint scope: [Mobile-web / Tablet / Desktop / Wide / Assumed]
Browser/engine scope: [Chromium / WebKit / Gecko / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Conversion goal and primary CTA
[the single primary conversion goal + the one dominant CTA]

## Above-the-fold (hero) structure
[value proposition visible without scrolling: headline, subhead, primary CTA, supporting visual]

## Scroll narrative and section rhythm
[ordered by visitor questions: problem → solution → proof → how it works → objections → final CTA]

## Value proposition and messaging hierarchy
[headline hierarchy, benefit-led copy, specificity over adjectives]

## Social proof and trust signals
[logos, testimonials, metrics, security/trust badges — specific, not generic]

## CTA hierarchy and placement
[one dominant CTA repeated down the page; secondary CTAs visually subordinate]

## Objection handling / FAQ
[the top objections answered inline or in an accordion]

## Accessibility considerations
[semantic structure, keyboard operability, contrast on hero overlays, reduced-motion for scroll effects, forced-colors]

## Performance considerations (Core Web Vitals, media weight)
[LCP from hero image/text, INP from interactive elements, CLS from media/fonts; image art-direction, lazy-load below fold]

## SEO and shareability
[semantic heading outline (one h1), meta title/description, Open Graph/Twitter cards, structured data, canonical]

## Design quality calibration
- Quality target: [4/5 by default unless context blocks it]
- Attention path:
- Composition and spacing:
- Typography:
- Color and state:
- Interaction polish:
- Production checks:

## Conversion-rate reasoning
[mechanisms and hypotheses tied to heuristics (goal-gradient, social proof, clarity) — never fabricated lift percentages or A/B results]

## Next actions
- [action]
- [action]
```
