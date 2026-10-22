# Known Weaknesses and Failure-Mode Prevention

This document names the predictable weaknesses of the skill and turns them into prevention checks.

It is not a public apology section. It is an internal calibration layer used before drafting, during self-review, and when adding evals. The goal is to catch weak output before it reaches the user.

---

## How to use this file

Before drafting a response:

1. Identify the 1-3 weakness patterns the task is most likely to trigger.
2. Add the corresponding prevention checks to the draft plan.
3. If the draft resembles any failure signal below, revise the root decision, not only the wording.

During maintenance:

- Add a new weakness here when a field failure appears more than once.
- Add the matching self-review prompt in `docs/self-review.md`.
- Add a structural or content eval in `docs/evals.md` when the weakness can be checked reliably.
- Add a Bad / Good pair to `examples/anti-patterns.md` when the weakness is easy to demonstrate.

---

## Severity model

| Severity | Meaning | Examples |
|----------|---------|----------|
| P0 | Harmful or misleading | invented web-standard or browser rules, fake research, unsupported compliance claims |
| P1 | Product-breaking | missing recovery paths, keyboard-inoperable interaction, responsive flattening (one layout in every breakpoint, no 320px reflow) |
| P2 | Quality regression | generic output, weak hierarchy, vague handoff, visual polish without mechanism |
| P3 | Craft issue | verbosity, unnecessary theory, weak next actions |

P0 and P1 weaknesses must block the response. P2 and P3 weaknesses should be fixed unless the user explicitly requested a quick sketch.

---

## Core weakness patterns

### 1. Generic artifact disguised as a design answer

Trigger:
- user gives a short prompt with little product, audience, breakpoint/browser, or task context

Failure signals:
- the answer could fit any app
- "main task", "primary content", or "user-friendly" appears without concrete meaning
- assumptions are too broad to constrain the design

Prevention:
- use the smallest labeled assumptions
- narrow the artifact to what the input can support
- ask for missing context only when a wrong assumption would mislead
- make `Next actions` pull the missing product facts

### 2. Template completion without real decisions

Trigger:
- the mode has many required sections, and the draft fills them mechanically

Failure signals:
- every section exists, but no tradeoff is visible
- recommendations use "use a card", "add CTA", "improve hierarchy" without saying why
- alternatives are absent or fake

Prevention:
- every major choice needs a chosen option, rejected alternative, and reason
- defaults must be named as defaults, not framed as decisions
- remove sections that only restate the template in different words

### 3. First-idea bias

Trigger:
- a familiar page type suggests an obvious pattern

Failure signals:
- hamburger nav, cards, modals, carousels, or accordions are chosen automatically
- a desktop table is collapsed to phone cards by reflex instead of by task fit
- no pattern matrix or heuristic is used
- losing alternatives are missing

Prevention:
- consult `docs/patterns-catalog.md` for pattern-level decisions
- state why the chosen pattern fits the task better than the plausible alternative
- in reviews, check whether the current pattern is solving the right problem

### 4. Aesthetic laundering

Trigger:
- user asks for "premium", "modern", "beautiful", "better design", or visual inspiration

Failure signals:
- style is used to hide weak hierarchy, missing states, or accessibility risk
- "clean", "delightful", or "premium" appears without a concrete mechanism
- moodboard sources become the reason for UX decisions

Prevention:
- translate style into size, spacing, alignment, color role, density, motion, or token decisions
- keep inspiration references separate from UX, platform, accessibility, and compliance rationale
- fix structure before visual character

### 5. Evidence overreach

Trigger:
- the task involves web-standard or browser behavior, accessibility, research, compliance, or benchmark claims

Failure signals:
- "HTML requires", "Safari mandates", "research proves", or "WCAG compliant" without evidence
- a Lighthouse/axe result is treated as a compliance verdict rather than a recommendation to verify
- user-provided claims are echoed as verified facts
- exact metrics or conversion lifts appear without a cited source or provided data

Prevention:
- separate `Known from input`, `Assumption`, `Recommendation`, and `Cannot verify`
- frame unsourced guidance as recommendation, not rule
- never claim compliance unless the user provided verified evidence for the exact artifact and state

### 6. Responsive flattening

Trigger:
- multi-breakpoint request or unspecified breakpoint/browser scope

Failure signals:
- the same layout is poured into every breakpoint with no behavior change
- there is no working 320px reflow, or the page two-dimensionally scrolls on small viewports
- hover/`:focus-visible` operability is ignored, or a desktop table is reflexively collapsed to phone cards regardless of task
- desktop density is wasted (a phone layout stretched across a wide viewport) instead of exploited
- browser/engine differences (form controls, scrollbars, back-forward cache, font rendering) are ignored

Prevention:
- share structure first, then specify behavior changes across the breakpoint ladder (not just visual reflow)
- verify the 320px reflow and 200% zoom; exploit desktop density where the task rewards it
- gate non-trivial features against caniuse / MDN Baseline and name the fallback
- treat hover, right-click, and keyboard operability as required web affordances, not problems

### 7. Context blindness

Trigger:
- task includes audience, domain, risk, or use-context signals

Failure signals:
- older adults, children, regulated domains, power users, low-bandwidth, keyboard-only/screen-reader, or wide-viewport contexts produce the same answer as a generic consumer site
- high-trust flows use playful patterns without justification
- dense comparison tasks (pricing tables, dashboards) are made sparse by default

Prevention:
- apply `docs/context-defaults.md`
- resolve conflicts in the documented order: safety/accessibility > regulated domain > use-context > audience > breakpoint/browser
- make density a task decision, not an aesthetic decision

### 8. Happy-path-only design

Trigger:
- flows, specs, onboarding, checkout, verification, payment, or form-heavy screens

Failure signals:
- default state is described, but empty/loading/error/partial/success states are absent
- recovery paths say "retry" without data persistence, user messaging, or next state
- back/forward and URL state are vague

Prevention:
- define default, loading, empty, error, success, disabled, and partial states where relevant
- name the main failure mode and the user's recovery path
- preserve user-entered data unless there is a clear safety reason not to

### 9. Weak design-quality calibration

Trigger:
- the output proposes, reviews, specifies, or rationalizes a visual artifact

Failure signals:
- visual hierarchy is asserted but not built through size, spacing, alignment, contrast, density, or position
- design quality section reads like an essay, not implementation guidance
- no production checks for large text, dark mode, contrast, state coverage, or tokens
- peer cards/tiles in a row render at ragged, content-driven heights, or their internal rows (title, description, CTA) don't line up across siblings, so bottom edges and footer CTAs do not align

Prevention:
- apply `docs/design-quality.md`
- define attention path, composition/spacing, typography, color/state, interaction polish, and production checks
- give peer tiles in a row a shared height (grid/flex `stretch`) and align their internal rows across siblings with subgrid (shared title/body/footer tracks), not just `margin-top: auto` on the footer; carry any single-tile emphasis through color/border/badge, not height
- keep the calibration concise and buildable

### 10. Visual overclaim in reviews

Trigger:
- Mode D with text description only or incomplete visual evidence

Failure signals:
- review asserts spacing, visual weight, contrast, balance, color, or target size from text alone
- severity is based on taste instead of user impact
- no real strength is identified

Prevention:
- classify D1/D2/D3/D4 explicitly
- for D2, restrict findings to structure and behavior; move visual uncertainty to `Unresolved assumptions`
- include at least one genuine strength

### 11. Weak handoff and buildability

Trigger:
- UI spec, typography system, design rationale, or engineering handoff request

Failure signals:
- component names do not map to a design system, native element, or explicit assumption
- spacing and typography are relative, not token-ready
- states and accessibility semantics are implied

Prevention:
- use concrete values, tokens, states, behavior rules, and QA checks
- identify implementation risks such as text scaling, focus order, analytics, state persistence, and performance
- keep open questions genuinely blocking or undecided
- when the handoff is code, ship a clean build: the source keeps its comments; the delivered bundle has no comments, debug flags, TODO/MVP markers, placeholder domains, credits to inspiration sources, or editor metadata and EXIF in images; tests run against that bundle

### 12. Overlong process theater

Trigger:
- ambiguous design request where the model compensates with methodology

Failure signals:
- long design-thinking explanation replaces the requested artifact
- sections are verbose but low-information
- `Next actions` are generic project-management verbs

Prevention:
- produce the artifact first
- keep theory only when it changes a decision
- make next actions concrete, observable, and tied to missing information or validation

---

## Mode risk map

| Mode | Most likely weaknesses | Required prevention |
|------|------------------------|---------------------|
| A. Page concept | generic artifact, first-idea bias, weak design-quality calibration | singular task, hierarchy order, states, alternatives, quality calibration |
| B. User flow | happy-path-only design, responsive flattening, invented business rules | end-to-end success path, URL/back-forward behavior, failure/recovery paths, assumptions |
| C. UI spec | weak handoff, template completion, responsive flattening | concrete states, behavior rules, tokens/values, breakpoint + browser implementation notes |
| D. Review | visual overclaim, severity-by-taste, no strengths | D sub-case, evidence limits, user-impact severity, actionable fixes |
| E. Typography/spacing | aesthetic laundering, weak buildability, accessibility afterthought | type roles, numeric scale, fluid scaling, target-size implications |
| F. Rationale/handoff | reverse-engineered rationale, fake validation, weak implementation notes | decisions with alternatives, validation method/metric, engineering concerns |
| G. Marketing/CRO | aesthetic laundering, evidence overreach, performance ignored | single CTA + hierarchy, specific proof, Core Web Vitals, mechanisms not lift % |

---

## Minimum weakness preflight

Before returning any response, silently answer:

- What weakness is this task most likely to trigger?
- Did I make any claim that the input does not support?
- Did I choose a pattern, density, or visual direction because it is familiar rather than because it fits?
- Did I define the states and recovery paths the artifact needs?
- Did I separate facts, assumptions, recommendations, and unverifiable items?
- Would a designer or engineer know what to change, build, or validate next?

If any answer is weak, revise before returning.
