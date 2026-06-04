# Clarification Policy

This document defines when the skill should ask clarifying questions and when it should proceed with labeled assumptions.

The policy exists to prevent two opposite failures:

- blocking useful work with unnecessary questions
- producing overconfident design output when a missing answer would materially change the recommendation

---

## Core rule

Ask only when the missing information would change the design decision in a meaningful way.

If the missing information only improves precision, proceed with the smallest safe assumption and surface the missing input in `Assumptions`, `Open questions`, `Unresolved assumptions`, or `Next actions`.

---

## Clarification decision tree

### 1. Is the user asking for an artifact now?

If yes, prefer producing the artifact with minimal assumptions unless a blocker exists.

Examples:

- page concept
- flow
- responsive UI spec
- review
- typography/spacing/grid system
- handoff rationale
- marketing landing page

Do not ask a discovery-style questionnaire before producing useful work.

### 2. Would a wrong assumption create a misleading or unsafe recommendation?

Ask before proceeding when the answer materially affects:

- breakpoint or browser behavior (e.g., a feature gated behind Baseline support)
- regulated or high-trust domain handling
- accessibility-sensitive constraints
- destructive or irreversible actions
- payments, identity, healthcare, legal, financial, or safety-critical flows
- whether visual review is possible from the provided evidence
- whether the surface is a marketing page or a dense web app (the marketing-vs-app split)

### 3. Can a conservative default safely cover the missing information?

Proceed with assumptions when:

- the scope can be treated as responsive (working down to 320px) on evergreen engines without hiding meaningful differences
- the audience can be treated as general consumer
- the design can be treated as desktop-first with a working mobile-web layout
- the missing brand direction does not affect core usability
- exact product policy can be flagged as an assumption
- a provisional review can be limited to structure and behavior

### 4. Is the user explicitly asking for precision?

Ask targeted questions when the user requests:

- pixel-perfect specification
- production-ready implementation guidance for specific engines
- critique of a visual artifact without providing the visual or a rendered URL
- accessibility/compliance review without evidence
- benchmark or inspiration references for a specific style or market
- domain-specific design decisions where policy or regulation matters

---

## Blocking vs non-blocking missing information

| Missing information | Default behavior |
|---------------------|------------------|
| Breakpoint/browser scope unspecified for a simple concept | Proceed with `Assumption: Responsive, working down to 320px on evergreen engines unless legacy support is specified.` |
| Browser scope unspecified for a non-Baseline feature (container queries, `:has()`, `<dialog>`) | Ask one question or gate the feature with a named fallback. |
| Product/domain missing | Ask if the primary task cannot be inferred; otherwise proceed with a structural placeholder labeled as provisional. |
| Primary user task missing | Ask, because hierarchy and component choice depend on task. |
| Audience missing | Proceed with general consumer defaults unless age, accessibility, risk, or domain makes it material. |
| Rendered artifact / screenshot missing for visual review | Proceed only with structure/behavior review; mark visual quality as unverifiable. |
| Compliance evidence missing | Do not ask for audits by default; state that compliance cannot be verified and recommend an axe + keyboard pass. |
| Business policy missing | Proceed with explicit assumption if the policy is not the design decision; ask if it changes flow/state behavior. |
| Brand direction missing | Proceed with neutral/accessible design unless the user asks for brand or visual exploration. |
| Data model missing for UI spec | Ask if states, fields, or permissions cannot be safely inferred. |

---

## How many questions

Ask at most **three** clarifying questions at once.

Order them by decision impact:

1. blocker that changes the mode or the breakpoint/browser scope
2. blocker that changes the primary task or flow
3. blocker that changes safety, accessibility, compliance, or implementation

Do not ask cosmetic questions before structural questions.

---

## Clarification response format

When clarification is required before a reliable artifact can be produced, use this compact structure:

```md
Mode: [best inferred mode]
Responsive/breakpoint scope: [known / unspecified / assumed]
Browser/engine scope: [known / unspecified / assumed]
Assumptions:
- [what is known]
- [what cannot be safely assumed]

## Clarifying questions
1. [blocking question]
2. [blocking question if needed]
3. [blocking question if needed]

## Why this blocks
- [short reason tied to task/breakpoint/browser/accessibility/implementation]

## Fast path
- If you want a provisional draft now, I can proceed with: [smallest safe assumption].

## Next actions
- Answer the questions above, or confirm the fast-path assumption.
```

This format is an exception to producing the full mode artifact. It still preserves the mode, scope axes, assumptions, and next-action contract.

---

## Proceed-with-assumptions pattern

When the missing information is not blocking, produce the artifact and include:

```md
Assumptions:
- [minimal assumption]
- [what the user can correct later]
```

Then include one of:

- `Unresolved assumptions` for review/spec uncertainty
- `Open questions` for handoff uncertainty
- `Next actions` for practical follow-up

Do not stop the workflow just to ask questions that can safely be handled this way.

---

## Examples

### Blocking

Prompt:

```text
Review this page for color contrast and spacing.
```

No screenshot, rendered URL, or visual description is provided.

Correct behavior:

- classify as Mode D
- ask for the rendered URL, screenshot, or a detailed visual description
- offer a fast path: structure-only review if the user describes the layout

### Non-blocking

Prompt:

```text
Design a profile edit page.
```

Correct behavior:

- proceed with a responsive, desktop-first assumption working down to 320px
- state that product/domain and audience are unknown
- keep the concept structural and avoid over-specified brand or browser behavior
- ask for product/domain in `Next actions`

### Mixed

Prompt:

```text
Create a production-ready UI spec for a medication refill page.
```

Correct behavior:

- proceed only if the output can stay policy-safe
- ask or flag blockers around medication safety states, refill eligibility, pharmacy pickup/delivery, and the breakpoint/browser scope
- avoid inventing clinical, legal, or pharmacy rules

---

## Self-review prompt

Before returning, silently answer:

- Did I ask only questions that materially change the recommendation?
- If I proceeded with assumptions, are they minimal and clearly labeled?
- If I asked questions, did I keep them to three or fewer?
- Did I avoid asking cosmetic questions before task/scope/safety blockers?
- Did I offer a fast path when a provisional draft would still be useful?

If any answer is no, revise before returning.
