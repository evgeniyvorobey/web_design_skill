# Benchmark report (web)

A synthetic example of turning 3–5 web references into design direction without copying screens, layouts, or brands. Follows [`../docs/benchmark-report-format.md`](../docs/benchmark-report-format.md).

## Prompt

```text
Use the web-design-skill.

We're redesigning the pricing page for our B2B SaaS. Make it feel premium and trustworthy and
help more visitors start a trial. Here are references I like:
- Linear pricing (clean, dense, confident)
- Stripe pricing (clear plan comparison)
- Vercel pricing (bold type, good hierarchy)
Breakpoints: desktop + mobile-web. Browsers: evergreen.
```

## Report output

```md
## Context
- Product/task: B2B SaaS pricing page redesign
- Breakpoints / browsers: desktop + mobile-web; evergreen Chromium/WebKit/Gecko
- Audience: evaluators and decision-makers comparing plans
- Design goal: clearer plan comparison + more trial starts
- Constraints: accessibility-sensitive, fast LCP, existing tokens
- What references can influence: hierarchy, comparison-table craft, type scale, CTA placement
- What references cannot decide: which plan structure converts, accessibility, performance

## References table
| # | Source | Name | Link | Why relevant | Known limitations |
| --- | --- | --- | --- | --- | --- |
| 1 | Production UI | Linear pricing | unavailable | dense, confident comparison craft | unknown a11y/perf; different IA |
| 2 | Production UI | Stripe pricing | unavailable | clear plan comparison + feature rows | broader product than ours |
| 3 | Production UI | Vercel pricing | unavailable | bold type hierarchy, scannable | marketing tone may not fit B2B trust |

## Borrow
- Mechanism to borrow: a sticky comparison-table header so plan columns stay labeled while scrolling features.
- Why it fits: long feature lists lose their column headers; sticky headers keep comparison legible.
- How to adapt it: build it as a real `<table>` with `<th scope="col">` and `aria-sort`, sticky via `position: sticky`.

## Do not copy
- Surface detail to avoid: a competitor's exact plan names, color palette, or hero illustration.
- Reason: brand mimicry erodes trust and risks IP issues; it does not transfer their (unknown) conversion.
- Safer alternative: derive a plan structure from our own packaging and express it with our tokens.

## Translate to tokens/components/states
- Tokens: type scale (plan price `clamp()`), spacing scale (4px base), semantic "recommended plan" accent.
- Components: comparison table, plan card, feature-row, billing toggle (monthly/annual), CTA button.
- States: hover/focus-visible on rows and CTAs; loading on plan fetch; empty (custom/enterprise) path; error.
- Motion/interaction: 150–250ms toggle transition with reduced-motion fallback.
- Content rules: benefit-led feature labels; one "recommended" plan, marked with text + badge, not color alone.
- QA checks: 320px reflow (table → stacked cards), axe pass, contrast on the accent, LCP under budget.

## Evidence boundaries
- Inspiration only: visual hierarchy, table craft, type scale, CTA placement.
- Evidence needed elsewhere: which plan structure converts (an A/B test), not these references.
- Platform/accessibility checks: keyboard table navigation, `aria-sort`, contrast, 320px reflow — verified independently.
- Compliance or domain checks: pricing/legal copy reviewed by the business; references cannot decide it.

## Risks
- Design risk: copying a dense competitor table that does not fit our 3-plan structure.
- Product risk: optimizing aesthetics over plan clarity.
- Accessibility risk: a "pretty" comparison table that is not keyboard-navigable.
- Implementation risk: sticky + virtualization edge cases in WebKit.
- Research gap: no real conversion data; trial-start lift is a hypothesis.

## Next actions
- Immediate design decision: 3 plans + a sticky-header comparison table.
- Prototype task: build the table component with `aria-sort` and the 320px card reflow.
- Validation task: A/B the billing toggle default and the recommended-plan emphasis.
- Open question: is an enterprise "contact us" a fourth column or a separate band?
```

These references inform visual range only. The recommendation stands on plan clarity, accessibility, and performance — not on the references — and would survive if every reference disappeared.
