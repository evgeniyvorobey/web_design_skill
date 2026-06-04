# Evaluation Criteria

This document defines concrete evaluation criteria for `web-design-skill` output by mode. It enables automated and human-judged quality checks, regression testing, and consistent feedback across iterations.

Use this document when:

- reviewing a skill response before shipping
- building evals for LLM-as-judge scoring
- regression-testing prompt or skill changes
- assessing whether a mode output meets the contract

Every mode is evaluated across three layers:

1. **Structural validation** — mechanical checks that can be automated via regex, parsing, or validators.
2. **Content validation** — semantic checks that require a human or LLM-as-judge.
3. **Fail conditions** — hard stops that invalidate the response regardless of other scores.

---

## Shared structural validation (all modes)

Every response must satisfy the following, regardless of mode:

- [ ] Starts with `Mode: [exact mode name]`
- [ ] Contains `Responsive/breakpoint scope:` and `Browser/engine scope:` lines (the two web scope axes, never a single `Platform scope:`)
- [ ] Contains `Assumptions:` section with at least 2 items
- [ ] Contains the mode-specific accessibility section with at least 3 concrete items:
  - Mode A / E / G: `## Accessibility considerations`
  - Mode B: `## Accessibility and usability risks`
  - Mode C: `## Accessibility requirements`
  - Mode D: `## Findings` containing at least one finding with `Lens: Accessibility` or `Lens: Keyboard operability`
  - Mode F: `## Accessibility and usability considerations`
- [ ] Contains a `## Next actions` section with at least 2 specific, testable items
- [ ] Does not contain the compliance-claim tokens: `compliant`, `WCAG-compliant`, `passes accessibility` unless the user provided verified evidence
- [ ] Does not contain fabricated quantitative research claims (regex: `\d+%`, `users completed`, `testing proved`, `research shows`, `lifted conversion by`) unless sourced
- [ ] If the response asks clarifying questions, it contains at most 3 questions and explains why the answers block reliable output
- [ ] If the request used `--judge` and produced a substantive artifact, the final response includes a compact `Judge summary`

## Shared fail conditions (all modes)

Any of the following invalidates the response:

- Missing the mode-specific accessibility section
- `Next actions` are generic (examples: "test it", "validate", "iterate", "improve")
- Hallucinated web standard or browser rule (example: "HTML requires X" or "Safari mandates Y" without source or "recommendation" framing)
- **Responsive flattening**: the same layout poured into every breakpoint with no behavior change, or no working 320px reflow, presented as a responsive answer
- **Keyboard / pointer operability ignored**: the design relies on hover-only actions, omits visible focus, loses focus on route/overlay change, or ships a modal without focus trap + restore. On web, ignoring hover/focus/keyboard operability is the failure — using hover, right-click menus (with a fallback), and keyboard-first interaction is expected and correct, not a red flag.
- Aesthetic-only recommendation without usability, readability, accessibility, performance, or implementation justification
- Visual polish, brand expression, motion, or illustration used to hide weak hierarchy, missing states, or inaccessible interaction
- Compliance claim echoed from user input without "cannot independently verify" qualifier
- Inspiration source used as evidence for usability, accessibility, performance, compliance, or user preference
- Template-complete but decision-empty output: required sections exist, but recommendations have no choices, rejected alternatives, context-specific reasons, or buildable mechanisms
- Non-blocking clarification: response asks questions instead of producing a useful artifact when safe assumptions would have worked
- More than three clarifying questions in one response
- `--judge` response asks the user to run `scripts/run_rubric_judge.py` manually instead of using the interactive judged-mode workflow

## Clarification validation

Use [`clarification-policy.md`](clarification-policy.md) when a response asks questions or proceeds with underspecified input.

- [ ] Blocking questions are tied to breakpoint/browser, primary task, safety/accessibility, compliance, visual evidence, or implementation.
- [ ] Non-blocking gaps are handled through labeled assumptions, unresolved assumptions, open questions, or next actions.
- [ ] A clarification-only response still includes Mode, both scope axes, Assumptions, Clarifying questions, Why this blocks, optional Fast path, and Next actions.
- [ ] The response does not ask cosmetic/style questions before structural blockers.
- [ ] The response offers a fast path when a provisional draft would still be useful.

## Known weakness validation

Use [`weaknesses.md`](weaknesses.md) as the regression map for content review. For every evaluated response:

- [ ] The likely weakness pattern is prevented by the response, not merely absent from wording.
- [ ] The output is specific to the user's product, task, audience, breakpoint/browser, or constraints.
- [ ] Major decisions include a chosen option, a rejected alternative where relevant, and a concrete reason.
- [ ] Evidence boundaries are clear: facts, assumptions, recommendations, and unverifiable items are separated where risk exists.
- [ ] The response is buildable: states, behaviors, values, tokens, QA checks, or validation focus are present as appropriate.
- [ ] The 1-5 design-quality rubric from [`design-quality-rubric.md`](design-quality-rubric.md) is applied when the response proposes, specifies, reviews, or rationalizes a design artifact.
- [ ] Relevant synthetic case studies, visual-review fixtures, domain packs, benchmark report format, or rendered-output QA guidance are used for calibration when the task matches those surfaces.

Hard-fail the response if it matches a P0 or P1 weakness in `docs/weaknesses.md`.

---

## Mode A: Generate web page concept

### Structural validation
- [ ] Response begins with `Mode: Generate web page concept`
- [ ] Contains sections: `Page goal`, `Primary user task`, `Information hierarchy`, `Recommended layout structure`, `Suggested components`, `Empty / loading / error states`, `Responsive and browser behavior`, `Design quality calibration`
- [ ] Contains `Alternatives considered` with at least one rejected alternative and reason
- [ ] Information hierarchy is ordered (numbered or priority-bulleted)
- [ ] All three edge states (empty, loading, error) are explicitly addressed
- [ ] Responsive behavior is described across the breakpoint ladder, not as a single fixed layout

### Content validation
- [ ] Primary user task is singular and explicit
- [ ] Hierarchy is task-driven (by user need), not visual-first (by prominence)
- [ ] Suggested components are real (native elements or named design-system components)
- [ ] Rationale connects each major choice to user goal, accessibility, performance, or implementation
- [ ] Design quality calibration defines attention path, composition/spacing, typography, color/state, interaction polish, and production checks
- [ ] Accessibility considerations are specific (semantic outline, keyboard operability, contrast), not generic "use labels"
- [ ] No invented standards or quantitative claims without source

### Fail conditions
- Primary user task is ambiguous or absent
- Empty/loading/error states missing
- Hallucinated component or standard
- Generic accessibility section copied across responses
- The same layout asserted for every breakpoint (responsive flattening)

---

## Mode B: Design web user flow

### Structural validation
- [ ] Response begins with `Mode: Design web user flow`
- [ ] Contains sections: `Flow goal`, `Entry points`, `Ordered steps / views`, `Decision points`, `Back/forward and URL state`, `Failure and recovery paths`
- [ ] Ordered steps are numbered or sequenced
- [ ] Decision points are explicit
- [ ] At least one failure path is defined

### Content validation
- [ ] Success path is end-to-end (entry → success state)
- [ ] URL/state behavior is defined: shareable URLs where appropriate, predictable back/forward, unsaved-input guard
- [ ] Recovery paths cover at least one of: network failure, validation error, session expiry, user abandonment — with entered data preserved
- [ ] The flow uses web affordances correctly (hover/hover-intent, right-click menus with a fallback, full keyboard operability, focus management on route change) rather than ignoring them
- [ ] The flow uses multi-pane / long-scroll / multi-tab where it helps, instead of forcing one view at a time
- [ ] Each step scopes what the user sees, what they can do, and what happens next
- [ ] Simplification opportunities are flagged separately from the flow

### Fail conditions
- Back/forward or URL-state logic missing or vague ("user goes back")
- No recovery path defined for the primary failure mode
- Flow ignores keyboard operability or relies on hover-only actions with no fallback
- Invented business rules not flagged as assumptions

---

## Mode C: Create responsive UI spec

### Structural validation
- [ ] Response begins with `Mode: Create responsive UI spec`
- [ ] Contains sections: `Structural zones`, `Components by section`, `State definitions`, `Behavior rules`, `Spacing and layout notes`, `Typography rules`, `Accessibility requirements`, `Design quality requirements`, `Responsive and browser implementation notes`, `Key decision tradeoffs`
- [ ] Specifies behavior across breakpoints with a verified 320px reflow, or states the scope is a single breakpoint
- [ ] State definitions cover at minimum: default, loading, empty, error (plus system states where relevant)
- [ ] Spacing values are concrete (example: "16px", "1.5rem", or "space-4 token"), not relative ("more spacing")

### Content validation
- [ ] An engineer can begin implementation without asking for missing structural information
- [ ] Component names match the named design system or a reasonable default (Carbon, Polaris, Radix, native, or custom)
- [ ] Behaviors are described as rules ("If X, then Y"), not narrative
- [ ] Typography rules specify role-to-size mapping (px/rem), not just a list of sizes
- [ ] Accessibility requirements include specific targets: target size, label/semantics, keyboard operability, focus management, contrast
- [ ] Design quality requirements include concrete attention path, composition/spacing, typography, color/state, interaction polish, and production checks
- [ ] Responsive notes reflect actual breakpoint behavior and browser/engine gating, not stereotypes

### Fail conditions
- States missing or only "default" defined
- Spacing/typography vague ("appropriate", "modern", "comfortable")
- The same layout poured into every breakpoint without behavior change
- Invented component names not tied to any design system or explicit assumption

---

## Mode D: Review page for usability/accessibility

### Structural validation
- [ ] Response begins with `Mode: Review page for usability/accessibility`
- [ ] Contains sections: `Quick summary`, `Strengths`, `Findings`, `Design quality score (current → projected)`, `Severity index`, `Unresolved assumptions`
- [ ] Sub-case is classified in the opening (D1 visual / D2 description-only / D3 problem-statement / D4 context-change)
- [ ] Severity uses the Nielsen 0–4 scale per finding
- [ ] At least one strength is identified

### Content validation
- [ ] Each finding is one causal chain: observation → violated principle → user consequence → change → predicted effect (no issue split from its fix)
- [ ] Every finding names the violated principle (heuristic/law/WCAG SC), not "feels off"
- [ ] Every predicted effect names a user outcome, stated directionally with a confidence level and no fabricated percentages
- [ ] The web lenses are applied where relevant — keyboard operability, Core Web Vitals, responsive-across-breakpoints, SEO & semantics, forced-colors
- [ ] Findings are concrete, not aesthetic opinions ("form is too long without grouping" vs "feels cluttered")
- [ ] Both a current and a projected score are present; the projection is conditional (IF fixes land AND assumptions hold) and capped at 4/5 unless resilience is named
- [ ] Unresolved assumptions list what cannot be verified from the provided material
- [ ] For description-only reviews: visual/aesthetic claims are qualified, and visual dimensions are not projected upward
- [ ] For problem-statement reviews: diagnosis is differentiated from assessment
- [ ] If a Bold move is present: trigger met, all fields complete, kept separate from required fixes
- [ ] Compliance language avoided (see shared fail conditions)

### Fail conditions
- Review asserts visual properties (color, contrast, spacing) from text-only input without qualifier
- No strengths section or "no strengths found"
- A finding splits the issue from its fix, or a change is stated without a predicted effect
- Projected score asserted without conditional phrasing, or a P0/Fail projected up to a number
- Bold move offered without its trigger met, or missing required fields
- Compliance claim without verified evidence

---

## Mode E: Create typography, spacing and grid system

### Structural validation
- [ ] Response begins with `Mode: Create typography, spacing and grid system`
- [ ] Contains sections: `Type roles`, `Size hierarchy`, `Weight usage`, `Line-height guidance`, `Spacing scale`, `Density rules`, `Visual rhythm rules`, `Pointer, target-size and input implications`
- [ ] Type roles are named (Display, Title, Body, Caption, Label, etc.)
- [ ] Size hierarchy includes concrete sizes in `px` / `rem` (16px / 1rem body minimum)
- [ ] Line-height guidance includes concrete ratios (1.5 body, 1.2–1.35 headings)
- [ ] Spacing scale is systematic (4px base: 4, 8, 12, 16, 24, 32, 48, 64)
- [ ] Target-size minimum is stated (24px WCAG 2.5.8; 44px 2.5.5 AAA) with pointer-aware notes

### Content validation
- [ ] Roles map to use cases, not just to components
- [ ] Sizing is rem-based and scales (fluid `clamp()`), with a capped measure (~65ch)
- [ ] Line-height values are specified per role
- [ ] Density rules explain when to tighten vs loosen based on task, including exploiting desktop density
- [ ] Visual rhythm rules explain how spacing, type roles, and grouping repeat across components/pages
- [ ] Accessibility considerations include 200% zoom, text spacing (1.4.12), and forced-colors
- [ ] If multilingual support was requested, script-specific adjustments (CJK, Arabic, Devanagari) are called out
- [ ] Examples show roles applied to common web surfaces (header/nav, card, form, table, article body)

### Fail conditions
- Type roles are absent, only a size list
- Target-size minimum missing
- Scaling behavior (rem, 200% zoom) not addressed
- Multilingual requested but no script-specific notes

---

## Mode F: Prepare design rationale / handoff

### Structural validation
- [ ] Response begins with `Mode: Prepare design rationale / handoff`
- [ ] Contains sections: `Design objective`, `Target users and context`, `Key design decisions`, `Pattern choices and why`, `Design quality rationale`, `Responsive and browser alignment`, `States and edge cases`, `Implementation notes`, `Open questions`, `Validation plan / recommended testing focus`
- [ ] Each key decision is separated from its justification
- [ ] Open questions list at least one genuinely open item

### Content validation
- [ ] Rationale connects decisions to user goals, context, or constraints, not aesthetic preference
- [ ] Pattern choices reference established web convention or design-system guidance
- [ ] Design quality rationale connects visual hierarchy, composition, density, brand, or motion to context with concrete mechanisms
- [ ] Responsive and browser alignment is substantive (breakpoint behavior, Baseline gating), not "follows best practices"
- [ ] Validation plan specifies WHAT to test and HOW (method, metric, acceptance: axe/keyboard pass, Lighthouse budget, 320px reflow)
- [ ] Implementation notes address a real engineering concern (state management, focus management, accessibility semantics, analytics, performance)

### Fail conditions
- Rationale reverse-engineered from the task with no actual design shown or referenced
- Validation plan is "test with users" without specifics
- Open questions list is empty or synthetic
- Fabricated research findings used as justification

---

## Mode G: Generate / critique a marketing landing page (conversion / CRO)

### Structural validation
- [ ] Response begins with `Mode: Generate / critique a marketing landing page (conversion / CRO)`
- [ ] Contains sections: `Conversion goal and primary CTA`, `Above-the-fold (hero) structure`, `Scroll narrative and section rhythm`, `Social proof and trust signals`, `CTA hierarchy and placement`, `Performance considerations (Core Web Vitals, media weight)`, `SEO and shareability`, `Design quality calibration`, `Conversion-rate reasoning`
- [ ] A single primary conversion goal and one dominant CTA are explicit
- [ ] Performance section names LCP / INP / CLS considerations

### Content validation
- [ ] Above-the-fold value proposition is clear without scrolling on both desktop and mobile-web
- [ ] Scroll narrative is ordered by visitor questions, not a feature list
- [ ] Social proof is specific (named logos, concrete metrics), not generic
- [ ] Conversion claims are mechanisms/hypotheses tied to heuristics, never fabricated lift percentages or A/B results
- [ ] The marketing-vs-web-app split is respected and named (expressive/editorial craft is appropriate here)

### Fail conditions
- Multiple competing primary CTAs with no hierarchy
- Fabricated conversion-rate statistics or A/B results
- Performance and accessibility treated as afterthoughts on a conversion-critical page
- Hero spectacle that fails contrast, reduced-motion, or LCP

---

## Scoring rubric

For evals, score each response across three dimensions:

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| Structural validation | 30% | Pass rate across the mode's structural checks |
| Content validation | 50% | Count of content checks passing / total |
| Hallucination & safety | 20% | Binary pass/fail on shared + mode fail conditions |

A response that fails any hard fail condition receives an overall score of **Fail** regardless of the weighted score.

## Design quality rubric

Use [`design-quality-rubric.md`](design-quality-rubric.md) for the design-quality score. Structural/content evals answer "does the response satisfy the skill contract?" The design-quality rubric answers "how strong is the design artifact itself?"

For generated concepts, UI specs, typography systems, and handoff:

- [ ] Internal target is 4/5 or higher.
- [ ] Any dimension below 4/5 is either revised or clearly blocked by missing input.
- [ ] The output does not average away a serious flaw such as missing states, weak accessibility behavior, or responsive flattening.

For reviews:

- [ ] `Design quality score (current → projected)` includes both a current and a projected score. The projected number is a flat median of assessable dimensions, not "up to"; any higher post-visual-pass figure is confined to a `Ceiling note`.
- [ ] The projection is conditional and capped at 4/5 unless resilience is named; a P0/Fail is not projected up to a number.
- [ ] Text-only reviews label both scores as structural/provisional, and visual dimensions are not projected upward.
- [ ] Score rationale references concrete dimensions.

### Rubric eval fixtures

The score-calibrated fixtures live in `../examples/evals/`. Use them as regression targets:

- `rubric-score-1.json` — should fail or score 1/5 because of hard guardrail violations
- `rubric-score-2.json` — should score 2/5 because it is structurally weak (e.g., responsive flattening or keyboard inoperability) and not buildable
- `rubric-score-3.json` — should score 3/5 because it is acceptable but lacks stronger mechanisms
- `rubric-score-4.json` — should score 4/5 because it is shippable with validation notes
- `rubric-score-5.json` — should score 5/5 because it is resilient across states, accessibility, breakpoints, browsers, and handoff

The upgrade example in [`../examples/rubric-before-after.md`](../examples/rubric-before-after.md) shows how a 2/5 response becomes a 4/5 response.

### LLM-as-judge runner

Use [`llm-judge-runner.md`](llm-judge-runner.md) and `../scripts/run_rubric_judge.py` to run semantic rubric calibration.

Minimum local check:

```bash
python3 scripts/run_rubric_judge.py --dry-run
```

Export judge requests:

```bash
python3 scripts/run_rubric_judge.py --export-jsonl tmp/rubric-judge-requests.jsonl
```

Validate judge outputs:

```bash
python3 scripts/run_rubric_judge.py --judge-output tmp/rubric-judge-results.jsonl
```

Run through an external judge agent without provider keys in the repository:

```bash
python3 scripts/run_rubric_judge.py \
  --judge-command "./scripts/local_judge_agent.sh" \
  --judge-command-output tmp/rubric-judge-results.jsonl
```

Self-test the runner without an LLM:

```bash
python3 scripts/run_rubric_judge.py --export-expected-output tmp/rubric-judge-expected.jsonl --judge-output tmp/rubric-judge-expected.jsonl
```

Self-test the external command adapter without an LLM:

```bash
python3 scripts/run_rubric_judge.py --judge-command "python3 scripts/rubric_judge_oracle_agent.py"
```

---

## How to run evals

### Automated structural checks

Run:

```bash
python3 scripts/validate_repo.py
```

The repository validator checks required files, relative links, root skill frontmatter, and the committed example outputs in `examples/`. It extracts each `## Example output` fenced block and verifies the mode-specific structural contract, including assumptions, required sections, accessibility sections, concrete numeric values where required, decision tradeoffs, and non-generic next actions.

These checks are intentionally structural. They catch contract drift and missing sections, but do not replace human or LLM-as-judge content review.

### Human or LLM-as-judge content checks

1. Provide the response alongside the mode-specific criteria from this file.
2. Score each content check as pass / partial / fail.
3. Record the rationale for any non-pass, so the pattern is visible across runs.

### Regression testing with examples

The files in `examples/` are treated as regression targets. The compact golden examples in [`../examples/golden/`](../examples/golden/) are taste and domain calibration targets.

Synthetic calibration resources:

- [`synthetic-case-studies.md`](synthetic-case-studies.md) and [`../examples/case-studies/`](../examples/case-studies/) — bad-to-good response calibration without real products or screenshots
- [`visual-review-fixtures.md`](visual-review-fixtures.md) and [`../examples/visual-review-fixtures/`](../examples/visual-review-fixtures/) — text review fixtures for Mode D evidence discipline
- [`domain-packs/index.md`](domain-packs/index.md) — domain playbooks for marketing/landing, ecommerce, content/publishing, docs/dev-portal, and web-app/dashboard
- [`benchmark-report-format.md`](benchmark-report-format.md) and [`../examples/benchmark-report.md`](../examples/benchmark-report.md) — benchmark reporting for 3-5 references without copying or evidence overreach
- [`rendered-output-qa.md`](rendered-output-qa.md) and [`../examples/rendered-output-qa/`](../examples/rendered-output-qa/) — optional post-implementation QA report structure

When the skill, `modes.md`, or `templates.md` changes:

1. Re-generate each example with the updated skill.
2. Score the regenerated response against this file.
3. Compare to the committed example; any content regression should block the change.
4. Spot-check the golden examples for domain-specific regressions.
5. Spot-check synthetic case studies, visual review fixtures, benchmark reports, and domain packs when changing prompt behavior that affects these surfaces.

---

## Maintenance

- When a new mode or section is added to `modes.md` or `templates.md`, add corresponding checks here.
- When a new guardrail is added to `guardrails.md`, add a matching shared fail condition here.
- Keep structural checks automatable; resist ambiguous criteria in that layer.
- Content checks should describe behavior, not enforce style.
