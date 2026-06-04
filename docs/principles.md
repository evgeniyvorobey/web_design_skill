# Design Principles

This skill enforces a practical set of website UI/UX design principles.

---

## 1. Start with user task clarity

A web page should make the user's primary task obvious — above the fold, and per scroll section on long pages.

Design quality starts with:
- knowing what the user is trying to do
- reducing competing priorities on the page (one dominant element per viewport)
- sequencing content by task relevance, not visual prominence

A visually polished page that obscures the main task is still a bad page.

---

## 2. Design for context of use

Web use spans wildly different conditions:
- viewport sizes from a 320px phone to an ultrawide monitor
- mouse, keyboard, and touch — often on the same session
- variable bandwidth and CPU
- interrupted attention and multi-tab workflows
- anonymous first visits and returning authenticated sessions

Recommendations should reflect actual use context across the breakpoint ladder and input methods, not a single studio-perfect desktop mockup.

---

## 3. Treat usability as effectiveness, efficiency, and satisfaction

Good UI/UX is not personal taste. Usability must consider:
- can the user complete the task?
- can they complete it with reasonable effort (and with a keyboard alone)?
- does the interaction remain understandable and confidence-building?

This is especially important when comparing competing layout or flow choices.

---

## 4. Accessibility is part of interaction design

Accessibility is not a final checklist layered on top of finished UI. It must influence:
- semantic structure and heading outline
- navigation structure and component behavior
- keyboard operability: tab order, visible focus, focus management, focus trap and restore
- target sizing and pointer-aware interaction
- text resizing (rem, 200% zoom, text spacing)
- readable hierarchy, contrast, and non-color cues
- error recovery and `aria-live` status

The skill assumes accessibility is always relevant unless the user explicitly narrows scope. Keyboard operability is mandatory, not optional.

---

## 5. Typography is a usability system

Typography affects scanability, reading speed, confidence, emphasis, error comprehension, and density tolerance. Guidance must cover:
- type roles
- hierarchy and scale (fluid `clamp()`)
- rem-based scaling and a capped measure (~65ch)
- weight, line-height, and spacing relationships
- web-font loading (swap, preload, no-CLS fallback metrics)

The skill rejects random font-size soup disguised as "creative direction."

---

## 6. Spacing and layout are structural, not cosmetic

Spacing and grid help users parse grouping, priority, interaction zones, density, and rhythm. A spacing system (4px base) and a grid (12-column desktop) should support repeatable decisions, not one-off nudges. Whitespace scales up with the viewport rather than stretching line length.

---

## 7. Respect web conventions and the two scope axes

Users learn patterns from the web (Jakob's Law). Respect link-vs-button semantics, native control behavior, and back/forward expectations.

Every answer carries two scope axes:
- **Responsive/breakpoint scope** — behavior must change deliberately across the ladder, not pour one layout into every width.
- **Browser/engine scope** — gate non-trivial features against Baseline/`caniuse` and name fallbacks; respect engine-specific behavior.

Share structure first, then specify where behavior diverges across breakpoints or engines.

---

## 8. Edge states are part of the design

A design is incomplete if it only covers the happy path. Every serious output should consider:
- empty, loading, error, validation, partial-success, and recovery states
- web system states: 404, 500, offline / network-lost, session-expired

Offline support is conditional (PWA / service worker), not a default state — pair it with the other error states.

---

## 9. Performance is a design constraint

Speed is part of usability. Design with the Core Web Vitals budget in mind: protect the LCP candidate, prevent layout shift (CLS), and keep interactions responsive (INP). A page that looks great but loads slowly or shifts under the user has failed a real quality bar.

---

## 10. Explainability matters

Strong design output should be explainable through user goals, task structure, web conventions, accessibility, performance, system consistency, and implementation constraints. If a recommendation cannot be justified beyond taste, it is not strong enough for this skill.

---

## 11. Prefer durable guidance over trends

Use long-lived guidance before trend language. Prefer open-web standards (WHATWG HTML, WAI-ARIA APG, WCAG), maintained design systems, established research, measurement tooling, and scalable token/component thinking. Avoid vague premium/minimal/modern language, arbitrary visual trends, unsupported UX claims, and decorative solutions to structural problems.

---

## 12. Structure output so teams can build from it

The skill should produce output that is useful in design exploration, critique, product review, engineering handoff, design-system alignment, and accessibility/performance review preparation. Useful output is explicit, scoped, structured, assumption-aware, and implementation-friendly.
