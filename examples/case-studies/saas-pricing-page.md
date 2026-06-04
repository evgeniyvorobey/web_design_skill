# Case study: SaaS pricing page with plan comparison and billing toggle

A bad-to-good calibration fixture for a three-tier pricing page: a monthly/annual
billing toggle, a feature comparison table, and per-plan calls to action. The weak
answer "looks like a pricing page" but fails on contrast, on communicating the
discount, on table semantics, and on production states. The strong answer reaches
the **4/5** shippable bar by fixing each with a concrete web mechanism.

## Prompt

```text
We're a B2B SaaS. Design the pricing page for our marketing site.

- Three plans: Starter, Growth, Scale. Growth is the one we want most people to pick.
- A toggle to switch between monthly and annual billing. Annual saves 20%.
- A comparison table so people can see which features are in each plan
  (about 14 feature rows across 6 groups: limits, collaboration, security,
  integrations, support, SLA).
- Each plan has a CTA: Starter -> "Start free", Growth/Scale -> "Start trial",
  plus a "Talk to sales" path for Scale.
- Responsive: phones through wide desktop. Must be accessible (we sell to
  regulated buyers and they run audits).

Give us layout, the toggle and table mechanics, states, and CSS/HTML specifics
we can hand to engineering.
```

## Weak response

```md
## Pricing layout

Three pricing cards centered on the page, with the Growth card in the middle,
slightly larger and a different color so it stands out as recommended. Below the
cards, a full comparison table with all the features and checkmarks.

### Billing toggle
A toggle switch at the top. When it's on annual, the prices update to the annual
numbers and we show "Save 20%" next to it. Use a styled checkbox so it looks like
a sliding switch.

### Cards
Each card has the plan name, the price in large text, a short description, the CTA
button, and a few bullet highlights. The recommended Growth card gets a colored
border and a "Most popular" badge. CTA buttons are filled; the others can be
outline buttons so Growth pops more.

### Comparison table
A table with feature names down the left and the three plans across the top. Use
green checkmarks for included features and leave the cell blank if not included.
Make the header row stick to the top as you scroll. On mobile, let the table
scroll sideways so it still fits.

### Colors and type
Use a light gray background with white cards. Price in a big bold font (~48px),
feature text in light gray (#aaa) so it's secondary. Brand purple for the Growth
accents and the buttons.

### Responsive
Stack the three cards vertically on mobile. Keep the table scrollable. Everything
should look clean and modern.
```

## Why this is weak

- **Color/state & contrast (WCAG 1.4.3, 1.4.11, 1.4.1).** `#aaa` text on white is ~2.3:1 — it fails the 4.5:1 body-text minimum, and "secondary" feature text is core content, not decoration. Green checkmark with a "blank means not included" scheme is **use of color alone** (1.4.1): a screen-reader user hears nothing for an empty cell, and a green check on white is likely under the 3:1 non-text contrast floor (1.4.11). The colored Growth border as the only "recommended" signal also leans on color.
- **Typography craft.** A hard `48px` price and unspecified body size give no fluid behavior and no stated 16px floor; the page will not honor 1.4.4 resize-to-200% or 1.4.12 text spacing gracefully, and a 48px price can collide on a 320px reflow.
- **Density & rhythm / production readiness.** No spacing scale, no container width, no reading measure. The toggle is described as a "styled checkbox / sliding switch" with no name on what it controls and no programmatic state — that is an unlabeled custom control, an APG anti-pattern.
- **Attention path & hierarchy.** "Make Growth pop" is asserted, not built: there's no defined order of emphasis, no stated relationship between the recommended badge and the CTA, and outline-vs-filled buttons are chosen for visual contrast rather than action hierarchy.
- **Interaction polish & motion / production readiness.** No states beyond default. Missing: `:focus-visible`, loading on the CTA, disabled, the empty/error path when prices fail to load, and what the toggle announces. "Sticky header" and "scroll sideways on mobile" are named but not made operable — a horizontally scrolling table with a sticky `<thead>` is a keyboard and reflow trap if not handled (1.4.10 reflow, 2.1.1 keyboard).
- **Context & brand fit.** "Save 20%" sits next to the toggle as static text; nothing ties the toggle's annual state to the actual savings, the strikethrough of the monthly price, or the "billed annually" clarification a regulated B2B buyer needs before signing.
- **Heuristics.** Violates Nielsen *Visibility of system status* (toggle state and price recalculation are not announced) and *Match between system and the real world* (annual price shown as a per-month figure without the "billed yearly" disclosure invites a trust/usability complaint).

## Strong response

```md
## Pricing page architecture

Three regions inside `<main>`: a billing control, a plan card row, and a full
comparison table. One `<h1>` ("Plans & pricing"); section headings step h2 -> h3
with no skipped levels. Container `max-width: 75rem` (1200px), centered, with
`padding-inline: clamp(1rem, 4vw, 2rem)`. Spacing uses the 4px scale
(4/8/12/16/24/32/48/64). Body is `1rem` minimum, line-height 1.5; the plan
description column is capped at ~60ch.

Card row is a 12-col grid on desktop (each card spans 4) and reflows to a single
column at the 320px floor:

` ``css
.plan-grid { display: grid; gap: 1.5rem; grid-template-columns: 1fr; }
@media (min-width: 768px)  { .plan-grid { grid-template-columns: repeat(3, 1fr); } }
.price { font-size: clamp(2rem, 1.5rem + 2.5vw, 3rem); line-height: 1.15;
         font-variant-numeric: tabular-nums; }
.plan-desc { max-width: 60ch; }
` ``

### Billing toggle (annual / monthly)

Use a two-button radio group, not a lone switch, so the *current* and *available*
billing periods are both visible and the saving is legible. It follows the WAI-ARIA
APG radio-group pattern: arrow keys move within the group, one Tab stop, roving
tabindex.

` ``html
<fieldset class="billing">
  <legend>Billing period</legend>
  <div role="radiogroup" aria-label="Billing period">
    <button role="radio" aria-checked="true"  id="bp-month">Monthly</button>
    <button role="radio" aria-checked="false" id="bp-year">
      Annual <span class="save">Save 20%</span>
    </button>
  </div>
  <p id="billing-note" aria-live="polite">Billed monthly. Cancel anytime.</p>
</fieldset>
` ``

On switch to Annual: each `.price` updates to the per-month-when-billed-annually
figure, the prior monthly figure is shown struck through with a visually-hidden
"was" label, and `#billing-note` (an `aria-live="polite"` region) changes to
"Billed annually — 20% less than monthly." The 20% saving is therefore conveyed
three ways: the badge text, the struck price + screen-reader "was", and the live
note — never color alone (1.4.1). Targets are at least 24x24px (2.5.8); the
recommended hit area is 44px (2.5.5 AAA).

### Plan cards and action hierarchy

Emphasis order is deliberate: recommended plan > its CTA > price > other CTAs >
feature highlights. The Growth card is marked recommended by **three** redundant
cues — a text `<span class="badge">Most popular</span>`, a 2px accent border, and
slightly raised elevation — so removing color still leaves the badge and border
weight. Buttons follow action hierarchy, not decoration: every primary CTA is a
filled `.btn-primary`; "Talk to sales" is a `.btn-secondary` (outline) because it
is the lower-frequency path, not because it must look quieter than Growth.

` ``html
<article class="plan" aria-labelledby="plan-growth">
  <p class="badge">Most popular</p>
  <h2 id="plan-growth">Growth</h2>
  <p class="price"><span class="vh">From</span>$<span data-price="growth">29</span>
     <span class="per">/user / month</span></p>
  <p class="plan-desc">For teams scaling collaboration and integrations.</p>
  <a class="btn-primary" href="/signup?plan=growth">Start trial</a>
</article>
` ``

CTA loading state: on submit the action becomes a `<button>` set
`aria-busy="true"` with an inline spinner and a visually-hidden "Starting your
trial…"; width is reserved so there is no layout shift (CLS <= 0.1).

### Comparison table (semantic + responsive)

A real `<table>` with `<caption>`, scoped headers, and row-group headers per
feature group. Inclusion is conveyed by an icon **plus** text, never a bare check:

` ``html
<table class="compare">
  <caption>Feature comparison across Starter, Growth, and Scale</caption>
  <thead>
    <tr>
      <th scope="col">Feature</th>
      <th scope="col">Starter</th>
      <th scope="col" aria-current="true">Growth</th>
      <th scope="col">Scale</th>
    </tr>
  </thead>
  <tbody>
    <tr><th scope="rowgroup" colspan="4">Security</th></tr>
    <tr>
      <th scope="row">SSO / SAML</th>
      <td><span class="vh">Not included</span><svg aria-hidden="true">…</svg></td>
      <td><span class="vh">Included</span><svg aria-hidden="true">…</svg>✓</td>
      <td><span class="vh">Included</span><svg aria-hidden="true">…</svg>✓</td>
    </tr>
  </tbody>
</table>
` ``

- **Sticky header** via `position: sticky; top: 0` on `<thead> th`, kept inside the
  scroll container so it never obscures focus (2.4.11 focus not obscured).
- **Reflow (1.4.10).** Below 768px the table does not side-scroll into a trap;
  it collapses to stacked per-plan cards (each feature group becomes a labeled
  block) driven by a container query, so a 320px viewport at 200% zoom (1.4.4)
  still reads top-to-bottom with no horizontal scroll.
- **Keyboard / scroll (2.1.1).** When the table *does* scroll on mid widths, the
  region is `tabindex="0"` with `role="region"` and an `aria-label`, so a
  keyboard user can scroll it and it isn't a trap.
- The recommended column reuses the same accent + the `aria-current` text cue,
  consistent with the card.

### Color, contrast, and states

- Body and "secondary" feature text use a token at >= 4.5:1 on the card surface
  (e.g. `#475569` on white ~ 7.5:1); the muted tone is achieved by hue/weight,
  not by dropping below contrast.
- Inclusion icon stroke and the focus ring meet 3:1 non-text contrast (1.4.11).
  `:focus-visible` is a 2px ring with 2px offset on every interactive element;
  `@media (forced-colors: active)` maps borders/icons to system colors and keeps
  the recommended border via `forced-color-adjust`.
- States covered: default, hover, `:focus-visible`, active, CTA loading
  (`aria-busy`), disabled (annual unavailable on a legacy plan), empty (prices
  unavailable -> "Pricing temporarily unavailable, contact sales" with the table
  still readable), and error (price fetch fails -> inline `role="alert"`).
- `@media (prefers-reduced-motion: reduce)` removes the price cross-fade and the
  card elevation transition.

### Performance

LCP target <= 2.5s: the plan headings/prices are server-rendered text (no
price-image), so the toggle only swaps numbers. The display font is preloaded with
`font-display: swap` and a metrics-matched fallback to avoid CLS. The comparison
table is in the DOM (not lazy) so anchored deep-links and Ctrl+F work. INP <= 200ms:
the toggle handler only rewrites `data-price` text nodes and `aria-checked`.
```

## Why this is stronger

- **Color/state & contrast.** Secondary text moves from `#aaa` (~2.3:1, fail) to a
  >= 4.5:1 token, satisfying 1.4.3; inclusion is icon **plus** visually-hidden
  text, removing the 1.4.1 use-of-color failure; icon stroke and focus ring meet
  1.4.11's 3:1; forced-colors support is explicit.
- **Attention path & hierarchy.** The recommended plan is signaled three redundant
  ways (badge text, border weight, elevation) and the emphasis order is named, so
  hierarchy survives grayscale and forced-colors — not just "make it pop." Button
  styling follows action frequency, fixing the outline-for-contrast confusion.
- **Typography craft.** Fluid `clamp()` price with a rem term, a stated 16px floor,
  `tabular-nums` so prices don't jitter on toggle, and a ~60ch measure — honoring
  1.4.4 resize and 1.4.12 text spacing.
- **Production readiness & interaction polish.** A full state matrix (default ->
  error/empty/loading/disabled), `aria-live` price/billing announcements (Nielsen
  *Visibility of system status*), reduced-motion handling, and reserved CTA width
  for CLS. The toggle is a labeled APG radio group, not an unnamed switch.
- **Density & rhythm + composition.** Explicit 4px scale, 75rem container, 12-col
  reflow to the 320px floor, and a comparison table that collapses to stacked
  cards instead of becoming a side-scroll trap (1.4.10), exploiting desktop density
  where it helps and degrading cleanly where it doesn't.
- **Context & brand fit.** The "billed annually" disclosure plus struck monthly
  price addresses *Match between system and the real world* and the regulated-buyer
  audit need — the saving is explained, not just asserted.

This reaches **4/5**: strong and shippable. The remaining gap to 5/5 is final
content (production copy, legal tax/VAT disclosure, locale/currency formatting) and
measured CWV from a live build rather than budgeted targets.

## Regression checks

A future answer to this prompt must still pass all of these:

- Every text and icon meets contrast: body/secondary text >= 4.5:1 (1.4.3), icons
  and focus ring >= 3:1 (1.4.11). No `#aaa`-on-white or similar sub-threshold tone.
- Plan inclusion and the recommended plan are **never** signaled by color alone
  (1.4.1): inclusion carries text (visually-hidden is fine); recommended carries
  a text badge plus a non-color cue.
- The billing toggle is a labeled, keyboard-operable group (APG radio group or
  equivalent), fully operable by keyboard with visible `:focus-visible` (2.1.1),
  and announces the new billing state and saving via `aria-live`.
- At the 320px reflow floor and at 200% zoom (1.4.10, 1.4.4) the page reads with
  no horizontal-scroll trap: the comparison table collapses to stacked content
  rather than relying on side-scroll.
- The comparison table is a semantic `<table>` with `<caption>`, `scope`-ed
  column/row headers, and a sticky header that does not obscure focus (2.4.11).
- The response specifies states beyond default — at minimum hover,
  `:focus-visible`, CTA loading (`aria-busy`), disabled, empty, and error — and
  respects `prefers-reduced-motion`.

Boundary: this is a SYNTHETIC calibration fixture authored to exercise the rubric;
it is not validation against a shipped pricing page, and its CWV figures are
budgets, not measurements from a live build.
