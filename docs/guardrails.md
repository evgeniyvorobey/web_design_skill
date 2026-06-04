# Guardrails

These guardrails are mandatory for the skill.

---

## 1. Do not invent web standards or browser rules

Never state a web-platform or browser-specific rule unless it is grounded in actual standards/reference (WHATWG HTML, WAI-ARIA APG, MDN, WCAG) or expressed carefully as a recommendation.

Bad:
- "HTML requires this pattern."
- "Safari forbids that layout."

Better:
- "Prefer a native `<dialog>` with focus trap and ESC-to-close, per the WAI-ARIA APG modal dialog pattern."
- "This CSS feature is not yet Baseline across the named engines — gate it and provide a fallback."

---

## 2. Do not invent research findings or test results

Never claim "users prefer", "testing proved", "research shows", or a conversion lift, unless the user supplied actual evidence or the claim is presented as general established guidance without fabricated specificity.

Bad:
- "Users completed this 23% faster."
- "This hero lifted conversion by 18%."

Better:
- "This change is likely to improve scanability by clarifying hierarchy."
- "This should be validated through usability testing and a measured A/B test."

---

## 3. Do not claim accessibility compliance unless explicitly verified

Do not say compliant, WCAG-compliant, accessible, or passes accessibility unless the user has provided enough verified evidence and specifically asked for that assessment. A clean axe/Lighthouse run is evidence to verify, not a compliance verdict.

Better phrasing:
- "Supports accessibility better by..."
- "Potential accessibility risks include..."
- "Compliance cannot be verified from the provided description; an axe + keyboard + screen-reader pass is needed."

---

## 4. Do not give aesthetic-only advice

Every recommendation should have a usability, hierarchy, readability, navigation, accessibility, performance, or implementation reason.

Bad:
- "Make it more premium." · "Use more whitespace." · "Give it a modern feel."

Better:
- "Increase separation between the summary and secondary controls so the primary task is easier to scan."
- "Reduce type-style variation so the page has a stable reading hierarchy."

Carve-out for bold moves: a recommendation that contradicts the current product or direction is not aesthetic-only when it is justified by a named usability, accessibility, or hierarchy mechanism AND surfaced in the Mode D `Bold move` block with its tradeoff and validation path. Aesthetic-only contradictions ("make it premium", "feels dated") remain a failure.

---

## 5. Do not treat inspiration sources as evidence

Inspiration sources such as Awwwards, CSS Design Awards, Land-book, SiteInspire, Godly, Mobbin Web, Refero, Page Flows, Behance, Dribbble, Pinterest, and Figma Community can help with visual range and comparable examples.

They must not be used as proof of usability, accessibility, performance, web-convention correctness, compliance, user preference, or business effectiveness.

Bad:
- "This is the right checkout pattern because it appears on Dribbble."
- "Awwwards sites use this scroll animation, so it is safe."

Better:
- "The pattern is justified by task structure, web conventions, and accessibility requirements. Use Mobbin Web / Page Flows for comparable production flows and Awwwards / Land-book for visual exploration — then re-check contrast, reduced-motion, keyboard, and Core Web Vitals."

---

## 6. Do not use visual polish to hide weak product design

Visual craft matters, but it must make the design clearer, not merely more impressive. Do not use brand expression to hide unclear hierarchy, animation to distract from missing feedback states, illustration to replace useful empty-state guidance, or surface styling to compensate for poor grouping — and never "premium"/"modern" language without concrete mechanisms.

Better:
- "Use a stronger title/body contrast and 24px section spacing so the primary status is readable before secondary actions."
- "Use a restrained brand accent for the primary action only; keep error and warning colors semantic and paired with icon and text."

---

## 7. Do not ignore typography, spacing, navigation, keyboard operability, or state coverage

Even when the user focuses on visuals, the skill should still consider hierarchy, readability, density, spacing, target sizing, keyboard operability and focus management, navigation/URL recovery, performance, and state handling.

A page review that ignores typography is incomplete. A flow review that ignores back/forward recovery is incomplete. A UI spec that ignores spacing or keyboard operability is barely a spec at all.

---

## 8. Do not flatten breakpoints, browsers, or input types

If a difference matters across the breakpoint ladder, across browser engines, or across pointer types (coarse vs fine, hover vs no-hover):
- specify the behavior change (not just visual reflow)
- note why it differs and gate features against Baseline/`caniuse`
- keep the shared structure first when useful

Do not pour one layout into every breakpoint (responsive flattening), and do not assume a single input type — keyboard, mouse, and touch are simultaneous. Ignoring hover/focus/keyboard operability is the failure, not using them.

---

## 9. Do not invent components, flows, or states without labeling assumptions

If something is unknown, say it is assumed, keep the assumption minimal, and avoid inventing downstream logic as fact.

Bad:
- inventing SSO, faceted filters, passkey flows, or moderation states without noting assumptions

Better:
- `Assumption: authentication is already complete before this page.`
- `Assumption: the error state includes inline validation and a retry action.`

---

## 10. Do not overcomplicate when the user needs a design artifact

If the user needs a concept, a flow, a spec, a critique, a system, or a handoff note, produce the artifact directly. Do not bury the answer inside a lecture about design thinking.

---

## 11. Always separate fact from recommendation

Useful phrasing: `Known from input:`, `Assumption:`, `Recommendation:`, `Cannot verify from provided information:`. This keeps outputs honest and reusable.

---

## 12. Always include practical next actions

End every output with practical next steps such as: refine missing states, run an axe + keyboard pass, check a Lighthouse/CWV budget, verify 320px reflow, convert to tokens, align with engineering constraints, or run usability testing. Do not end with empty inspiration.

---

## 13. Do not return template-complete but decision-empty output

A response can satisfy the visible section structure and still fail the user. Watch for generic placeholders, recommendations that name components without choosing between alternatives, rationale that repeats the request, or output with no concrete state, behavior, typography, spacing, or validation implication.

Better: name the chosen option, name the rejected alternative where the decision matters, tie the reason to user task, web convention, accessibility, context, or implementation; if the input is too thin, narrow the artifact and state what cannot be decided yet. Use `docs/weaknesses.md` as the failure-mode map for this guardrail.

---

## 14. Do not let scores hide design risk

The 1-5 rubric in `docs/design-quality-rubric.md` is a quality tool, not a laundering mechanism. Do not average a serious accessibility, state, responsive, or evidence flaw into an acceptable-looking score; do not give 4/5 or 5/5 to a design with unresolved P0/P1 weakness; do not expose a precise visual quality score from text-only input without labeling evidence limits; do not use the score instead of explaining the concrete mechanism.

Better: apply the rubric caps (including the responsive-flattening and keyboard-inoperability caps), score the weak dimension explicitly, revise generated artifacts below 4/5 when context supports it, and attach review scores to a short evidence-based reason.

---

## 15. Do not ask unnecessary questions

Clarifying questions are useful only when the answer changes the recommendation. Do not ask a discovery questionnaire before producing a simple artifact, ask brand/style questions before task/breakpoint/browser/safety/accessibility/implementation blockers, ask more than three questions at once, or block a provisional draft when a safe assumption would work.

Better: apply `docs/clarification-policy.md`, proceed with the smallest labeled assumption when the gap is not blocking, ask one to three high-impact questions when the gap changes the design decision, and offer a fast path when the user can accept a provisional draft.
