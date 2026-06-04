# Case study: A pricing page that survives the full breakpoint ladder down to 320px

This is a SYNTHETIC fixture for calibration, not validation against a shipped pricing page. No analytics, usability sessions, or field data back the numbers below; treat it as a worked teaching example, not evidence about any specific product.

## Prompt

```text
We have a SaaS pricing page with three plan cards (Starter, Team, Business),
a monthly/annual billing toggle, and a comparison table of ~18 features
across the three plans. Right now it looks fine on a 1440px laptop but
breaks badly on phones: the three cards sit in a fixed 3-column grid that
overflows horizontally, the comparison table forces a sideways scroll of
the whole page, and the billing toggle is a pair of tiny text links.

Make this responsive across the breakpoint ladder. It must hold together
from a 320px phone up through tablet to a wide 1920px desktop. Give me the
layout strategy, the CSS, and the accessibility details — not just
"use a media query." Tell me what changes at each breakpoint and why.
```

## Weak response

```md
Here's how to make the pricing page responsive.

Use a mobile-first grid for the cards and add breakpoints:

```css
.cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}
@media (min-width: 768px) {
  .cards { grid-template-columns: repeat(3, 1fr); }
}
```

So on phones the cards stack in one column, and at 768px and up you get
three columns side by side. That covers the overflow problem.

For the comparison table, wrap it in a scrolling container so it doesn't
push the page sideways:

```css
.table-wrap { overflow-x: auto; }
```

Now only the table scrolls horizontally instead of the whole page.

For the billing toggle, make it bigger and use a switch:

```html
<label>
  <input type="checkbox" id="billing"> Annual billing
</label>
```

That's tappable on mobile and works fine.

Test it by resizing your browser window from wide down to narrow and make
sure nothing overflows. Use Chrome DevTools device mode to check a phone
size. With these three changes the page will be responsive on phone,
tablet, and desktop.
```

## Why this is weak

- **Breakpoint ladder collapsed to one jump (production readiness 2/5).** The prompt asked what changes at each rung; the answer only has a single 768px switch from 1 to 3 columns. Between ~480px and 767px the page is a lonely single column of wide cards, and there is no intermediate 2-column step, no `min()`/`clamp()` fluidity, and nothing said about 1280/1440/1920 — the very wide range the prompt called out. This is a media-query reflex, not a layout strategy.
- **Fails 1.4.10 Reflow at the 320px floor.** The answer never tests 320px and never sizes anything to survive it. A comparison table wrapped only in `overflow-x: auto` reintroduces a horizontal scroll region; at 320px the card padding and any fixed widths can still trigger two-axis scrolling of content. 1.4.10 specifically prohibits requiring scrolling in two dimensions for this kind of content. "Wrap it so only the table scrolls" treats the symptom, not the reflow requirement.
- **The scroll container is a keyboard and discovery trap.** An `overflow-x: auto` div with no `tabindex="0"`, no accessible name, and no scrollbar affordance is not reachable or operable by keyboard (fails 2.1.1 Keyboard) and gives no cue that content is clipped — a visibility-of-system-status (Nielsen heuristic 1) miss. On a desktop with a trackpad the hidden columns are easy to miss entirely.
- **Billing toggle ignores Use of Color and state semantics (1.4.1, color/state 2/5).** A bare checkbox labeled "Annual billing" carries no visible selected/unselected styling beyond the native box, gives no `:focus-visible` ring, and conveys the active billing mode by position alone. There is no live announcement that prices changed, so screen-reader and zoom users get no feedback (fails 4.1.3 Status Messages). Calling it "tappable on mobile" also ignores 2.5.8 target-size and pointer-agnostic input.
- **No states, no rhythm, no type scale (typography craft 2/5, density & rhythm 2/5).** Fixed `16px` gaps everywhere, no fluid type, no `~65ch` measure on the plan descriptions, and no loading/empty/error story for prices that arrive from an API. The composition is "stack on small, three-up on large" with nothing in between governing spacing or emphasis.
- **Verification is eyeballing.** "Resize your browser and check a phone size in device mode" is not a reflow test. It never names 320px, 200% zoom (1.4.4), text-spacing overrides (1.4.12), or keyboard traversal — so regressions in exactly the dimensions the prompt cares about would pass unnoticed.

## Strong response

```md
## Layout strategy across the ladder

Mobile-first, three coordinated systems, each with its own reflow story.
Container max width ~1200px for the cards, reading columns capped at ~65ch.

Rungs that actually change something (min-width, mobile-first):

| Breakpoint | Cards            | Comparison table        | Billing toggle      |
|------------|------------------|-------------------------|---------------------|
| 320–479    | 1 col, full-bleed| stacked per-plan blocks | full-width segmented|
| 480–767    | 1 col, centered  | stacked per-plan blocks | inline segmented    |
| 768–1023   | 2 col + featured | true table, sticky head | inline segmented    |
| 1024–1439  | 3 col            | true table, sticky head | inline segmented    |
| 1440+      | 3 col, wider gap | true table, density opt | inline segmented    |

The 320px floor is the design target, not an afterthought.

## Cards: fluid first, snap to columns later

Let the cards size themselves before any media query, then add explicit
column counts only where the content earns them.

```css
.cards {
  --gap: clamp(0.75rem, 2vw, 1.5rem);   /* 12–24px */
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--gap);
  max-inline-size: 75rem;               /* ~1200px */
  margin-inline: auto;
  padding-inline: clamp(1rem, 4vw, 2rem);
}
@media (min-width: 768px) {
  .cards { grid-template-columns: repeat(2, 1fr); }
  .cards > .plan--featured { grid-column: 1 / -1; }  /* Team spans full width */
}
@media (min-width: 1024px) {
  .cards { grid-template-columns: repeat(3, 1fr); }
  .cards > .plan--featured { grid-column: auto; }
}
@media (min-width: 1440px) { .cards { --gap: clamp(1.5rem, 2vw, 2rem); } }

.plan__desc { max-inline-size: 60ch; }   /* keep measure readable */
```

Type and rhythm are fluid, not stepped per breakpoint:

```css
:root { --step-0: clamp(1rem, 0.95rem + 0.25vw, 1.125rem); }   /* body >= 16px */
.plan__name  { font-size: clamp(1.25rem, 1.1rem + 0.8vw, 1.75rem); line-height: 1.25; }
.plan__price { font-size: clamp(2rem, 1.6rem + 2vw, 3rem); line-height: 1.2; }
body { font-size: var(--step-0); line-height: 1.5; }
```

## Comparison table: two genuinely different shapes

Below 768px, do not scroll an 18×3 grid sideways — that fails 1.4.10.
Re-author the data as one stacked block per plan (cards of label/value
pairs) so it reflows in a single column. At 768px and up, present the real
`<table>` with a sticky header.

```css
/* small screens: stacked, no horizontal scroll */
.compare__table { display: none; }
.compare__stack { display: grid; gap: 1.5rem; }   /* 24px between plans */

@media (min-width: 768px) {
  .compare__stack { display: none; }
  .compare__table { display: table; inline-size: 100%; border-collapse: collapse; }
  .compare__table thead th {
    position: sticky; top: 0; background: var(--surface);
  }
  .compare__table th, .compare__table td {
    padding: 0.75rem 1rem; text-align: start;     /* 12px / 16px */
  }
}
```

If a wide-screen variant still needs horizontal overflow (e.g. a 6-plan
enterprise view), the scroll region must be keyboard-reachable and named:

```html
<div class="table-wrap" role="region"
     aria-label="Plan comparison" tabindex="0">
  <table>…</table>
</div>
```

`tabindex="0"` makes it focusable so arrow keys scroll it (2.1.1); the
`role="region"` + `aria-label` announce it; a persistent thin scrollbar
plus a right-edge fade cue signals more content (Nielsen: visibility of
system status). A density toggle (comfortable/compact row padding) lets
desktop users exploit the extra room without shrinking targets on coarse
pointers (`@media (pointer: coarse)`).

## Billing toggle: a real segmented control

Two radios styled as a segmented control — never a position-only switch.
State is shown by fill **and** a checkmark glyph, not color alone (1.4.1),
and price changes are announced.

```html
<fieldset class="billing">
  <legend class="sr-only">Billing period</legend>
  <label><input type="radio" name="billing" value="monthly" checked> Monthly</label>
  <label><input type="radio" name="billing" value="annual"> Annual <span class="badge">Save 20%</span></label>
</fieldset>
<p class="prices" aria-live="polite">Team: $24 / user / month</p>
```

```css
.billing { display: inline-flex; gap: 0; border: 1px solid var(--border);
  border-radius: 0.5rem; }
.billing label { display: inline-flex; align-items: center; gap: 0.5rem;
  min-block-size: 2.75rem; padding-inline: 1rem; cursor: pointer; }  /* 44px tall */
.billing input:focus-visible + * ,
.billing label:focus-within { outline: 2px solid var(--focus); outline-offset: 2px; }
.billing input:checked + * { font-weight: 600; }            /* weight, not just color */
.billing input:checked ~ .check { opacity: 1; }             /* glyph confirms state */
@media (max-width: 479px) { .billing { display: flex; }     /* full-width segmented */ }
@media (forced-colors: active) { .billing input:checked + * { forced-color-adjust: none; } }
```

Updating the price text inside `aria-live="polite"` announces the change
to assistive tech (4.1.3). Each segment is >= 44px tall (2.5.8 / 2.5.5 AAA)
and works for mouse, keyboard (radio arrow semantics), and touch alike.

## States and resilience

Prices arrive async, so reserve their space to protect CLS (target <= 0.1):
skeleton bars sized to the final price box (avoid layout shift), an error
state ("Couldn't load pricing — retry") with an aria-live region, and a
disabled state on the CTA while a plan is being selected. `:focus-visible`
rings on every interactive element; ESC and proper focus restore if the
"Compare all features" control opens an off-canvas panel on small screens.

## Verification

Real checks, named explicitly:
- 320px CSS width: no two-axis scroll anywhere; cards, table-stack, and
  toggle all reflow in one column (1.4.10).
- 200% browser zoom and 400% on a 1280px viewport: content reflows, no
  clipping (1.4.4).
- Text-spacing bookmarklet (line-height 1.5, etc.): nothing truncates (1.4.12).
- Keyboard-only pass: tab order header → toggle → cards → table region →
  footer; visible focus throughout; scroll region operable by arrow keys.
- Contrast: body and price text 4.5:1, badges/borders 3:1 (1.4.3, 1.4.11);
  selected segment readable in forced-colors mode.
- Lighthouse / field budgets: LCP <= 2.5s, INP <= 200ms, CLS <= 0.1.
```

## Why this is stronger

- **The whole ladder does work, with reasons (production readiness 4/5).** Every rung — 320, 480, 768, 1024, 1440 — has a stated job: full-bleed vs centered single column, a 2-up step with the featured plan spanning before 3-up arrives, and a density bump at wide widths. Cards are fluid via `clamp()` gaps and a `max-inline-size` cap *before* any media query, so the breakpoints add column counts rather than rescue overflow. That is layout strategy, not a single 768px reflex.
- **320px reflow is designed, not hoped for (composition 4/5, satisfies 1.4.10).** The comparison data is re-authored into stacked per-plan blocks below 768px instead of side-scrolling an 18×3 grid, so there is genuinely no two-axis scroll at the floor. Where horizontal overflow is unavoidable on a wide variant, the region is `tabindex="0"` + `role="region"` + `aria-label`, restoring keyboard operability (2.1.1) and visibility of system status (Nielsen heuristic 1) that the weak answer dropped.
- **State is conveyed by more than color, and changes are announced (color/state & contrast 4/5).** The segmented control uses fill, weight, and a check glyph (1.4.1 Use of Color), exposes `:focus-visible` (2.4.7), meets 44px targets (2.5.8 / AAA 2.5.5), and pushes price updates through `aria-live="polite"` (4.1.3 Status Messages) — closing the silent-update gap. `forced-colors` is handled explicitly.
- **Typography and rhythm are fluid and bounded (typography craft 4/5, density & rhythm 4/5).** Body stays >= 16px via a `clamp()` step with a rem term, headings sit at 1.2–1.25 line-height, body at 1.5, and `.plan__desc` is capped at 60ch so the measure never sprawls on wide screens. Gaps scale with `clamp()` instead of fixed 16px everywhere, and a density toggle exploits desktop room without flattening it to a phone layout.
- **Resilience and CLS are first-class (interaction polish 4/5).** Async prices get skeletons sized to the final box, an error state with retry, and a disabled CTA during selection — the default/loading/empty/error/disabled set the weak answer omitted, with reserved space protecting the CLS <= 0.1 budget and an explicit LCP/INP target.
- **Verification names the criteria a regression would hit (context & brand fit 4/5).** Instead of "resize the window," it enumerates 320px width, 200%/400% zoom (1.4.4), text-spacing (1.4.12), a keyboard tab-order trace, contrast ratios (1.4.3 / 1.4.11), and Core Web Vitals — the exact dimensions the prompt asked to be protected. This is a solid, shippable **4/5**: strong and buildable, with room left only for fine motion/brand tuning.

## Regression checks

- At a 320px CSS viewport width, no part of the page (cards, billing control, or comparison data) requires scrolling in two dimensions; the table reflows to stacked per-plan blocks rather than side-scrolling an 18×3 grid (1.4.10 Reflow).
- The card grid changes column count at named rungs — 1 col below 768, a 2-col step with the featured plan spanning full width at 768, 3-col at 1024 — and remains fluid via `clamp()`/`max-inline-size` between them, never snapping straight from 1 to 3 (production readiness).
- Any horizontal-scroll container is `tabindex="0"` with `role="region"` and an `aria-label`, so it is keyboard-reachable and announced; a visible scrollbar or edge cue signals clipped content (2.1.1 Keyboard, Nielsen visibility of system status).
- The billing toggle shows its selected state by more than color (fill + weight + check glyph), exposes a visible `:focus-visible` ring, meets the 44px target size, and announces price changes through an `aria-live` region (1.4.1, 2.4.7, 2.5.8, 4.1.3).
- Body text stays >= 16px and survives 200% zoom (1.4.4) and the 1.4.12 text-spacing overrides with no clipping or truncation; reading columns stay near 65ch.
- Async prices reserve their final space so the layout holds CLS <= 0.1, and the full state set (loading skeleton, empty, error-with-retry, disabled CTA) is present, not just the happy path.
