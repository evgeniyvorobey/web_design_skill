# Case study: Empty, error, 404, 500, offline, and session-expired states for a web analytics app

A bad-to-good calibration case for the "non-happy-path" surfaces of a responsive
web app. These states are where teams under-invest, yet they decide whether a user
recovers or bounces. The strong target here is **4/5** across the eight design-quality
dimensions: strong and shippable, not a perfect showpiece.

## Prompt

```text
We're building a web analytics dashboard (responsive, used on laptops and tablets).
Design the "nothing/something-went-wrong" screens for the Reports section:

  1. Empty state — a brand-new workspace with zero reports yet.
  2. Error state — the reports list failed to load (API 500).
  3. 404 — user hit a deep link to a report that was deleted.
  4. Offline — the user's connection dropped mid-session.
  5. Session expired — auth token lapsed after idle; the next action 401s.

Give me layout, copy, the exact components, responsive behavior, and how each state
recovers. Accessibility matters — we ship to enterprise customers with audits.
```

## Weak response

```md
Here are the empty and error states for the Reports section.

**Empty state**
Center a friendly illustration on the page. Below it, a heading "No reports yet"
and a subtext "Create your first report to get started." Add a big blue
"Create report" button. Use lots of whitespace so it feels clean.

**Error state**
Show a red icon and the text "Something went wrong." Add a "Retry" link in red so
users know it's an error. Keep it centered like the empty state.

**404**
Show "404" in huge type, "Page not found" underneath, and a link back home.

**Offline**
Pop a toast that says "You are offline." It disappears after a few seconds.

**Session expired**
Redirect the user straight to the login page when their session expires so they
can sign in again.

Use the same centered card for all of them so it's consistent. Keep the copy short
and the buttons obvious. That should cover the edge cases.
```

## Why this is weak

- **Attention path & hierarchy (2/5):** Every state is "centered card + icon + button,"
  so the design never distinguishes *recoverable* (retry) from *navigational* (404) from
  *blocking* (session expired). One template flattens five different user intents.
- **Color/state & contrast (1/5):** "Retry link in red" and "red error icon" lean on
  **color alone** to carry meaning, failing WCAG **1.4.1 Use of Color**. Red text on a
  card also risks failing **1.4.3 Contrast (Minimum)** at 4.5:1, and the red is never
  paired with an icon shape or label that conveys severity non-chromatically (**1.4.11
  Non-text Contrast**, 3:1 for the icon/control boundary).
- **Production readiness (1/5):** No HTTP status mapping, no `aria-live` for async
  failures, no focus management. "Redirect straight to login" on session expiry silently
  destroys unsaved work and the user's place — a data-loss bug, not a design.
- **Interaction polish & motion (2/5):** The offline toast auto-dismisses after a few
  seconds, but offline is a *persistent* condition, not a transient event. This violates
  Nielsen's **Visibility of system status** — the status vanishes while the problem
  remains, so the user is told "everything is fine" while writes keep failing.
- **Typography craft (2/5):** "404 in huge type" with no scale guidance; "lots of
  whitespace" and "big blue button" are vibes, not values. No measure, no clamp(), no
  line-height, nothing buildable.
- **Context & brand fit (2/5):** Treats an enterprise analytics tool like a consumer
  splash screen. An empty *workspace* and an empty *filtered result* are different
  problems; the answer collapses them.
- **Density & rhythm (2/5):** "Lots of whitespace so it feels clean" wastes a laptop
  viewport. On desktop these states should still respect the app shell (nav + header)
  rather than blanking the whole page.
- **Heuristics missed:** **Help users recognize, diagnose, and recover from errors**
  (no diagnosis, no specific recovery), **Error prevention** (no protection of in-flight
  work on 401), **User control and freedom** (forced redirect, no escape).

## Strong response

```md
# Reports — non-happy-path states

## Shared shell and tokens
All five states render *inside* the app shell: persistent `<header>` (logo, search),
`<nav aria-label="Primary">` sidebar, and `<main id="main">`. We never blank the whole
page except for true full-app failures (the offline banner and the top-level 500
boundary are global; the rest are scoped to `<main>`). Skip link
`<a href="#main" class="skip">` stays first in tab order.

Design tokens (4px base spacing scale): `--s-1:4px --s-2:8px --s-3:12px --s-4:16px
--s-6:24px --s-8:32px --s-12:48px --s-16:64px`. Body type 1rem (16px) min,
`line-height: 1.5`; state headings `clamp(1.5rem, 1.25rem + 1.2vw, 2rem)` with
`line-height: 1.25`. State copy capped at `max-width: 60ch`; the whole state block is
centered horizontally but pinned near the top third, not vertically dead-center, so it
reads above the fold at 768px tablet height.

A reusable `<StatePanel>` component (NOT a single template — it has a `variant` prop):
- `role` of the panel: `status` for non-error (empty, 404), `alert` for
  error/offline/expired.
- Icon is decorative (`aria-hidden`) and ALWAYS paired with a text heading + a colored
  *and* shaped status chip ("Error", "Offline") so meaning never rides on hue alone
  (1.4.1). Icon stroke/fill meets 3:1 against its background (1.4.11).
- Primary action is a native `<button>` or `<a>` with `min-height: 44px` (2.5.5 AAA
  target; floor is 24px per 2.5.8). `:focus-visible` shows a 2px outline + 2px offset,
  scrolled into view so it is never obscured (2.4.11).

Color: severity comes from a token PAIR — `--danger-fg` (text/icon, 4.5:1 on surface)
plus a left border + chip label. We also ship `@media (forced-colors: active)` rules so
chips/borders survive Windows High Contrast (use `CanvasText` / `Mark`, keep
`forced-color-adjust: auto`). `prefers-reduced-motion: reduce` disables all entrance
motion.

## 1. Empty state (zero reports) — role="status"
Scoped to `<main>`. Layout: centered column, illustration (decorative, `aria-hidden`,
reserved `aspect-ratio: 4/3` so there is no CLS), `<h1>No reports yet</h1>`, one line of
guidance (≤60ch), then a primary `<button>Create report</button>` and a secondary
`<a>Import from CSV</a>` (button hierarchy: one primary, one quiet secondary — no
competing CTAs). Below the fold: a 3-up "starter templates" grid on `>=1024px` that
collapses to 1-up under 640px via a container query on the panel, exploiting laptop
density instead of wasting it. Distinguish this from an *empty filtered result*: when a
filter yields nothing we show "No reports match these filters" + a "Clear filters"
button, not the onboarding empty state.

## 2. Error state (list failed, 500) — role="alert"
Scoped to `<main>`; the rest of the app stays usable. On fetch rejection we render the
panel and move focus to its heading (`tabIndex={-1}`), with the live region announcing
"Couldn't load reports." Copy diagnoses + recovers: heading "We couldn't load your
reports", body "This is on our end, not you. The error ID below helps support."
Show a monospace **error ID** (`req_8f2a…`) the user can copy — that is the production
tell. Primary `<button>Try again</button>` re-runs the query with a skeleton loader
(reserved row heights, no layout shift); after 2 failed retries we surface a
"Contact support" link prefilled with the error ID. The density toggle and table
controls remain in the header so the user isn't stranded.

## 3. 404 (deleted/unknown report) — navigational, NOT alert
Server returns a real 404; the SPA route renders a `role="status"` panel inside `<main>`.
`<h1>This report no longer exists</h1>`, body "It may have been deleted or the link is
out of date." Recovery is *navigational*, so we give choices: primary
`<a>Go to all reports</a>`, secondary `<a>Search reports</a>`, plus a breadcrumb so the
user keeps their place. Set the document `<title>` to "Report not found" and return the
404 status to crawlers (a soft-404 hurts SEO and audits). No retry button — retrying a
404 is a dead end.

## 4. Offline — persistent global banner, NOT a toast
Listen for `window` `offline`/`online` events. On offline, render a **persistent**
`role="status"` banner pinned below the header (it does NOT auto-dismiss — the condition
is ongoing): "You're offline. We'll keep your last loaded data and reconnect
automatically." Disable write actions (`aria-disabled`, with an explanatory tooltip)
instead of letting them fail. Queue the failed request; on `online` fire it and swap the
banner to a brief `role="status"` "Back online" that *can* auto-dismiss (the event is now
transient). All of this respects **Visibility of system status** — status persists exactly
as long as the underlying state does.

## 5. Session expired (401 after idle) — non-destructive re-auth
The dangerous one. On a 401 we do NOT redirect away. We open a `<dialog>` modal
("Your session expired"), trap focus, restore focus to the triggering control on close,
ESC closes, scroll is locked, `aria-modal="true"`, labelled by its heading. Body:
"Sign back in to continue. Your unsaved changes are kept." Primary `<button>Sign back
in</button>` opens auth in place (or a popup) and, on success, **resumes the original
action** with its preserved payload — no work lost (Error prevention + User control and
freedom). Secondary "Copy my draft" escape hatch for the worst case. Only if re-auth
itself fails do we fall back to the full login route, preserving `?returnTo=` so we land
back here.

## Responsive & states matrix
- 320px reflow floor: panels stay single-column, no horizontal scroll (1.4.10); chips
  wrap; targets stay ≥24px.
- 768px tablet: panel max-width ~60ch centered; starter grid 2-up.
- 1024–1440px: app shell + sidebar visible; empty-state starter grid 3-up.
- Every state defines: default, loading (skeleton), success-after-recovery, and its own
  failure (e.g., "retry also failed"). Resize to 200% and text-spacing overrides
  (1.4.4 / 1.4.12) must not clip the panel.

This is a **4/5** target: strong, accessible, and buildable. The remaining point is
reserved for motion/illustration polish and content tuning from real telemetry.
```

## Why this is stronger

- **Attention path & hierarchy (4/5):** Five states map to three *recovery intents* —
  recoverable (empty/error/offline), navigational (404), and blocking (session expired) —
  and each gets a layout and CTA hierarchy that matches its intent. One primary action per
  state, secondaries kept quiet.
- **Color/state & contrast (4/5):** Severity is carried by a **token pair plus a shaped
  chip and label**, never hue alone (**1.4.1**). Text meets **1.4.3** 4.5:1; icon/border
  boundaries meet **1.4.11** 3:1; `forced-colors: active` support keeps chips legible in
  Windows High Contrast.
- **Production readiness (4/5):** Explicit HTTP mapping (500 → alert, 404 → navigational
  status, 401 → re-auth dialog), `aria-live`/`role` per state, focus moved to the panel
  heading on async failure, copyable **error ID** for support, a real 404 for crawlers, and
  a request queue for offline.
- **Interaction polish & motion (4/5):** Offline is a **persistent** banner (matching the
  ongoing condition) that swaps to a dismissible "Back online" only once the event is
  transient — a correct read of **Visibility of system status** and of dismissal semantics.
  `prefers-reduced-motion` is honored.
- **Heuristics satisfied:** **Recognize, diagnose, recover** (error ID + specific cause +
  scoped retry), **Error prevention** (401 preserves unsaved work and resumes the action),
  **User control and freedom** (ESC, focus restore, no forced redirect, breadcrumb on 404).
- **Typography & density (4/5):** Concrete `clamp()` heading scale with a rem term, 1rem
  body floor, `line-height` values, ~60ch measure, and a starter grid that *exploits*
  laptop density via a container query instead of blanking the viewport.
- **Context & brand fit (4/5):** Renders inside the app shell, separates empty *workspace*
  from empty *filtered result*, and treats an enterprise/audited tool as such rather than a
  consumer splash.

## Regression checks

- Severity and error meaning must NEVER be conveyed by color alone (1.4.1): every
  error/offline state keeps a shaped + labeled status chip and a text heading alongside any
  red token.
- Session expiry (401) must NOT hard-redirect away from in-progress work: it opens a
  focus-trapped `<dialog>` that preserves the unsaved payload and resumes the original
  action on re-auth, with `returnTo` only as the last-resort fallback.
- The offline indicator must be a PERSISTENT `role="status"` banner that lives exactly as
  long as the offline condition; it must not auto-dismiss while still offline, and the
  "Back online" confirmation may auto-dismiss only after the `online` event.
- Async failures must move focus to the panel heading and announce via a live region; the
  500 path must surface a copyable error ID and a `:focus-visible` outline that is not
  obscured (2.4.11), with targets ≥24px (2.5.8).
- All states must reflow at the 320px floor with no horizontal scroll (1.4.10) and survive
  200% resize plus text-spacing overrides (1.4.4 / 1.4.12) without clipping.

Boundary: this is a SYNTHETIC calibration fixture authored to exercise the rubric; it is
**not** validation against a shipped, audited build, and the scores are illustrative
rather than measured. Do not treat the 4/5 here as a guarantee that any specific
implementation will pass a third-party audit.
