# Golden: Multi-step web form (account application / signup)

A compact calibration example of a strong, shippable web answer for a multi-step
account-application form with client- and server-side validation. The goal is a
form that survives a real browser: keyboard-operable, reflows at 320px, announces
errors, and never loses the user's place across steps or a refresh.

## Prompt

```text
We're building the signup / account-application flow for our B2B billing product.
It's 3 steps: (1) Account — work email, company, country; (2) Business details —
legal name, tax ID, billing address; (3) Review & submit. Desktop is the primary
device but ~30% of applicants finish on a phone. We need inline validation, a
visible progress indicator, and the back button has to work. Give me the
structure, the validation/state model, and the accessibility details a dev can
build from. Tailwind + plain React is fine.
```

## Golden output

```md
# 3-step account application — structure, states, and a11y

## Layout & grid

Single reading column, not a full-bleed form. Center an `<main>` with
`max-width: 40rem` (~640px, comfortably under the ~65ch measure for label+input
pairs) and `padding-inline: clamp(1rem, 4vw, 2rem)`. The form is one column at
every breakpoint — multi-column field grids on signup hurt completion and break
the left-to-right tab order people expect. The two exceptions, gated behind a
container query on the fieldset (not a viewport media query), are paired fields:

- `City / State` and `Postal / Country` sit side-by-side at `@container (min-width: 32rem)`
  using `grid-template-columns: 1fr 1fr; gap: 1rem;` and stack to one column below.

Vertical rhythm uses the 4px scale: `0.5rem` (8px) label→input, `1.5rem` (24px)
field→field, `2rem` (32px) section→actions. Sticky step actions live in a
`<footer>` inside the form: `position: sticky; bottom: 0;` with a top border and
`background` so buttons stay reachable on a phone without a floating overlay.

## Step model & navigation (the "back button has to work" part)

Drive steps from the URL, not just React state, so back/forward and refresh behave:

- `?step=account | business | review` via the History API (`pushState` on
  Next, `popstate` listener syncs the active step). Sharing/reloading a URL lands
  on the right step.
- Persist entered values to `sessionStorage` on each `change` (debounced 300ms) and
  rehydrate on mount, so a refresh mid-application doesn't wipe work. Clear it on
  successful submit.
- A `beforeunload` handler warns only when the form is dirty and unsubmitted.
- Progress indicator is an ordered list, not just dots:
  `<ol>` with `aria-current="step"` on the active item, each step labelled
  "Step 2 of 3: Business details". Completed steps are links back; future steps
  are inert. Status is conveyed by text + a checkmark icon + color — never color
  alone (WCAG 1.4.1).

Moving Next runs that step's validation; invalid → focus moves to the first
errored field (focus management, 2.4.3). Moving Back never validates and never
discards input.

## Markup skeleton (semantic first)

\`\`\`html
<main>
  <h1>Apply for a billing account</h1>
  <ol class="steps" aria-label="Application progress"> … </ol>

  <form novalidate aria-labelledby="step-heading">
    <!-- novalidate: we render our own messages, but keep type=email etc.
         for mobile keyboards and as a server-validation backstop -->
    <fieldset>
      <legend id="step-heading">Step 1 of 3: Account</legend>

      <div class="field">
        <label for="work-email">Work email</label>
        <input id="work-email" name="email" type="email"
               inputmode="email" autocomplete="email"
               aria-describedby="work-email-hint work-email-err"
               aria-invalid="false" required />
        <p id="work-email-hint" class="hint">Use your company domain.</p>
        <p id="work-email-err" class="error" hidden></p>
      </div>
      …
    </fieldset>

    <footer class="actions">
      <button type="button" class="btn-ghost" data-back>Back</button>
      <button type="submit" class="btn-primary">Next</button>
    </footer>
  </form>

  <p class="sr-only" role="status" aria-live="polite" id="form-status"></p>
</main>
\`\`\`

Each input is a real `<label for>` (not placeholder-as-label — placeholders
vanish on input and fail 1.4.3 contrast). `autocomplete` tokens (`email`,
`organization`, `country-name`, `address-line1`, `postal-code`) let password
managers and browser autofill do their job. `inputmode`/`type` pick the right
on-screen keyboard; this is the input-type meaning of "keyboard" and is separate
from tab/focus operability, which dominates.

## Validation & state model

Validate on **blur** for the first pass, then on **change** once a field has
errored (validate-on-blur, re-validate-on-input) — this avoids yelling at users
mid-typing but corrects them live after a mistake.

\`\`\`ts
type FieldState =
  | { status: 'default' }
  | { status: 'validating' }       // async, e.g. email-already-exists
  | { status: 'valid' }
  | { status: 'error'; message: string };
\`\`\`

Per-field rendering:

- **default** — neutral border, hint visible.
- **error** — `aria-invalid="true"`, red 2px border, error `<p>` unhidden and
  linked via `aria-describedby`. Message is specific ("Enter a valid tax ID —
  9 digits, no dashes"), prefixed with an alert icon, and uses a red that holds
  4.5:1 on the form background plus the icon so it's not color-alone (1.4.1).
- **validating** — inline spinner + `aria-busy="true"`; Next is disabled with an
  accessible reason, not a dead gray button.
- **valid** — optional check icon; no color-only signalling.

Form-level: an `aria-live="polite"` status region announces "3 fields need
attention" when a step fails, and submission outcomes ("Application submitted").
On submit failure from the server, map field errors back onto inputs by `name`,
move focus to the summary, and render an **error summary** list at the top of the
step with in-page anchor links to each bad field (a WCAG-friendly pattern that
also helps screen-magnifier users who can't see inline errors).

## States to ship (web is more than happy-path)

default · :hover · :focus-visible · active · loading (skeleton on the review
step while we fetch a tax-ID check) · disabled (with reason) · field error ·
form/server error · success · empty (Step 3 review shows "Nothing entered yet →
go to Step 1" if storage is empty) · offline (queue submit, show a retry banner)
· session-expired (re-auth modal, then resume on the same step from storage).

## Accessibility checklist (named criteria)

- **2.1.1 Keyboard** — every control is a native `<button>`/`<input>`/`<a>`;
  logical tab order; no traps; ESC closes the session-expired `<dialog>` and
  restores focus to the trigger.
- **2.4.7 / 2.4.11** — `:focus-visible` ring (`outline: 2px solid; outline-offset: 2px`)
  with 3:1 contrast (1.4.11); the sticky footer must not obscure a focused field —
  use `scroll-padding-bottom` so focus isn't hidden behind it.
- **2.5.8 Target size** — interactive controls ≥ 24×24px; primary buttons get
  `min-height: 2.75rem` (44px) to clear the AAA bar, with ≥ 8px spacing.
- **1.4.3 / 1.4.11** — text 4.5:1, borders/icons/focus 3:1.
- **1.4.10 Reflow** — usable at 320px with no horizontal scroll; paired-field
  grids collapse to one column.
- **1.4.4 / 1.4.12** — survives 200% zoom and the text-spacing override; nothing
  clips because the layout is flow + `min()`-capped widths, not fixed heights.
- **3.3.1 / 3.3.2 / 3.3.3** — errors identified in text, labels+instructions
  present, suggestions offered.
- `forced-colors: active` — borders and focus use `currentColor` / system colors
  so error and focus survive Windows High Contrast.

## Tokens & type

\`\`\`css
:root {
  --space-1:.25rem; --space-2:.5rem; --space-3:.75rem; --space-4:1rem;
  --space-6:1.5rem; --space-8:2rem;
  --text-body: clamp(1rem, 0.96rem + 0.2vw, 1.0625rem); /* 16→17px */
  --text-h1:   clamp(1.5rem, 1.3rem + 1vw, 2rem);
  --radius: .5rem; --ring: 2px;
}
body  { font-size: var(--text-body); line-height: 1.5; }
h1    { font-size: var(--text-h1);   line-height: 1.25; }
label { font-weight: 600; }
\`\`\`

Body never below 16px; `line-height: 1.5` on prose, ~1.25 on `h1`. Load the UI
font with `font-display: swap`, preload the one above-the-fold weight, and set
fallback `size-adjust` metrics so swapping doesn't shift the form (CLS ≤ 0.1).

## Performance budget

LCP ≤ 2.5s (the `h1` + first fieldset are server-rendered, no blocking JS for
first paint), INP ≤ 200ms (validation is synchronous per field; async checks are
debounced and never block keystrokes), CLS ≤ 0.1 (error `<p>` is rendered with
`hidden` toggled, reserving no jump — or min-height reserved — so unhiding a
message doesn't shove the next field).
```

## Design-quality notes

Quality target: 4/5

Why this lands at **4/5 — strong and shippable** across the relevant dimensions:

- **Attention path & hierarchy (4)** — one `h1`, a single reading column, an
  ordered progress list with `aria-current`, and a sticky action footer give an
  unambiguous "where am I / what's next" read. The error-summary-at-top pattern
  directs attention on failure instead of leaving users hunting.
- **Composition & spacing (4)** — disciplined 4px scale (8/24/32px rhythm), a
  ~640px / 65ch-aware measure, and `clamp()` inline padding. Paired fields use a
  *container* query so the component reflows by its own width, not the viewport.
- **Typography craft (4)** — 16px+ fluid body via `clamp()` with a rem term,
  1.5 body line-height, real `<label>`s over placeholders, and font-loading that
  protects CLS.
- **Color/state & contrast (4)** — every status is text + icon + color (1.4.1),
  4.5:1 text / 3:1 non-text, focus ring contrast called out, and forced-colors
  handled. A full state inventory (loading/empty/error/offline/session-expired)
  is enumerated, not implied.
- **Interaction polish & motion (4)** — validate-on-blur then re-validate-on-input,
  focus moved to the first error, ESC-to-close dialog with focus restore, and
  debounced async checks that never block typing (protects INP).
- **Production readiness (4)** — URL-as-state via History API, `sessionStorage`
  rehydrate, `beforeunload` guard, `autocomplete`/`inputmode` tokens, and a
  concrete CWV budget. A developer can build directly from this.

What would push it to **5/5**:

- Ship the actual `useFormStep` hook and a Zod (or Valibot) schema per step so
  client and server validate from one source of truth, with typed server-error
  mapping back onto fields by `name`.
- Add a tested `prefers-reduced-motion` path for the step transition and spinner,
  plus a real focus-trap implementation (or rely solely on native `<dialog>`'s
  trap) verified with a screen reader (NVDA + VoiceOver) and axe-core in CI.
- Specify analytics/telemetry for per-step drop-off and validation-error rates so
  the form can be tuned with evidence, not guesses — and a documented density
  variant for the desktop-heavy 70% (e.g. inline review edit-in-place) that
  exploits desktop space without flattening the mobile single-column flow.
