# Worked example: Design web user flow (Mode B)

## Example prompt

```text
Use the web-design-skill.

Design the web user flow for guest checkout on an ecommerce site, from cart to confirmation.

Inputs:
- User goal: buy without creating an account, with the option to save details at the end
- Breakpoints: mobile-web and desktop
- Browsers: evergreen engines; payment via a hosted card field
- Constraints: reduce abandonment, address + payment autocomplete, accessibility-sensitive
```

## Example output

```md
Mode: Design web user flow
Responsive/breakpoint scope: Mobile-web and desktop, working down to 320px
Browser/engine scope: Evergreen Chromium / WebKit / Gecko; hosted payment iframe
Assumptions:
- Inventory and price are re-validated server-side at the review step.
- Guest checkout is allowed; account creation is offered only after a successful order.
- Tax/shipping are calculated once an address is entered.

## Flow goal
Get a guest from a reviewed cart to an order confirmation with the fewest blocking steps and a clear recovery from every failure.

## Entry points
- "Checkout" from the cart page or the mini-cart drawer
- A restored cart via a returning session or a shared cart URL
- A direct link back to an abandoned checkout step from a reminder email

## Ordered steps / views
1. Cart review (`/cart`) — line items, quantity edit, promo code, subtotal
2. Contact + shipping (`/checkout/address`) — email, shipping address (autocomplete), shipping method
3. Payment (`/checkout/payment`) — hosted card field, billing address (default: same as shipping)
4. Review + place order (`/checkout/review`) — final totals, edit links back to each step
5. Confirmation (`/checkout/confirmation/:orderId`) — order summary + optional "save my details" account offer

## Decision points
- Promo code valid? → apply and recalculate / show inline error, keep the entered code
- Address serviceable and in-stock at review? → continue / surface the blocked line item with options
- Payment authorized? → confirmation / return to payment with a specific decline reason

## Back/forward and URL state
- Each step is its own URL so browser back/forward moves between steps predictably; step state is restored from the server-side cart, not lost.
- Use History `push` between steps and `replace` for in-step validation so back does not trap the user in an error.
- A `beforeunload` guard warns on unsaved payment entry; scroll position restores when returning to the cart.

## Failure and recovery paths
- Network failure on submit → inline retry; entered data preserved; an idempotency key prevents a double-charge.
- Payment declined → return to the payment step with the specific reason; card field cleared, other fields kept.
- Session expired mid-checkout → re-establish the cart from the server and resume at the last valid step, not step 1.
- Item went out of stock at review → flag the line, offer remove-and-continue or save-for-later.

## Responsive and browser behavior
- Mobile-web: one step per view, a collapsible order summary with a "view details" toggle, and a sticky primary button.
- Desktop: two columns with a persistent order summary on the right; steps shown as a progress indicator.
- The hosted payment iframe must be keyboard-focusable and styled to match; verify focus traversal across the iframe boundary in each engine.

## Accessibility and usability risks
- Focus must move to the new step's h1 on each route change, and to the first error on a failed submit.
- The progress indicator needs `aria-current="step"` and a text label, not color alone.
- Inline errors must be tied to fields via `aria-describedby` and announced with `aria-live`; the iframe payment field needs a programmatic label and visible focus.
- Autocomplete tokens (`email`, shipping address, card fields where allowed) reduce typing and error for keyboard and screen-reader users.

## Simplification opportunities
- Default billing address to shipping with a single toggle to cut a whole field set.
- Collapse contact + shipping into one step on desktop where vertical space allows.
- Defer the account offer to confirmation so it never blocks the purchase.

## Next actions
- Confirm the idempotency-key and double-submit strategy with the payments team.
- Prototype the cross-iframe keyboard focus path and verify it in WebKit and Gecko.
- Define the out-of-stock-at-review copy and the save-for-later behavior.
```
