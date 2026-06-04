# Golden: Account settings page

A compact calibration example of a strong, shippable (4/5) web answer for an
account settings surface that bundles profile editing, security, notification
preferences, and destructive actions on one page.

## Prompt

```text
Design the account settings page for our SaaS web app. It needs profile
fields (name, email, avatar), a security section (password change + 2FA),
notification toggles, and a danger zone with "Delete account". Desktop-first
but it has to work on phones too. Give me the layout, the key states, and the
accessibility details — our last settings page failed an audit on keyboard
and contrast.
```

## Golden output

```md
# Account settings

A single `<main>` with a left in-page nav (sticky on desktop) and a content
column capped at a ~720px reading width so forms don't stretch into unusable
line lengths on wide screens. One `<h1>` ("Account settings"); each section is
a `<section>` with its own `<h2>`, giving a clean heading outline (no skipped
levels — WCAG 2.4.6 / 1.3.1).

## Layout & responsive behavior

- Container: `max-inline-size: min(100% - 2rem, 1200px)`, centered.
- Desktop (>= 1024px): two columns via CSS grid —
  `grid-template-columns: 220px minmax(0, 1fr); gap: 48px`. Left column is the
  in-page nav (`<nav aria-label="Settings sections">` with anchor links +
  `aria-current="true"` on the active one, kept in sync via IntersectionObserver
  and reflected in the URL hash so a section is shareable/bookmarkable).
- 768–1023px: nav collapses to a horizontal, scrollable tab strip above content.
- < 640px (down to the 320px reflow floor, WCAG 1.4.10): single column, nav
  becomes a `<details>` "Jump to section" disclosure; no horizontal scroll.
- Section rhythm: 32px between field rows, 48px between sections, 64px above the
  danger zone to physically separate it. Card padding 24px.

## Profile section

- `<form>` with a visible `<label>` per field (never placeholder-as-label).
- Fields use `type` + `inputmode` + `autocomplete`: name →
  `autocomplete="name"`; email → `type="email" inputmode="email"
  autocomplete="email"`.
- Avatar: native `<input type="file" accept="image/*">` styled as a labeled
  button; preview reserves space with `aspect-ratio: 1` so swapping the image
  causes no layout shift (CLS budget <= 0.1). Drag-and-drop is an enhancement
  with the file input as the keyboard/click fallback.
- Email change is sensitive: editing it reveals an inline note ("We'll send a
  confirmation link to the new address") and requires the current password —
  surfaced inline, not in a surprise modal.
- Per-section "Save changes" (primary `<button type="submit">`) + "Cancel"
  (secondary). Buttons disable + show an inline spinner with
  `aria-busy="true"` while saving; a result is announced via an
  `aria-live="polite"` region ("Profile updated").

## Security section

- "Change password": current / new / confirm, each with a show/hide toggle
  (`<button type="button" aria-pressed>` — icon + text, never color alone,
  WCAG 1.4.1). New-password field has an `aria-describedby` rule list whose
  items flip to met/unmet with a text label + icon, not just green/red.
- Two-factor: a labeled switch (WAI-ARIA APG `switch` pattern, or native
  checkbox styled as a toggle) with current status as text ("2FA is on").
  Enabling opens a `<dialog>` showing the QR + manual key and a code input;
  ESC closes, focus is trapped while open and restored to the trigger on close.
- "Active sessions": a real data table — `<table>` with sortable columns
  (Device, Location, Last active), a sticky `<thead>`, and a per-row
  "Sign out" plus a header "Sign out all". On < 640px each row collapses to a
  stacked card. Exploit desktop density here; don't flatten it to a phone list.

## Notifications section

- Grouped switches (Product, Security, Billing) as a `<fieldset>` with a
  `<legend>`. Each switch shows on/off as text, not just position. Changes
  autosave with a debounced PATCH; the polite live region confirms ("Saved")
  and reverts with an inline error on failure.

## Danger zone

- Visually separated card: 1px error-token border, a tinted background, and a
  warning `<h2>` "Danger zone" — relying on the heading + icon + copy, not red
  alone (WCAG 1.4.1).
- "Delete account" is a destructive secondary button (not the page's loudest
  control) that opens a confirmation `<dialog role="alertdialog">`. Confirm is
  gated: the user must type their workspace name to enable the destructive
  button (prevents accidental, irreversible loss). Cancel is the default-focused
  action; ESC cancels.

## Tokens & states

- Type: body 1rem/1.5; field labels 0.875rem; `<h1>`
  `clamp(1.5rem, 1.25rem + 1.2vw, 2rem)`; line-height 1.25 on headings.
- Spacing scale (4px base): 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64.
- Targets: every control >= 24×24px (WCAG 2.5.8); touch-primary actions 44px.
- Focus: `:focus-visible` ring 2px solid + 2px offset, contrast >= 3:1 against
  both the field and the page (WCAG 1.4.11), never clipped by sticky headers
  (2.4.11 focus not obscured).
- Color/state: text >= 4.5:1, UI borders/icons >= 3:1; error states pair the
  error color with an icon and `aria-describedby` text + `aria-invalid`.
- States covered per form: default, hover, focus-visible, active, disabled,
  loading (button spinner / skeleton on initial load), success (live region),
  error (inline, field-level and form-level), plus session-expired (a banner
  with "Sign in again" if a save 401s).
- `forced-colors: active`: switches and the focus ring use system colors and
  keep a visible border so they survive Windows High Contrast.

## Why it holds up

- Keyboard: logical tab order, skip link to `<main>`, no traps, dialogs trap +
  restore focus, ESC closes overlays (WCAG 2.1.1 / 2.1.2).
- Reflow & zoom: usable at 320px and at 200% zoom with no loss of content
  (WCAG 1.4.10 / 1.4.4); text-spacing override survives (1.4.12).
- Performance: above-the-fold font preloaded with `font-display: swap` and a
  metric-matched fallback; media space reserved; targets LCP <= 2.5s,
  INP <= 200ms, CLS <= 0.1.
```

## Design-quality notes

Quality target: 4/5

This response is strong and shippable across the dimensions that matter for a
settings surface, without over-reaching into a portfolio piece.

- Attention path & hierarchy (4/5): one `<h1>`, a clean `<h2>` outline, and a
  sticky in-page nav with `aria-current` give an obvious scan path. The danger
  zone is deliberately demoted (destructive secondary button, not the loudest
  control) — correct hierarchy for an irreversible action.
- Composition & spacing (4/5): the ~720px form column prevents unusable line
  lengths on wide screens, and the 32/48/64 rhythm encodes meaning (intra-row,
  inter-section, danger-zone separation) rather than being decorative.
- Typography craft (4/5): 1rem body at 1.5, fluid `clamp()` heading with a rem
  term, restrained label size. Measure is controlled by the column cap.
- Color/state & contrast (4/5): named thresholds (4.5:1 text, 3:1 non-text),
  and every status uses icon + text, never color alone (WCAG 1.4.1) — exactly
  what the prior audit failed.
- Density & rhythm (4/5): the active-sessions data table exploits desktop
  density (sortable, sticky header, bulk "Sign out all") and collapses to cards
  only at the narrow breakpoint, instead of flattening everything to a list.
- Interaction polish & motion (4/5): autosave with debounce + polite live
  region, type-to-confirm delete gating, dialog focus trap/restore, ESC to
  close, session-expired recovery. States are enumerated, not implied.
- Production readiness (4/5): real tokens, the full breakpoint behavior down to
  320px, forced-colors handling, and Core Web Vitals budgets make this buildable
  as written.

What would push it to 5/5: a documented optimistic-update + rollback contract
for the autosaving toggles (request id, conflict/last-write-wins behavior, and
the exact revert + error-announcement timing); a concrete focus-management
script for the QR `<dialog>` including the post-enable success path and where
focus lands; and a motion spec honoring `prefers-reduced-motion` for the
spinner and the section-scroll behavior, with durations/easing tokenized.
