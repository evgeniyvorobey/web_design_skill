# Golden example: SaaS marketing landing page

A compact calibration example showing a strong (4/5) web answer for a marketing landing page: hero, social proof, pricing teaser, and a closing call to action. Use it to anchor what "shippable and strong" looks like before pushing for 5/5.

## Prompt

```text
We're launching Cadence, a B2B scheduling tool for revenue teams.
Design the marketing landing page: a hero with our value prop and a
primary CTA, a social-proof strip with customer logos, a pricing
teaser (3 plans, link to full pricing), and a closing CTA band.

Mobile-first, accessible, fast. Give me real layout values and the
key HTML/CSS so engineering can build it, not just a moodboard.
```

## Golden output

```md
# Cadence landing page

## Page structure and goals

One conversion goal: start a free trial. Everything ladders to that.
Secondary goal: "Book a demo" for buyers who need a human. Single h1 in
the hero, no skipped heading levels, landmarks throughout
(header > nav, main, footer).

Section order (each is a section with an aria-labelledby heading):
1. Hero — value prop + primary CTA
2. Social proof — logo strip + one metric
3. Feature trio — how it works (3 cards)
4. Pricing teaser — 3 plans, link to /pricing
5. Closing CTA band

## Foundations (design tokens)

\`\`\`css
:root {
  /* Type — fluid via clamp(), every clamp keeps a rem term */
  --step-0: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);   /* body 16–18px */
  --step-1: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);   /* sub-lead */
  --step-2: clamp(1.5rem, 1.2rem + 1.5vw, 2rem);       /* h2 */
  --step-3: clamp(2rem, 1.4rem + 3vw, 3.25rem);        /* hero h1 */

  /* Spacing — 4px base scale */
  --space-1: 0.25rem; --space-2: 0.5rem;  --space-3: 0.75rem;
  --space-4: 1rem;    --space-6: 1.5rem;  --space-8: 2rem;
  --space-12: 3rem;   --space-16: 4rem;

  /* Color — AA-verified pairings on #ffffff */
  --ink: #15181e;        /* body text, 15.8:1 on white */
  --ink-muted: #4a5160;  /* secondary text, 7.4:1 */
  --brand: #1d4ed8;      /* CTA fill, 6.3:1 with white label */
  --brand-ink: #ffffff;
  --line: #d6dae2;       /* borders, 1.6:1 — decorative only */
  --focus: #0b3ad6;
}

body {
  font: var(--step-0)/1.5 system-ui, sans-serif;
  color: var(--ink);
}
h1 { font-size: var(--step-3); line-height: 1.15; }
h2 { font-size: var(--step-2); line-height: 1.25; }

/* Reading column ~65ch; page shell ~1200px */
.prose { max-width: 65ch; }
.shell { max-width: 75rem; margin-inline: auto; padding-inline: var(--space-4); }

:where(a, button, summary):focus-visible {
  outline: 3px solid var(--focus);
  outline-offset: 2px;       /* 2.4.11 focus not obscured */
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
\`\`\`

## Hero

Left-aligned text column, product screenshot on the right at >=1024px;
stacked single column below. The text leads (attention path), the image
supports.

\`\`\`html
<section class="hero shell" aria-labelledby="hero-h">
  <div class="hero__copy prose">
    <p class="eyebrow">Scheduling for revenue teams</p>
    <h1 id="hero-h">Book the meeting before the moment passes.</h1>
    <p class="lede">Cadence turns a reply into a confirmed call in one
      click — round-robin routing, buffers, and CRM sync, no back-and-forth.</p>
    <div class="cta-row">
      <a class="btn btn--primary" href="/signup">Start free — no card</a>
      <a class="btn btn--ghost" href="/demo">Book a demo</a>
    </div>
    <p class="reassure">14-day trial · cancel anytime · SOC 2 Type II</p>
  </div>
  <img class="hero__shot" src="/img/board.avif" alt="Cadence routing
    inbound replies to the right rep on a shared calendar"
    width="1120" height="760" loading="eager" fetchpriority="high">
</section>
\`\`\`

\`\`\`css
.hero { display: grid; gap: var(--space-8); padding-block: var(--space-12); }
@media (min-width: 64rem) {       /* 1024px */
  .hero { grid-template-columns: 1.05fr 1fr; align-items: center; }
}
.hero__shot { width: 100%; height: auto; aspect-ratio: 1120 / 760; }
.cta-row { display: flex; flex-wrap: wrap; gap: var(--space-3); margin-block: var(--space-6); }
.btn { min-height: 2.75rem; padding: 0.625rem 1.25rem; border-radius: 8px;
  font-weight: 600; display: inline-flex; align-items: center; }
.btn--primary { background: var(--brand); color: var(--brand-ink); }
.btn--ghost { border: 1px solid var(--line); color: var(--ink); }
\`\`\`

Hero notes: image ships sized (width/height + aspect-ratio) so it
reserves space — protects CLS (<= 0.1). It is the LCP element, so
fetchpriority="high" and the above-the-fold font is preloaded with
font-display: swap plus a fallback-metrics override to keep CLS flat.
Targets are 44px tall (2.5.5 AAA), comfortably past the 24px floor (2.5.8).

## Social proof

\`\`\`html
<section class="proof shell" aria-labelledby="proof-h">
  <h2 id="proof-h" class="visually-hidden">Teams that run on Cadence</h2>
  <p class="proof__metric"><strong>38%</strong> faster time-to-meeting,
    on average, in the first month.</p>
  <ul class="logos" role="list">
    <li><img src="/logo/northwind.svg" alt="Northwind" width="120" height="32"></li>
    <li><img src="/logo/lumen.svg" alt="Lumen" width="120" height="32"></li>
    <!-- 4 more, each with a real alt -->
  </ul>
</section>
\`\`\`

Logos are real img with text alt (not background images), so the proof
survives images-off and screen readers. The metric is live text, not
baked into an image — it stays selectable and scales to 200% (1.4.4).

## Pricing teaser

Three cards; the middle is recommended. The recommendation is shown with
a visible "Most popular" badge AND a heavier border — never color alone
(1.4.1). Full detail lives at /pricing; this is a teaser.

\`\`\`html
<section class="pricing shell" aria-labelledby="price-h">
  <h2 id="price-h">Simple, seat-based pricing</h2>
  <ul class="plans" role="list">
    <li class="plan">
      <h3>Starter</h3>
      <p class="plan__price"><span class="amount">$0</span> / user / mo</p>
      <ul class="plan__feats" role="list"><li>1 calendar</li><li>Basic routing</li></ul>
      <a class="btn btn--ghost" href="/signup?plan=starter">Start free</a>
    </li>
    <li class="plan plan--featured" aria-labelledby="plan-team">
      <p class="badge">Most popular</p>
      <h3 id="plan-team">Team</h3>
      <p class="plan__price"><span class="amount">$14</span> / user / mo</p>
      <ul class="plan__feats" role="list"><li>Round-robin</li><li>CRM sync</li></ul>
      <a class="btn btn--primary" href="/signup?plan=team">Start free trial</a>
    </li>
    <li class="plan">
      <h3>Scale</h3>
      <p class="plan__price"><span class="amount">Custom</span></p>
      <ul class="plan__feats" role="list"><li>SSO/SAML</li><li>Audit log</li></ul>
      <a class="btn btn--ghost" href="/demo">Talk to sales</a>
    </li>
  </ul>
  <p><a href="/pricing">Compare all plans and features →</a></p>
</section>
\`\`\`

\`\`\`css
.plans { display: grid; gap: var(--space-4); padding: 0; }
@media (min-width: 48rem) {        /* 768px tablet: 3-up */
  .plans { grid-template-columns: repeat(3, 1fr); align-items: start; }
}
.plan { border: 1px solid var(--line); border-radius: 12px; padding: var(--space-6); }
.plan--featured { border: 2px solid var(--brand); }
.badge { display: inline-block; background: var(--brand); color: #fff;
  font-size: 0.8125rem; padding: 0.125rem var(--space-2); border-radius: 999px; }
\`\`\`

## Closing CTA band

\`\`\`html
<section class="cta-band" aria-labelledby="end-h">
  <div class="shell prose">
    <h2 id="end-h">Stop chasing calendars. Start booking.</h2>
    <a class="btn btn--primary btn--lg" href="/signup">Start your free trial</a>
  </div>
</section>
\`\`\`

## States, responsive, and a11y checklist

- Button states: default, hover (darken 8%), :focus-visible (3px ring,
  offset), active, loading (label swaps to an aria-busy spinner, width
  locked to avoid layout shift), disabled.
- Reflow (1.4.10): single column down to 320px, no horizontal scroll;
  CTA row wraps instead of overflowing.
- Text spacing (1.4.12): layout survives the user-stylesheet test
  (line-height 1.5, letter/word/paragraph spacing) without clipping.
- Keyboard (2.1.1): every CTA is a real a/button; logical tab order
  top-to-bottom; visible focus on each; skip link to #main.
- Color use (1.4.1): recommended plan = badge text + border weight, not
  hue. Forced-colors: borders use currentColor, CTAs keep a 1px outline
  so they survive Windows High Contrast.
- Performance: hero image AVIF + fetchpriority, fonts preloaded with
  swap, no render-blocking script; targets LCP <= 2.5s, INP <= 200ms,
  CLS <= 0.1.
```

## Design-quality notes

This lands at a solid 4/5 — strong and shippable — across the dimensions that matter for a landing page.

**Attention path & hierarchy (4/5).** One conversion goal drives the page; a single h1 carries the value prop and the primary CTA sits directly under it with a quieter secondary action. The fluid type ramp (`--step-0` through `--step-3`) creates clear rank, and the social-proof metric is live text so it reads as a claim, not decoration.

**Composition & spacing (4/5).** A consistent 4px-base scale, a ~1200px shell, and a ~65ch reading column give the page rhythm without hand-tuned magic numbers. The hero's asymmetric `1.05fr / 1fr` split at 1024px keeps copy leading and the screenshot supporting.

**Typography craft (4/5).** Body is 16–18px with 1.5 line-height; headings tighten to 1.15–1.25; every `clamp()` keeps a rem term so it honors user zoom and resize to 200% (1.4.4 Resize text).

**Color/state & contrast (4/5).** Token pairings are AA-verified with named ratios (body 15.8:1, muted 7.4:1, CTA 6.3:1 — all clearing 1.4.3 at 4.5:1). Decorative borders are flagged as below the 3:1 non-text bar (1.4.11) precisely because they carry no meaning — and where a border does carry meaning (the featured plan), it is reinforced by a text badge (1.4.1 Use of Color).

**Production readiness (4/5).** Real semantic HTML, landmarks, sized media to protect CLS, fetchpriority/font preload for LCP, an explicit state inventory, reflow at 320px (1.4.10), forced-colors handling, and reduced-motion support. Engineering can build straight from this, which is the bar for this dimension.

**What would push it to 5/5:**
- Wire the CTAs to real analytics events and a measured INP budget per interaction, not just a stated target.
- Add a container query on the plan card so its feature list reflows independently of the page breakpoint — true component responsiveness, not just page-level media queries.
- Ship the loading and error states for the signup handoff (network failure, session-expired) as real markup, plus an aria-live region for async feedback (4.1.3 Status Messages).
- Provide the fallback-metrics @font-face override values explicitly rather than describing them, closing the last CLS gap.

Quality target: 4/5
