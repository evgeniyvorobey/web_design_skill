# Ecommerce Domain Pack

Synthetic calibration material for shaping ecommerce web work: catalog browse, product detail (PDP), cart, checkout, and the trust signals that move a shopper from "looking" to "paid". This pack tunes hierarchy, trust language, state coverage, responsive and browser behavior, and handoff so a design lands at 4/5 on the eight design-quality dimensions and is buildable as-is.

## When To Use

Reach for this pack when the surface participates in a path-to-purchase: a category/PLP listing grid, a faceted search results page, a product detail page, a mini-cart or full cart, a multi-step or one-page checkout, an order-confirmation screen, or trust-adjacent pages (shipping, returns, size guide, store locator). It also applies to merchandising components that ride on top of those pages: price/promo badges, inventory and delivery-estimate widgets, ratings, "frequently bought together", and post-purchase upsell.

Do not use it for pure content marketing (campaign landing pages without a transactional grid), for account/settings flows with no cart, or for back-office order management. Those borrow individual patterns here but their primary job is not conversion under purchase anxiety.

The defining constraint of this domain: every screen is read by someone deciding whether to spend money, often on a phone, often comparing tabs. Friction and ambiguity are measured in lost revenue, so hierarchy and state coverage are not polish — they are the product.

## Primary User Jobs

- **Find a candidate quickly.** From a category grid or search, narrow a large catalog to a short list. Jobs: scan, filter (size, color, price, availability), sort, compare. The grid must surface price, primary image, and at-a-glance differentiators (color swatches, rating, "Few left") without a click.
- **Evaluate one product with confidence.** On the PDP: confirm this is the right variant (size/color/quantity), understand total cost (price + shipping + tax signals + any promo), judge quality (gallery, reviews, specs, Q&A), and de-risk the purchase (returns, delivery date, stock).
- **Assemble and review a cart.** Add, change quantity, remove, apply a code, see the running subtotal and the delta to free-shipping or a discount threshold. The shopper is doing arithmetic and wants the page to do it for them.
- **Pay with minimum friction.** Enter or autofill contact, shipping, and payment; pick a delivery option; confirm the order. Express paths (wallet buttons) should short-circuit this for known shoppers.
- **Confirm and track.** See an unambiguous "order placed", an order number, an itemized receipt, and what happens next (email, ship date, tracking).
- **Recover from a stumble.** Out-of-stock variant, declined card, expired session, invalid promo code, address that fails validation — the shopper needs a clear, non-blaming path forward, not a dead end.

## Trust And Safety Risks

Ecommerce trust failures are specific and costly. Design against these named risks:

- **Hidden-cost shock.** Shipping, tax, or fees that only appear at the final step are a top driver of checkout abandonment. Surface a shipping signal on the PDP and a full cost breakdown in the cart, not just at payment.
- **Dark patterns.** Pre-checked add-ons, fake scarcity ("Only 2 left" when untrue), countdown timers that reset, hard-to-find unsubscribe/remove controls, and drip pricing are increasingly regulated. Treat urgency and social-proof copy as claims that must be true; a design that depends on deception is not shippable.
- **Payment-security doubt.** Shoppers abandon when the payment step feels untrustworthy. Show recognizable payment marks, a lock affordance tied to real transport security (never a decorative padlock as the only signal), and never echo full card numbers.
- **Account/guest friction.** Forcing account creation before purchase is a known abandonment cause. Offer guest checkout as a first-class path.
- **Variant/price mismatch.** The price, image, and availability shown must update atomically when a variant changes. A user who adds a $40 item and is charged $60 will dispute and distrust.
- **Promo and coupon traps.** A code field that silently fails, or terms hidden behind fine print, erodes trust. State why a code was rejected (expired, minimum not met, not eligible).
- **Data minimization.** Ask only for what the purchase requires at the step it is required. Marketing opt-in is opt-in (unchecked), separated from the transactional consent.

Urgency, scarcity, and social-proof components carry the highest reputational and legal exposure; design them so the truthful state is the only state the component can render.

## Common Web Surfaces

- **Category / PLP (product listing page):** responsive product grid, faceted filter rail (sidebar on desktop, off-canvas or bottom sheet on small screens), sort control, applied-filter chips, pagination or load-more/infinite scroll with a stable URL, result count.
- **Search results:** the PLP plus query echo, zero-results state with suggestions, typo/synonym handling, and scoped filters.
- **PDP (product detail page):** image gallery (thumbnails + zoom), title, price block (price, compare-at, unit price, promo), variant selectors (swatches, size pills/select), quantity stepper, primary "Add to cart" plus optional "Buy now"/wallet express, delivery-estimate and stock widget, accordions for details/shipping/returns, reviews, recommendations.
- **Cart:** line items with thumbnail, variant, quantity stepper, line price and remove; order summary with subtotal, shipping estimate, tax signal, discount, and total; promo field; free-shipping progress meter; primary "Checkout" and secondary "Continue shopping"; saved-for-later and empty-cart states.
- **Mini-cart / side-sheet:** slide-in panel after add-to-cart confirming the item with subtotal and a checkout CTA, dismissible with ESC.
- **Checkout:** contact, shipping address with validation, delivery method, payment, review/place-order; order summary persistent in a side rail (desktop) or collapsible (small screens); guest vs. account choice; express wallet buttons at the top.
- **Order confirmation:** order number, itemized receipt, shipping/delivery info, next steps, account-creation offer for guests.
- **Trust pages:** shipping & returns, size guide (often a dialog from the PDP), store locator, reviews detail.

## Hierarchy Guidance

The conversion path dictates emphasis. One primary action per surface, sized and colored to win the contrast contest, with everything else demoted.

- **PLP:** the product card is the unit. Within a card the rank is image → price → name → differentiators (rating, swatches, scarcity). Keep one primary-action philosophy: either the whole card navigates to the PDP or a clear "Add to cart" sits on the card — do not make both compete. The filter rail is a tool, not a hero: visually quieter than the grid. Applied-filter chips must be obvious and individually removable.
- **PDP:** the buy box (price block + variant selectors + Add to cart) is the single dominant zone above the fold on desktop and pinned within reach on small screens. Rank: title and price → variant selection → primary CTA → trust strip (delivery date, returns, stock) → secondary detail (gallery interactions, reviews, specs). "Add to cart" is the only fully-weighted button; "Buy now" or wallet express is visually distinct but secondary. Reviews and recommendations live below the fold; never let them outrank the buy box.
- **Cart:** the order total and the "Checkout" button are the climax. Line-item controls are functional and quiet; the summary block is the emphasis. The free-shipping meter, if present, sits near the total where it motivates one more item.
- **Checkout:** strip global nav and distractions — this is a focused flow with a clear step indicator and a persistent order summary. The active step's primary action ("Continue to payment", "Place order") is the only loud element. Edit affordances for completed steps are present but quiet.
- **Price emphasis:** the price the shopper pays is the largest number in the price block; compare-at/strikethrough is smaller and uses strikethrough plus a label (never color alone, per WCAG 1.4.1) to signal a markdown.

Use one h1 per page (the product name on a PDP, the category name on a PLP), no skipped heading levels, and landmark regions (`header`, `nav`, `main`, `footer`) so the buy box and summary are reachable structurally, not just visually.

## State And Recovery Requirements

Every transactional component ships its full state set. Minimum coverage:

- **Product card / grid:** default, hover (desktop, with quick-add or quick-view intent), `:focus-visible`, loading (skeleton cards reserving final dimensions to protect CLS), empty/zero-results (with reset-filters and suggestions), error (catalog fetch failed, with retry).
- **Variant selector:** available, selected, unavailable-for-combination (visibly disabled with reason, not silently removed), out-of-stock, low-stock ("Only N left" only when true).
- **Add to cart:** default, hover, `:focus-visible`, active, pending/loading (button shows progress, stays in place to avoid layout shift), success (confirmation via mini-cart and an `aria-live="polite"` announcement), error (e.g., stock claimed during add), disabled (no variant chosen — pair with a hint so the disabled state is explained).
- **Quantity stepper:** min (1, or 0-with-remove), max (inventory cap with message), invalid input handling.
- **Promo / coupon field:** default, applying (loading), applied (with removable chip and the discount reflected in the total), rejected with a specific reason (expired, minimum not met, not eligible), surfaced via `aria-live` so assistive tech hears the result.
- **Cart:** populated, empty (with a path back to browse and to saved items), item-removed (with undo where feasible), price/availability changed since add (flag it before checkout), loading on quantity change (optimistic with rollback on failure).
- **Checkout:** field validation (inline, on blur and on submit, error summary at top linking to fields), address validation/suggestion, payment declined (clear, non-blaming, with retry and alternative method), 3-D Secure / step-up redirect handling, session-expired (preserve cart, re-auth without data loss), network failure mid-submit (idempotent — never double-charge; show a determinate pending state).
- **Order confirmation:** success; plus a recovery view for "payment captured but confirmation failed to load" that points to order history and email.
- **Global app states:** 404 (product/category not found, with search and popular links), 500, offline (queue the action or block with a clear message), session-expired.

Recovery principle: never strand the shopper with the cart as collateral. Failures preserve cart contents and entered data, name the cause in plain language, and offer the next action.

## Accessibility Notes

Target WCAG 2.2 AA across the path-to-purchase; these criteria bite hardest here:

- **1.4.1 Use of Color:** sale price, error, "in stock" vs. "out of stock", and selected swatch must carry a non-color cue — text, icon, strikethrough, border weight, checkmark. A red "Out of stock" with no label fails.
- **1.4.3 / 1.4.11 Contrast:** body and price text meet 4.5:1 (3:1 for large headings); swatch borders, stepper controls, focus rings, and the cart badge meet 3:1 non-text contrast. Sale-price red on white frequently fails 4.5:1 — verify.
- **1.4.10 Reflow / 1.4.4 Resize:** the entire flow works at a 320px viewport with no horizontal scroll and at 200% zoom; the checkout side-summary reflows above or into a collapsible without breaking. Test the price block and stepper under 1.4.12 text-spacing overrides.
- **2.5.8 Target Size:** quantity stepper +/- buttons, swatches, remove-item, and filter chips meet the 24px minimum (AAA 2.5.5 prefers 44px — favor it for the stepper and remove controls, which are mis-tap magnets).
- **2.1.1 Keyboard:** filters, variant selectors, gallery, stepper, and the full checkout are operable by keyboard with logical tab order and a visible `:focus-visible` ring. The mini-cart/side-sheet and size-guide dialog use a `<dialog>` or APG modal pattern: focus moves in on open, is trapped, ESC closes, focus restores to the trigger (2.4.11 focus not obscured by sticky headers).
- **Semantics & ARIA:** prefer native `<button>`, `<a>`, `<select>`, `<dialog>`. Variant swatches are a radiogroup (WAI-ARIA APG) when single-select. The cart count is announced via `aria-live`; price-after-promo updates and "added to cart" use `aria-live="polite"`; the inline error summary uses `role="alert"` or focus management. Star ratings expose a text equivalent ("4.3 out of 5, 212 reviews"), not just stars.
- **Forms:** every checkout field has a persistent visible `<label>`, correct `autocomplete` tokens (`given-name`, `address-line1`, `postal-code`, `cc-number`), and `inputmode`/`type` for numeric and email fields — these speed touch entry without affecting operability.
- **Forced colors:** verify swatches, badges, focus, and disabled states under forced-colors / Windows High Contrast so meaning does not vanish when authored colors are replaced.

## Responsive And Browser Notes

Mobile-first up the ladder: 320 (reflow floor) / 360 / 480 / 640 / 768 (tablet) / 1024 / 1280 (desktop) / 1440 / 1920+.

- **PLP grid:** 1–2 columns at 320–480, 2–3 at 640–768, 3–4 at 1024, 4–6 at 1280+. Use CSS Grid with `repeat(auto-fill, minmax(…, 1fr))` for fluid reflow; constrain the content container to ~1200–1440px on wide screens so cards do not stretch. Filters are a sidebar at ≥1024 and an off-canvas/bottom-sheet (ESC + scroll-lock + focus trap) below. Long card titles cap near ~65ch.
- **PDP:** stacked single column below 768 with the buy box following the gallery and a sticky add-to-cart bar appearing once the inline button scrolls off; two-column (gallery + buy box) at ≥1024 with the buy box sticky within its column. Reserve gallery space with `aspect-ratio` or width/height to prevent CLS as images load.
- **Cart / checkout:** order summary is a collapsible above the form on small screens and a sticky side rail at ≥1024. Never let the summary or "Place order" get pushed below an on-screen keyboard without a path back.
- **Container queries:** size the product card by its container, not the viewport, so the same card behaves correctly in a 4-up grid, a 2-up "related" strip, and a mini-cart line.
- **Input model:** `@media (pointer: coarse)` enlarges steppers/swatches and replaces hover quick-view with an explicit tap target; `(pointer: fine)` enables hover zoom and quick-add. Gallery zoom and swatch selection have a non-hover, non-drag fallback. Right-click on a product image should not hijack the browser context menu.
- **Browser/engine:** test WebKit (Safari) where `<dialog>`, `:focus-visible`, container queries, and sticky positioning have historically lagged or differed — confirm the mini-cart dialog and sticky buy box. Verify `inputmode`/`autocomplete` autofill in Safari and Chromium since wallet/address autofill UIs differ. Wallet express buttons render per browser/engine and must degrade to the standard card form when unavailable. Honor `prefers-reduced-motion` for add-to-cart fly animations and carousel transitions. Use `font-display: swap`, preload the above-the-fold font, and set fallback font metrics so the price block does not shift.

## Evidence And Compliance Boundaries

This pack is **synthetic calibration material**, not real-product validation. It encodes recommendations and conventions; it is **not proof** that a given design converts, is accessible, or is lawful in any jurisdiction.

- The patterns here do not constitute **compliance** with WCAG, consumer-protection rules on drip pricing and dark patterns, payment standards (e.g., PCI scope, strong customer authentication), tax/VAT display rules, or privacy/consent law. Real **compliance** requires audited testing, legal review, and assessment against the actual markets you ship to.
- Conversion, revenue, and trust claims in this document are heuristics, not measured outcomes. Treat any urgency/scarcity/social-proof copy as a factual claim that must be independently verified; the design providing such a component is not proof the claim is true.
- Inspiration galleries (Awwwards, Land-book, Mobbin Web) are never evidence for usability, accessibility, performance, or legal **compliance**. Authoritative specs (WCAG, WAI-ARIA APG, web platform/MDN docs) and your own instrumented testing are the sources of record.
- Numbers given (breakpoints, target sizes, contrast ratios, Core Web Vitals budgets) are calibration targets to design against, not certification. Verify against live audits, real-device testing, and field data before claiming any result.

## Design-Quality Traps

- **Buy box loses the contrast contest.** Reviews, promo banners, or a wallet button out-shout "Add to cart". Fix: one fully-weighted primary per surface.
- **CLS from late price/badge/image.** Sale badge, stock line, or gallery image injects after paint and shoves the buy box. Reserve space with `aspect-ratio` and skeletons.
- **Color-only sale/stock signaling.** Red price and red "Out of stock" with no label — fails 1.4.1 and fails low-vision users. Add strikethrough + label, icon + text.
- **Silent variant swap.** Changing color updates the image but not price/availability, or removes an unavailable size with no explanation. Update atomically; disable with a reason.
- **Hidden total until the last step.** Shipping/tax appear only at payment. Surface a shipping signal earlier; show the breakdown in the cart.
- **Disabled CTA with no explanation.** "Add to cart" is greyed out because no size is chosen, but nothing says so. Pair the disabled state with an inline hint, or keep it enabled and validate on click.
- **Stepper mis-tap.** +/- targets under 24px adjacent to "remove" cause accidental deletions. Size to 44px and separate destructive controls.
- **Fake or contrived urgency.** A countdown that resets, "Only 2 left" that never changes — a dark pattern and a trust/legal liability.
- **Filter state lost on back.** Applying facets without writing to the URL breaks back/forward and sharing. Encode filters, sort, and page in the URL.
- **Forced account creation.** Hiding guest checkout to harvest accounts is a top abandonment cause. Offer guest as a peer path.
- **Density flattened to a phone.** Collapsing a desktop PLP or comparison view to a single thin column wastes the screen where scanning many products rewards density. Exploit columns and a sticky filter rail on desktop.

## Handoff Checks

Before "ready for build", confirm each item is specified, not implied:

- [ ] One h1 per page; heading outline has no skipped levels; `header`/`nav`/`main`/`footer` landmarks present.
- [ ] Buy box is the single dominant action on the PDP; cart "Checkout" and checkout "Place order" are the only loud buttons on their surfaces.
- [ ] Price block specced: pay-price size, compare-at with strikethrough + label, unit price, promo treatment — no color-only meaning.
- [ ] Full state set delivered for product card, variant selector, add-to-cart, stepper, promo field, cart, and each checkout step (default/hover/focus-visible/active/loading/empty/error/success/disabled).
- [ ] Recovery states specced: out-of-stock variant, declined payment, invalid/expired promo, address validation, session-expired (cart preserved), network failure (idempotent, no double-charge), plus 404/500/offline.
- [ ] `aria-live` regions named for cart count, "added to cart", promo result, and async price updates; error summary uses focus management or `role="alert"`.
- [ ] Variant swatches as a radiogroup; mini-cart and size-guide as `<dialog>`/APG modal with focus trap, ESC, scroll-lock, and focus restore.
- [ ] Contrast verified: text 4.5:1 (3:1 large), non-text 3:1 for swatch borders, stepper, focus ring, cart badge; checked under forced-colors.
- [ ] Target sizes ≥24px (≥44px for stepper and remove); checkout fields have visible labels, `autocomplete` tokens, and `inputmode`/`type`.
- [ ] Responsive specs at 320/360/480/640/768/1024/1280/1440/1920: grid column counts, filter rail vs. off-canvas, PDP stack-to-two-column + sticky bar, cart summary collapse vs. side rail; container-query behavior for the product card.
- [ ] CWV guarded: LCP image (PDP hero or first card) preloaded, media space reserved (`aspect-ratio` or width/height), INP ≤200ms on stepper/filter/add-to-cart, CLS ≤0.1 with font `swap` + preload + fallback metrics.
- [ ] Filters, sort, and pagination encoded in the URL; back/forward and scroll restoration verified; `beforeunload` guard on a dirty checkout where appropriate.
- [ ] WebKit pass on `<dialog>`, sticky buy box, container queries, and autofill; wallet express degrades to card form; `prefers-reduced-motion` honored.
- [ ] Guest checkout present as a first-class path; marketing opt-in unchecked and separated from transactional consent; only purchase-required data requested per step.
- [ ] Urgency/scarcity/social-proof components render only truthful state and are flagged for content/legal review before launch.
