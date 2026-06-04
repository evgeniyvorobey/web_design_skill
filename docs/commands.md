# Command Reference

This skill supports two invocation styles, depending on the host:

- in Claude Code: invoke it directly with `/web-design-skill`
- in Codex: use the installed skill normally via `Use the web-design-skill...` or `$web-design-skill`, depending on your Codex surface

The seven operating modes below behave like reusable commands once the skill is active.

---

## How to invoke the skill

### Claude Code

A skill at `.claude/skills/<skill-name>/SKILL.md` can be invoked with `/skill-name`. For this repository, the direct command is:

```text
/web-design-skill
```

With inline arguments:

```text
/web-design-skill create a responsive UI spec for an order-tracking page
```

With judged mode:

```text
/web-design-skill --judge create a responsive UI spec for a billing dashboard
```

`--judge` asks the skill to draft privately, run an independent rubric judge pass in the same session when the host supports subagents, revise if needed, and return the final answer with a compact `Judge summary`. It should not require the user to run a separate script manually. See [`judged-mode.md`](judged-mode.md).

This repository includes the Claude Code wrapper at:

- [`.claude/skills/web-design-skill/SKILL.md`](../.claude/skills/web-design-skill/SKILL.md)

### Codex-style invocation

```text
Use the web-design-skill.

Task: [what you need]
Breakpoints: [mobile-web / tablet / desktop / wide / unknown]
Browsers: [evergreen / specific engines / unknown]
User goal: [goal]
Context: [product, audience, constraints]
```

### Codex short explicit invocation

```text
Use the web-design-skill.

Review this account settings page for usability and accessibility.
```

### Codex skill mention

```text
Use $web-design-skill to create a responsive UI spec for an order-tracking page.
```

### Compatibility note

This repository is packaged to support both products, but the invocation UX is not identical:

- Claude Code: `/web-design-skill`
- Codex: standard skill usage or explicit skill mention

---

## Important note

The skill classifies every request into exactly one primary mode. You can either ask explicitly for the mode you want, or describe the task and let the skill classify it automatically. Use `--judge` for higher-confidence outputs when the extra latency of an independent judge pass is acceptable.

---

## 1. Generate web page concept

Use this when you need a first-pass concept for a web page.

Best for: new pages, layout direction, hierarchy planning, component recommendations.

```text
Use the web-design-skill.

Generate a web page concept for a project overview page in a SaaS tool.
Breakpoints: desktop-first, must work down to 320px
Audience: project managers, frequent return users
Constraints: dense status data, keyboard-operable, accessibility-sensitive
```

Returns: page goal, primary user task, information hierarchy, layout structure, suggested components, interaction notes, empty/loading/error states, responsive and browser behavior, accessibility considerations, design quality calibration, rationale, next actions.

---

## 2. Design web user flow

Use this when you need a multi-step task flow across views rather than a single page.

Best for: onboarding, checkout, signup, account recovery, verification flows.

```text
Use the web-design-skill.

Design a web user flow for guest checkout from cart to confirmation.
Breakpoints: mobile-web and desktop
Constraints: reduce abandonment, address + payment autocomplete, accessibility-sensitive
```

Returns: flow goal, entry points, ordered steps/views, decision points, back/forward and URL state, failure and recovery paths, responsive and browser behavior, accessibility and usability risks, simplification opportunities.

---

## 3. Create responsive UI spec

Use this when you know the page or flow and want an implementation-friendly spec across breakpoints.

Best for: turning wireframes into specs, preparing handoff, making states and behavior explicit.

```text
Use the web-design-skill.

Create a responsive UI spec for an admin users page with a sortable, selectable data table.
Breakpoints: desktop-first, usable on mobile-web
Constraints: thousands of rows, keyboard power-users, existing tokens
```

Returns: structural zones, components by section, state definitions, behavior rules, content guidance, spacing/typography rules, accessibility requirements, design quality requirements, responsive and browser implementation notes, key decision tradeoffs.

---

## 4. Review page for usability/accessibility

Use this when you have a page description, wireframe, rendered URL, or UI summary and want critique.

Best for: design review, accessibility-aware critique, finding usability problems, prioritizing fixes.

```text
Use the web-design-skill.

Review this account settings page for usability, keyboard operability, and accessibility.
Page description:
- long single-column form
- save button only at the bottom
- placeholders used as labels
- errors appear only after submit
Constraints: accessibility-sensitive, keyboard users common
```

Returns: sub-case (D1–D4), quick summary, strengths, causal findings (with the web lenses), current→projected design-quality score, severity index, optional bold move, convention mismatches, unresolved assumptions.

---

## 5. Create typography, spacing and grid system

Use this when you need a type, spacing, and grid foundation rather than a single page.

Best for: defining type roles, fluid scales, spacing, a grid, density guidance, token preparation.

```text
Use the web-design-skill.

Create a typography, spacing and grid system for a documentation website.
Audience: developers, scanning + deep reading
Constraints: long-form readability, code blocks, sidebar nav, accessibility-sensitive
```

Returns: type roles, size hierarchy, weight usage, line-height guidance, spacing scale, density rules, visual rhythm rules, pointer/target-size implications, accessibility considerations, usage examples.

---

## 6. Prepare design rationale / handoff

Use this when the design direction exists and you need to explain or package it for a team.

Best for: handoff notes, design rationale, cross-functional review, documenting why a solution was chosen.

```text
Use the web-design-skill.

Prepare a design rationale and handoff for a primary-navigation redesign (top nav + mega-menu on
desktop, off-canvas drawer on mobile-web).
Breakpoints: mobile-web through wide desktop
Constraints: SEO matters, accessibility-sensitive, existing tokens
```

Returns: design objective, target users and context, key decisions, pattern choices and why, design quality rationale, responsive and browser alignment, accessibility and usability considerations, states and edge cases, implementation notes, open questions, validation plan.

---

## 7. Generate / critique a marketing landing page (conversion / CRO)

Use this when the primary job is persuasion and conversion, not task completion.

Best for: landing pages, hero structure, scroll narrative, CTA hierarchy, social proof, conversion paths.

```text
Use the web-design-skill.

Critique our SaaS landing page and propose changes to improve free-trial signups.
Breakpoints: mobile-web and desktop
Constraints: fast LCP, reduced-motion respected, accessibility-sensitive, SEO matters
```

Returns: conversion goal and primary CTA, above-the-fold hero structure, scroll narrative, value-proposition hierarchy, social proof, CTA hierarchy, objection handling, accessibility, Core Web Vitals, SEO/shareability, design quality calibration, conversion-rate reasoning.

---

## How to write better prompts

The skill works best when your prompt includes product or domain, user goal, breakpoint and browser scope, page or flow scope, audience, constraints, and an existing wireframe or page summary if available. If some of that is missing, the skill proceeds with minimal labeled assumptions.

If the missing information would materially change the recommendation, the skill follows [`clarification-policy.md`](clarification-policy.md): it asks at most three blocking clarifying questions, explains why they matter, and offers a fast path when a provisional draft is still useful.

---

## What not to expect

This skill is not meant for pure visual inspiration, aesthetic-only feedback, fabricated UX research claims, fake accessibility compliance statements, or generic "make it more modern" advice. It is designed for structured, explainable, implementation-friendly website design output.
