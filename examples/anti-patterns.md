# Anti-patterns (web)

Calibration pairs for the most common web design traps. Each shows a plausible **Bad** answer, why it fails, and a **Good** rewrite with a concrete mechanism. These map to the failure modes in [`../docs/weaknesses.md`](../docs/weaknesses.md).

## Bad / Good pairs

### 1. Modal without focus management

Bad:
- "Open a custom `<div>` modal for the confirmation; style an overlay behind it and a close X in the corner."

Why it fails: a div modal with no focus trap, no `aria-modal`, no ESC, and no focus restore leaves keyboard and screen-reader users behind the overlay — a 2.1.1 / 2.4.3 failure and a Nielsen "user control and freedom" failure.

Good:
- "Use a native `<dialog>` (APG modal-dialog pattern): open with `showModal()`, move focus to the dialog heading, trap focus inside, close on ESC and on backdrop click, and restore focus to the trigger on close. Lock body scroll while open."

### 2. Off-canvas table (responsive flattening)

Bad:
- "On mobile, just let the data table scroll horizontally inside an off-canvas panel so the desktop layout still fits."

Why it fails: forcing a wide table into a horizontal-scroll drawer is responsive flattening — it breaks 1.4.10 Reflow at 320px (two-dimensional scrolling) and hides comparison behind a swipe.

Good:
- "Below 768px, reflow the table into stacked label/value cards (one record per card) with the key column as the card title; keep the full sortable table at ≥ 1024px where desktop density helps. Verify no horizontal scroll at 320px."

### 3. Hover-only actions

Bad:
- "Show the row's edit/delete actions on `:hover` to keep the table clean."

Why it fails: hover-only actions are invisible to keyboard and touch users (no hover on coarse pointers) — a 2.1.1 operability failure and a discoverability problem.

Good:
- "Render a persistent row-actions menu button (`<button>` opening an APG menu) that is in the tab order and visible on touch; reveal the inline quick-actions on hover *and* on `:focus-within` as a progressive enhancement, never as the only path."

### 4. Aesthetic laundering vs. a justified bold move

Bad:
- "Make the dashboard feel more premium with a bold full-bleed hero and a glassmorphism panel."

Why it fails: no mechanism, no user benefit — visual polish over a task surface (aesthetic laundering), and it likely costs density, contrast, and LCP.

Good (a *bold move*, justified and quarantined): a recommendation that contradicts the current product is a failure **only when its justification is aesthetic**. Justified by a named mechanism and surfaced in the Mode D `Bold move` block, it is encouraged:
- "Replace the hamburger-hidden navigation (used at all widths) with a persistent top nav plus a command palette (Cmd/Ctrl-K). Deviates from the 'one hidden menu everywhere' model. JTBD: when I jump between sections often, I want the destination in one step. Upside: lowers choice cost (Hick), recognition over recall, shorter cursor path to edges (Fitts). Risk: nav is denser. De-risk: tree-test findability + axe/keyboard pass + 320px reflow; kill if findability drops. Score: safe fixes → 4/5; this targets 5/5 once validated. Conviction: worth a spike."

### 5. Evidence overreach

Bad:
- "This checkout is WCAG AA compliant and our research shows it converts 22% better."

Why it fails: an unverified compliance claim plus a fabricated metric — a P0 evidence-overreach failure.

Good:
- "This checkout is designed to support WCAG 2.2 AA; conformance must be verified with an axe + keyboard + screen-reader pass. The simplified step order is expected to reduce abandonment (mechanism: lower per-step load); validate with a measured A/B test — no lift is claimed here."

### 6. Placeholder-as-label

Bad:
- "Use the placeholder text as the field label to save vertical space."

Why it fails: the label vanishes on focus/entry, fails 1.3.1 / 3.3.2, and hurts recall and error recovery.

Good:
- "Use a persistent visible `<label>` associated with the input; reserve the placeholder for an example format. Tie inline errors to the field via `aria-describedby` and set `aria-invalid` on failure."
