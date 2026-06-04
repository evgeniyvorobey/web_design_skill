# Visual review fixture: Checkout form, desktop 1280px with sticky order summary

## Review setup

This is a text fixture that stands in for a static screenshot of a single checkout
page. It exists to calibrate Mode D (visual review) by encoding exactly what a
competent reviewer can and cannot conclude from one desktop frame.

**Synthetic fixture only** — there is no live build behind this description. The
reviewer is scoring the frame as rendered, not auditing a running app. Treat every
measurement below as ground truth captured from the artboard. Where behavior is not
visible in a still frame (hover, focus ring, async errors), the fixture states the
intended spec so the reviewer knows what to assume versus what to flag.

Render target: light theme, logged-out guest checkout, one shipping address entered,
payment step not yet started. Default browser zoom 100%, no forced-colors mode active
in the captured frame.

## Page description

A single-column page chrome wrapping a two-column checkout body at the desktop
breakpoint. The left rail (~760px) holds the form: contact, shipping address,
delivery method, and payment. The right rail (~380px) holds a sticky order summary
card with line items, a promo-code input, the cost breakdown, and the primary
"Pay $214.60" button. The visible state shows the Contact and Shipping sections
completed (filled inputs), Delivery method as a radio group with the "Standard"
option selected, and the Payment section as the next actionable block with an empty,
focused card-number field.

A slim top bar shows a wordmark logo on the left and a "Secure checkout" lock label
on the right; there is no global nav, matching a focused conversion flow. A footer
with legal links sits below the fold.

## Viewport specs

- Desktop frame (primary): **1280px** wide, 832px tall visible, 12-column grid,
  72px outer gutters, 24px column gap, content max-width 1136px, centered.
- Form rail spans columns 1-7 (~760px); summary rail spans columns 8-12 (~380px).
- Mobile-web reference frame (described, not the primary art): **390px** wide; the
  two columns reflow to one, summary collapses into an expandable "Order summary
  ($214.60)" `<details>` disclosure pinned above the form, primary button becomes a
  sticky bottom bar inside a `position: sticky` footer (not a floating overlay).
- Reflow floor checked at **320px**: fixture asserts no horizontal scroll, but see
  Expected critique — the summary card min-width is suspect.
- Sticky behavior: summary card uses `position: sticky; top: 24px` within the right
  rail; it stops sticking when its container's bottom is reached.

## Visible hierarchy

1. `h1` "Checkout" — top of form rail, 28px.
2. Order summary total "Pay $214.60" inside the primary button — strongest single
   visual weight on the page (filled brand button, top of the right rail).
3. Section headings `h2`: "Contact", "Shipping address", "Delivery method",
   "Payment" — 20px, consistent left alignment with the form fields.
4. Field labels and the cost breakdown rows — body weight.
5. Footer legal links — de-emphasized, 14px.

Heading outline is one `h1` then four `h2`s with no skipped levels. The summary card
title "Order summary" is also an `h2`, giving five `h2`s total — flag-worthy only if
the reviewer can argue the card title competes with form sections (see Severity).

## Components

- **Text inputs**: 44px tall, 1px border `#9AA0A6` on `#FFFFFF`, 8px radius, 16px
  label above field, 12px vertical gap between fields. Filled fields show value in
  `#202124`.
- **Radio group (Delivery method)**: three stacked cards, each 56px tall, selected
  card has a 2px `#1A73E8` border + tinted `#E8F0FE` fill; unselected cards use the
  1px `#9AA0A6` border.
- **Promo-code field + "Apply" button**: input plus a secondary (outline) button,
  inline, right-aligned Apply.
- **Cost breakdown**: Subtotal, Shipping, Tax, Total rows; Total is 18px semibold.
- **Primary button**: "Pay $214.60", full-width of summary rail (~380px), 48px tall,
  `#1A73E8` fill, white label.
- **Secondary links**: "Edit" affordances next to completed Contact and Shipping
  sections, rendered as 14px `#1A73E8` text links.
- **Trust row**: small card-network icons + "Encrypted" text under the Pay button.

## Typography

Font stack: `Inter, system-ui, sans-serif`, `font-display: swap`, Inter preloaded.

- `h1` "Checkout": **28px / 1.75rem**, line-height 1.25, weight 600.
- `h2` section titles: **20px / 1.25rem**, line-height 1.3, weight 600.
- Body / input values: **16px / 1rem**, line-height 1.5, weight 400.
- Field labels: **14px / 0.875rem**, line-height 1.4, weight 500.
- Helper / hint text under inputs: **13px / 0.8125rem**, line-height 1.4 — below the
  16px body minimum (see Expected critique).
- Cost breakdown rows: 16px; Total row 18px / 1.125rem weight 600.
- Footer links: 14px / 0.875rem.
- Fluid sizing on `h1` only: `clamp(1.5rem, 1.2rem + 1.2vw, 1.75rem)`; all other
  sizes are fixed px (no fluid ramp on `h2`).

## Color and state notes

Contrast pairs (the reviewer should trust these numbers):

- Body text `#202124` on `#FFFFFF`: **15.8:1** — passes 1.4.3 AA.
- Field label `#5F6368` on `#FFFFFF`: **5.9:1** — passes.
- Helper hint `#80868B` on `#FFFFFF`: **3.5:1** — **fails 1.4.3** for 13px text
  (needs 4.5:1).
- Input border `#9AA0A6` on `#FFFFFF`: **2.6:1** — **fails 1.4.11** non-text
  contrast (needs 3:1) for the resting field boundary.
- Primary button: white `#FFFFFF` on `#1A73E8`: **4.6:1** — passes 1.4.3 (large/UI).
- Selected radio border `#1A73E8` on `#FFFFFF`: 3.6:1 — passes 1.4.11.
- Placeholder text `#9AA0A6` on `#FFFFFF`: 2.6:1 — fails if placeholder is the only
  label, but labels are persistent here, so this is informational.

Required-field indication: required fields are marked with a red asterisk `#D93025`
only, no text "(required)" — partial reliance on color (see Expected critique re:
1.4.1).

## Interaction states

The frame is a still capture; these are the intended specs the reviewer should
assume rather than independently verify:

- **Focus**: 2px `#1A73E8` `:focus-visible` ring with 2px offset on all inputs,
  radios, and buttons. The captured frame shows the card-number field focused.
- **Hover** (pointer: fine): button darkens to `#1765CC`; links underline.
- **Active / loading**: Pay button shows an inline spinner + "Processing..." and is
  `aria-busy="true"`; the form is not disabled wholesale.
- **Error**: per-field error text in `#D93025` with an inline alert icon, tied via
  `aria-describedby`, plus a summary `aria-live="assertive"` region above the form.
- **Empty / disabled**: Apply button is disabled until the promo field is non-empty.
- **Touch (pointer: coarse)** on the mobile-web frame: targets >=44px; the desktop
  "Edit" text links are ~32px tall hit areas — meets 2.5.8 (24px) but not 2.5.5 AAA.

## Known constraints

- Single static frame; no video, no live DOM. Hover/focus/animation are described,
  not shown (except the one focused field).
- No design tokens, CSS, or HTML source is provided — only rendered measurements.
- Brand palette is fixed (`#1A73E8` primary); the reviewer may not propose a brand
  recolor, only contrast-safe adjustments.
- Copy is placeholder-realistic; microcopy quality is in scope, content strategy is
  not.

## Expected critique

A good reviewer should surface these (severity = Nielsen 0-4):

1. **[Sev 3] Input border fails non-text contrast.** Resting field border `#9AA0A6`
   on white is 2.6:1, below the 3:1 floor of WCAG 1.4.11. Fields read as low-affordance
   and the boundary may vanish in bright conditions. Fix: darken to >=`#74787D`.
2. **[Sev 3] Helper hint text fails AA.** 13px `#80868B` on white is 3.5:1 (needs
   4.5:1, 1.4.3) and is below the 16px body minimum. Bump size to 16px and darken to
   >=`#5F6368`.
3. **[Sev 2] Required-field meaning carried by color alone.** Red asterisk only
   leans on 1.4.1 (use of color). Add a visible "(required)" or mark optional fields
   instead, and expose via `aria-required`.
4. **[Sev 2] 320px reflow risk on the summary card.** Fixture asserts no scroll, but
   the ~380px summary min-width plus line-item labels is the likely overflow point at
   320px (1.4.10). Verify the card flexes/wraps below 360px.
5. **[Sev 2] Total "Pay $214.60" duplicates the price two places** (button + Total
   row) without a clear single source — minor, but if they ever disagree it is an
   error-prevention (heuristic 5) and trust problem.
6. **[Sev 1] Five `h2`s flatten section ranking.** The "Order summary" card title
   shares the `h2` level with the four form steps, slightly muddying the form's
   sequential outline. Consider an `h2`/`h3` split or visual de-emphasis.
7. **[Sev 1] Promo "Apply" disabled-until-typed has no visible hint.** Acceptable,
   but a reviewer may note the disabled state needs a non-color cue and an accessible
   name explaining why.

## Prohibited critique

The reviewer must NOT make these claims from this fixture alone:

- **Do not claim** the focus ring is missing or invisible — the spec states a 2px
  `#1A73E8` `:focus-visible` ring at 2px offset; only the card-number field shows it
  because it is the focused element in this still.
- Do not claim body text fails contrast — `#202124` on white is 15.8:1.
- Do not claim there is no error handling — per-field errors and an `aria-live`
  summary are specified; they are simply not triggered in this captured state.
- Do not claim the primary button contrast fails — white on `#1A73E8` is 4.6:1.
- Do not claim a missing global nav is a defect — a focused checkout intentionally
  omits top nav to reduce exits; that is a conversion pattern, not an error.
- Do not claim LCP/INP/CLS numbers — no performance trace is in scope here; you may
  only note static risks (e.g., unreserved image space) if the fixture shows them,
  and it does not.
- Do not invent touch-target failures on desktop "Edit" links — they are ~32px,
  which meets 2.5.8 (24px); AAA 44px is not the AA bar.

## Severity expectations

Nielsen 0-4 scale (0 = not a problem, 4 = catastrophe):

- The two contrast failures (border, helper text) are the highest at **Sev 3** —
  real accessibility violations, not cosmetic, but localized and easily fixed.
- The color-only required marker and 320px reflow risk are **Sev 2** — would
  bite a subset of users / narrow viewports.
- Heading flattening and duplicated price are **Sev 1** — minor, fix if time allows.
- A reviewer who escalates any single contrast fix to **Sev 4** is over-scoring;
  none of these block the happy-path checkout for most users.

## Rubric score expectation

Scored against the 8 design-quality dimensions:

- **Current expected: 3.5/5.** Strong attention path (button is the clear primary
  action), clean composition and rhythm, solid type scale on headings/body. Held
  back by color/state & contrast (border + helper failures, color-only required),
  and a small production-readiness gap (sub-16px helper text, 320px reflow unproven).
- **Projected after Expected critique fixes: 4.3/5.** Darkening the border and helper
  text, adding a non-color required indicator, and confirming the 320px reflow lift
  color/state and production readiness to 4/5 each, clearing the "strong and
  shippable" bar without touching the brand palette or layout.
