# Visual Benchmark Playbooks

Source-specific checklists for extracting web inspiration responsibly. Each playbook says when to use the source, what to extract, what NOT to treat as evidence, a checklist, and red flags.

The firewall, restated for every source below: **Do not use benchmarks as evidence** for usability, accessibility, performance, web-convention correctness, compliance, user preference, or business results. **Translate references into implementable mechanisms** — tokens, components, states, layout rules — then justify those mechanisms from [`sources.md`](sources.md) and [`quality-bars.md`](quality-bars.md), never from the reference. Every borrowed craft idea must re-pass contrast, `prefers-reduced-motion`, keyboard operability, focus visibility, and Core Web Vitals before it ships.

This complements [`inspiration-sources.md`](inspiration-sources.md) (the tiers and firewall) and [`benchmark-report-format.md`](benchmark-report-format.md) (the structured report).

---

## Awwwards

The strongest single signal for current web visual and interaction craft (Site of the Day / Honors).

### When to use
- The user wants best-in-class web craft, motion vocabulary, or a bold marketing/editorial direction.
- Exploring expressive hero treatments, scroll storytelling, or type-forward layouts.

### What to extract as inspiration
- Type scale and pairing, color restraint, spacing rhythm, hero composition.
- Motion timing and choreography (as a vocabulary, not a spec).
- Layout breadth: how an editorial idea is expressed.

### What NOT to treat as evidence
- That a pattern is usable, accessible, or performant. Award sites routinely trade reduced-motion, contrast, and Core Web Vitals for spectacle.
- That heavy scroll-jacking or autoplay video is "safe" — it usually is not.

### Checklist
- Re-check every borrowed effect against contrast, reduced-motion, keyboard, and LCP/INP/CLS.
- Convert the look into tokens and components; name what you are NOT copying.
- Keep the reference in an `Inspiration references` block.

### Red flags
- Scroll-jacking, autoplay sound/video, motion with no reduced-motion fallback, text-over-image with failing contrast, 5MB+ heroes.

---

## CSS Design Awards / FWA / Webby

Experimental and production craft awards; the web replacement for native-OS award galleries.

### When to use
- The user wants experimental interaction craft (FWA), polished production sites (CSSDA), or broad category benchmarks (Webby).
- Comparing how award-winners in a category solve a similar surface.

### What to extract as inspiration
- Interaction polish, micro-interaction timing, and component craft.
- Category conventions (what a great site in this vertical tends to do).

### What NOT to treat as evidence
- That the award implies measured usability, accessibility, or conversion.
- That an experimental FWA interaction belongs in a high-throughput task flow.

### Checklist
- Separate "production craft" references from "experimental" ones before borrowing.
- Translate references into implementable mechanisms; validate against the quality bars.
- Note the marketing-vs-web-app context: experimental craft suits marketing, not dense app tasks.

### Red flags
- Interactions that require a mouse, hide content until hover, or have no keyboard path.

---

## Land-book / SiteInspire / Godly

Curated galleries for marketing/landing and portfolio layout breadth.

### When to use
- The user needs landing-page layout range, section ordering ideas, or visual tone references.
- Building a marketing surface and wanting breadth across many solutions.

### What to extract as inspiration
- Section ordering and scroll narrative shapes, hero layouts, social-proof placement.
- Color/type tone and whitespace rhythm for a given vibe.

### What NOT to treat as evidence
- That a layout converts, or that a curated screenshot reflects the live site's performance or accessibility.

### Checklist
- Pull from 3+ references that solve the job differently to avoid cloning one.
- Translate the chosen shape into a section spec with tokens and a CTA hierarchy.
- Re-check the hero against LCP and contrast before committing.

### Red flags
- Treating a static gallery thumbnail as proof the real site is fast, accessible, or keyboard-operable.

---

## Mobbin Web / Refero / Page Flows

Production-flow references: real web app screens and recorded end-to-end journeys.

### When to use
- The user needs real product UI for a specific surface (Mobbin Web, Refero) or a full journey (Page Flows: onboarding, checkout, cancellation).
- Benchmarking how shipping products solve a flow before designing your own.

### What to extract as inspiration
- Step ordering, state coverage, empty/error handling, and pattern choices in real flows.
- Comparable surfaces to sanity-check your structure against convention (Jakob's Law).

### What NOT to treat as evidence
- That a captured flow is optimal or accessible — it is one product's choice at one point in time.

### Checklist
- Use these for flow/structure benchmarking before craft galleries.
- Translate references into implementable mechanisms (steps, states, URL behavior).
- Keep the production references separate from moodboards.

### Red flags
- Copying a flow's missing-state gaps, or assuming a captured screen passes accessibility.
