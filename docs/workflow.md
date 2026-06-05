# Internal Workflow

This document defines the internal workflow the skill must follow for every request.

---

## Step 1: Classify the request

Choose exactly one primary mode:

1. Generate web page concept
2. Design web user flow
3. Create responsive UI spec
4. Review page for usability/accessibility
5. Create typography, spacing and grid system
6. Prepare design rationale / handoff
7. Generate / critique a marketing landing page (conversion / CRO)

### Classification intent cues

#### Generate web page concept
Use when the user wants a new page idea, first-pass structure, content hierarchy, or layout/component recommendations.

#### Design web user flow
Use when the user wants ordered steps, navigation/URL logic, path design, recovery, and branching across views.

#### Create responsive UI spec
Use when the user wants implementation-ready structure, section-by-section component breakdown, explicit states and behavior, and breakpoint-by-breakpoint handoff.

#### Review page for usability/accessibility
Use when the user wants critique, issue finding, usability/accessibility review, or prioritization of problems.

#### Create typography, spacing and grid system
Use when the user wants type roles, hierarchy, line-height guidance, a spacing scale, a grid, and density rules.

#### Prepare design rationale / handoff
Use when the user wants explanation of decisions, handoff notes, justification, or a design summary for cross-functional use.

#### Generate / critique a marketing landing page (conversion / CRO)
Use when the primary job is persuasion and conversion (hero, scroll narrative, CTA hierarchy, social proof), not task completion.

---

## Step 2: Identify context

Extract or infer product/domain, user goal, breakpoint and browser targets, page or flow scope, constraints, density level, accessibility sensitivity, and whether the user needs exploration, critique, or handoff structure.

### Useful context prompts internally
- What is the user trying to accomplish?
- Is this a marketing surface (expressive, editorial) or a web-app surface (dense, task-first)?
- Is the product consumer, enterprise, high-trust, regulated, or utility-focused?
- Which breakpoints matter, and is it mobile-first or desktop-first?
- Which browser engines must be supported, and is any feature gating needed?
- Is readability or density the dominant concern?
- Is the user asking for concept generation, critique, or structured documentation?

### Apply context-aware defaults

Consult `docs/context-defaults.md` for the defaults tuned to that context (audience × domain × platform/browser × use-context). Conflict resolution order:

1. Safety and accessibility constraints
2. Regulated domain constraints (finance, health, government)
3. Use-context constraints (low bandwidth, keyboard-only/screen-reader, wide-viewport, anonymous-first vs returning-auth)
4. Audience constraints
5. Breakpoint/browser defaults

When multiple contexts apply, state the resolution in `Assumptions`.

If the request matches marketing/landing, ecommerce, content/publishing, docs/dev-portal, or web-app/dashboard, load the closest pack from `docs/domain-packs/`.

---

## Step 3: Determine scope (the two axes)

Identify, separately, the two scope axes every response carries:

- **Responsive/breakpoint scope** — mobile-web, tablet, desktop, wide, or unspecified.
- **Browser/engine scope** — Chromium, WebKit, Gecko, or unspecified, plus any Baseline/`caniuse` gating.

If a scope is unspecified, ask only when a wrong assumption would mislead; otherwise continue with a labeled assumption (e.g. `Assumption: responsive, working down to 320px, on evergreen engines unless legacy support is specified`). Gate any non-trivial CSS/JS feature against `caniuse` / MDN Baseline and name the fallback.

---

## Step 4: Check information sufficiency

Determine whether the request includes enough information for the chosen mode. Use `docs/clarification-policy.md` to decide whether to ask or proceed.

### If sufficient
Proceed directly.

### If partially sufficient
Continue with minimal labeled assumptions.

### If clarification is required
Ask at most three clarifying questions when a missing answer would materially change the recommendation. Include best inferred mode, both scope axes, assumptions, `Clarifying questions`, `Why this blocks`, optional `Fast path`, and `Next actions`. Do not ask non-blocking questions before producing useful work.

### If severely underspecified
Still provide a useful structure, but limit specificity, state missing inputs clearly, and avoid invented certainty.

---

## Step 5: Select source priority

Use the source hierarchy in this order:

1. Web platform standards & reference
2. Accessibility, usability & measurement tooling
3. Public-sector and enterprise design systems
4. Established research and case-study sources
5. Browser support & capability data (gating)

### Decision rules
- Use WHATWG HTML + WAI-ARIA APG + MDN for the correct element, role, and keyboard-interaction model; prefer native elements over re-implemented ARIA widgets.
- Use `docs/clarification-policy.md` when missing input could materially change task, breakpoint/browser, accessibility, safety, compliance, or implementation guidance.
- Use WCAG 2.2 (AA primary) for accessibility framing; cite specific success criteria.
- Use tooling output (Lighthouse/CrUX, axe-core/WAVE, Playwright) as first-class evidence when a claim is measurable; treat it as a recommendation to verify, never a compliance verdict.
- Use GOV.UK/NHS/USWDS for clarity, forms, and high-trust task completion; enterprise systems (Carbon, Polaris, Fluent, Material Web, Primer) and utility stacks (Tailwind, shadcn, Radix) for dense app surfaces and tokens.
- Use Baymard/NN/g/Wroblewski for e-commerce, IA, and forms research framing.
- Use caniuse/Baseline/Browserslist to gate non-trivial features against the declared browser scope; name the fallback.
- Use `docs/design-quality.md` and `docs/design-quality-rubric.md` for calibration and the 1-5 score.
- Use `docs/domain-packs/index.md` and the closest pack when the domain materially changes trust, hierarchy, state coverage, or handoff.
- Use `docs/synthetic-case-studies.md` and `examples/case-studies/` for weak-vs-strong calibration (synthetic, not real-world validation).
- Use `docs/inspiration-sources.md` only when the user asks for inspiration; keep it non-authoritative.
- Use `docs/benchmark-report-format.md` to turn 3-5 references into tokens/components/states/QA.
- Use `docs/visual-review-fixtures.md` as Mode D calibration and apply the same evidence limits live.
- Use `docs/rendered-output-qa.md` only after a rendered artifact exists.
- Use `docs/weaknesses.md` as an internal preflight when the task could invite generic output, unsupported claims, first-idea bias, responsive flattening, happy-path-only flows, or weak handoff.

---

## Step 6: Build the response by mode

Use the response structure defined in `skill/templates.md`.

### Mandatory response header
Every response begins with:
- Mode
- Responsive/breakpoint scope
- Browser/engine scope
- Assumptions

### Mandatory response footer
Every response ends with:
- Next actions

---

## Step 7: Apply universal review lenses

Before finalizing, check the draft against these lenses. The first group is general; the lenses marked **(web)** are the web-specific additions and must be checked on every relevant artifact.

### Task clarity
- Can the user's main task be identified immediately, above the fold?

### Clarification need
- Would any missing answer materially change the recommendation? If yes, did the response ask no more than three high-impact clarifying questions? If no, did it proceed with minimal labeled assumptions?

### Known weakness prevention
- Which weakness pattern from `docs/weaknesses.md` is most likely, and has the draft actively prevented it (not just avoided banned words)?

### Information hierarchy
- Is priority ordered by user need and decision timing — per page and per scroll section?

### Design quality and visual craft
- Does the proposal define the intended attention path?
- Are composition, spacing, typography, color, and density translated into concrete mechanisms rather than taste words?
- What is the design-quality target/score from `docs/design-quality-rubric.md`, and what prevents the next level?

### Navigation predictability
- Can the user understand where they are, where they can go, and how to recover? Are URLs shareable, and do back/forward behave predictably?

### Web-convention alignment
- Does the answer respect web-platform and browser conventions (link vs button semantics, native controls, Jakob's Law expectations) where relevant?

### Readability and typography
- Are type roles and reading structure appropriate? Is the measure capped (~65ch)? Do the numbers match `docs/quality-bars.md` (16px/1rem body minimum, line-height, fluid scaling)?

### Spacing, density and responsive behavior **(web)**
- Are interaction zones separated clearly using the 4px spacing scale?
- Does the layout behave deliberately across the breakpoint ladder (320 → 768 → 1024 → 1440+), not the same layout poured into every width?
- Does it reflow at 320px (WCAG 1.4.10) and stay usable at 200% zoom (1.4.4)?
- Does it exploit desktop density where the task rewards it?

### Accessibility implications
- Does the output address semantics, heading outline, scaling, labels, contrast, and non-color cues? Does contrast meet WCAG 2.2 AA per `docs/quality-bars.md`?

### Keyboard operability **(web)**
- Is everything reachable and operable by keyboard with a logical tab order?
- Is `:focus-visible` present, is focus managed on route/overlay change, and are dialogs focus-trapped with focus restored on close?
- Are skip links present, is there no keyboard trap, and does ESC close overlays?
- Are pointer/target sizes met (24px min, 44px AAA) and pointer-aware?

### Performance — Core Web Vitals **(web)**
- Is the LCP candidate (hero text/image) prioritized and not lazy-loaded?
- Is layout shift prevented (reserved media space, font-loading without CLS)? Budget: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1.

### SEO & semantics **(web)**
- One h1 and a logical heading outline; landmarks; meaningful link text; metadata/Open Graph and structured data on marketing/content surfaces.

### Forced-colors and theming **(web)**
- Does the design survive `forced-colors` / Windows High Contrast (outlines/focus preserved, not shadow-only) and provide a real `prefers-color-scheme` dark theme?

### Edge states
- Are loading, empty, error, and recovery states included, plus 404/500/offline/session-expired where relevant?

### Implementation usefulness
- Can design and engineering act on this without reverse-engineering vague prose?

---

## Step 8: Apply design reasoning

Every major design decision in the response must have:

- an explicit choice (not "use a button" but "use a filled primary button, one per view, in the sticky form footer")
- at least one alternative that was considered
- a reason the chosen option wins, tied to user goal, task, breakpoint/browser, accessibility, or implementation

If a decision has no alternative, it was a default — flag it. This step prevents first-idea-wins output, the most common failure mode in LLM-generated design.

For design-quality decisions, state the mechanism: size, spacing, alignment, contrast, density, color role, motion duration, state treatment, or token. Avoid "premium", "clean", "modern", "delightful", or "polished" unless translated into concrete UI decisions.

### Applies to
- Mode A: layout choice, component choice, hierarchy order
- Mode B: step ordering, recovery strategy, URL/decision-point design
- Mode C: structural zone choice, state granularity, breakpoint divergence choices
- Mode D: fix recommendations (why this fix, not another)
- Mode E: role scale ratio, weight strategy, density preset
- Mode F: every "Key design decision" pairs with an alternative and a reason
- Mode G: hero structure, CTA hierarchy, proof placement, scroll order

### How to surface
- In Mode A, C, and F: populate the `Alternatives considered` / decision blocks.
- In other modes: fold the alternative inline into the rationale.

### Ground reasoning in established heuristics
When a decision is driven by a known heuristic, cite it by name (Fitts' Law, Hick's Law, Doherty Threshold, Jakob's Law, Zeigarnik, goal-gradient, Gestalt). See `docs/heuristics.md` for the catalog with web applications and red-flag patterns; use the red flags during Mode D reviews. When two heuristics conflict, name both, pick one by context (see `docs/context-defaults.md`), and explain the tradeoff.

### Choose from known patterns, do not invent
For every pattern-level decision (navigation, overlay, list/grid/table, primary action placement, form pattern, feedback surface, search, auth), consult the decision matrices in `docs/patterns-catalog.md` first. Use the Use-when / Avoid-when criteria; cite the choice in `Pattern choices and why`; put the losing pattern in `Alternatives considered`. Never invent a novel pattern when an established one covers the case — novelty breaks Jakob's Law.

### Calibrate design quality
When the mode proposes or packages a design artifact, consult `docs/design-quality.md` and include the relevant calibration: attention path; composition and spacing (grid, responsive placement); typography (roles, clamp range, measure, font-loading); color and state (semantic roles, contrast, dark/forced-colors); interaction polish (feedback timing, motion budget, reduced-motion); production checks (tokens, states, breakpoints, semantic outline, CWV budget, axe/keyboard). Keep it concise and buildable. When the artifact warrants motion, consult `docs/motion-and-animation.md`: propose animation **only where it serves a functional purpose**, pick easing/duration tokens and a build mechanism (CSS → WAAPI → View Transitions → library) from its palette, and emit a compact Motion plan — do not animate high-frequency/keyboard actions, dense tables, or forms.

### Score design quality
Use `docs/design-quality-rubric.md` after calibration. Internally target 4/5 for generated concepts, specs, type systems, and handoff; revise a weak dimension when context allows, or state the missing input. For Mode D reviews, expose both a current and a projected (conditional) score, capped at 4/5 unless resilience is named. Do not let a high visual score hide P0/P1 weaknesses, missing states, accessibility risks, or unsupported claims.

### Keep inspiration separate from rationale
When the response uses inspiration sources: keep them in an `Inspiration references` block; separate production-flow references (Mobbin Web, Page Flows, Refero) from craft galleries (Awwwards, Land-book) and moodboards (Dribbble, Behance, Pinterest); never use inspiration as the reason a UX pattern is correct; return to the normal decision criteria before choosing.

---

## Step 9: Check concrete quality bars

Compare the draft against `docs/quality-bars.md`. At minimum confirm: typography roles cover the hierarchy with sizes/line-heights in range and a capped measure; target sizes and spacing met; contrast meets WCAG 2.2 AA; motion durations in range and reduced-motion respected; Core Web Vitals budget plausible (LCP/INP/CLS); states include at least default, loading, empty, error; spacing from the 4px scale; breakpoint behavior and 320px reflow; design-quality calibration/score applied; known weakness patterns addressed.

When the mode does not produce concrete values (Mode B flow, Mode F rationale), this check is lighter — confirm the output does not contradict any bar.

---

## Step 10: Self-review against the quality bar

Run the self-review pass defined in `docs/self-review.md`. Silently answer every prompt in the universal and mode-specific sections. If any answer is "no" or "not sure", revise and re-run. Never return a response that fails self-review with a disclaimer. Self-review is the single highest-impact quality mechanism in this skill.

---

## Step 11: Finalize responsibly

Make sure the final answer states assumptions clearly, distinguishes facts from recommendations, remains structured and reusable, avoids unsupported claims, and ends with concrete next actions.

---

## Quality bar

A good output from this skill should feel immediately usable in a design or product workflow, grounded in web standards and accessibility realities, concise without being thin, specific without pretending certainty, and helpful to both design and implementation.

If the output sounds stylish but not buildable, it failed.
