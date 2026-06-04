# Source Hierarchy

This document ranks the sources the skill leans on, from most to least authoritative, and maps them to tasks. Higher tiers win when guidance conflicts. On the web, the platform *is* the open standards stack — there is no single vendor OS owner — so Tier 1 is the standards bodies and their reference documentation, not a design-award gallery.

A defining web rule: **measurement tooling is first-class evidence, not a final footnote.** Lighthouse, CrUX, axe-core, and Playwright produce reproducible, artifact-backed results about a real rendered page. They sit near the top of the evidence stack, above opinion and benchmark inspiration. (Inspiration galleries are a separate, non-authoritative layer — see [`inspiration-sources.md`](inspiration-sources.md).)

---

## Priority order

1. **Tier 1 — Web platform standards & reference**
   - WHATWG HTML Living Standard (semantics, forms, the `<dialog>`/popover platform)
   - W3C WAI-ARIA Authoring Practices Guide (APG) — the canonical pattern + keyboard-interaction reference
   - MDN Web Docs (HTML/CSS/JS/ARIA reference behavior)
   - web.dev / Chrome team guidance on Core Web Vitals and rendering
   - ECMAScript / CSS Working Group specs where behavior is contested

2. **Tier 2 — Accessibility, usability & measurement (primary)**
   - **WCAG 2.2** (AA primary, AAA on request) — promoted to a primary source on web; ARIA in HTML; ATAG where relevant
   - ISO 9241-210 (human-centered design) and 9241-11 (usability definition) for justification through context of use
   - **Tooling as evidence (first-class, not last):** Lighthouse / PageSpeed Insights / CrUX field data (performance, a11y, SEO), axe-core / WAVE (automated a11y), Playwright (cross-browser behavior, keyboard/focus capture, reflow), BrowserStack (real-device/engine matrix). Tool output is reproducible evidence about a specific build, not a substitute for human judgment.

3. **Tier 3 — Design systems & component libraries**
   - Public-sector / high-trust: **GOV.UK Design System, NHS Digital service manual, U.S. Web Design System (USWDS)** — strongest for clarity, forms, and task completion
   - Enterprise systems: **IBM Carbon, Shopify Polaris, Atlassian Design System, Microsoft Fluent (web), Material Web / Material 3 (web), Ant Design, Salesforce Lightning, GitHub Primer**
   - Utility / headless stack: **Tailwind CSS** (token discipline), **shadcn/ui** (composition patterns), **Radix Primitives / React Aria** (accessible behavior primitives)
   - Use these for component anatomy, states, and token structure — not as proof of usability for a specific product.

4. **Tier 4 — Research & domain references**
   - **Baymard Institute** (e-commerce / checkout UX research)
   - **Nielsen Norman Group** (usability + information architecture)
   - **Luke Wroblewski — Web Form Design** (forms, input, progressive disclosure) — promoted
   - Established case-study and IA literature

5. **Tier 5 — Browser support & capability data (gating, not ranking)**
   - **caniuse**, **MDN Baseline**, **Browserslist** — decide what is safe to ship to the named engines; pair every modern feature with a fallback or a Baseline note.

**Legal/regulatory (orthogonal, never a design substitute):** Section 508, the European Accessibility Act (EAA) and EN 301 549. These set obligations; they do not tell you a specific layout is "compliant" — only verified evaluation can.

When a Tier 3 design system contradicts a Tier 1/2 standard (e.g., a component with a 3:1 text contrast), the standard wins.

## Source application rules

- Use **WHATWG HTML + WAI-ARIA APG + MDN** for the correct element, role, and keyboard-interaction model before reaching for a library. Prefer native elements (`<button>`, `<dialog>`, `<details>`, `<a>`) over re-implemented ARIA widgets.
- Use **WCAG 2.2** for accessibility framing; cite specific success criteria (e.g., 1.4.10, 2.4.11, 2.5.8) rather than "accessible."
- Use **tooling output as evidence** when a claim is measurable: cite "Lighthouse LCP 3.1s / axe: 2 contrast violations / Playwright: focus lost on route change," not "feels slow / looks accessible." Treat tool output as a recommendation to verify, never as a compliance verdict.
- Use **public-sector systems (GOV.UK/NHS/USWDS)** when clarity, forms, error recovery, and high-trust task completion matter; use **enterprise systems** for dense app surfaces, tables, and design-token structure.
- Use **Baymard / NN/g / Wroblewski** for e-commerce, IA, and forms research framing — as research, not as guarantees of conversion.
- Use **caniuse / Baseline / Browserslist** to gate any non-trivial CSS/JS feature against the declared Browser/engine scope; name the fallback.
- Never invent a standard ("HTML requires…", "WCAG mandates…") without a citation or an explicit "recommendation" framing. See [`weaknesses.md`](weaknesses.md) (evidence overreach) and the clarification rules in [`clarification-policy.md`](clarification-policy.md).

## Source-to-task mapping

| Task | Primary sources |
|------|-----------------|
| Semantic structure, forms, overlays | WHATWG HTML, WAI-ARIA APG, MDN |
| Keyboard / focus / screen-reader behavior | WAI-ARIA APG, WCAG 2.2 (2.1.1, 2.4.3, 2.4.11), axe-core, Playwright |
| Contrast, reflow, text spacing, target size | WCAG 2.2 (1.4.3/1.4.10/1.4.11/1.4.12/2.5.8), axe-core / WAVE |
| Performance / Core Web Vitals | web.dev/CWV, Lighthouse / PSI / CrUX |
| Component anatomy, states, tokens | Carbon, Polaris, Fluent, Material Web, Primer, Radix, Tailwind |
| Forms & checkout | GOV.UK, Wroblewski Web Form Design, Baymard |
| Data tables, dense app UI | Carbon, Ant Design, Lightning, NN/g |
| Information architecture, navigation | NN/g, GOV.UK, WAI-ARIA APG (menu/disclosure) |
| Browser/feature gating | caniuse, MDN Baseline, Browserslist |
| Legal obligation framing | Section 508, EAA / EN 301 549 (with "verify" qualifier) |

This hierarchy feeds the design-quality scoring in [`design-quality-rubric.md`](design-quality-rubric.md): unsupported standard/compliance claims cap or fail a response regardless of polish.

## Canonical URL appendix

- WHATWG HTML — https://html.spec.whatwg.org/
- WAI-ARIA Authoring Practices Guide — https://www.w3.org/WAI/ARIA/apg/
- MDN Web Docs — https://developer.mozilla.org/
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- web.dev Core Web Vitals — https://web.dev/articles/vitals
- Lighthouse — https://developer.chrome.com/docs/lighthouse/
- CrUX (Chrome UX Report) — https://developer.chrome.com/docs/crux/
- axe-core — https://github.com/dequelabs/axe-core · WAVE — https://wave.webaim.org/
- Playwright — https://playwright.dev/ · BrowserStack — https://www.browserstack.com/
- GOV.UK Design System — https://design-system.service.gov.uk/
- NHS service manual — https://service-manual.nhs.uk/ · USWDS — https://designsystem.digital.gov/
- IBM Carbon — https://carbondesignsystem.com/ · Shopify Polaris — https://polaris.shopify.com/
- Atlassian — https://atlassian.design/ · Microsoft Fluent — https://fluent2.microsoft.design/
- Material Web / M3 — https://m3.material.io/ · Ant Design — https://ant.design/
- Salesforce Lightning — https://www.lightningdesignsystem.com/ · GitHub Primer — https://primer.style/
- Tailwind CSS — https://tailwindcss.com/ · shadcn/ui — https://ui.shadcn.com/ · Radix — https://www.radix-ui.com/primitives
- Baymard Institute — https://baymard.com/ · Nielsen Norman Group — https://www.nngroup.com/
- Luke Wroblewski — https://www.lukew.com/ · caniuse — https://caniuse.com/ · MDN Baseline — https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility

---

These sources ground usability, accessibility, semantics, and performance. They do not govern visual inspiration — keep that in [`inspiration-sources.md`](inspiration-sources.md), and keep its discipline in [`weaknesses.md`](weaknesses.md) (aesthetic laundering, evidence overreach). When two sources conflict and the gap is precision-sensitive, surface it per [`clarification-policy.md`](clarification-policy.md) rather than guessing.
