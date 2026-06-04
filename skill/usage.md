# Usage Guide

This guide explains how to invoke `web-design-skill` in Claude Code or Codex.

---

## Quick start

Load `SKILL.md` as the active instruction set, then provide a design task.

If you want the expanded reference pack available during use, keep these files nearby:

- `skill/skill.md`
- `skill/modes.md`
- `skill/templates.md`
- `docs/sources.md`
- `docs/workflow.md`
- `docs/clarification-policy.md`
- `docs/judged-mode.md`
- `docs/principles.md`
- `docs/guardrails.md`
- `docs/quality-bars.md`
- `docs/context-defaults.md`
- `docs/heuristics.md`
- `docs/patterns-catalog.md`
- `docs/design-quality.md`
- `docs/design-quality-rubric.md`
- `docs/golden-examples.md`
- `docs/synthetic-case-studies.md`
- `docs/domain-packs/index.md`
- `docs/weaknesses.md`
- `docs/inspiration-sources.md`
- `docs/visual-benchmark-playbooks.md`
- `docs/benchmark-report-format.md`
- `docs/visual-review-fixtures.md`
- `docs/rendered-output-qa.md`
- `docs/self-review.md`

The skill will:

1. classify the request into one mode
2. determine the two scope axes (responsive/breakpoint and browser/engine)
3. identify missing information
4. apply clarification policy: ask only blocking questions, otherwise proceed with assumptions
5. apply judged mode when invoked with `--judge`
6. make only minimal labeled assumptions
7. return a structured mode-specific output
8. include accessibility and keyboard operability by default
9. include design-quality calibration for visual hierarchy, rhythm, craft, and production readiness when producing design artifacts
10. apply a 1-5 design-quality rubric, targeting 4/5 for generated artifacts and exposing the current score in reviews
11. use `examples/evals/`, `examples/rubric-before-after.md`, `examples/golden/`, and `examples/case-studies/` as calibration references when tuning quality and taste
12. use domain packs for marketing/landing, ecommerce, content/publishing, docs/dev-portal, and web-app/dashboard when the product category materially changes risk, hierarchy, state coverage, or trust language
13. use visual benchmark playbooks and benchmark report format to keep references separate from evidence claims
14. use visual-review fixtures to calibrate text-only review discipline and avoid unsupported visual overclaims
15. use rendered-output QA only after a rendered artifact exists; do not block normal design generation waiting for screenshots or builds
16. use `scripts/run_rubric_judge.py` for provider-agnostic LLM-as-judge calibration, including external-agent command runs
17. run known-weakness preflight from `docs/weaknesses.md` to avoid generic output, first-idea bias, evidence overreach, responsive flattening, happy-path-only design, and weak handoff
18. keep inspiration references separate from UX, accessibility, and web-convention rationale when inspiration is requested

---

## Minimal prompt pattern

```text
Use the web-design-skill.

Task: [describe the request]
Breakpoints: [mobile-web / tablet / desktop / wide / unknown]
Browsers: [evergreen Chromium/WebKit/Gecko / specific / unknown]
User goal: [goal]
Context: [audience, product, constraints]
```

---

## Recommended prompt pattern

```text
Use the web-design-skill.

Task:
Create a responsive UI spec for an invoice detail page in a small-business billing web app.

Inputs:
- Product: small-business invoicing web app
- User goal: review invoice status and send a reminder
- Breakpoints: desktop-first, must work down to 320px
- Browsers: evergreen Chromium/WebKit/Gecko
- Audience: busy owners with moderate financial literacy
- Page type: detail page with a line-item table
- Constraints: dense content, keyboard-operable, accessibility-sensitive, existing token system
- Current wireframe: header with status, totals, line-item table, activity timeline, action row
```

---

## Choosing the right mode intentionally

You can let the skill classify automatically, or specify intent directly.

### Generate web page concept
Use for new pages, early structure, and component/layout direction.

```text
Design a first-pass concept for a SaaS pricing page.
```

### Design web user flow
Use for onboarding, checkout, signup, verification, and multi-step tasks across views.

```text
Map the web user flow from signup to first activated workspace.
```

### Create responsive UI spec
Use for turning wireframes into structured, breakpoint-by-breakpoint specs.

```text
Turn this wireframe into a responsive UI spec for desktop and mobile-web.
```

### Review page for usability/accessibility
Use for critiquing existing pages and prioritizing fixes.

```text
Review this account settings page for usability, keyboard operability, and accessibility.
```

### Create typography, spacing and grid system
Use for type roles, fluid scale, spacing, grid, and density guidance.

```text
Create a typography, spacing and grid system for a documentation site.
```

### Prepare design rationale / handoff
Use for documenting decisions and engineering handoff.

```text
Prepare a design rationale and handoff for this dashboard redesign.
```

### Generate / critique a marketing landing page (conversion / CRO)
Use when the primary job is persuasion and conversion.

```text
Critique our landing page and propose changes to improve signups.
```

---

## Input quality tips

The skill works best when the prompt includes product or domain, user goal, breakpoint and browser targets, page or flow scope, constraints, audience, and a current wireframe summary if available. It will still proceed with minimal labeled assumptions when context is missing.

---

## Good example prompts

### Example 1
```text
Use the web-design-skill.

Create a web page concept for a flight-booking results page.
Breakpoints: desktop + mobile-web
Audience: travelers comparing options under time pressure
Constraints: faceted filters, URL-shareable state, accessibility-sensitive
```

### Example 2
```text
Use the web-design-skill.

Design the flow for resetting a forgotten password in an enterprise web app.
Constraints: regulated environment, passkeys + MFA, session-expiry handling, older employee base
```

### Example 3
```text
Use the web-design-skill.

Review a profile edit page.
Page description:
- avatar at top
- long single-column form
- save button at the very bottom
- optional fields mixed with required
- weak inline error messaging
Constraints: accessibility-sensitive, keyboard-operable
```

### Example 4
```text
Use the web-design-skill.

Generate a marketing landing page concept for a premium habit-tracker web app and include inspiration references.
Audience: general consumer
Constraints: calm visual direction, reduced-motion respected, accessibility-sensitive, fast LCP
```

---

## What the skill will not do

The skill will not invent web standards or browser behavior, invent validated research, claim verified accessibility compliance without evidence, block useful output with nonessential questions, provide aesthetic-only advice, return a section-complete response with no real decisions, or ignore typography, spacing, navigation, keyboard operability, or states.

---

## Interpreting the output

Every response starts with `Mode:`, `Responsive/breakpoint scope:`, `Browser/engine scope:`, and `Assumptions:`, and ends with `Next actions:`. This makes outputs easy to reuse in product docs, design reviews, tickets, or handoff notes.

---

## Best practices for teams

1. keep prompts tied to a user task, not just a page name
2. include constraints and the breakpoint/browser scope early
3. state when keyboard-first or dense desktop behavior matters
4. use the review mode before final handoff
5. use the rationale mode after major design changes
6. use the typography/spacing/grid mode before components drift into chaos
