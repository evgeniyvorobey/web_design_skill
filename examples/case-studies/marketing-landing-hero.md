# Case study: Marketing landing hero — above-the-fold and CTA hierarchy

A bad-to-good calibration fixture for a marketing landing page hero: the first viewport a visitor sees, the value proposition it carries, and the call-to-action hierarchy that routes intent. The weak answer ships a centered headline and a button. The strong answer treats the hero as a measured composition with a defined attention path, a clear primary/secondary CTA split, reserved media space, and accessible interactive states.

> Boundary: this is a SYNTHETIC fixture written to calibrate review judgment. It is not validation against a shipped product, and its conversion claims are illustrative, not measured. Treat the numbers as design intent, not evidence.

## Prompt

```text
We're a B2B scheduling SaaS ("Cadence"). Design the above-the-fold hero for our
new marketing homepage. It needs a headline, supporting copy, a primary CTA
("Start free trial") and a way for hesitant visitors to learn more before
committing. There's a product screenshot to show. Desktop is the priority but it
has to hold up on phones. Give me layout, type, spacing, color/state, and the
accessibility + performance details an engineer can build from.
```

## Weak response

```md
Here's a clean, modern hero for Cadence.

**Layout**
- Full-width hero section, content centered.
- Big headline, a sentence of subtext, then the button.
- Put the product screenshot underneath, centered, full width.

**Copy**
- Headline: "Scheduling, simplified."
- Subtext: "Cadence helps teams book meetings faster."
- Button: "Start free trial" — make it big and a bright color so it pops.
- Add a "Learn more" link under the button.

**Type**
- Headline large and bold (like 48px), subtext smaller and grey so it
  recedes. Use a nice sans-serif.

**Color**
- Brand purple gradient background. White headline text. Purple button.
- Use light grey for the subtext so the headline stands out.

**Responsive**
- On mobile everything stacks and stays centered. Shrink the headline so it
  fits. The screenshot scales down to full width.

**Accessibility**
- Use a real <button> for the CTA and alt text on the screenshot. Make sure
  colors look good.
```

It is plausible, it names a few right things (`<button>`, alt text, stacking), and a junior engineer could fake something from it. But it collapses under any real review.

## Why this is weak

- **Attention path and hierarchy (2/5).** Centering everything gives no entry point — eyebrow, headline, subtext, CTA, and screenshot all compete on the same axis with no F- or Z-pattern to ride. "Make it big and a bright color so it pops" is decoration, not hierarchy. There is no stated relationship between the primary and secondary action, so both read as equal weight — a direct violation of a clear-hierarchy heuristic (Nielsen's "aesthetic and minimalist design" is misread as "center and enlarge").
- **CTA hierarchy is undefined.** "Start free trial" and "Learn more" are described but never ranked as a filled primary vs. a quieter secondary. Two equally loud calls split intent and lower the odds of either being taken (Hick's law: more equally-weighted choices, slower decision).
- **Color/state and contrast (1/5).** "Light grey subtext" on a purple gradient is the classic 1.4.3 failure — grey-on-gradient rarely clears 4.5:1, and it is unspecified so it cannot be checked. "Looks good" is not a contrast ratio. The button relies on color alone to signal importance, brushing against 1.4.1 Use of Color. Worst of all: **no hover, no :focus-visible, no active, no disabled, no loading** state is given for the one interactive element on the screen. There is no forced-colors / Windows High Contrast plan.
- **Typography craft (2/5).** A single 48px headline size with no fluid scaling means it will overflow at 320px or look tiny on a 1440px canvas. No line-height, no measure (line length), no clamp(), no rem. "Smaller and grey so it recedes" conflates size and contrast as one knob.
- **Composition and spacing (2/5).** "Full width" for both copy and screenshot ignores a reading measure (~65ch) and a max content width — text will run to 1900px on a wide monitor. No spacing scale; "underneath" and "big" are not buildable values.
- **Production readiness (1/5).** The screenshot has "alt text" but **no reserved space** (no width/height or aspect-ratio), so it will cause layout shift and blow the CLS budget. No font-loading strategy, so the gradient plus web font will flash and shift (CLS again). No LCP consideration even though the headline or screenshot is almost certainly the LCP element. No empty/error/offline thinking for the trial form the CTA leads to.
- **Density and rhythm (2/5).** Mobile "just shrinks and stays centered" — it flattens the desktop composition to a phone column instead of rebalancing. No breakpoint ladder.
- **Interaction polish and motion (1/5).** None specified. No hover-intent, no reduced-motion stance, no focus management when the CTA opens a trial flow.

## Strong response

```md
# Cadence homepage hero — above-the-fold spec

## Intent and attention path
One primary job: get a qualified B2B visitor to "Start free trial". One
secondary job: let the hesitant visitor self-qualify via "See how it works"
without leaving the page. The hero reads as a left-to-right Z: eyebrow →
headline → subhead → CTA pair → (eye lands on) product screenshot on the right,
which visually "shows" what the trial gives. Exactly ONE primary action,
visually dominant; the secondary is a quiet, equal-affordance-but-lower-emphasis
button so intent is not split (Hick's law: rank, don't tie).

## Layout and grid
- Desktop (>= 1024px): 12-col grid, max content width 1200px, centered in a
  1440px container with 24px gutters. Copy column spans cols 1-6 (text measure
  capped at ~60ch via `max-width: 60ch`); screenshot spans cols 7-12.
- Two-column hero uses CSS grid: `grid-template-columns: minmax(0, 1fr)
  minmax(0, 1.1fr); gap: 48px; align-items: center;`
- Tablet (768-1023px): same two columns but `gap: 32px` and screenshot drops to
  a smaller scale.
- Phone (320-767px): single column, text-block first, screenshot below.
  Reflows cleanly at 320px (1.4.10) with no horizontal scroll; vertical rhythm
  via a 4px-based scale (16 / 24 / 32 / 48px between blocks).
- Section vertical padding: `clamp(48px, 8vw, 96px)` top and bottom.

## Typography (16px / 1rem base, fluid)
- Eyebrow: 0.875rem (14px), letter-spacing 0.04em, uppercase, weight 600.
- Headline (h1, ONE per page): `font-size: clamp(2rem, 1.2rem + 3.2vw, 3.5rem);
  line-height: 1.15; letter-spacing: -0.01em; text-wrap: balance;` Caps at
  56px on wide. Copy: "Stop chasing calendars. Book the meeting."
- Subhead: `clamp(1rem, 0.95rem + 0.4vw, 1.25rem); line-height: 1.5;
  max-width: 52ch.` Copy: "Cadence turns 'when works for you?' into a single
  link your prospects actually click. Set availability once; let booking,
  reminders, and routing run themselves."
- Body line-height 1.5, headings 1.15-1.3. System-font fallback stack tuned to
  match metrics (see font-loading) so swap causes no reflow.

## CTA hierarchy and states
- Primary `<a role="button">`/`<button>` "Start free trial": filled, brand
  accent background, min target 44x44px (2.5.5 AAA, well past the 24px 2.5.8
  floor), `padding: 12px 24px`, `border-radius: 8px`, weight 600. Does NOT rely
  on color alone — it is the only FILLED control and carries a trailing arrow
  glyph, so shape + fill + label all signal primacy (1.4.1).
- Secondary "See how it works": outline/ghost button, same height, opens an
  in-page product tour `<dialog>` (ESC closes, scroll-lock, focus trap, focus
  restored to the trigger on close — 2.1.1, 2.4.3). Lower emphasis, equal
  reachability.
- States for BOTH:
  - default
  - hover: bg darkens ~8% (primary) / subtle tint (secondary), 120ms ease-out;
    suppressed under `@media (hover: none)` so touch doesn't get stuck-hover.
  - :focus-visible: 3px outline, 2px offset, token `--focus-ring`, contrast
    >= 3:1 against both the button and the page (1.4.11, 2.4.11 not obscured by
    a sticky header).
  - active: 1px translateY, slightly darker.
  - loading: primary swaps label for a spinner plus `aria-busy="true"`,
    `aria-live="polite"` status "Setting up your trial…"; width is locked so the
    button doesn't reflow (no CLS).
  - disabled: only if a required field upstream is empty; `aria-disabled`,
    3:1 non-text contrast still met, tooltip explains why.
- `prefers-reduced-motion: reduce` removes the arrow nudge and any entrance
  transition; color/opacity state changes remain (they are not motion).

## Color and contrast (tokens, not vibes)
- Background: solid `--surface` (#0E1525) OR a low-contrast gradient whose
  DARKEST stop is used to compute text contrast. Headline `--text-strong`
  (#F4F6FB) on that = 14.8:1. Subhead `--text-muted` (#B9C2D6) = 7.1:1 — still
  past 4.5:1 (1.4.3), so "muted" is achieved by hue/weight, not by failing
  contrast.
- Primary button bg `--accent` (#3B6EF6) with #FFFFFF label = 4.9:1; its focus
  ring and its border vs. surface clear 3:1 (1.4.11).
- Forced-colors: `@media (forced-colors: active)` — buttons fall back to
  `ButtonText`/`ButtonFace`, focus ring uses `Highlight`, the arrow glyph stays
  visible via `forced-color-adjust: auto`. Gradient is dropped for `Canvas`.
- Honors text-spacing overrides (1.4.12) — no fixed heights on text blocks;
  nothing clips at 200% zoom (1.4.4).

## Media and performance
- Screenshot reserves space to kill layout shift: `<img>` with explicit
  `width`/`height` attrs and `aspect-ratio: 16 / 10` so the box exists before
  the asset loads (protects CLS <= 0.1). Responsive `srcset` plus `sizes`,
  `decoding="async"`. Meaningful `alt`: "Cadence dashboard showing a shared team
  availability calendar with three open booking slots."
- LCP element is the h1 (text) — so we PRELOAD the headline web font
  (`<link rel="preload" as="font" crossorigin>`), `font-display: swap`, and ship
  a metrics-matched fallback (`size-adjust`, `ascent-override`) so swap causes
  zero reflow. The screenshot is the second-heaviest paint: `fetchpriority="high"`
  on it, lazy-load everything BELOW the fold. Target LCP <= 2.5s, INP <= 200ms,
  CLS <= 0.1.
- No render-blocking hero animation; entrance fade is CSS-only, opt-out via
  reduced-motion, and never delays the LCP paint.

## Semantics, landmarks, keyboard
- `<header>` (site nav with skip link "Skip to main content") → `<main>` →
  hero is the first `<section aria-labelledby="hero-h1">`. Single h1, no skipped
  levels. Landmarks: header / nav / main / footer.
- Tab order: skip link → nav → primary CTA → secondary CTA. The screenshot is
  not a tab stop (decorative-but-described). Logical order, no keyboard trap
  (2.1.1).
- Trial flow opened by the primary CTA manages focus to the first field and
  announces the route change via `aria-live`.

## States beyond the happy path
- Slow network: skeleton block for the screenshot (same aspect-ratio box) so
  the layout is stable while it streams.
- Trial CTA failure: inline `role="alert"` error ("Couldn't start the trial —
  try again"), CTA returns from loading to default. Session-expired and offline
  variants route to a retry, never a dead button.

## Responsive ladder (min-width, mobile-first)
320 (reflow floor, single col) / 480 (larger type step) / 640 / 768 (two-col
appears, tighter gap) / 1024 (full 12-col, 1200px content) / 1280 / 1440
(container caps, side whitespace grows) / 1920+ (content stays 1200px, hero does
NOT stretch text to the viewport).
```

This is a 4/5 answer: shippable and strong. It is not flawless — it leaves exact copy-test variants, real screenshot dimensions, and analytics event names to the build — but every quality bar is met with a concrete web mechanism.

## Why this is stronger

- **Attention path and hierarchy (4/5).** A named Z-path with exactly one dominant primary action and a deliberately quieter secondary resolves the split-intent problem. The screenshot is placed to *complete* the path ("shows what the trial gives"), not float underneath. Matches Nielsen's "match between system and the real world" and a clear visual-hierarchy heuristic; Hick's law is addressed by ranking the two CTAs instead of tying them.
- **CTA hierarchy is explicit and accessible.** Primacy is carried by fill plus shape plus glyph plus label, not color alone (1.4.1 Use of Color). Both buttons are real controls with full state machines (default → hover → :focus-visible → active → loading → disabled) and a loading state that locks width to avoid CLS.
- **Color/state and contrast (4/5).** Every text/background pair is a named token with a measured ratio that clears 1.4.3 (14.8:1, 7.1:1) and the button clears 4.5:1; non-text/focus contrast clears 1.4.11 (3:1). "Muted" subhead is achieved by hue and weight while still passing contrast — the exact trap the weak answer fell into. Forced-colors / high-contrast and 1.4.12 text-spacing / 1.4.4 200% zoom are all handled.
- **Typography craft (4/5).** Fluid `clamp()` with a rem term scales the h1 between 320px and wide without overflow or shrinkage; line-height (1.15 head / 1.5 body), measure (~60ch / 52ch), `text-wrap: balance`, and metric-matched fallback are all specified.
- **Composition and spacing (4/5).** 12-col grid, 1200px content cap inside a 1440px container, a 4px-based vertical scale (16/24/32/48), and a capped reading measure stop text from running edge-to-edge on wide screens.
- **Production readiness (4/5).** Reserved media space via width/height plus aspect-ratio, font preload plus swap plus metric-matched fallback, correct LCP element identified and prioritized, and Core Web Vitals budgets stated (LCP <= 2.5s, INP <= 200ms, CLS <= 0.1). Failure, slow-network, session-expired, and offline states exist for the path the CTA opens.
- **Density, rhythm, interaction (4/5).** The phone layout rebalances the composition rather than shrinking it; reduced-motion is an explicit stance; hover is suppressed on coarse pointers so touch users don't get stuck-hover.

## Regression checks

A future answer to a hero / above-the-fold / CTA-hierarchy prompt must still pass all of these, or it has regressed below the 4/5 target:

- Exactly ONE primary CTA, visually dominant, with a deliberately lower-emphasis secondary — primacy signaled by fill plus shape plus label, never by color alone (1.4.1). Two equally-loud calls is an automatic fail.
- Every interactive control specifies the full state set — default, hover, :focus-visible, active, loading, disabled — with a measured focus ring (>= 3:1, 1.4.11) that is not obscured by a sticky header (2.4.11), and `hover` suppressed under `@media (hover: none)`.
- Every text/background and button color pair is a named token with a stated contrast ratio meeting 1.4.3 (4.5:1 body, 3:1 large); a "grey/muted" subhead must still clear 4.5:1, and forced-colors / high-contrast behavior is described.
- The headline uses fluid `clamp()` with a rem term, line-height in the 1.15-1.35 band for headings and 1.5 for body, and a capped reading measure (~60ch) so copy never runs the full viewport width.
- The hero media reserves space (width/height attrs or `aspect-ratio`) and the LCP element is identified with a font-loading plan (preload plus `font-display: swap` plus metric-matched fallback) so CLS <= 0.1 and LCP <= 2.5s are achievable; INP <= 200ms is named.
- The layout reflows at 320px with no horizontal scroll (1.4.10), holds at 200% zoom (1.4.4), honors text-spacing overrides (1.4.12), and rebalances for phone rather than merely shrinking the desktop composition.
- Semantics are correct: one h1, no skipped levels, header/nav/main/footer landmarks, a skip link, logical tab order with no keyboard trap (2.1.1), and focus management for any dialog/route the CTA opens (ESC plus focus trap plus restore).
