# Case study: Account settings with a destructive "Delete workspace" flow

A bad-to-good calibration case for a settings/account surface in a B2B web app. The
hard part is not the form fields — it is making destructive actions safe, reversible
where possible, and accessible, without burying the everyday controls under friction.

## Prompt

```text
We have a SaaS web app. Design the "Account & workspace settings" page for an
admin. It needs:
- Profile (name, email, avatar) with inline save
- Workspace name + slug
- Plan/billing summary with an "Upgrade" link
- Danger zone: "Transfer ownership", "Leave workspace", "Delete workspace"

"Delete workspace" is irreversible and wipes all members' data. Give me the
layout, the states, and exactly how the delete confirmation should work.
Desktop-first, but it must hold up on a narrow viewport. Production-ready HTML/CSS
intent, not a mood board.
```

## Weak response

```md
# Account & Workspace Settings

Use a single centered column. Stack the sections top to bottom with a card
around each one.

**Profile**
- Name, email, and avatar fields.
- Changes save automatically as you type.

**Workspace**
- Workspace name and slug inputs.

**Billing**
- Show the current plan with an "Upgrade" button in your brand color.

**Danger Zone**
- A red box at the bottom with three red buttons: Transfer ownership,
  Leave workspace, Delete workspace.
- When the user clicks "Delete workspace", show a `window.confirm()` popup
  that says "Are you sure?". If they click OK, delete it.

Styling: light gray background (#f7f7f7) on white cards, red (#ff3b3b) buttons
for the danger zone, 14px text, lots of padding so it feels clean and modern.
Make the danger buttons big and red so people notice them.
```

This looks plausible — there is structure, a danger zone, a confirmation — but it
fails the moment you build it.

## Why this is weak

- **Destructive action has almost no friction or undo (Nielsen #3 "User control
  and freedom", #5 "Error prevention").** A single `window.confirm("Are you
  sure?")` for an *irreversible, multi-user data wipe* is the canonical
  under-protected destructive flow. Type-to-confirm and an undo/grace window are
  missing.
- **`window.confirm()` is an accessibility and UX dead end.** It cannot be styled,
  cannot host a typed confirmation, traps focus inconsistently across engines, and
  reads poorly to assistive tech. It also blocks the main thread. A native
  `<dialog>` with proper ARIA is the right primitive.
- **Color is the only signal (WCAG 1.4.1 Use of Color).** "Make them red so people
  notice" encodes danger purely in hue. `#ff3b3b` on white is roughly 3.3:1 — it
  fails 1.4.3 (4.5:1) for the button label and offers no icon or text-weight cue.
- **"Save as you type" on email is dangerous and untestable.** Auto-saving identity
  fields gives no commit point, no validation gate, and no error/success state — it
  collapses *attention path & hierarchy* and *production readiness*. There is no
  account of loading, empty, error, success, disabled, or conflict states.
- **14px body text violates the type floor and the legibility bar.** Below the 16px
  (1rem) minimum; *production readiness* and *typography craft* both drop.
- **Single centered column flattens desktop density.** On a 1280px+ admin surface a
  one-column stack wastes the canvas; there is no two-pane or anchored-nav structure,
  no *composition & spacing* rhythm, no reading-measure control.
- **No keyboard or focus story (WCAG 2.1.1, 2.4.3, 2.4.11).** Nothing about focus
  moving into the dialog, ESC to close, focus restore to the trigger, or the
  destructive button not being obscured by a sticky bar.
- **Three equally-weighted red buttons destroy hierarchy.** "Transfer", "Leave",
  and "Delete" carry very different blast radii but look identical — *attention path*
  fails. Leaving and transferring are not even destructive to *others'* data.

Scored against the 8 dimensions this lands around 2/5: real intent, but unsafe and
unshippable.

## Strong response

```md
# Account & workspace settings — layout, states, and the delete flow

## Page shell and layout
Use a settings shell with a left **anchored sub-nav** (sticky, `position: sticky;
top: 64px`) and a content column capped at a ~65ch reading measure
(`max-inline-size: 65ch`) inside a `max-inline-size: 1200px` container.

- Semantics: `<main>` holds an `<h1>Account &amp; workspace settings</h1>`; each
  section is a `<section aria-labelledby>` with one `<h2>`. The sub-nav is a
  `<nav aria-label="Settings sections">` of in-page `<a href="#section">` links;
  the active link gets `aria-current="true"`.
- Grid: desktop is a 2-column CSS grid `grid-template-columns: 220px minmax(0,
  65ch)` with a `gap: 32px`. Below 768px the nav collapses above the content
  (single column), driven by a **container query** on the shell so it reflows
  by available space, not just viewport.
- Reflow: holds at 320px with no horizontal scroll (WCAG 1.4.10) and survives 200%
  zoom (1.4.4) and the 1.4.12 text-spacing overrides.

## Type and spacing
- Body `font-size: 1rem` (16px floor); fluid headings via
  `clamp(1.5rem, 1.2rem + 1.5vw, 2rem)` with a rem term; body `line-height: 1.5`,
  headings `1.25`.
- Spacing uses the 4px scale: field gap 12px, label-to-input 8px, section padding
  24px, section-to-section 48px.

## Profile section — explicit commit, not auto-save
Name, email, avatar in a real `<form>`. **Save is an explicit `<button
type="submit">`**, disabled until the form is dirty (`:disabled` + `aria-disabled`
mirror). Email changes route through a verification step (send-confirmation), never
a silent write.

States, all designed:
- **default / hover / :focus-visible / active** on inputs and buttons (visible
  focus ring `outline: 2px solid; outline-offset: 2px`, never removed).
- **loading**: submit button shows a spinner, label swaps to "Saving…",
  `aria-busy="true"` on the form; fields stay readable (skeleton only on first
  page load).
- **success**: an `aria-live="polite"` status region announces "Profile saved",
  plus a non-color check icon + text.
- **error**: field-level `aria-describedby` error text, summary at top with
  `role="alert"`, focus moved to the first invalid field (3.3.1).
- **disabled**: greyed with `aria-disabled` and a tooltip explaining why.

## Workspace section
Name + slug. Slug shows a live preview (`acme.app/{slug}`) and validates async with
a debounced check; the "taken/available" result is text + icon (not color alone)
in an `aria-live` region.

## Billing summary
Read-mostly panel: current plan, seats used, renewal date in a small **data block**
(definition list `<dl>`). "Upgrade" is a secondary-weight link-button. No destructive
affordance lives here.

## Danger zone — tiered, not three identical red buttons
A `<section aria-labelledby="danger-heading">` with a 1px `currentColor`-tinted
border and a heading `<h2 id="danger-heading">Danger zone</h2>`. Each row is a
description + an action, and the **visual weight escalates with blast radius**:

| Action | Reversible? | Affordance |
| --- | --- | --- |
| Transfer ownership | Yes (re-transfer) | Neutral/secondary button |
| Leave workspace | Yes (re-invite) | Neutral/secondary button |
| Delete workspace | **No — wipes all members' data** | Outlined danger button, leading warning icon, the only one styled destructive |

Danger styling never relies on hue alone: a leading warning icon, a "This cannot
be undone" helper line, and bold weight carry the meaning too (1.4.1). The danger
text/border meets 4.5:1 against the surface; the icon and border meet 3:1 (1.4.11).

## The delete confirmation — native `<dialog>`, type-to-confirm, grace window
Trigger opens a modal `<dialog>` via `.showModal()` (top layer, backdrop, inert
background for free). Pattern follows the WAI-ARIA APG **Dialog (Modal)** pattern.

```html
<dialog id="delete-ws" aria-labelledby="del-title" aria-describedby="del-desc">
  <h2 id="del-title">Delete "Acme" workspace?</h2>
  <p id="del-desc">
    This permanently deletes the workspace and <strong>all data for its
    12 members</strong>. This cannot be undone.
  </p>
  <label for="confirm-name">Type <strong>Acme</strong> to confirm</label>
  <input id="confirm-name" autocomplete="off" inputmode="text"
         aria-describedby="confirm-help" />
  <p id="confirm-help">Workspace name is case-sensitive.</p>
  <div class="dialog-actions">
    <button value="cancel" formmethod="dialog">Cancel</button>
    <button id="confirm-delete" disabled>Delete workspace</button>
  </div>
</dialog>
```

Behavior:
- **Focus management (2.4.3, 2.4.11):** on open, focus the first interactive
  element (or the heading); focus is trapped inside; ESC closes; on close, focus
  **restores to the trigger button**. The confirm button is not obscured by any
  sticky footer.
- **Type-to-confirm:** "Delete workspace" stays `disabled` until the typed value
  exactly equals the workspace name (Nielsen #5 error prevention). This defeats
  muscle-memory and double-click deletes.
- **Two-stage safety:** confirming does *not* hard-delete immediately. The
  workspace enters a **7-day soft-deleted / suspended** state with a global
  `role="status"` banner ("Workspace scheduled for deletion — Undo"). An emailed
  receipt + in-app **Undo** gives real "user control and freedom".
- **Async + result:** the confirm button shows loading (`aria-busy`), result is
  announced via `aria-live`; on failure, an inline `role="alert"` keeps the dialog
  open with the typed value preserved.
- **Pointer parity:** works identically for mouse, touch (`pointer: coarse`
  targets >= 24px, 2.5.8), and keyboard. No right-click-only or hover-only path.

## Cross-cutting
- `:focus-visible` rings everywhere; skip-link to `<main>`; logical tab order.
- `forced-colors` / high-contrast: danger conveyed by icon + `forced-color-adjust`
  fallbacks, not just a red fill.
- CLS budget <= 0.1: avatar and plan card reserve space with `aspect-ratio`;
  dialog open does not shift the page (top layer). INP <= 200ms on the
  type-to-confirm keystroke handler (cheap string compare, no network).
```

This is the **4/5** target: shippable, safe, and accessible, with the destructive
path carrying the most design weight.

## Why this is stronger

- **Destructive safety is layered (Nielsen #5 error prevention, #3 user control).**
  Type-to-confirm *plus* a 7-day soft-delete grace window *plus* in-app Undo turns
  an irreversible click into a recoverable, deliberate act — directly fixing the
  weak answer's `confirm("Are you sure?")`.
- **Native `<dialog>` + APG Dialog pattern** gives top-layer rendering, inert
  background, ESC-to-close, focus trap, and focus restore — covering WCAG 2.1.1,
  2.4.3, and 2.4.11 that the weak answer ignored.
- **Color is never the sole carrier (1.4.1).** Danger reads through icon, helper
  copy, weight, and border in addition to hue, and the contrasts are pinned to
  4.5:1 text / 3:1 non-text (1.4.3, 1.4.11) instead of an unmeasured `#ff3b3b`.
- **Hierarchy matches blast radius.** Only "Delete" is styled destructive; transfer
  and leave are neutral because they are reversible — restoring *attention path &
  hierarchy*.
- **Explicit commit + full state set** (default, hover, focus-visible, active,
  loading, empty, error, success, disabled) replaces fragile auto-save and lifts
  *production readiness*; the live regions cover async announcement.
- **Desktop density is exploited, not flattened** — anchored sub-nav + 65ch measure
  + container-query reflow give *composition & spacing* and *density & rhythm* that a
  single centered column lacks, while still holding 320px reflow and 200% zoom.
- **Type floor and rhythm fixed**: 16px body, clamp() headings with a rem term, 4px
  spacing scale — *typography craft* and *composition* both rise.

## Regression checks

- The destructive confirm MUST use a native `<dialog>` (or an APG-compliant custom
  modal) with focus trap, ESC-to-close, and focus restore to the trigger — never
  `window.confirm()` and never hover-only or right-click-only invocation.
- Irreversible delete MUST require **type-to-confirm matching the workspace name**
  AND offer a recovery path (soft-delete grace window or Undo); a single "Are you
  sure?" step does not pass.
- Danger MUST be conveyed by more than color (icon + text + weight), with button
  label contrast >= 4.5:1 (1.4.3) and non-text/border >= 3:1 (1.4.11); no reliance
  on hue alone (1.4.1).
- Body text MUST be >= 16px (1rem); the layout MUST reflow with no horizontal scroll
  at 320px (1.4.10) and survive 200% zoom (1.4.4).
- Identity fields (email) MUST have an explicit commit + validation + error/success
  states; silent auto-save of email does not pass.
- The three danger actions MUST be visually tiered by blast radius — only the
  irreversible action carries destructive styling.

Boundary: this is a SYNTHETIC calibration fixture written to exercise the rubric; it
is **not** validation against a shipped, real product, and the "4/5" score is an
authoring target, not a measured usability result.
