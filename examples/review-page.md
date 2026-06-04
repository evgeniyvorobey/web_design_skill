# Worked example: Review page (Mode D)

## Example prompt

```text
Use the web-design-skill.

Review this account settings page (text description only, no screenshot):
- one long single-column form: profile, email, password, notifications, danger zone
- all fields rendered at once
- a single "Save" button fixed at the very bottom of the page
- "Delete account" is a red link inside the form, right above Save
- inline errors appear only after pressing Save
- no visible focus styling mentioned
Constraints: accessibility-sensitive, keyboard users common.
```

## Example output

```md
Mode: Review page for usability/accessibility
Responsive/breakpoint scope: Assumed desktop + mobile-web (not specified)
Browser/engine scope: Assumed evergreen engines (not specified)
Sub-case: D2 — text description only
Assumptions:
- The page is authenticated and saves to a single endpoint.
- "Danger zone" actions are irreversible.
- No visual treatment (spacing, contrast, focus styling) was provided, so visual claims stay provisional.

## Quick summary
The structure is recoverable but risky: one giant form with a single bottom Save mixes low-stakes edits with an irreversible delete, defers all validation to submit, and (as described) gives no focus styling. The biggest risks are accidental destructive action and keyboard inoperability. This is a structure-and-behavior review only; visual properties are unverifiable from text.

## Strengths
- A single consolidated settings page is a reasonable mental model for infrequent edits.
- Grouping into profile / email / password / notifications / danger zone is a sound information structure.

## Findings
> Each finding is one causal chain, ordered by severity.

### F1 — Destructive action adjacent to Save
- Lens: Usability
- Observation: "Delete account" sits as a red link directly above the page's only Save button.
- Violated principle: Nielsen #5 Error prevention; Fitts's Law (two opposite-consequence targets crowded together).
- User consequence: a mis-click or mistargeted keyboard activation can trigger an irreversible account deletion while the user intended to save.
- Change: move the danger zone to its own section with separation, require a typed-confirmation dialog (focus-trapped, ESC-cancel), and never place it adjacent to Save.
- Predicted effect: should sharply reduce accidental deletions; confidence H.
- Severity: 4 — low frequency but catastrophic impact and irreversible.
- Moves: lifts cap (keyboard/destructive risk) and Context & brand fit 2→4.

### F2 — No visible focus styling described
- Lens: Keyboard operability
- Observation: the description mentions no focus indicator on fields or actions.
- Violated principle: WCAG 2.4.7 Focus Visible / 2.4.11 Focus Not Obscured; keyboard operability.
- User consequence: keyboard and switch users cannot tell where they are in a long form, making it effectively unusable without a mouse.
- Change: add a `:focus-visible` outline ≥ 2px at ≥ 3:1 contrast on every control; ensure the bottom-fixed Save bar does not obscure the focused field.
- Predicted effect: should restore keyboard operability for the whole form; confidence H (behavioral, not visual).
- Severity: 3 — frequent for keyboard users, high impact, persistent.
- Moves: lifts the keyboard-inoperability cap; Production readiness 2→4.

### F3 — Validation deferred to submit
- Lens: Usability
- Observation: inline errors appear only after pressing Save at the bottom of a long form.
- Violated principle: Nielsen #1 Visibility of system status; Wroblewski inline-validation.
- User consequence: users discover errors far from the field, must scroll back, and may lose confidence on a long page.
- Change: validate on blur per field, summarize errors on submit, move focus to the first error with `aria-describedby` ties.
- Predicted effect: should reduce failed-save loops and scroll-hunting; confidence M (D2 text-only).
- Severity: 2 — frequent, moderate impact.
- Moves: Interaction polish 2→4.

## Design quality score (current → projected)
- Current: 2/5 — provisional (D2). Structure is sound but a catastrophic destructive-adjacency and probable keyboard inoperability dominate.
- Projected: 3/5 — the median of the assessable projected dimensions once F1–F3 land; conditional: requires F1 AND F2 AND F3 and the no-focus-styling assumption being real. Visual dimensions stay unassessable (n/v) and are not projected upward.
- Ceiling note: with a visual pass confirming contrast, spacing, and focus appearance, the ceiling is 4/5 (capped at 4/5 unless resilience across states/forced-colors is named).
- Primary lever(s): F1 (removes the catastrophe cap) and F2 (removes the keyboard cap).

| Dimension | Now | Projected | Gated by (cap / ladder rung) | Confidence |
|-----------|-----|-----------|------------------------------|------------|
| Attention path & hierarchy | 3 | 4 | danger-zone separation | provisional |
| Composition & spacing | n/v | n/v | no visual provided | not-from-text |
| Typography craft | n/v | n/v | no visual provided | not-from-text |
| Color, state & contrast | n/v | n/v | no visual provided | not-from-text |
| Density & rhythm | 3 | 3 | — | provisional |
| Interaction polish & motion | 2 | 4 | F3 inline validation | provisional |
| Context & brand fit | 2 | 4 | F1 destructive handling | provisional |
| Production readiness | 2 | 4 | F2 focus + semantics | provisional |
- Projected overall = the median of the assessable (non-`n/v`) projected dimensions, lowered if a critical task dimension stays weak. It is not the sum of per-dimension gains.

## Severity index
- 4 (catastrophe): F1
- 3 (major): F2
- 2 (minor): F3

## Platform-convention mismatches
- The single bottom-fixed Save for a very long form fights the web convention of section-level save or autosave; consider per-section save or an explicit "unsaved changes" guard on navigation (`beforeunload`).
- A destructive "Delete account" as a plain red link breaks the link-vs-button convention; it should be a button that opens a confirmation dialog.

## Unresolved assumptions
- Whether any focus styling actually exists (the review treats its absence as the described state).
- Contrast, spacing, and visual weight — all unverifiable without a screenshot or rendered URL.
- Whether notifications settings autosave or wait for the single Save.

## Next actions
- Restructure the danger zone with a typed-confirmation dialog and verify the focus trap with a keyboard pass.
- Add `:focus-visible` styling and run an axe + screen-reader check on the full tab order.
- Share a screenshot or rendered URL so the visual dimensions (contrast, spacing, focus appearance) can be scored.
```
