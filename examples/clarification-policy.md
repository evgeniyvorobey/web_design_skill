# Clarification policy examples (web)

Three calibration examples of when to ask vs proceed with assumptions, per [`../docs/clarification-policy.md`](../docs/clarification-policy.md). Ask only when a missing answer would materially change the recommendation; otherwise proceed with the smallest labeled assumption and offer a fast path.

---

## Example 1: Blocking visual review

Prompt: "Is this hero accessible?" with a screenshot of text over a photographic background, no markup, no contrast values, no breakpoint stated.

This blocks because the core question (contrast, focus, reflow) cannot be answered from an image alone, and the answer changes entirely depending on the rendered values.

## Clarifying questions
1. Can you share the rendered URL or the markup/CSS so contrast and focus can be measured (not estimated)?
2. Which breakpoints must this hero support — does it need to work at 320px?
3. Is the headline real text or baked into the image (this decides the SEO and zoom answer)?

## Why this blocks
- Contrast over a photo cannot be verified from a static thumbnail; an axe/Playwright pass on the real render is required.
- Reflow and focus behavior are unknowable without markup or a URL.

## Fast path
- If you only need a directional read: assuming the headline is live text and the background is a mid-tone photo, add a solid scrim behind the text to reach ≥ 4.5:1 and a visible focus ring on the CTA — but treat this as provisional until a rendered pass confirms the numbers.

---

## Example 2: Non-blocking concept request

Prompt: "Design a dashboard home page for a SaaS analytics tool." No breakpoint, browser, or brand stated.

This does NOT block: a useful concept can be produced with minimal labeled assumptions, and a wrong assumption is cheap to correct.

## Clarifying questions
- None are blocking. Proceed with assumptions and surface them.

## Why this blocks
- It does not. The defaults (desktop-first dashboard, evergreen engines, general professional audience) are safe and stated, so producing the artifact beats interrogating the user.

## Fast path
- Proceed with: `Assumption: desktop-first dashboard working down to 320px, evergreen engines, neutral professional brand.` Note breakpoint/brand as confirm-or-correct items in Next actions.

---

## Example 3: Policy-sensitive spec

Prompt: "Spec the checkout page; we're PCI compliant and WCAG AA compliant, so just make it match." Compliance claims are asserted by the user.

This partially blocks: the design work can proceed, but the compliance claims must not be echoed as verified fact.

## Clarifying questions
1. Should card data stay inside the hosted/iframe field (so the page never touches PAN), or is there a custom card form to spec?
2. Has the WCAG AA conformance been verified by an audit, or is it a target? (This changes how I phrase accessibility claims.)

## Why this blocks
- Whether card entry is hosted vs custom changes the entire security and DOM model of the spec.
- Echoing "WCAG AA compliant" without verification would be an evidence-overreach failure; the spec must say "cannot independently verify" and recommend an axe + keyboard pass.

## Fast path
- Proceed assuming a hosted card iframe (the safer default) and frame accessibility as "designed to support WCAG 2.2 AA; conformance to be verified," then spec the page.
