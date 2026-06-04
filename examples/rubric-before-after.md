# Rubric before/after (web)

A worked upgrade from a 2/5 response to a 4/5 response for the same task, then the resilience step to 5/5. Calibrated against [`../docs/design-quality-rubric.md`](../docs/design-quality-rubric.md).

Task: a responsive UI spec for a newsletter signup section embedded on a marketing page.

## Weak response

> One layout for all widths: a centered box with an email input and a "Subscribe" button side by side. Placeholder says "Enter your email". On success, swap the box for "Thanks!". Style it to match the brand — make it pop.

Why this is 2/5:

- **Responsive flattening:** "one layout for all widths" — the side-by-side input+button overflows below ~360px and there is no 320px reflow.
- **Keyboard / semantics gaps:** placeholder-as-label (fails 1.3.1/3.3.2), no described error path, no focus management on the success swap (focus is lost).
- **Aesthetic-only:** "make it pop" with no mechanism; no tokens, no contrast values, no states beyond default + success.

Score: 2/5.

## Improved response

> Section with a visible `<label for="nl-email">Email address</label>` above a single `type="email" inputmode="email" autocomplete="email"` input and a primary `<button>`. Below 480px the input and button stack full-width; at >=480px they sit on one row; verified no horizontal scroll at 320px. Body 16px/1rem, label 0.875rem; spacing on the 4px scale (16px gap, 24px section padding). States: default, focus-visible (2px ring, 3:1), submitting (button shows a spinner, disabled), success (inline confirmation; focus moves to the confirmation text via `aria-live` so it is announced), and error (inline, tied via `aria-describedby`, `aria-invalid`, focus moved to the field). Brand accent on the button only; text >=4.5:1 on the section background.

Why this is 4/5:

- Real label + autocomplete + correct input type; full state set with focus management on success and error.
- Genuine responsive behavior with a verified 320px reflow; concrete spacing-scale and contrast values.
- Brand expressed through a token (accent on the button) without harming semantics — strong and shippable.

Score: 4/5.

## What would make it 5/5

The resilience step:

- A real `prefers-color-scheme` dark theme and `forced-colors` support (the focus ring and button border survive), re-checking every contrast pair.
- `prefers-reduced-motion` removes the spinner animation in favor of a static "Submitting…" label.
- A measured Core Web Vitals check (the section must not shift layout on submit — reserve the success/error space so CLS stays <= 0.1; keep INP <= 200ms on submit).
- Localization and RTL-safe layout, and an axe-clean + keyboard pass captured as a regression artifact across breakpoints.
