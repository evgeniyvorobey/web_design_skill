# Case study: Ecommerce checkout funnel (cart to review)

A bad-to-good calibration fixture for a multi-step checkout: cart -> address -> payment -> review. The weak answer "looks like a checkout" but leaks conversion through CLS, focus loss between steps, color-only error signalling, and a desktop layout that flattens to a single narrow column for no reason. The strong answer is a buildable spec a front-end engineer can implement without guessing.

This is a SYNTHETIC fixture written to calibrate review judgement; it is not validation against a shipped checkout, and the conversion claims below are illustrative, not measured.

## Prompt

```text
We're a mid-size online retailer. Design the checkout flow for desktop and
mobile web: cart review, then shipping address, then payment, then a final
order review before "Place order". Guest checkout must work. Keep the cart
summary visible. We care about conversion and we have to pass an accessibility
audit before launch. Give me layout, states, and the accessibility rules the
front-end team should follow.
```

## Weak response

```md
## Checkout design

Use a clean 4-step checkout. Show a progress bar at the top with the four
steps (Cart, Address, Payment, Review) and highlight the current step in
your brand color.

**Cart**
List the items with image, name, price, and a quantity dropdown. Show the
subtotal at the bottom and a big "Continue" button.

**Address**
A form with fields for name, address, city, ZIP, country. Mark required
fields with a red asterisk. If a field is wrong, turn it red.

**Payment**
Card number, expiry, CVC fields. Add a "Same as shipping" checkbox.

**Review**
Show everything the user entered and a "Place order" button. After they
click it, show a spinner while it processes.

Make it responsive so it stacks into one column on mobile. Use a modal
popup to confirm the order was placed. Keep the order total in a sidebar
on the right so it's always visible.

Tips:
- Use large tap targets so it's easy on phones.
- Use placeholder text inside inputs to save space and label the fields.
- Autofocus the first field on each step so people can start typing.
```

## Why this is weak

- Attention path & hierarchy: a "progress bar highlighted in brand color" is the only step indicator, which fails WCAG 1.4.1 Use of color. There is no current/complete/upcoming distinction conveyed by text, shape, or `aria-current`, so a screen-reader user and a colorblind user cannot tell where they are.
- Production readiness: states are barely specified. "Turn it red" is the entire error story, the spinner has no accessible name or `aria-live` region, and there is no empty cart, expired session, declined payment, network error, or disabled-button-while-submitting state. Per Nielsen heuristic "Visibility of system status," an unannounced spinner leaves assistive tech silent.
- Typography craft: placeholder-as-label is a known anti-pattern. It fails WCAG 1.3.1 (no programmatic label association), disappears on input, and placeholder gray rarely clears 4.5:1 contrast (1.4.3). It also breaks browser autofill labelling.
- Color/state & contrast: "red asterisk" plus "turn it red" conveys both required-ness and error purely by color, violating 1.4.1 again, and gives no text explaining what is wrong, so 3.3.1 Error Identification and 3.3.3 Error Suggestion are unmet.
- Density & rhythm: "stacks into one column on mobile" is fine, but the answer applies one single column everywhere and never exploits desktop width. On a 1280px viewport the cart summary and the form should sit side by side; collapsing to one narrow column wastes the medium and pushes the order total below the fold.
- Interaction polish & motion: "autofocus the first field on each step" steals focus, can summon the on-screen field too early, and combined with a route change leaves no managed focus target, violating 2.4.3 Focus Order and disorienting keyboard users. A modal "popup" with no focus trap, ESC handling, or focus restore fails 2.1.2 No Keyboard Trap and the WAI-ARIA APG dialog guidance.
- Composition & spacing: no spacing scale, no measure, and no reserved space for thumbnails means images shift the layout as they load (CLS risk against the 0.1 budget).
- Context & brand fit: it relies on "brand color" as the load-bearing signal everywhere, coupling accessibility to a single hue and giving the team nothing to build a token system around.

## Strong response

```md
## Checkout funnel: layout, states, accessibility

### Flow model and URL
Four steps as real routes so back/forward, refresh, and shareable state work:
/checkout/cart -> /checkout/address -> /checkout/payment -> /checkout/review.
Each step is its own document with one <h1> ("Your cart", "Shipping address",
"Payment", "Review your order"). Persist progress server-side keyed to the
cart so a refresh or session resume lands on the correct step. Use the History
API; warn with beforeunload only when there is unsaved address/payment input.

### Stepper (not a color-only progress bar)
Render an ordered list as the step indicator inside a <nav aria-label="Checkout
steps">. Each step shows a number, a label, and a status conveyed THREE ways:
- text: a visually-hidden "Completed" / "Current step" / "Not yet available";
- shape/icon: check glyph for done, filled ring for current, hollow for upcoming;
- aria-current="step" on the active item.
Completed steps are links (editable); upcoming steps are inert text, not links.
Never rely on hue alone (1.4.1). Connector line and labels meet 1.4.11 (3:1).

### Two-column desktop, deliberate reflow to one column
Desktop (>= 1024px): 12-col grid. Form occupies the left ~8 cols with a reading
measure of ~60ch; the order summary is an <aside aria-label="Order summary"> in
the right ~4 cols, sticky (position: sticky; top: 24px) so the total stays in
view. Below 1024px the summary moves ABOVE the form as a collapsible
<details>/<summary> reading "Total $128.40 - view items," so the price is never
hidden. Everything reflows to a single column at 320px with no horizontal scroll
(1.4.10) and survives 200% zoom (1.4.4) and the 1.4.12 text-spacing overrides.

### Spacing, type, motion budget
4px spacing scale (4/8/12/16/24/32/48/64 px). Body 1rem (16px) minimum, fluid
headings via clamp(1.5rem, 1.2rem + 1.5vw, 2rem), body line-height 1.5. Reserve
every product thumbnail with aspect-ratio: 1 / 1 and explicit width/height so
loading images do not move the layout (CLS <= 0.1). Preload the above-the-fold
heading font with font-display: swap and a metrics-matched fallback. Honor
prefers-reduced-motion: reduce for step transitions. Target INP <= 200ms by
keeping validation work off the main-thread critical path.

### Forms (address + payment)
- Every input has a persistent visible <label> tied with for/id. No
  placeholder-as-label; placeholders, if used, show example FORMAT only.
- Required state is text + visual: append a visible "(required)" and set the
  required attribute; do not signal required by color alone.
- Correct autocomplete tokens: name, address-line1, address-line2, postal-code,
  country, cc-number, cc-exp, cc-csc; plus inputmode="numeric" on card/ZIP so
  the on-screen field type matches and browser/keychain autofill works.
- "Same as shipping" is a real <input type="checkbox"> that copies values and
  moves focus to the next actionable field; toggling it announces the change.
- Validate on submit and on blur-after-touch. Each error: red border AND a
  warning icon AND a text message under the field; the input gets
  aria-invalid="true" and aria-describedby pointing at the message
  (3.3.1 Error Identification, 3.3.3 Error Suggestion). On failed submit, move
  focus to a summary <div role="alert"> listing each error as an in-page link
  to its field (2.4.3).
- Targets >= 24x24px (2.5.8); primary actions comfortably larger. :focus-visible
  ring 2px with offset, contrast >= 3:1, never obscured by the sticky summary or
  a sticky footer (2.4.11). Support forced-colors / Windows High Contrast.

### Per-step states (all of them)
default / hover / :focus-visible / active / loading (skeleton) / empty / error /
success / disabled, plus 404 / session-expired / payment-declined / offline.
- Empty cart: heading "Your cart is empty," a "Continue shopping" link, no
  dead-end. The "Continue" button is absent, not merely disabled.
- Submitting: the step's primary button enters a busy state with
  aria-busy="true", keeps its label, shows an inline spinner, and is disabled
  against double-submit. A polite aria-live region announces "Placing order."
- Payment declined: inline error at the payment summary with a clear next
  action ("Try another card"), focus moved to it; cart and entered data are
  preserved (Nielsen "Error prevention" + "Help users recover from errors").
- Session expired: an inline banner or side-sheet offering "Resume checkout";
  do not silently drop the cart.

### Place order (no blocking modal of mystery)
"Place order" lives in the Review step. On success, navigate to
/checkout/confirmation (a real, shareable route, <h1> "Order confirmed"),
NOT a modal. If a confirmation dialog is genuinely needed before charging, use
native <dialog> with focus trap, ESC to close, scroll-lock, focus restore to the
trigger, and labelled by its heading (APG Dialog pattern, 2.1.2).

### Keyboard & SR summary
Logical tab order matches visual order. On each route change, move focus to the
new step's <h1> (tabindex="-1") so SR users hear the step; do not autofocus the
first input. Skip link to <main>. Order-summary updates announce via a polite
live region. Landmarks: header / nav / main / footer, one h1 per step, no
skipped heading levels.
```

This is the 4/5 target: strong and shippable, with named states, tokens, and WCAG criteria, while leaving room for a 5/5 pass (e.g. saved-card management, address autocomplete with a full keyboard listbox, animated tax/shipping recalculation).

## Why this is stronger

- Attention path & hierarchy: the stepper conveys status by text, shape, and `aria-current` (1.4.1), and completed steps become editable links, matching the real mental model of "go back and fix my address."
- Production readiness: every web state is enumerated including session-expired, payment-declined, and offline, and submission is double-submit-guarded with `aria-busy` and a polite live region, satisfying "Visibility of system status" and giving engineers an unambiguous build list.
- Typography craft & color/state: persistent labels (1.3.1), required-ness signalled by text not hue (1.4.1), errors carry border + icon + message wired with `aria-invalid`/`aria-describedby` (3.3.1, 3.3.3), and contrast targets are explicit (1.4.3 text 4.5:1, 1.4.11 non-text 3:1).
- Density & rhythm: it exploits desktop width with a two-column grid and a sticky order summary, then reflows deliberately, keeping the total visible on small viewports instead of flattening every breakpoint to one column. Reflow holds at 320px (1.4.10), 200% zoom (1.4.4), and text-spacing overrides (1.4.12).
- Interaction polish & motion: focus is managed to the new step heading on route change (2.4.3) rather than autofocusing inputs; the optional confirmation uses native `<dialog>` with trap/ESC/restore (2.1.2, APG); CLS is controlled with reserved media space and `prefers-reduced-motion` is honored.
- Context & brand fit & composition: a 4px spacing scale, fluid type with a rem term, and a ~60ch measure make this a tokenable system rather than one hue doing all the work; the confirmation is a shareable route, not a dead-end modal.

## Regression checks

- Step status must be conveyed by text and shape and `aria-current`, never by color alone (WCAG 1.4.1); colorblind and screen-reader users can identify current/complete/upcoming steps.
- Form errors must include a text message plus a non-color cue, wire `aria-invalid` + `aria-describedby`, and move focus to a `role="alert"` error summary on failed submit (WCAG 3.3.1 / 3.3.3 / 2.4.3); no placeholder-as-label.
- All product thumbnails and media reserve space via `aspect-ratio` or explicit width/height so cart loading keeps CLS <= 0.1; fonts use `font-display: swap` with a metrics-matched fallback.
- On every route change focus moves to the step `<h1>` (no input autofocus), tab order is logical, and the focus ring stays visible and not obscured by the sticky summary or footer (2.4.3, 2.4.11).
- Desktop (>= 1024px) uses a two-column layout with a sticky order summary and does not flatten to a single narrow column; layout still reflows cleanly at 320px (1.4.10) and 200% zoom (1.4.4).
- Order confirmation is a real shareable route, not a blocking modal; any genuine confirmation dialog is native `<dialog>` with focus trap, ESC, scroll-lock, and focus restore (2.1.2, APG Dialog).
- Submit buttons guard against double-submit with `aria-busy` and a polite live-region announcement; empty-cart and session-expired states each have a recovery path, never a dead end.
