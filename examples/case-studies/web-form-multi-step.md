# Case study: Multi-step web form (progress, validation, save-and-resume)

A bad-to-good calibration case for a multi-step web form: a four-step business
account application with a progress indicator, inline validation, and the
ability to save a partial draft and resume later from a different device. The
target audience fills this on desktop and on phones in roughly equal numbers,
often interrupted, so resumability and a trustworthy error model matter as much
as visual polish.

## Prompt

```text
We're building the onboarding application for our B2B banking product. It's a
4-step form: (1) Business details, (2) Owners & signatories, (3) Documents
upload, (4) Review & submit. People often start on a laptop and finish on
their phone the next day, so we need "save and resume." We also get a lot of
support tickets about validation: people don't know what they did wrong, or
they fix one field and a different error appears.

Design the form. Cover the progress indicator, how validation should behave,
the save-and-resume flow, and how it holds up on a 360px phone and a 1280px
desktop. We care about accessibility (we have to pass an audit) and about not
losing people's work. Give me concrete HTML/CSS/JS behavior, not just a
wireframe description.
```

## Weak response

```md
# Multi-step onboarding form

Use a stepper at the top with 4 circles labelled 1-4 and the step names. The
active step is highlighted in your brand blue. As users move forward, completed
circles turn green with a checkmark.

**Layout**
- Center the form in a card, max-width 600px.
- One step visible at a time. "Back" and "Next" buttons at the bottom.
- On mobile it stacks naturally since it's a single column.

**Validation**
- Validate when the user clicks Next. If a field is wrong, turn its border red
  and show the message underneath.
- Use HTML5 `required` and `type="email"` so the browser helps too.

**Save and resume**
- Add a "Save" button. On click, write the form values to `localStorage` so when
  they come back the data is still there. Show a toast that says "Saved!".

**Styling**
- 14px body text, generous padding, rounded corners, a subtle box-shadow on the
  card. Use red for errors and green for success so it's obvious.
- Animate the step transition with a slide so it feels smooth.

This gives a clean, modern multi-step form that works on mobile and desktop and
saves progress.
```

## Why this is weak

- **Save-and-resume is fiction, not a feature.** `localStorage` is bound to one
  browser on one device; the prompt explicitly says "start on a laptop, finish
  on a phone." This design cannot do the one thing it was asked to do. There is
  no server draft, no resume token, no expiry, no conflict story, and uploaded
  documents (step 3) cannot live in `localStorage` at all. This is the central
  failure: **production readiness** scores 1/5.
- **The progress indicator is decorative, not a state machine.** "Circles 1-4,
  active is blue, done is green with a check" describes a picture. It says
  nothing about the accessible name, current-step semantics
  (`aria-current="step"`), whether steps are clickable to jump back, what
  happens to a step with unresolved errors, or how the indicator reflows at
  360px. **Attention path & hierarchy** and **production readiness** both suffer.
- **Color alone carries meaning.** "Turn the border red," "completed circles
  turn green" — this violates WCAG **1.4.1 Use of Color**. A red border with no
  icon, no text, and no programmatic association is invisible to colorblind
  users and to screen readers. There is no mention of `aria-invalid`,
  `aria-describedby`, or an error summary.
- **The validation model ignores the actual complaint.** The ticket is "I fix
  one field and a new error appears" — a whack-a-mole validation experience.
  Validating everything only on Next, with no on-blur correction and no error
  summary, is exactly what produces that. There's no answer for cross-field
  rules (e.g. ownership percentages must sum to 100), no `aria-live` region, and
  no focus management to the first error. This is a **context & brand fit** miss
  (it doesn't solve the stated problem) and a heuristics miss (Nielsen #9, help
  users recognize, diagnose, and recover from errors).
- **14px body text fails the floor.** Below the 16px (1rem) minimum; combined
  with no `clamp()` and no stated line-height, **typography craft** is at most
  2/5. "max-width 600px" also throws away the 1280px desktop the prompt named —
  **density & rhythm** is unconsidered, not chosen.
- **No keyboard or focus story.** No `:focus-visible`, no statement about where
  focus lands after Next/Back (WCAG **2.4.3 Focus Order**), no skip handling, no
  mention of the slide animation respecting `prefers-reduced-motion`. The slide
  also risks layout shift against the **CLS <= 0.1** budget if step heights
  differ.
- **Missing states.** No loading state on Save/Submit, no error state if the
  draft save fails, no offline/session-expired handling — all named web states
  the prompt's "don't lose people's work" demand requires.

## Strong response

```md
# Business account application — multi-step form

## Architecture: server-backed draft, URL-addressable steps

A draft is a **server resource** created on first input, not browser storage.
That is what makes "laptop today, phone tomorrow" real.

- On first meaningful change, `POST /applications` returns
  `{ applicationId, draftToken }`. Subsequent autosaves are
  `PATCH /applications/:id` (debounced 800ms, also flushed on step change and
  on `visibilitychange === "hidden"`). Document uploads (step 3) go to
  `POST /applications/:id/documents` and are referenced by id, never inlined.
- Resume is a magic link emailed to the applicant:
  `/apply/:id?t=<draftToken>`. The token is single-purpose, expires in 7 days,
  and is exchanged for a session cookie on landing (so it isn't left in
  History/Referer). Drafts older than 30 days are purged; the UI states this.
- Each step is a real URL: `/apply/:id/business`, `/owners`, `/documents`,
  `/review`. We use the **History API** (`pushState`) so Back/Forward,
  refresh, deep-link, and scroll restoration all work. Guard with
  `beforeunload` only when there are unsaved changes (a debounce in flight),
  not unconditionally.
- `localStorage` is used for exactly one thing: a tiny "you have a draft in
  progress" breadcrumb on the marketing site, with the id — never as the source
  of truth and never for PII.

## Progress indicator: an accessible state machine, not a picture

Markup is an ordered list inside `<nav aria-label="Application progress">`.
Each step has one of four states: `complete`, `current`, `upcoming`, `error`.

```html
<nav aria-label="Application progress">
  <ol class="stepper">
    <li class="step step--complete">
      <a href="/apply/42/business">
        <span class="step__icon" aria-hidden="true"><!-- check --></span>
        <span class="step__num">1</span>
        Business details <span class="u-visually-hidden">— completed</span>
      </a>
    </li>
    <li class="step step--current">
      <a href="/apply/42/owners" aria-current="step">
        <span class="step__num">2</span>
        Owners &amp; signatories <span class="u-visually-hidden">— current step</span>
      </a>
    </li>
    <li class="step step--error">
      <a href="/apply/42/documents">
        <span class="step__icon" aria-hidden="true"><!-- alert triangle --></span>
        <span class="step__num">3</span>
        Documents <span class="u-visually-hidden">— 2 problems to fix</span>
      </a>
    </li>
    <li class="step step--upcoming">
      <span aria-disabled="true">
        <span class="step__num">4</span> Review &amp; submit
      </span>
    </li>
  </ol>
</nav>
```

- State is conveyed three ways, never color alone (WCAG **1.4.1**): an icon
  (check / alert triangle), a visually-hidden text suffix, and color. The error
  count is in the accessible name.
- Completed and current steps are real `<a>` links so users can jump back to
  edit; upcoming steps are non-interactive (`aria-disabled`) until reachable.
- Non-text state borders/icons meet **1.4.11** (3:1 against background).
- Reflow (**1.4.10**, 320px floor): below 480px the labels collapse to a
  single line `Step 2 of 4 — Owners & signatories` plus a 4px-tall progress
  bar; the full labelled stepper returns at >=480px. The bar has
  `width`/`height` reserved so it never shifts layout (**CLS**). We use a
  **container query** on the form region, not a viewport query, so the stepper
  adapts to the column it's in (e.g. narrower beside a summary rail on desktop).

## Layout & type

- **Type:** body `font-size: clamp(1rem, 0.95rem + 0.3vw, 1.125rem)`;
  `line-height: 1.5`; one `<h1>` per page (the step name), section `<h2>`s, no
  skipped levels. Reading/label column capped near **65ch**. Resize to 200%
  (**1.4.4**) and the text-spacing override (**1.4.12**) both reflow cleanly
  because nothing is height-locked.
- **Spacing:** 4px base scale — 16px between label and control, 24px between
  fields, 32px between fieldsets, 48px above the action row.
- **Desktop (1280px) earns its density** rather than being a stretched phone:
  a two-column shell — the form in a ~720px reading column on the left, a
  **sticky summary rail** on the right showing the live review of what's been
  entered (and, on step 3, the upload checklist). Below 1024px the rail moves
  below the form. Inputs use a 12-col grid: short fields (postcode, country)
  share a row at >=768px, full-width at 360px.
- **Targets:** all controls >=24px (**2.5.8**); primary actions are 44px tall
  to clear the AAA **2.5.5** bar and to be comfortable under
  `@media (pointer: coarse)`.

## Validation: correct-on-blur, summarize-on-submit

This directly kills the "fix one, a new one appears" loop.

1. **Don't punish typing.** Fields validate on `blur`, never on every
   keystroke, except that once a field is already in an error state we
   re-validate on `input` so the error clears the instant it's correct
   (positive reinforcement, not nagging).
2. **Per-field error model.** A wrong field gets `aria-invalid="true"`, an
   error `<p id="x-err">` linked via `aria-describedby`, and a leading alert
   icon — so the error survives both colorblindness and screen readers
   (**1.4.1**, **3.3.1 Error Identification**, **3.3.3 Error Suggestion** with
   a concrete fix, e.g. "Use the format MM/YYYY"). Borders meet 3:1 (**1.4.11**).
3. **Cross-field / business rules** (ownership % must sum to 100; at least one
   signatory) validate on the relevant `change` and on Next. The sum is shown
   live in an `aria-live="polite"` "Total: 92% — must equal 100%" helper so the
   relationship is visible, not a surprise at submit.
4. **Submit / Next** runs the full step validation. If it fails, focus moves to
   an **error summary** at the top of the step: `role="alert"` heading "There
   are 2 problems" with a list of in-page anchor links to each bad field.
   Activating a link moves focus to the field. This is the error-summary
   pattern and it satisfies **2.4.3 Focus Order** and Nielsen #9 (recognize,
   diagnose, recover). Each remaining step that has unresolved errors flips to
   `step--error` in the stepper.
5. **No keyboard trap, visible focus.** `:focus-visible` ring (3:1, **1.4.11**)
   on every control; focus is never obscured by the sticky rail or sticky action
   footer (**2.4.11 Focus Not Obscured**) — we add `scroll-margin-top` so an
   anchored field clears the sticky header.

## States (all of them)

- **Autosave** indicator near the stepper, polite `aria-live`:
  `Saving…` → `Saved 14:32` → on failure `Couldn't save — retry` (a real
  button, not just a toast). Network loss flips it to an **offline** banner;
  edits queue and flush on reconnect.
- **Next/Submit:** button enters a `loading` state (spinner + `aria-busy`,
  label "Submitting…", disabled to prevent double-submit) with the label width
  reserved so the button doesn't resize (**CLS**).
- **Documents step:** per-file rows with `uploading` (determinate progress),
  `success`, `error` (with reason + retry), plus an **empty** state ("No
  documents yet — drag files here or browse") and a hard list of accepted types
  / max size before the user picks.
- **Session-expired:** if the draft token/cookie lapses mid-session, we capture
  the current field values, show a re-auth dialog (native `<dialog>`, ESC to
  close, scroll-lock, focus trap + restore), re-establish the session, and
  replay the pending PATCH — work is never lost.
- **404/500:** a 500 on PATCH degrades to "Saved locally, will retry" backed by
  an in-memory + sessionStorage buffer so a transient blip doesn't lose input.

## Motion

Step changes are a 180ms cross-fade, not a horizontal slide, to avoid implying
the next step already validated and to keep height stable. All of it sits behind
`@media (prefers-reduced-motion: reduce)`, which drops to an instant swap.
`forced-colors` / high-contrast mode is honored: state is icon+text, borders use
`CanvasText`/system colors, so it survives with the palette stripped out.
```

## Why this is stronger

- **It actually solves save-and-resume** (the prompt's core ask) by making the
  draft a **server resource** with a token-based resume link, debounced
  autosave, document references rather than inlined blobs, and an explicit
  expiry/purge policy. `localStorage` is correctly demoted to a non-PII
  breadcrumb. This moves **production readiness** from 1/5 to 4/5.
- **The progress indicator is a state machine** with four named states, real
  semantics (`aria-current="step"`, error counts in the accessible name,
  links for completed steps), and a defined reflow at 480px/320px with reserved
  height. **Attention path & hierarchy** and **composition & spacing** are now
  deliberate, including a container-query-driven adaptation.
- **It directly attacks the reported pain.** Correct-on-blur + clear-on-input +
  an error summary with anchor links is the documented fix for whack-a-mole
  validation, and live cross-field totals (`aria-live`) defuse the sum-to-100
  surprise. This is Nielsen #9 and WCAG **3.3.1 / 3.3.3** met with concrete
  mechanisms — a real **context & brand fit** win, not generic advice.
- **No color-only signalling anywhere** (**1.4.1**): icon + visually-hidden text
  + color on every state, `aria-invalid` + `aria-describedby` on fields,
  `forced-colors` honored. Non-text contrast (**1.4.11**) and focus visibility
  (**1.4.11 / 2.4.7 / 2.4.11**) are stated, lifting **color/state & contrast**.
- **Type and density are chosen, not defaulted.** 1rem-floored fluid `clamp()`,
  1.5 line-height, ~65ch measure, and a desktop two-column shell with a sticky
  summary rail that exploits 1280px instead of centering a 600px card — so
  **typography craft** and **density & rhythm** both reach 4/5.
- **Every web state is named** (autosave/saving/saved/error, loading,
  offline, session-expired, upload progress/empty/error, 404/500) and motion
  respects `prefers-reduced-motion` while protecting the **CLS <= 0.1** budget,
  lifting **interaction polish & motion** and **production readiness**. Overall
  the strong answer lands at the 4/5 "strong and shippable" target.

## Regression checks

A future answer to this prompt must still pass all of these:

- Save-and-resume MUST be server-backed and cross-device (a token/magic-link
  resume, document references, an expiry/purge policy). An answer that relies on
  `localStorage`/`sessionStorage` as the source of truth for resume is an
  automatic fail — it cannot do laptop-to-phone.
- Validation MUST avoid the whack-a-mole loop: validate on blur (not every
  keystroke), clear an existing error on input the moment it's valid, and on
  submit move focus to an error summary with in-page anchor links to each
  failing field (WCAG 2.4.3, 3.3.1, 3.3.3; Nielsen #9).
- State MUST never be color-only (WCAG 1.4.1): every error/complete/current
  state needs icon + text + programmatic association (`aria-invalid`,
  `aria-current`, `aria-describedby`), and `forced-colors`/high-contrast must be
  honored.
- The progress indicator MUST be a semantic state machine (`aria-current="step"`,
  error count in the accessible name, completed steps navigable) with a defined
  reflow at the 480px and 320px breakpoints and reserved height (no CLS), not a
  decorative row of circles.
- Body type MUST be >= 16px (1rem) with line-height 1.5, and the design MUST use
  the 1280px desktop deliberately (e.g. summary rail / multi-column), not center
  a single narrow card; targets >= 24px (2.5.8).
- Async and risky actions MUST surface explicit states: autosave
  saving/saved/failed-with-retry, loading on Next/Submit (no double-submit),
  offline, and session-expired with focus-managed re-auth and no lost input.

---

Boundary: this is a SYNTHETIC calibration fixture authored to exercise the
skill's quality bars; it is **not** validation against a shipped product, and
the support-ticket numbers and endpoints are illustrative, not measured.
