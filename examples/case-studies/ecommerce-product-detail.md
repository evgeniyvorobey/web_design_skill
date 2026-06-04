# Case study: Ecommerce product detail page (gallery, variants, add-to-cart, reviews)

A bad-to-good calibration case for a product detail page (PDP): media gallery,
variant selectors, add-to-cart, and a reviews block. The PDP is the highest-stakes
template on a storefront — it has to load fast, make the variant decision legible,
and never let a shopper add an out-of-stock combination by mistake.

> Boundary: this is a SYNTHETIC fixture for calibration. It is not validation
> against a shipped storefront — no analytics, conversion data, or usability
> sessions back these numbers. Treat the values as defensible defaults, not
> measured results from a live store.

## Prompt

```text
We're building the product detail page for our online shoe store. Each product
has multiple color and size variants, a few photos plus one video, a price,
an add-to-cart button, and customer reviews with star ratings.

Design the desktop and mobile layout and tell me how to build the variant
picker and the gallery. It needs to be accessible and fast — our current PDP
is sluggish and shifts around while it loads. Give me concrete CSS/HTML
direction, not just a wireframe description.
```

## Weak response

```md
Here's a clean, modern product detail page.

**Layout**
- Two columns on desktop: gallery on the left, product info on the right.
- Stack to one column on mobile.
- Use a card with a subtle shadow and rounded corners for the buy box.

**Gallery**
- Big main image with thumbnails underneath.
- Click a thumbnail to swap the main image.
- Add a lightbox on click for zoom.

**Variants**
- Show color swatches as little circles.
- Show sizes as a dropdown `<select>`.
- Highlight the selected one with a border.

**Add to cart**
- A big bright button that stands out: `background: #ff5722; color: #fff;`.
- On click, show a toast that says "Added to cart!".

**Reviews**
- Star rating at the top with the average.
- List reviews below with name, stars, and text.
- A "Write a review" button.

**Styling notes**
- Font size 14px for body to keep it compact.
- Use a CSS transition on the button hover for polish.
- Lazy-load all images so the page is fast.

This gives you a responsive, good-looking PDP that works on all devices.
```

## Why this is weak

- **Production readiness / CLS (dim 8; Web Vitals 0.1 budget):** "Lazy-load all
  images" with no reserved space and no `aspect-ratio` on the gallery is the
  direct cause of the "shifts around while it loads" complaint. Lazy-loading the
  LCP hero image actively delays LCP past the 2.5s budget. The answer repeats the
  user's symptom as if it were a fix.
- **Typography craft (dim 3):** 14px body violates the 16px (1rem) minimum and
  reads poorly on dense review text; no measure cap, no line-height, no fluid
  scale, so it degrades under 1.4.4 Resize Text.
- **Color/state & contrast (dim 4; WCAG 1.4.1, 1.4.11, 1.4.3):** Color swatches
  "as little circles" selected by border alone lean on color as the only signal,
  failing 1.4.1 Use of Color. `#ff5722` on `#fff` is ~3.6:1 — below 4.5:1 for the
  button label. No non-text contrast (1.4.11) commitment for the swatch ring.
- **Interaction polish / states (dim 6):** No loading, disabled, error, or
  out-of-stock states. A `<select>` for sizes can't show per-size stock, can't be
  styled as a grid, and hides the fact that "size 9 in red" is sold out until
  after selection — a top PDP failure mode.
- **Attention path & hierarchy (dim 1):** "Big bright button that stands out" is
  the only hierarchy reasoning. No price/variant/CTA priority order, no
  relationship between the chosen variant and the gallery or price.
- **Accessibility — operability (WCAG 2.1.1, 4.1.2):** "Highlight the selected"
  swatch has no role, no `aria-pressed`/radio semantics, no keyboard model. A
  toast with no `aria-live` is invisible to screen readers (defeats the intent of
  4.1.3 Status Messages). Lightbox with no focus trap/restore or ESC.
- **Heuristics:** Fails Nielsen "Visibility of system status" (no stock/async
  feedback) and "Error prevention" (lets you try to buy unavailable combos).

## Strong response

```md
## Layout and grid

Desktop (>=1024px): two-column 12-col grid, max content width 1200px.
Gallery spans 7 cols, buy box spans 5 and is `position: sticky; top: 24px` so
the price and add-to-cart stay visible while the description scrolls.

- Single column below 1024px; buy box flows under the gallery.
- Reflow floor verified at 320px (WCAG 1.4.10): no horizontal scroll, swatches
  wrap, gallery becomes a swipeable + keyboard-operable carousel.
- Spacing on the 4px scale: 16px gutters on mobile, 24–32px desktop; 48–64px
  between major sections (gallery / buy box / reviews).

```css
.pdp { display: grid; gap: 24px; max-inline-size: 1200px; margin-inline: auto; }
@media (min-width: 1024px) {
  .pdp { grid-template-columns: 7fr 5fr; gap: 48px; }
  .buy-box { position: sticky; top: 24px; align-self: start; }
}
```

## Type and rhythm

- Body 1rem (16px) minimum; fluid headings
  `clamp(1.5rem, 1.2rem + 1.5vw, 2.25rem)` — the rem term keeps zoom working
  (1.4.4 at 200%).
- Description and review text capped near 65ch (`max-inline-size: 65ch`),
  line-height 1.5; headings 1.2–1.35.
- Price is the typographic anchor of the buy box: `clamp(1.5rem, …)`, weight 600,
  with sale price plus the struck original (`<s>` + visually-hidden "was").

## Gallery (no CLS, fast LCP)

- Reserve space with `aspect-ratio: 4 / 5` on every slot so nothing shifts
  (protects CLS <= 0.1). First/hero image: `fetchpriority="high"`, NOT lazy —
  it is the LCP element. Thumbnails and below-fold media: `loading="lazy"`.
- `<picture>` with AVIF/WebP plus responsive `srcset`/`sizes`; explicit
  `width`/`height` on every `<img>`.
- Pattern: thumbnail rail (vertical on desktop, horizontal scroll-snap on
  mobile) plus a main stage. Thumbnails are real `<button>`s in a
  `role="tablist"`, the main stage is the `tabpanel`; Left/Right arrows move
  selection (WAI-ARIA APG Tabs).
- Zoom uses a native `<dialog>`: ESC closes, focus is trapped, focus is restored
  to the trigger on close, scroll-lock via `:modal`. Pointer-aware —
  `@media (pointer: fine)` adds a hover magnifier; `(pointer: coarse)` uses
  pinch / double-tap. The video has `<track kind="captions">` and visible
  controls.

```css
.gallery-slot { aspect-ratio: 4 / 5; }
.gallery-main img { inline-size: 100%; block-size: 100%; object-fit: cover; }
```

## Variant pickers (color + size as radio groups)

Color and size are each single-select → native radios styled as a swatch/chip
grid, wrapped in `<fieldset>` + `<legend>` ("Color: Cobalt", live-updated).

- **Use of color (1.4.1):** every color swatch carries a text label (visible name
  on the selected one, `aria-label` on each) AND a checkmark/ring on selection —
  never color alone. The selection ring uses `:focus-visible` + `:checked` with a
  3:1 non-text contrast token (1.4.11).
- **Error prevention (Nielsen) + stock:** out-of-stock sizes render as `disabled`
  radios with a diagonal-strike treatment AND the text "Sold out", so an
  unavailable size 9 / red combo cannot be selected — not buried in a `<select>`.
  Selecting a color repaints size availability via `aria-live="polite"`.
- Targets >= 24px (2.5.8); 44px on coarse pointers (2.5.5 AAA). Visible
  `:focus-visible` ring on every chip, not obscured (2.4.11).
- Roving focus inside each group (native radios give arrow-key nav for free);
  Tab moves between the color group, size group, and Add to cart.

```html
<fieldset class="size-group">
  <legend>Size <span aria-live="polite">— selected: 9</span></legend>
  <label class="chip"><input type="radio" name="size" value="8"> 8</label>
  <label class="chip is-oos">
    <input type="radio" name="size" value="9" disabled> 9
    <span class="vh">Sold out</span>
  </label>
</fieldset>
```

```css
.chip { min-block-size: 44px; min-inline-size: 44px; display: grid;
        place-items: center; border: 2px solid var(--border); }
.chip:has(:checked) { border-color: var(--accent); outline: 2px solid var(--accent); }
.chip:has(:focus-visible) { outline: 3px solid var(--focus); outline-offset: 2px; }
.is-oos { text-decoration: line-through; opacity: .6; cursor: not-allowed; }
@media (forced-colors: active) {
  .chip:has(:checked) { outline: 2px solid Highlight; }
}
```

## Add to cart — states and feedback

A native `<button type="submit">` with a documented state machine:
default → hover → :focus-visible → active → loading (disabled +
`aria-busy="true"` + skeleton/spinner) → success → disabled (no variant chosen).

- Disabled until both a color and an in-stock size are selected; while disabled,
  helper text "Select a size" sits in an `aria-live="polite"` region.
- On submit, the cart count and a confirmation update a *persistent*
  `role="status"` region (not a vanishing toast) so 4.1.3 Status Messages passes
  for screen readers; an optional side-sheet cart (`<dialog>`-based, ESC +
  focus trap + restore) slides in.
- Button label contrast >= 4.5:1 — verify the accent token, e.g. `#0B5FFF` on
  white is ~4.7:1; never rely on a 3.6:1 orange. The label is text plus an icon,
  not icon-only.

```css
.add-to-cart { min-block-size: 44px; }
.add-to-cart[aria-busy="true"] { pointer-events: none; }
.add-to-cart:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { .add-to-cart { transition: none; } }
```

## Reviews

- One `<h2>` "Reviews", summary first: average rating as text ("4.6 out of 5")
  PLUS the star glyphs marked `aria-hidden`, plus the count — the number is the
  source of truth, not color/shape alone (1.4.1).
- Rating distribution as accessible bars (label + value text). Each review is an
  `<article>` with a heading, author, date `<time>`, "Verified purchase" badge.
- Sort/filter controls are real `<select>`/buttons that update the list region
  with `aria-live="polite"`; paginate or "Load more" rather than auto-infinite,
  moving focus to the first new item.
- Skeleton placeholders reserve height so loading reviews do not shift the page.

## Performance budget

- LCP <= 2.5s: hero image preloaded + `fetchpriority="high"`, dimensions
  reserved; CLS <= 0.1: `aspect-ratio` everywhere, `font-display: swap` with a
  preloaded above-the-fold font and a metric-matched fallback; INP <= 200ms:
  variant repaint is class-toggle + CSS, no layout thrash.
- Container queries on the buy box and review card so they adapt to their slot,
  not just the viewport.
```

## Why this is stronger

- **Production readiness / Web Vitals (dim 8):** Directly fixes the "shifts and is
  sluggish" complaint with `aspect-ratio` reservations (CLS <= 0.1),
  `fetchpriority="high"` + preload on the LCP hero (LCP <= 2.5s), and `swap` +
  metric-matched fallback fonts. Class-toggle variant updates keep INP <= 200ms.
- **Interaction polish / states (dim 6):** Names a full state machine for
  add-to-cart (default → … → loading/`aria-busy` → success → disabled) and treats
  out-of-stock as a *disabled radio*, satisfying Nielsen "Error prevention" and
  "Visibility of system status."
- **Color/state & contrast (dim 4):** Every variant signal is redundant — label +
  ring + checkmark — passing 1.4.1; the selection ring and chip borders meet
  1.4.11 3:1; the button label uses a verified 4.5:1 token (1.4.3); `forced-colors`
  is mapped to system `Highlight`.
- **Accessibility — operability (WCAG 2.1.1, 4.1.2, 4.1.3, 2.4.11, 2.5.8):**
  Native radios give roving arrow-key selection; the gallery follows APG Tabs;
  zoom is a `<dialog>` with ESC + focus trap + restore; status uses a persistent
  `role="status"`/`aria-live` region instead of a silent toast; targets >= 24px
  (44px coarse); focus rings are visible and not obscured.
- **Typography craft + density (dims 3, 5):** 16px floor, fluid `clamp()` with a
  rem term (survives 200% zoom, 1.4.4), ~65ch measure, line-height 1.5, and a
  clear price-as-anchor hierarchy in the buy box.
- **Attention path & hierarchy (dim 1):** Sticky buy box, price as the
  typographic anchor, variant → availability → CTA order, and the gallery/price
  reacting to the chosen variant give a deliberate path rather than "make the
  button bright."
- **Composition (dim 2):** A 12-col 7/5 split, the 4px spacing scale, container
  queries on the buy box and review cards, and verified 320px reflow (1.4.10).

## Regression checks

A future answer to this prompt must still pass all of these:

- The LCP hero image is NOT lazy-loaded; it is preloaded with
  `fetchpriority="high"`, and every gallery/media slot reserves space via
  `aspect-ratio` or explicit `width`/`height` (CLS <= 0.1, LCP <= 2.5s).
- Variant selection never relies on color alone: each swatch/size carries a text
  label plus a non-color selection indicator (ring/checkmark), satisfying WCAG
  1.4.1, with selection/border tokens at >= 3:1 (1.4.11).
- Out-of-stock variants are surfaced as disabled, clearly-labeled ("Sold out")
  controls so an unavailable combination cannot be added to cart (Nielsen Error
  prevention) — not hidden inside a `<select>`.
- Body text is >= 16px (1rem), fluid type uses `clamp()` with a rem term, reading
  measure is capped near 65ch, and layout survives 200% zoom and a 320px viewport
  (WCAG 1.4.4, 1.4.10).
- Add-to-cart confirmation and stock/validation messages use a persistent
  `aria-live`/`role="status"` region, not a vanishing toast (WCAG 4.1.3), and the
  button exposes a real loading/disabled state.
- The zoom/lightbox is a `<dialog>` (or equivalent) with ESC to close, a focus
  trap, and focus restored to the trigger; no keyboard trap (WCAG 2.1.1, 2.1.2,
  2.4.11).

Target quality for the strong response is 4/5 across the eight design-quality
dimensions — strong and shippable, with room left for motion craft and brand
expression. This remains a synthetic calibration fixture and is not a substitute
for testing against a live storefront with actual shoppers.
