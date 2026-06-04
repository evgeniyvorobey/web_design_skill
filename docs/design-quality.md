# Design Quality Calibration

This layer turns "make it good" into concrete, buildable mechanisms. It improves visual hierarchy, composition, typography, color, density, interaction polish, brand expression, and production readiness — **without** replacing usability and accessibility reasoning. A high visual score never compensates for missing states, weak hierarchy, or inaccessible interaction.

Use it whenever a response proposes, specifies, reviews, or rationalizes a web artifact. Score the result with the 1–5 system in [`design-quality-rubric.md`](design-quality-rubric.md). Translate every quality claim into a mechanism (size, spacing, alignment, contrast, density, color role, motion duration, state treatment, or token); avoid taste words unless they cash out in implementation.

---

## Quality dimensions

Eight dimensions, each with the mechanisms that move it on web:

1. **Attention path & hierarchy** — what the eye lands on first, second, then acts on. Mechanisms: above-the-fold composition, F/Z scan alignment, one dominant element per viewport, size/weight/color contrast, position in the reading order, a single primary CTA. On long-scroll pages, hierarchy is *per section* as well as per page.
2. **Composition & spacing** — grouping, alignment, rhythm, and responsive placement. Mechanisms: the 4px spacing scale, a 12-column grid with consistent gutters, proximity grouping, alignment to a baseline, **responsive placement** across the breakpoint ladder (where elements land at 320 vs 768 vs 1280), and whitespace that scales up with viewport rather than stretching line length.
3. **Typography craft** — role-based type that reads and scales. Mechanisms: a defined type scale, fluid `clamp()` sizing, ~65ch measure, 1.5 body line-height, weight discipline, and **web-font loading craft** — `font-display: swap`, preloaded above-the-fold faces, and fallback-metric matching so the FOUT swap does not shift layout.
4. **Color, state & contrast** — semantic roles that survive themes. Mechanisms: color roles (not raw hex sprinkled in), WCAG-passing contrast, non-color cues, a real `prefers-color-scheme` dark theme, `forced-colors` survival, and complete state colors (hover/focus/active/error/success).
5. **Density & rhythm** — information per screen matched to the task. Mechanisms: density presets (comfortable/compact), repeated spacing rhythm across components, and exploiting **desktop density** where the task rewards it (real tables, multi-pane, inline actions) instead of artificially sparse layouts.
6. **Interaction polish & motion** — feedback that confirms and never blocks. Mechanisms: hover/`:focus-visible`/active/loading/saving/success/error feedback within ~100ms, 150–300ms easing, optimistic UI, skeletons over spinners, and `prefers-reduced-motion` honored.
7. **Context & brand fit** — visual language that fits trust, domain, and the marketing-vs-app spectrum. Mechanisms: brand color/type expressed through tokens, restraint in high-trust flows, expressive editorial craft on marketing surfaces, dense utilitarian craft on app surfaces — without overriding semantics.
8. **Production readiness** — buildable, tokenized, QA-able. Mechanisms: token-ready values, component/state mapping, responsive behavior across breakpoints, semantic HTML + heading outline, Core Web Vitals budget, and an axe-clean / keyboard-pass expectation.

## Distinctiveness levers

A page can be competent on all eight dimensions and still be forgettable. Distinctiveness is earned through deliberate, owned choices — not random novelty:

- **One owned visual asset** — a signature type pairing, an owned accent color used with discipline, a custom illustration/iconography system, or a recurring motion signature.
- **A signature moment** — one place where craft is concentrated (a hero treatment, an empty-state illustration, a satisfying success animation) that a competitor's template would not have.
- **Editorial point of view** — content rhythm and voice that match the brand, especially on marketing/content surfaces.
- **Considered density** — choosing to be denser or calmer than the category default *for a reason*, and owning it consistently.

Distinctiveness must never come at the cost of semantics, contrast, reduced-motion, or keyboard operability. An owned asset that fails accessibility is not an asset.

## Inert / faceless test

Apply this before settling on a 4/5:

> If this page lost its logo and brand color, would it still be distinguishable from a competitor's template?

If the answer is no, the page is **inert** — competent but faceless. Cap it at **3/5 with an upside note** (not a quiet 4/5) until it carries at least one owned distinctive asset or a justified signature moment. This test matters *more* on web than on native apps: the web is a sea of near-identical component-library templates, and an inert page reads as generic even when every metric passes. Inertness is a hierarchy/brand observation, not a license to add decoration over weak structure.

## Calibration template

When packaging a design artifact, include a concise calibration (this is the block the modes emit):

```md
## Design quality calibration
- Quality target: 4/5 — [what's solid, what still needs validation]
- Attention path: [first glance → second glance → primary action]
- Composition and spacing: [grid, spacing-scale values, responsive placement across breakpoints]
- Typography: [roles, clamp() range, measure, line-height, font-loading note]
- Color and state: [semantic roles, contrast, dark-theme + forced-colors note, state colors]
- Interaction polish: [feedback timing, motion budget, reduced-motion fallback]
- Production checks: [tokens, states, breakpoints, semantic outline, CWV budget, axe/keyboard pass]
```

Keep it tight and buildable — it should make the design more implementable, not turn the answer into a visual-design essay. Feed the result into [`design-quality-rubric.md`](design-quality-rubric.md) for the 1–5 score, and check it against the numbers in [`quality-bars.md`](quality-bars.md).
