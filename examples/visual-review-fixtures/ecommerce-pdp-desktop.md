# Visual review fixture: Ecommerce product detail page, desktop 1280px

## Review setup

**Synthetic fixture only.** This file is a text stand-in for a screenshot or Figma frame. It exists to calibrate Mode D visual reviews: a good reviewer reads the description below and should surface the issues listed under **Expected critique** while avoiding everything under **Prohibited critique**. There is no live DOM, no running CSS, and no rendered pixels — only the prose specification. Treat every value here as ground truth for the review; do not invent measurements that are not stated.

Reviewer task: critique the product detail page (PDP) as described, score it on the 8 design-quality dimensions, and rank findings on the Nielsen 0–4 severity scale.

## Page description

A direct-to-consumer apparel storefront PDP for a single product: "Merino Crew Sweater — Slate." The page renders at a 1280px desktop viewport inside a centered 1200px content container (40px gutters). A 390px mobile-web reflow is described for contrast but is secondary.

Above the fold the layout is a two-column split: a sticky media gallery on the left (~620px wide) and a buy-box column on the right (~520px wide) holding title, price, swatches, size selector, and the primary "Add to cart" button. Below the fold, full-width sections stack: a tabbed details/specs block, a size-and-fit table, a star-rating reviews summary with a sortable reviews list, and a "You may also like" carousel of four product cards. A persistent top nav with mega-menu sits above; a fat footer closes the page.

The visual tone is editorial and quiet — generous whitespace, a near-monochrome palette with one warm accent. The brand wants the page to feel "premium and calm" but also to convert.

## Viewport specs

- **Primary viewport:** 1280px desktop (breakpoint ladder rung: 1280). Content container 1200px max-width, centered, 40px left/right gutters. The internal split uses the 12-col desktop grid: gallery spans 6 cols, buy box spans 5 cols, 1 col of gap.
- **Secondary viewport (reflow reference):** 390px mobile-web. Columns stack to a single column; the gallery becomes a horizontal swipe strip; the buy box flows beneath. Sticky behavior is disabled below 768px.
- **Reading column:** long-form spec copy in the details tab is constrained to ~65ch; review bodies are ~60ch.
- **Vertical rhythm:** section padding 64px top/bottom on desktop, 32px on mobile-web. Card and control spacing follows the 4px scale (4 / 8 / 12 / 16 / 24 / 32 / 48 / 64).

## Visible hierarchy

1. Product title (h1) "Merino Crew Sweater — Slate."
2. Price "$148" with a struck-through "$185" compare-at price beside it.
3. Color swatch row (5 swatches) and the selected-color label.
4. Size selector (XS–XXL as a segmented button group) plus a "Size guide" text link.
5. Primary CTA "Add to cart" (filled accent button), full-width within the buy box.
6. Secondary "Add to wishlist" (heart icon-only button) to the right of the CTA.
7. Trust row: "Free shipping over $75 · Free 60-day returns."
8. Below fold: Details / Specs tabs (h2), Size & fit table (h2), Reviews (h2), You may also like (h2).

The intended attention path is title → price → color → size → Add to cart. Headings below the fold use a single h1 and h2 section heads, no skipped levels.

## Components

- **Sticky media gallery:** one large hero image (620 × 775px, 4:5) with a vertical thumbnail rail of 5 thumbnails (64 × 80px each) on its left edge. The hero is `position: sticky; top: 24px`. Thumbnails are `<button>`s; the active thumbnail carries a 2px accent ring. The hero ships with explicit `width`/`height` so its box is reserved (aspect-ratio 4:5), preventing layout shift.
- **Buy box:** title, price, swatches, size group, CTA, wishlist, trust row.
- **Color swatches:** 5 round chips, each 28 × 28px, rendered as `<input type="radio">` styled chips inside a `<fieldset>` with a visually-hidden `<legend>` "Color". Selected state = accent ring + the text label "Slate" updates below the row. Out-of-stock colors render at 40% opacity with a diagonal slash.
- **Size selector:** a segmented group of 6 `<button>`s (XS, S, M, L, XL, XXL), each 40px tall × 56px wide, 8px gap. Unavailable sizes are dimmed to 40% opacity and set `aria-disabled`. No size is preselected; the CTA is enabled regardless.
- **Add to cart button:** filled accent button, 48px tall, full buy-box width, label "Add to cart." On click it shows an inline spinner and the cart count in the nav increments via an `aria-live="polite"` region.
- **Wishlist button:** 24 × 24px icon-only heart `<button>` with `aria-label="Add to wishlist"`. The hit target is exactly 24 × 24px with no surrounding padding.
- **Tabs (Details / Specs / Care):** WAI-ARIA APG Tabs pattern (`role="tablist"`, arrow-key navigation, `aria-selected`). Panels swap without a scroll jump.
- **Size & fit table:** a real `<table>` — columns Size / Chest (in) / Length (in) / Sleeve (in), 6 body rows, `<th scope="col">` headers, sticky header on scroll within the block.
- **Reviews:** average "4.6" with a 5-star glyph row, count "(212)", a sort `<select>` (Most recent / Highest / Lowest), and a list of review cards each with a star row, author, date, body (~60ch), and a "Helpful" toggle button.
- **Recommendations carousel:** 4 product cards, horizontal, with prev/next `<button>`s. Cards have image, name, price.

## Typography

System UI variable font, `font-display: swap`, above-the-fold display weight preloaded; fallback metrics tuned to avoid CLS.

- **Body:** 16px / 1rem, line-height 1.5, weight 400.
- **Product title (h1):** fluid `clamp(1.75rem, 1.4rem + 1.2vw, 2.25rem)` — 28px → 36px, line-height 1.25, weight 600.
- **Price (current):** 1.5rem / 24px, weight 600, line-height 1.2.
- **Compare-at price:** 1rem / 16px, weight 400, line-through.
- **Section h2:** 1.5rem / 24px, line-height 1.3, weight 600.
- **Swatch/size labels:** 0.875rem / 14px, line-height 1.4.
- **Trust row:** 0.8125rem / 13px, line-height 1.4.
- **Microcopy (review dates, "Helpful (12)"):** 0.75rem / 12px, line-height 1.4.
- Spec body copy capped at ~65ch; review bodies ~60ch.

## Color and state notes

Near-monochrome with one warm accent. Stated foreground/background pairs (sRGB):

- **Body text** `#2A2D31` on `#FFFFFF` — contrast ≈ 13.1:1 (passes 1.4.3 AA and AAA).
- **Trust row** `#6B7177` on `#FFFFFF` — contrast ≈ 4.6:1 at 13px (passes AA for normal text).
- **Compare-at struck price** `#9AA0A6` on `#FFFFFF` — contrast ≈ 2.9:1 (FAILS 1.4.3 AA for the 16px strikethrough text).
- **Accent CTA:** label `#FFFFFF` on accent fill `#C8642A` (warm terracotta) — contrast ≈ 3.4:1 (FAILS 1.4.3 AA for the 16px button label).
- **Accent ring / selected swatch indicator:** `#C8642A` ring on `#FFFFFF` — non-text contrast ≈ 3.1:1 (passes 1.4.11 3:1 as a UI indicator).
- **Discount cue:** the markdown is communicated *only* by the accent color of the current price plus the strikethrough — no "Sale" text label or percent-off badge (relevant to 1.4.1 use of color).
- **Out-of-stock swatch:** 40% opacity + diagonal slash; the slash is a non-text graphic at ≈ 2.4:1 against the chip.
- **Focus indicator:** `:focus-visible` = 2px `#1A57C4` outline + 2px offset on all interactive controls; ≈ 4.9:1 against white (passes 1.4.11).
- **Disabled/unavailable size:** 40% opacity text, no other cue.

## Interaction states

- **Default / hover / :focus-visible / active** are defined for CTA, swatches, size buttons, tabs, carousel arrows, and the wishlist heart. Hover on cards lifts 2px with a shadow; `@media (pointer: coarse)` suppresses the hover-lift.
- **Loading:** Add-to-cart shows an inline spinner; the recommendations rail shows skeleton cards on first paint.
- **Empty:** the reviews block has an empty state ("Be the first to review") when count = 0.
- **Error:** if add-to-cart fails, an inline error message renders below the button and is announced via `aria-live="assertive"`.
- **Success:** the cart count increments via `aria-live="polite"`; no toast.
- **Disabled:** unavailable sizes use `aria-disabled` (focusable, not actionable).
- **Keyboard:** tab order follows DOM (title → swatches → sizes → CTA → wishlist → tabs → table → reviews → carousel). Tabs use arrow keys; carousel arrows are reachable. No skip link to the buy box is present. The "Size guide" link opens a `<dialog>` with focus trap, ESC-to-close, and focus restore.
- **Reflow (320–390px):** single column, no horizontal scroll at 320px; size buttons wrap to two rows.

## Known constraints

- The compare-at price color and the CTA fill color are locked brand tokens for this fixture; the reviewer should still flag them, but note that they are brand-locked.
- No real product imagery is described beyond dimensions.
- Analytics, pricing logic, and inventory sync are out of scope.

## Expected critique

A strong reviewer SHOULD raise these, roughly in priority order:

1. **CTA label contrast fails 1.4.3 (Severity 4).** "Add to cart" white text on `#C8642A` is ≈ 3.4:1 — below the 4.5:1 AA floor for 16px text. This is the single most important conversion control on the page; darken the fill (e.g. toward `#A24A18`, ≈ 5.6:1) or use a darker label.
2. **Compare-at struck price fails 1.4.3 (Severity 3).** `#9AA0A6` at 16px is ≈ 2.9:1. Darken into the `#767C82` range for 4.5:1; strikethrough alone does not exempt it from contrast.
3. **Discount communicated by color + strikethrough only — 1.4.1 use of color (Severity 3).** No "Sale" text or percent-off badge. Color-blind and low-vision shoppers may not perceive the markdown. Add a text label such as "Sale −20%."
4. **Wishlist hit target is 24 × 24px with no padding — borderline 2.5.8 (Severity 3).** It meets the 24px AA minimum exactly but has zero spacing slack; on a dense buy box adjacent to the CTA this invites mis-clicks. Recommend a ≥ 24px target with padding, ideally toward 44px (2.5.5 AAA).
5. **No size preselected yet the CTA is enabled (Severity 3).** A shopper can add to cart with no size chosen; either preselect a default, gate the CTA on selection, or surface an inline "Choose a size" validation tied to `aria-live`.
6. **Out-of-stock swatch slash is low non-text contrast ≈ 2.4:1 — 1.4.11 (Severity 2).** The 40% opacity + label partly redeem it, but the slash glyph alone is below 3:1. Strengthen the slash or add explicit "Out of stock" text on focus/hover.
7. **No skip link to the buy box / main content (Severity 2).** Keyboard users tab through the full mega-menu before reaching the title; a "Skip to product" link would shorten the path (2.4.1).
8. **Disabled size relies on 40% opacity alone for state (Severity 2).** `aria-disabled` carries it for assistive tech, but the visual-only opacity cue is weak and the dimmed label may itself drop below contrast; add a slash or "Sold out" affordance.
9. **Attention-path / hierarchy nit (Severity 1).** Current price 24px vs h1 28–36px is fine, but the compare-at price at full 16px body weight competes with the trust row; de-emphasize it further so the eye lands title → price → size → CTA cleanly.
10. **Density strength (Severity 1).** At 1280px the size table and reviews exploit desktop density well (sticky `<th>`, sortable list). Call this out as a strength, not a defect.

## Prohibited critique

Do not raise these — they are not supportable from this text, or are explicitly handled:

- **Do not claim** the page causes layout shift / fails CLS. The hero reserves space via explicit width/height and 4:5 aspect-ratio, and fonts use `font-display: swap` with tuned fallback metrics. CLS is addressed.
- Do not claim the focus indicator is missing or invisible; a 2px `#1A57C4` `:focus-visible` outline at ≈ 4.9:1 with 2px offset is specified for all controls.
- Do not claim body text fails contrast; `#2A2D31` on white is ≈ 13.1:1.
- Do not claim the tabs, size-guide dialog, or carousel are keyboard-inaccessible; an arrow-key tablist, a `<dialog>` with focus trap + ESC + focus restore, and reachable arrow buttons are specified.
- Do not claim the size & fit data is "just divs" or non-semantic; it is a real `<table>` with `<th scope="col">`.
- Do not claim there is a floating circular action control or that the CTA floats; the primary action is an in-flow filled button in the buy box.
- Do not invent mobile-web pixel values, gesture conflicts, or device-specific behaviors beyond the stated 390px reflow notes.
- Do not claim missing alt text or specific image content — imagery is described only by dimensions; alt text is neither specified nor contradicted, so it is out of scope.
- Do not claim the trust row fails contrast; `#6B7177` on white at 13px is ≈ 4.6:1, which passes AA for normal text.
- Do not invoke inspiration galleries (Awwwards, Land-book, Mobbin Web) as evidence for or against usability, accessibility, performance, or compliance.

## Severity expectations

Nielsen 0–4 scale (0 = not a problem, 1 = cosmetic, 2 = minor, 3 = major, 4 = catastrophe):

- **Severity 4 (must fix before ship):** CTA label contrast failure (#1).
- **Severity 3 (major):** compare-at price contrast (#2), use-of-color discount cue (#3), wishlist target slack (#4), no-size-but-enabled-CTA (#5).
- **Severity 2 (minor):** out-of-stock slash contrast (#6), missing skip link (#7), disabled-size opacity-only cue (#8).
- **Severity 1 (cosmetic):** hierarchy de-emphasis nit (#9), density note (#10, framed as a strength).

A reviewer who finds only Severity 1–2 items and misses the two contrast failures (#1, #2) has under-graded this fixture. A reviewer who reports CLS, missing focus rings, or non-semantic tables has over-reached.

## Rubric score expectation

Scored on the 8 dimensions (1–5 each), the page **as described** sits at a current **3/5** overall — strong layout, rhythm, and density let down by two AA contrast failures and a couple of state gaps on the most important controls.

| Dimension | Current | Projected after fixes |
| --- | --- | --- |
| Attention path & hierarchy | 4 | 4 |
| Composition & spacing | 4 | 4 |
| Typography craft | 4 | 4 |
| Color/state & contrast | 2 | 4 |
| Density & rhythm | 4 | 4 |
| Interaction polish & motion | 3 | 4 |
| Context & brand fit | 4 | 4 |
| Production readiness | 3 | 4 |

**Projected after fixes: 4/5** — once the CTA and compare-at contrast pass AA (#1, #2), the discount carries a text cue (#3), and the size/CTA validation plus wishlist target slack are resolved (#4, #5), the page is strong and shippable. Color/state & contrast is the dimension carrying the current deficit; everything else is already at or near target.
