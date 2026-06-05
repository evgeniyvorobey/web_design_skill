# Inspiration Sources

This is a **non-authoritative** layer. It feeds visual range, comparable surfaces, and exploration breadth — never usability, accessibility, semantics, platform, performance, or compliance claims. Those come from [`sources.md`](sources.md).

## Core rule (inspiration is never evidence)

An inspiration reference can tell you *what a design feels like* and *what is possible*. It can never tell you *what is correct*. A site can win an award and still fail keyboard operability, ship 8MB of hero video, hide content behind scroll-jacking, or fail contrast. Awards reward craft and novelty, not measured usability.

So the firewall is absolute:

- Inspiration may inform visual direction, layout breadth, motion vocabulary, and "what good looks like" — and nothing else.
- Inspiration may **never** be cited as the reason a pattern is usable, accessible, performant, on-convention, or compliant.
- When you use a reference, translate it into a concrete, buildable mechanism (token, component, state, layout rule), then justify that mechanism from Tier 1–4 sources, the quality bars, and the pattern catalog — not from the reference.
- Keep references in a clearly labeled `Inspiration references` block, never mixed into UX, accessibility, or platform rationale.

Every craft idea borrowed from this layer carries mandatory caveats: re-check **contrast, `prefers-reduced-motion`, keyboard operability, focus visibility, and Core Web Vitals** before it ships. A gorgeous reference that fails any of these is a liability, not a model.

## Source tiers

**Primary web craft (promoted):**
- **Awwwards** (Site of the Day / Honors) — the strongest single signal for current web visual + interaction craft. Caveats above apply with full force (award sites routinely trade performance and reduced-motion for spectacle).
- **CSS Design Awards, FWA, Webby Awards** — experimental and production craft; replaces the old native-OS award playbooks.

**Curated galleries (layout & taste range):**
- **Land-book, SiteInspire, Godly, Lapa Ninja, One Page Love, httpster** — marketing/landing and portfolio breadth.
- **SaaS Landing Page** — conversion-oriented marketing patterns for the Mode G end of the spectrum.

**Production-flow references (real product surfaces & journeys):**
- **Mobbin Web** — captured real web app flows and screens.
- **Refero** — real product UI reference by surface/pattern.
- **Page Flows** — recorded end-to-end web user journeys (onboarding, checkout, cancellation).

**Visual portfolios / moodboards (lowest authority, ideation only):**
- Dribbble, Behance, Pinterest, Figma Community — aspirational, frequently non-buildable; use for mood only.

Deliberately **demoted / dropped** for web: app-store-style galleries and mobile-pattern catalogs (Pttrns, UI Sources) — they index native mobile UI, not responsive web, and pull recommendations toward the wrong platform.

## Reasoning / derivation layer

When the user asks for inspiration or "best-in-class" references:

1. Name 3–5 references and *why each is relevant* to this product and task (not "it's pretty").
2. For each, extract the **transferable mechanism** — the specific token, spacing rhythm, type pairing, component, motion timing, or layout move that could carry over.
3. Re-ground each mechanism in the quality bars and [`sources.md`](sources.md). Drop anything that cannot survive contrast / reduced-motion / keyboard / CWV checks.
4. Present the result as design direction, with the references quarantined in an `Inspiration references` block.

## Generative direction method

To explore visual direction without copying:

- Define the **job** the visual direction must serve (trust, energy, calm, density, editorial authority) before browsing references.
- Pull breadth from 3+ references that solve that job *differently*, so the output is a synthesis, not a clone.
- Convert the synthesis into tokens (color roles, type scale, spacing rhythm, motion budget) and a one-line rationale per choice.
- Stop at the point where a reference's signature would be recognizably copied — that breaks Jakob's Law expectations and is not yours to ship.

## Reference to transferable mechanism

| Reference signal | Transferable mechanism (what you actually borrow) |
|------------------|---------------------------------------------------|
| "Bold editorial hero" | type scale ratio + measure cap + a single dominant headline weight |
| "Calm, premium feel" (the user's words) | restrained 3-hue palette with one accent role, spacing scale stepped up one level (e.g. 24/32/48px section rhythm), 200–300ms ease-out |
| "Dense, powerful dashboard" | token spacing tightened one step, sticky table header, keyboard row nav |
| "Playful scroll story" | scroll-triggered opacity reveals **with a reduced-motion fallback** |
| "Trustworthy checkout" | clear step indicator, persistent order summary, inline validation |

For source-specific checklists (when to use, what to extract, what NOT to treat as evidence, red flags), see [`visual-benchmark-playbooks.md`](visual-benchmark-playbooks.md). To turn 3–5 references into a structured borrow / do-not-copy / token-component-state plan, see [`benchmark-report-format.md`](benchmark-report-format.md).
