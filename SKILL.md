---
name: web-design-skill
description: Use when designing, reviewing, specifying, or justifying website UI/UX for responsive web (desktop, tablet, mobile-web) and marketing or web-app surfaces. Produces structured, breakpoint- and browser-aware outputs for pages, flows, UI specs, typography systems, accessibility-aware reviews, and handoff rationale.
version: 1.3.0
---

# Website Design Skill

Use this skill for practical website design work across responsive web (desktop, tablet, mobile-web), marketing/landing pages, and web apps.

This skill prioritizes:
- usability
- navigation predictability (URLs, back/forward, deep links)
- readability and typography (fluid type, measure, scaling)
- spacing, density, and responsive layout across breakpoints
- accessibility and keyboard operability
- web-platform and browser conventions
- performance (Core Web Vitals)
- implementation-ready structure

If deeper detail is needed during a task, load only the relevant references:
- `skill/modes.md` for per-mode requirements and validation checklists
- `skill/templates.md` for output skeletons
- `docs/workflow.md` for the full internal workflow and universal review lenses
- `docs/clarification-policy.md` for deciding when to ask questions vs proceed with assumptions
- `docs/judged-mode.md` for `/web-design-skill --judge` orchestration with an independent judge pass
- `docs/principles.md` for durable web design principles
- `docs/guardrails.md` for hard safety, evidence, accessibility, and convention constraints
- `docs/sources.md` for the source hierarchy and canonical URLs
- `docs/quality-bars.md` for concrete numeric thresholds (typography, target size, contrast, motion, spacing, Core Web Vitals)
- `docs/design-quality.md` for visual hierarchy, composition, density, typography craft, color semantics, interaction polish, and production-readiness calibration
- `docs/motion-and-animation.md` for the motion layer: the appropriateness gate (animate only where it earns its place), easing/duration tokens, spring-vs-tween, the CSS → WAAPI → View Transitions → library build ladder, performance/accessibility rules, and wow-effect resources
- `docs/design-tool-handoff.md` for tool-agnostic interop: consuming a structured design extract from Figma / Pencil / Penpot / Sketch (via the host's MCP connector) as Mode D input, and emitting handoff + W3C Design Tokens (DTCG 2025.10) as Mode F output
- `docs/design-tool-runbooks.md` for the concrete, ordered call sequences behind that interop: per-tool READ runbooks (Figma `get_metadata`/`get_variable_defs`/`get_design_context`; Pencil `get_editor_state`/`get_variables`/`batch_get`) and REVERSE runbooks that write a DTCG `.tokens.json` back as Figma Variables (`use_figma` Plugin API or REST `POST /v1/files`) or Pencil variables (`set_variables`/`batch_design`), with the DTCG↔native mapping tables, idempotency, and alias-ordering rules
- `docs/design-quality-rubric.md` for 1-5 quality scoring, target levels, caps, and the improvement ladder
- `docs/golden-examples.md` and `examples/golden/` for taste and domain calibration across marketing landing, ecommerce PDP + checkout, content article, docs / dev portal, web-app dashboard, web form, and settings / account
- `docs/synthetic-case-studies.md` and `examples/case-studies/` for synthetic bad-to-good calibration cases when tuning output quality
- `docs/domain-packs/index.md` and `docs/domain-packs/` for domain playbooks covering marketing/landing, ecommerce, content/publishing, docs/dev-portal, and web-app/dashboard
- `docs/weaknesses.md` for known failure modes and prevention checks that keep outputs from becoming generic, overconfident, aesthetic-only, responsive-flattened, or weakly buildable
- `docs/evals.md` for structural, content, and fail-condition evaluation criteria
- `docs/llm-judge-runner.md` and `scripts/run_rubric_judge.py` for semantic rubric fixture calibration, including external-agent command runs during maintenance
- `docs/context-defaults.md` for audience, domain, breakpoint/browser, and use-context defaults
- `docs/heuristics.md` for the usability heuristics catalog with web applications and red-flag patterns
- `docs/patterns-catalog.md` for web pattern decision matrices (navigation, overlays, lists/grids/tables, actions, forms, feedback, states, search, auth)
- `docs/inspiration-sources.md` for visual inspiration and production reference sources, used only after UX/convention/accessibility reasoning is grounded
- `docs/visual-benchmark-playbooks.md` for source-specific Awwwards, CSS Design Awards / FWA / Webby, Land-book / SiteInspire / Godly, and Mobbin Web / Refero / Page Flows benchmark checklists
- `docs/benchmark-report-format.md` and `examples/benchmark-report.md` for turning 3-5 references into borrow / do-not-copy / token-component-state guidance
- `docs/visual-review-fixtures.md` and `examples/visual-review-fixtures/` for text-only review fixtures and expected critique discipline
- `docs/rendered-output-qa.md` and `examples/rendered-output-qa/` for optional QA after a design exists as HTML, prototype, screenshot, or rendered URL
- `docs/self-review.md` for the mandatory self-review pass run before any response is returned
- `examples/` for regression-style worked examples
- `examples/evals/` and `examples/rubric-before-after.md` for design-quality rubric score calibration
- `examples/anti-patterns.md` for calibration on ambiguous or hallucination-inviting inputs

## Supported modes

Classify every request into exactly one primary mode before responding:

1. Generate web page concept
2. Design web user flow
3. Create responsive UI spec
4. Review page for usability/accessibility
5. Create typography, spacing and grid system
6. Prepare design rationale / handoff
7. Generate / critique a marketing landing page (conversion / CRO)

If a request overlaps multiple modes, choose the single best primary mode and note any secondary considerations briefly inside the response.

## Invocation flags

If the request begins with `--judge` or explicitly asks for judge mode, strip the flag before classifying the design task and apply `docs/judged-mode.md`.

Judged mode means:
- draft the response privately using the normal workflow
- run an independent judge pass in the same session when the host supports subagents or parallel reviewers
- revise the draft when the judge score is below 4/5 and the issue can be fixed without inventing facts
- append a compact `Judge summary` section to the final response

Do not ask the user to run `scripts/run_rubric_judge.py` manually for interactive judged mode.

## Required workflow

### 1. Classify the request
Choose exactly one primary mode.

### 2. Identify context
Extract or infer product/domain, user goal, breakpoint and browser targets, page or flow scope, constraints, density level, accessibility sensitivity, and whether the user needs exploration, critique, or handoff structure.

Apply the context-aware defaults in `docs/context-defaults.md`. Precedence when signals conflict: safety/accessibility > regulated domain > use-context > audience > breakpoint/browser. State the resolution in `Assumptions`.

If the request matches marketing/landing, ecommerce, content/publishing, docs/dev-portal, or web-app/dashboard, load the closest domain pack from `docs/domain-packs/` before drafting. Domain packs are synthetic calibration material: they can shape hierarchy, trust language, states, and handoff checks, but they do not prove compliance, user preference, safety, or business performance.

### 3. Determine scope (the two axes)
Identify, separately, the **Responsive/breakpoint scope** (mobile-web / tablet / desktop / wide / unspecified) and the **Browser/engine scope** (Chromium / WebKit / Gecko / unspecified, plus Baseline gating). If unspecified, ask only when necessary, or continue with a minimal labeled assumption such as:
- `Assumption: Responsive, working down to 320px, on modern evergreen engines unless legacy support is specified.`

### 4. Check information sufficiency and clarification need
Apply `docs/clarification-policy.md`. Proceed with minimal labeled assumptions when safe; do not invent research, behavior, states, flows, or business rules as facts. If missing information would materially change the recommendation, ask at most three clarifying questions, explain why they block reliable output, and offer a fast path.

### 5. Apply source priority
Use this order:

1. Web platform standards & reference (WHATWG HTML, WAI-ARIA APG, MDN)
2. Accessibility, usability & measurement tooling (WCAG 2.2, ISO 9241, Lighthouse/CrUX, axe-core, Playwright — tooling is first-class evidence)
3. Public-sector and enterprise design systems (GOV.UK/NHS/USWDS; Carbon/Polaris/Fluent/Material Web/Primer; Tailwind/shadcn/Radix)
4. Established research and case-study sources (Baymard, NN/g, Wroblewski)
5. Browser support & capability data (caniuse, MDN Baseline, Browserslist)

When web standards/accessibility guidance conflicts with trend-based aesthetics, prefer the standards. See `docs/sources.md`.

Use `docs/design-quality.md` when the output proposes, critiques, specifies, or rationalizes a design artifact. Use `docs/design-quality-rubric.md` to score 1-5: target 4/5 for generated/specified artifacts; expose the current score in reviews.

Use `docs/synthetic-case-studies.md` and `examples/case-studies/` for weak-vs-strong calibration (synthetic, not real-world validation). Use `docs/clarification-policy.md` for underspecified or precision-sensitive requests. Use `docs/inspiration-sources.md`, `docs/visual-benchmark-playbooks.md`, and `docs/benchmark-report-format.md` as a separate non-authoritative inspiration layer. Use `docs/visual-review-fixtures.md` for Mode D evidence discipline. Use `docs/rendered-output-qa.md` only when a rendered artifact exists. Use `docs/weaknesses.md` as an internal preflight.

### 6. Build the response by mode
Use the matching structure from `skill/modes.md` and `skill/templates.md`.

### 7. Apply universal review lenses
Before finalizing, check: task clarity; clarification need; known weakness prevention; information hierarchy; design quality and visual craft; navigation predictability; web-convention alignment; readability and typography; spacing, density, and responsive behavior; accessibility implications; keyboard operability; performance (Core Web Vitals); SEO & semantics; forced-colors resilience; edge states; implementation usefulness.

### 8. Apply design reasoning
For every major design decision: state the choice explicitly; name at least one alternative considered; give a reason the chosen option wins, tied to user goal, task, breakpoint/browser, accessibility, or implementation; cite the heuristic by name (Fitts, Hick, Doherty, Jakob, Zeigarnik, goal-gradient, Gestalt, Nielsen) from `docs/heuristics.md`; use the decision matrices in `docs/patterns-catalog.md` for pattern-level choices — never invent a novel pattern when an established one applies. If a decision has no alternative, it was a default — flag it. State the concrete mechanism for design-quality decisions. Keep inspiration in a labeled `Inspiration references` block.

### 9. Check concrete quality bars
Compare against `docs/quality-bars.md`: typography (16px/1rem body minimum), line-height, ~65ch measure; target size (24px / 44px AAA) and pointer-aware spacing; WCAG 2.2 AA contrast; motion durations and reduced-motion; Core Web Vitals (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1); state coverage; the 4px spacing scale, breakpoint ladder, and 320px reflow; design-quality calibration/score; likely weakness patterns from `docs/weaknesses.md` (generic output, first-idea bias, evidence overreach, responsive flattening, happy-path-only design, weak handoff).

### 10. Run mandatory self-review
Run the pass defined in `docs/self-review.md`. Silently answer every prompt. If any answer is "no" or "not sure", revise and re-run.

### 11. Finalize responsibly
State assumptions; distinguish facts from recommendations; keep outputs structured and reusable; end with practical next actions.

## Output contract

Every response must:
- begin with `Mode:`
- include `Responsive/breakpoint scope:` and `Browser/engine scope:`
- include `Assumptions:`
- include accessibility considerations by default
- include responsive and browser behavior notes when relevant
- separate known facts from recommendations
- ask clarifying questions only when missing information would materially change the recommendation; otherwise proceed with labeled assumptions
- include design quality calibration when the response proposes, specifies, reviews, or rationalizes a design artifact
- apply the 1-5 design-quality rubric internally; expose the score in reviews and the target when useful
- apply known weakness prevention before returning; do not expose it as a separate section unless asked
- separate inspiration references from UX, accessibility, and convention rationale
- end with `Next actions:`

## Mode output requirements

### Mode 1: Generate web page concept
Include: Page goal · Primary user task · Information hierarchy · Recommended layout structure · Suggested components · Interaction notes · Empty / loading / error states · Responsive and browser behavior · Accessibility considerations · Design quality calibration · Rationale for major choices · Alternatives considered.

### Mode 2: Design web user flow
Include: Flow goal · Entry points · Ordered steps / views · Decision points · Back/forward and URL state · Failure and recovery paths · Responsive and browser behavior · Accessibility and usability risks · Simplification opportunities.

### Mode 3: Create responsive UI spec
Include: Screen or flow scope · Structural zones · Components by section · State definitions · Behavior rules · Content guidance · Spacing and layout notes · Typography rules · Accessibility requirements · Design quality requirements · Responsive and browser implementation notes · Key decision tradeoffs.

### Mode 4: Review page for usability/accessibility
A review is a set of causal-chain findings, not two separate lists of problems and fixes. Include: Sub-case (D1–D4) · Quick summary · Strengths · Findings (each one chain: Lens, Observation, Violated principle, User consequence, Change, Predicted effect + confidence, Severity Nielsen 0–4, Moves) · Design quality score (current → projected, per-dimension table) · Severity index · Bold move (optional, only when the trigger is met) · Platform-convention mismatches · Unresolved assumptions. The Lens enum includes the web lenses: Keyboard operability, Performance (Core Web Vitals), Responsive (breakpoints), SEO & semantics, and Forced-colors.

### Mode 5: Create typography, spacing and grid system
Include: Type roles · Size hierarchy · Weight usage · Line-height guidance · Spacing scale · Density rules · Visual rhythm rules · Pointer, target-size and input implications · Accessibility considerations · Usage examples.

### Mode 6: Prepare design rationale / handoff
Include: Design objective · Target users and context · Key design decisions · Pattern choices and why · Design quality rationale · Responsive and browser alignment · Accessibility and usability considerations · States and edge cases · Implementation notes · Open questions · Validation plan or recommended testing focus.

### Mode 7: Generate / critique a marketing landing page (conversion / CRO)
Include: Conversion goal and primary CTA · Above-the-fold (hero) structure · Scroll narrative and section rhythm · Value proposition and messaging hierarchy · Social proof and trust signals · CTA hierarchy and placement · Objection handling / FAQ · Accessibility considerations · Performance considerations (Core Web Vitals, media weight) · SEO and shareability · Design quality calibration · Conversion-rate reasoning (mechanisms, not guarantees). Respect the marketing-vs-web-app split: expressive, editorial craft is appropriate here; dense task efficiency belongs to the web-app modes.

## Hard constraints

Do not:
- invent web standards or browser behavior
- invent research findings or usability test results
- claim accessibility compliance unless explicitly verified
- treat inspiration galleries, award sites, portfolios, or moodboards as proof of usability, accessibility, performance, or compliance
- give aesthetic-only advice without usability reasoning
- use visual polish, brand expression, motion, or illustration to hide weak hierarchy, missing states, or inaccessible interaction
- return template-complete but decision-empty output
- ignore typography, spacing, navigation, keyboard operability, or state coverage
- pour the same layout into every breakpoint or ignore hover/focus/keyboard operability
- overcomplicate when the user needs a design artifact
- invent components, flows, or states unless clearly labeled as assumptions
- block useful output with nonessential questions

## Responsive and browser policy

When the scope spans breakpoints: provide a shared structure first, then specify behavior changes across the ladder (not just visual reflow), verify 320px reflow and 200% zoom, and exploit desktop density where the task rewards it. When the browser/engine scope is constrained: gate non-trivial features against `caniuse` / MDN Baseline and name the fallback; call out engine-specific behavior where it matters.

## Accessibility policy

Accessibility is built in by default. At minimum consider: semantic HTML and heading outline (one h1) + landmarks; keyboard operability (tab order, focus-visible, focus management, trap+restore, skip links, ESC); text scaling (rem, 200% zoom, text spacing); contrast and non-color cues; forced-colors resilience; target size; predictable navigation; error clarity and recovery; `aria-live` for async. Use careful phrasing such as `Accessibility considerations`, `Potential accessibility risks`, `Cannot verify compliance from the provided description`.

## Final reminder

This skill is for usable, explainable, responsive, browser-aware, accessible, performant website design output.

If the answer sounds stylish but not buildable, it failed.
