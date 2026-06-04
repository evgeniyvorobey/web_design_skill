# Golden example: Ecommerce PDP into add-to-cart and checkout

A compact calibration example of a strong, shippable (4/5) web answer. The prompt is a realistic request; the golden output is a condensed but concrete response; the notes explain the scoring.

## Prompt

```text
We're an apparel brand on Shopify-style infra. Design the product detail page (PDP)
for a pair of running shoes, the add-to-cart interaction, and the first checkout step
(contact + shipping). Mobile-first, but it has to feel dense and fast on desktop too.
Hand it to engineering — I want real values, states, and accessibility called out,
not vibes. Conversion matters, so don't bury the buy box.
```

## Golden output

```md
# Running Shoe PDP into Checkout

## Information architecture

One `h1` = product name. Heading outline never skips levels: `h1` product
title, then `h2` for Gallery / Buy box / Details / Reviews / Recommendations.
Landmarks: `header`, `nav` (breadcrumb), `main`, `footer`. A skip link
("Skip to product details") is the first focusable element.

Route flow: `/products/velocity-runner` (PDP) -> cart side-sheet -> `/checkout`
(contact + shipping). Cart state lives in a URL-shareable cart token; back/forward
and reload restore the cart (History API + scroll restoration). A `beforeunload`
guard fires only on the checkout step when fields are dirty.

## Layout and grid

Mobile-first, 12-col desktop grid, `max-inline-size: 1200px` container, 24px gutters.

- 320-639px: single column. Gallery scrolls away; buy box flows below it.
- 640-1023px: gallery left, details right at a 7/5 split, reading copy capped ~65ch.
- 1024px+: gallery 7 cols, buy box 5 cols and `position: sticky; top: 24px` so price,
  size, and the add-to-cart button stay on screen while specs scroll. This is where we
  exploit desktop density — thumbnails, size grid, and shipping estimate are all
  visible without scrolling.

Reserve media space to protect CLS: every gallery image ships `width`/`height` and
`aspect-ratio: 4 / 5`; the LCP hero is `fetchpriority="high"` and preloaded.

## Type and spacing

Body 1rem (16px) minimum, line-height 1.5. Fluid headings carry a rem term:
`h1 { font-size: clamp(1.5rem, 1.2rem + 1.5vw, 2.25rem); line-height: 1.2; }`.
Price uses `font-variant-numeric: tabular-nums` so it does not jiggle across variants.
Spacing from the 4px scale: 8 inside chips, 16 between form rows, 24 section padding,
48 between major sections. Font loading: `font-display: swap`, preload the
above-the-fold weight, fallback metrics tuned to the web font to avoid reflow.

## Buy box (the conversion core)

Order, top to bottom: name, star rating (anchors to reviews), price, color swatches,
size selector, add-to-cart, shipping/returns reassurance.

The size selector is a `radiogroup` (WAI-ARIA APG Radio Group pattern), not a native
`select`, so all sizes are visible and arrow-key navigable. Each size is a 44px target
(exceeds the 2.5.8 24px floor; meets 2.5.5 AAA 44px). Sold-out sizes use
`aria-disabled="true"` plus a diagonal strike AND the text "Sold out" on focus — never
color alone (1.4.1). The selected state is a filled token plus a checkmark glyph, not
hue alone.

The primary button is a native `<button>`: "Add to cart - $140". One primary action
per view; "Save to wishlist" takes the secondary (outline) treatment. On mobile, a
pinned bottom action bar (NOT a floating circular button) keeps add-to-cart reachable
and carries the live price and selected size.

States for add-to-cart:
- default / hover / `:focus-visible` (2px outline, `outline-offset: 2px`) / active
- disabled until a size is chosen, with helper text "Select a size" so the disabled
  state is explained, not mysterious
- loading: spinner + `aria-busy="true"`, label switches to "Adding…", width locked to
  prevent layout shift
- success: the cart side-sheet opens and `aria-live="polite"` announces "Velocity
  Runner, size 10, added to cart"
- error (network or oversold race): inline `role="alert"` "That size just sold out —
  pick another", the button returns to default, focus moves to the size group

## Add-to-cart side-sheet (overlay contract)

A `<dialog>`-backed off-canvas panel slides from the inline-end edge. ESC closes;
scroll-lock on `body`; focus is trapped inside and restored to the add-to-cart button
on close (2.4.3 focus order; 2.4.11 focus not obscured — the sticky header never covers
the focused control). Contents: line item with thumbnail, quantity stepper
(`-` / value / `+`, each a 44px target, value in an `aria-live` region), subtotal,
"Checkout" primary + "View cart" secondary. The free-shipping progress uses a bar AND
a label ("$10 to free shipping"), not color alone.

## Checkout step 1: contact + shipping

Single-column form, ~480px field column even on wide screens (forms do not get denser
when wider — they get error-prone). Labels are visible and persistent (no
placeholder-as-label). Inputs declare intent for the on-screen keyboard and autofill:

- Email: `type="email" inputmode="email" autocomplete="email"`
- Postal code: `inputmode="numeric" autocomplete="postal-code"`
- Phone: `type="tel" autocomplete="tel"`
- Address: `autocomplete="address-line1"`, and so on

Validation runs on blur, not on every keystroke; errors render with `aria-describedby`
linking the field to its message, an icon plus text (1.4.1), and `aria-invalid="true"`.
On submit, a summary `role="alert"` at the top lists errors and links to each field.
Button hierarchy: primary "Continue to payment", secondary text link "Return to cart".
No keyboard trap; tab order matches visual order (2.1.1, 2.4.3).

The order summary is a collapsible `<details>` on mobile (collapsed, with the total
visible) and a sticky sidebar on desktop. Totals use tabular-nums and a clear ladder:
subtotal / shipping / tax / **Total**.

## Color, contrast, and forced colors

Body text 4.5:1 against its background; large headings and the price >=3:1 (1.4.3).
Focus ring and input borders meet 1.4.11 non-text 3:1. Error red is paired with an
icon and text so it survives `@media (forced-colors: active)` (Windows High Contrast)
— we let system colors through and keep `outline` on focus. We honor
`prefers-reduced-motion`: the side-sheet slide and the add-to-cart success pulse drop
to a simple opacity fade.

## Responsive and reflow

Verified at the 320px reflow floor (1.4.10): no horizontal scroll, and the pinned
bottom bar still fits the add-to-cart label. Container queries drive the recommendation
cards so a 2-up rail becomes 1-up inside a narrow slot regardless of viewport. The text
spacing override (1.4.12) and 200% zoom (1.4.4) both leave the buy box usable.

## Performance budget

LCP <= 2.5s (preloaded hero, `fetchpriority="high"`, no render-blocking gallery JS);
INP <= 200ms (size selection and quantity steppers are pure DOM, no round-trip);
CLS <= 0.1 (reserved media + locked button widths + font fallback metrics). Gallery
thumbnails below the fold use `loading="lazy"`.

## Engineering handoff checklist

- [ ] Size `radiogroup`: keyboard nav + sold-out (`aria-disabled`, text, strike)
- [ ] Add-to-cart six states incl. loading width-lock and `aria-busy`
- [ ] Side-sheet `<dialog>`: ESC, scroll-lock, focus trap + restore, `aria-live` add
- [ ] Checkout fields: correct `type`/`inputmode`/`autocomplete`, blur validation,
      `aria-describedby` errors, submit `role="alert"` summary
- [ ] Sticky buy box (desktop) and pinned bottom bar (mobile), tested at 320px
- [ ] CWV: preload hero, reserve media, tabular-nums price, reduced-motion paths
```

## Design-quality notes

Quality target: 4/5

Why this lands at 4/5 (strong and shippable) across the relevant dimensions:

- **Attention path and hierarchy (4):** The buy box is never buried — sticky on
  desktop, pinned bottom bar on mobile — and there is exactly one primary action per
  view. The heading outline and landmarks give a reading order that matches the visual
  order.
- **Composition and spacing (4):** A real 12-col grid with a 1200px container, a 7/5
  split that collapses sanely to the 320px floor, and a consistent 4px spacing scale.
  Forms deliberately stay narrow (~480px) instead of stretching with the viewport.
- **Typography craft (4):** 16px floor, 1.5 body leading, `clamp()` fluid headings with
  a rem term, ~65ch measure, and tabular-nums on prices so variant switches do not
  shift numbers.
- **Color/state and contrast (4):** Named WCAG criteria (1.4.3, 1.4.11, 1.4.1) are
  applied, not merely cited; sold-out and selected states never rely on color alone;
  forced-colors and reduced-motion are handled.
- **Density and rhythm (4):** Desktop density is exploited where it pays (the sticky
  buy box keeps price + size + CTA on screen; thumbnails and shipping stay visible)
  rather than flattening the desktop into a phone layout — while the checkout form
  resists false density.
- **Interaction polish and motion (4):** Add-to-cart carries a full state set (default,
  hover, focus-visible, active, disabled-with-reason, loading, success, error), the
  side-sheet honors the full overlay contract (ESC, scroll-lock, focus trap + restore,
  `aria-live`), and motion respects `prefers-reduced-motion`.
- **Production readiness (4):** Explicit CWV budgets with concrete mechanisms, correct
  input affordances (`inputmode`/`autocomplete`), and a handoff checklist an engineer
  can actually tick through.

What would push this to 5/5:

- Name the design tokens (color, space, radius, elevation scale) and the exact
  focus-ring token, so the buy box and checkout are pixel-reproducible from a shared
  system rather than described inline.
- Add the resilience screens the prompt implies but the output only gestures at:
  payment-declined, session-expired mid-checkout, offline (cart cached and replayed),
  plus the empty-cart and 404-product states.
- Give measured evidence instead of budgets: a field-data or Lighthouse trace showing
  LCP, INP, and CLS actually hitting target, plus a documented keyboard-only and
  screen-reader pass of the size group, side-sheet, and checkout form against the
  WAI-ARIA APG patterns.
