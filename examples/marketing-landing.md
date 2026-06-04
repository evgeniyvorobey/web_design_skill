# Worked example: Marketing landing page (Mode G)

## Example prompt

```text
Use the web-design-skill.

Generate a marketing landing page concept for "Cadence", a SaaS that automates standup updates
for engineering teams.

Inputs:
- Conversion goal: free-trial signups
- Audience: engineering managers and team leads
- Breakpoints: mobile-web and desktop
- Browsers: evergreen engines
- Constraints: fast LCP, reduced-motion respected, accessibility-sensitive, SEO matters
```

## Example output

```md
Mode: Generate / critique a marketing landing page (conversion / CRO)
Responsive/breakpoint scope: Mobile-web and desktop, working down to 320px
Browser/engine scope: Evergreen Chromium / WebKit / Gecko
Assumptions:
- Primary traffic is warm (content + search), not paid cold traffic.
- A free trial requires only email + workspace, no credit card.
- This is a marketing surface, so expressive editorial craft is appropriate — distinct from the dense, task-first web app behind the login.

## Conversion goal and primary CTA
One goal: start a free trial. One dominant CTA — "Start free trial" — repeated down the page; every secondary action (watch demo, read docs) is visually subordinate.

## Above-the-fold (hero) structure
- Headline (benefit-led): "Standups that write themselves."
- Subhead (specificity): "Cadence collects async updates from your team and posts a clean summary every morning."
- Primary CTA + a one-line trust nudge ("No card required · 2-minute setup")
- Supporting visual: a static, art-directed product screenshot (the LCP candidate), not autoplaying video.

## Scroll narrative and section rhythm
Ordered by the visitor's questions, not a feature dump:
1. Hero — what is it / why care
2. Problem — the standup tax (meetings, interruptions, missed updates)
3. How it works — three steps with small product shots
4. Proof — logos, a metric, a testimonial
5. Outcome/features — the 3–4 features that matter to a team lead
6. Objections/FAQ
7. Final CTA band

## Value proposition and messaging hierarchy
- Headline carries the benefit; subhead carries the mechanism; section headings carry sub-benefits.
- Copy is concrete ("posts a morning summary") over adjectives ("powerful, seamless").
- One idea per section; the eye should land on a heading, then a CTA.

## Social proof and trust signals
- A row of recognizable customer logos near the hero (specific, not "trusted by thousands").
- One quantified testimonial with a name, role, and team size.
- A security/trust line (SSO, data handling) close to the signup CTA where hesitation peaks.

## CTA hierarchy and placement
- Primary "Start free trial" in the hero, after "How it works", and in the final band.
- A single secondary "Watch 90-sec demo" as a text/ghost button, never competing visually.
- The sticky header keeps a compact primary CTA available on scroll without obscuring content.

## Objection handling / FAQ
- "Does it work with Slack/Teams?" · "What about timezones?" · "Is my data private?" · "What happens after the trial?"
- Answered inline in an accessible accordion (disclosure pattern, keyboard-operable, `aria-expanded`).

## Accessibility considerations
- Semantic structure: one h1 (the headline), logical heading outline, landmarks; the FAQ uses real disclosure buttons.
- Keyboard operability: visible `:focus-visible` on all CTAs and FAQ toggles; logical tab order; skip link to main.
- Contrast: text over the hero image meets ≥ 4.5:1 via an overlay or solid panel, not hope; non-color cues on the active nav item.
- `prefers-reduced-motion` removes scroll-triggered reveals and any parallax; content is fully present without motion.

## Performance considerations (Core Web Vitals, media weight)
- LCP: the hero screenshot is the LCP element — preload it, serve responsive `srcset`/`sizes`, avoid render-blocking webfonts on the headline; budget LCP ≤ 2.5s.
- CLS: reserve hero image and logo-row space with `aspect-ratio`; `font-display: swap` with fallback-metric matching; budget CLS ≤ 0.1.
- INP: defer non-critical JS (analytics, chat widget); keep CTA handlers light; budget INP ≤ 200ms.
- Media weight: no autoplay video in the hero; lazy-load below-the-fold imagery.

## SEO and shareability
- One descriptive h1, a logical heading outline, and meaningful link text.
- `<title>`/meta description targeting the core query; Open Graph + Twitter card image for shares; `Organization`/`Product` structured data; a canonical URL.
- Server-rendered copy so crawlers see the value proposition without executing JS.

## Design quality calibration
- Quality target: 4/5 — expressive, fast, and operable; 5/5 adds validated localization and a measured A/B on the hero.
- Attention path: headline → primary CTA → proof; each section repeats land-then-act.
- Composition and spacing: 12-col grid, generous section spacing (64–96px) that scales with viewport, measure capped ~60ch for marketing prose.
- Typography: expressive display `clamp()` headline, 16px/1rem body, 1.5 line-height.
- Color and state: brand-forward but accessible; CTA states (hover/focus/active) defined; dark-mode and forced-colors checked.
- Interaction polish: 200–300ms reveals with a reduced-motion fallback; CTA feedback within 100ms.
- Production checks: tokens for type/color/spacing; disclosure/CTA components mapped; CWV budget (LCP/INP/CLS); axe-clean and keyboard-pass; verified 320px reflow.

## Conversion-rate reasoning
- A single dominant CTA reduces choice cost (Hick's Law) and concentrates intent.
- Proof placed where hesitation peaks (near signup) addresses risk at the decision point.
- A benefit-led, specific headline raises clarity, which is the strongest lever on a warm-traffic landing page.
- These are mechanisms and hypotheses, not guarantees — validate the hero and CTA copy with a measured A/B test; no lift percentage is claimed here.

## Next actions
- Draft the three "How it works" product shots and confirm the hero screenshot as the LCP asset.
- Set up an A/B test on headline + primary CTA copy with a clear primary metric (trial-start rate).
- Run a Lighthouse + axe pass on the prototype and verify reduced-motion and 320px reflow.
```
