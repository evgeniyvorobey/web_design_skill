# Visual review fixture: Marketing landing above-the-fold hero (desktop + mobile-web)

> Synthetic fixture only. This file is a text stand-in for a screenshot or Figma frame. It exists to calibrate Mode D visual reviews. There is no rendered pixel buffer, no DOM, and no live CSS behind it — every value below is asserted in prose. A reviewer must treat the described values as ground truth and reason only from what is written here.

## Review setup

- Artifact type: marketing landing page, single above-the-fold hero section, pre-launch SaaS product ("Cadence", a release-notes scheduling tool).
- Frames provided: one desktop frame at 1280px and one mobile-web frame at 390px. Both are first paint, default state, no scroll.
- Goal of review: catch hierarchy, contrast, spacing, and production-readiness issues that would block a 4/5 "strong and shippable" bar across the 8 design-quality dimensions.
- What the reviewer can see: layout, copy, stated colors, stated type sizes, stated states. What the reviewer cannot see: motion timing curves, real font files, actual measured LCP, screen-reader output, focus order in a running browser.
- Heuristic frame: Nielsen 10 usability heuristics + WCAG 2.2 AA named criteria. Severity uses the Nielsen 0–4 scale.

## Page description

A centered single-column hero on a near-white canvas (`#FBFBFD`). Above the hero is a sticky top-nav. The hero stacks: an eyebrow pill, an h1 headline, a supporting paragraph, a primary + secondary CTA pair, a row of three trust logos in grayscale, and a product screenshot placeholder framed in a rounded card. On desktop the screenshot sits to the right of the text in a 12-column split (text spans columns 1–6, image spans 7–12). On mobile-web the screenshot drops below the CTA pair into a single reflowed column.

The visual tone is restrained: one accent (indigo `#4F46E5`), generous whitespace, a single sans-serif family. The intent is a calm, credible developer-tool landing page, not a high-density dashboard.

## Viewport specs

Desktop frame:

- Viewport width: 1280px (desktop rung of the breakpoint ladder). Device pixel ratio assumed 1.
- Content container: max-width 1200px, centered, with 32px gutters left and right.
- Grid: 12 columns, 24px gutters. Hero text occupies columns 1–6; product image card occupies columns 7–12.
- Top-nav height: 64px, sticky, full-bleed background with a 1px bottom hairline border `#E5E5EA`.
- Hero vertical padding: 96px top (below the 64px nav) and 64px bottom before the fold.

Mobile-web frame:

- Viewport width: 390px (between the 360 and 480 rungs). One column.
- Container side padding: 16px each edge → 358px usable.
- Top-nav collapses to a 56px bar: wordmark left, a hamburger control right.
- Hero stack order: eyebrow → h1 → paragraph → primary CTA → secondary CTA → trust logos → screenshot card. Vertical rhythm uses the 4px scale (gaps of 12, 16, 24, 32px).
- The reflow floor at 320px is claimed to hold (no horizontal scroll), but the 320px frame itself is not provided.

## Visible hierarchy

1. h1 headline: "Ship release notes on a schedule, not a scramble." — largest element, top of reading order in the text column.
2. Primary CTA button: "Start free trial" — solid indigo, highest contrast interactive element.
3. Eyebrow pill: "Now in open beta" — small uppercase label above the h1.
4. Supporting paragraph: one sentence of body copy under the h1.
5. Secondary CTA: "Watch 2-min demo" — text-style link button with a play glyph.
6. Trust logo row: three grayscale company marks at 40% opacity with the label "Trusted by teams at".
7. Product screenshot card: large but visually muted (it is a placeholder), so it reads as supporting, not as the primary focal point.

Intended attention path: eyebrow → h1 → paragraph → primary CTA. The screenshot is meant to be peripheral validation.

## Components

- `TopNav` — wordmark, 4 nav links (Product, Pricing, Docs, Changelog), and a trailing "Sign in" link + "Start free trial" button. Sticky, `position: sticky; top: 0`.
- `EyebrowPill` — rounded-full pill, indigo text on a 10%-tint indigo background.
- `Heading` — single `<h1>`, two-line wrap on desktop, three-line wrap on mobile-web.
- `Lede` — one `<p>`, constrained to ~60ch on desktop.
- `ButtonGroup` — `PrimaryButton` (solid) + `SecondaryButton` (ghost/text). Native `<button>`/`<a>` assumed.
- `TrustRow` — `<ul>` of three `<img>` logos with a preceding caption.
- `MediaCard` — rounded 16px card, 1px border `#E5E5EA`, holding an `<img>` screenshot placeholder.

## Typography

Family: "Inter", system-ui fallback. Single family across the hero. `font-display: swap` is stated, but no preload is declared for the above-the-fold weight.

Desktop:

- h1: 48px / 3rem, line-height 1.2, weight 700, letter-spacing -0.02em. Two lines.
- Lede paragraph: 18px / 1.125rem, line-height 1.5, weight 400, measure ~60ch.
- Eyebrow pill: 12px / 0.75rem, uppercase, letter-spacing 0.06em, weight 600.
- Primary CTA label: 16px / 1rem, weight 600.
- Secondary CTA label: 16px / 1rem, weight 500.
- Trust caption: 13px / 0.8125rem, weight 500.
- Nav links: 15px / 0.9375rem, weight 500.

Mobile-web:

- h1: stated as a fixed 34px / 2.125rem, line-height 1.25, weight 700. (Note: fixed px, not a `clamp()` — flagged below.)
- Lede paragraph: 16px / 1rem, line-height 1.5.
- Eyebrow pill: 12px / 0.75rem.
- CTA labels: 16px / 1rem.

Body minimum of 16px is met on both frames. The h1 does not use a fluid `clamp()` with a rem term; it switches between two hard-coded px values at the 640px breakpoint.

## Color and state notes

Palette and stated contrast pairs (ratios are asserted, computed from the stated hexes):

- Body text `#1D1D1F` on canvas `#FBFBFD` → ~16.3:1. Passes 1.4.3 (AA, normal) comfortably.
- h1 `#1D1D1F` on `#FBFBFD` → ~16.3:1. Passes.
- Primary CTA: white `#FFFFFF` label on indigo `#4F46E5` → ~6.3:1. Passes 1.4.3 AA for normal text and 1.4.11 for the button shape vs canvas.
- Secondary CTA text `#4F46E5` on `#FBFBFD` → ~6.1:1. Passes AA normal comfortably.
- Eyebrow pill: indigo `#6D5FE8` text on 10%-tint indigo fill `#ECEBFC` → ~4.0:1. FAILS 1.4.3 AA for 12px normal text (needs 4.5:1).
- Trust caption `#8A8A8E` on `#FBFBFD` → ~3.3:1. FAILS 1.4.3 AA for 13px normal text.
- Trust logos rendered at 40% opacity gray → effective contrast well under 3:1 against canvas. As decorative brand marks this is tolerable, but they carry meaning ("who trusts us"), and that meaning is conveyed by the logos plus a low-contrast caption only.
- Secondary CTA is distinguished from the primary by fill vs no-fill plus weight, not by color alone, so 1.4.1 (use of color) is satisfied for the CTA pair specifically.

State notes that ARE specified:

- Primary CTA hover: background darkens to `#4338CA` (~7.9:1 with white). Specified.
- Primary CTA `:focus-visible`: 2px indigo ring with a 2px white offset. Specified.
- Disabled state for CTAs: not specified.
- Loading state for "Start free trial" (it submits to a sign-up flow): not specified.

## Interaction states

- Default: as described above.
- Hover: only the primary CTA hover is defined. Nav links, secondary CTA, and trust logos have no stated hover treatment.
- `:focus-visible`: defined for the primary CTA only. Not stated for nav links, secondary CTA, or the hamburger control.
- Active/pressed: not specified for any control.
- Mobile-web hamburger: opens an off-canvas menu. The fixture states the trigger exists but does NOT describe the opened panel, its focus trap, ESC-to-close, or scroll-lock.
- Pointer adaptation (`@media (pointer: coarse)`): not mentioned; CTA hit areas are stated only as visual sizes.

Stated target sizes:

- Primary CTA: 44px tall × 168px wide. Meets 2.5.8 (24px) and 2.5.5 AAA (44px).
- Secondary CTA: 40px tall × 150px wide. Meets 2.5.8.
- Nav links: 64px-tall nav bar but each link's clickable box is stated as 20px tall text with 8px vertical padding → ~36px target. Meets 2.5.8, below 2.5.5 AAA.
- Mobile hamburger control: stated as a 24px glyph with no stated padding → effective target may be exactly 24px, at the 2.5.8 minimum with no margin. Flagged as borderline.

## Known constraints

- This is a marketing page; SEO and LCP matter. The hero screenshot is the likely LCP element. The fixture states the `<img>` has a `width`/`height` attribute pair and `aspect-ratio` reserved, so CLS from the image should be low. It does NOT state `fetchpriority="high"` or a preload for the LCP image.
- The font preload for the above-the-fold weight is not declared, only `font-display: swap`. Fallback metric overrides (`size-adjust` / `ascent-override`) are not mentioned.
- Copy and brand are fixed by the client; do not critique the wording of the headline.
- Only the hero is in scope. Anything below the fold is out of scope and not described.

## Expected critique

A good reviewer SHOULD surface these (each maps to a named criterion/heuristic and a severity):

1. Eyebrow pill contrast fails AA. Indigo `#6D5FE8` on `#ECEBFC` ≈ 4.0:1 at 12px normal weight — below the 4.5:1 floor of WCAG 2.2 1.4.3. Severity 3. Fix: darken the text to ~`#3730A3` or deepen the fill.
2. Trust caption contrast fails AA. `#8A8A8E` on `#FBFBFD` ≈ 3.3:1 at 13px — below 4.5:1 (1.4.3). Severity 3. Fix: use `#636366` or darker.
3. h1 is not fluid. It hard-switches between 48px and 34px at one breakpoint with no `clamp()` and a rem term, risking awkward sizing on the 480–640px band and missing the skill's fluid-type bar. Relates to 1.4.4 (resize) robustness. Severity 2.
4. Focus-visible coverage is incomplete. Only the primary CTA has a stated `:focus-visible` ring; nav links, the secondary CTA, and the hamburger lack one, risking a 2.4.7 / 2.4.11 keyboard-visibility gap and missing "visible focus on every interactive element." Severity 3.
5. Hamburger target is borderline. A 24px glyph with no stated padding sits exactly at the 2.5.8 minimum with zero margin; on a 390px touch frame this is uncomfortable. Severity 2. Fix: pad to a 44px box.
6. Off-canvas menu behavior is unspecified. No stated focus trap, focus restore, ESC-to-close, or scroll-lock for the mobile menu (2.1.1 keyboard operability, 2.1.2 no keyboard trap, WAI-ARIA APG disclosure/menu pattern). Severity 3 as a production-readiness gap.
7. Missing CTA states. No disabled and no loading/skeleton state for "Start free trial", which submits to sign-up; users get no feedback on a slow network (Nielsen H1 visibility of system status). Severity 2.
8. LCP image not prioritized. The hero screenshot is the likely LCP element but lacks `fetchpriority="high"` and a preload; the above-the-fold font weight is not preloaded. Risks the LCP <= 2.5s budget. Severity 2.
9. Trust logos carry meaning but render at ~40% opacity (well under 3:1), conveying "who trusts us" via low-contrast marks plus a sub-4.5:1 caption only. Severity 1 (advisory): give the logo row an accessible group label and a readable caption.

## Prohibited critique

Do not claim the following — the text does not support them. "Synthetic fixture only" means absence of a detail in this file is NOT evidence of a defect unless the file explicitly says the detail is missing.

- Do not claim the primary CTA text fails contrast. White on `#4F46E5` is ~6.3:1 and passes; do not assert otherwise.
- Do not claim the h1 or body text fails contrast. Both are ~16.3:1 and pass.
- Do not claim there is a horizontal scrollbar or a reflow failure at 320px. The fixture states reflow holds and the 320px frame is not provided; you cannot measure it from this text.
- Do not claim LCP, INP, or CLS measured values. No real measurement exists here; only budgets and risk factors are stated. Speak in terms of risk, not measured numbers.
- Do not claim the screenshot causes layout shift. The fixture explicitly reserves `width`/`height` and `aspect-ratio`.
- Do not claim a color-only violation for the CTA pair (1.4.1). The fixture states fill vs no-fill plus weight distinguish them, which is a non-color cue.
- Do not claim the headline copy is weak, off-brand, or should be reworded. Copy is client-fixed and out of scope.
- Do not invent motion, transition timing, or easing problems. No motion is described; absence is not a defect to assert here.
- Do not critique below-the-fold content, the pricing page, or anything not in this single hero frame.
- Do not claim the body font is below 16px. Both frames meet the 16px body minimum.

## Severity expectations

Nielsen 0–4 severity scale (0 = not a problem, 4 = usability catastrophe):

- Eyebrow pill contrast fail (1.4.3): 3 — major, affects readability of a labeled element, must fix before ship.
- Trust caption contrast fail (1.4.3): 3 — major.
- Incomplete `:focus-visible` coverage (2.4.7 / 2.4.11): 3 — major keyboard-access gap.
- Unspecified off-canvas menu semantics (2.1.1 / 2.1.2): 3 — major production-readiness gap.
- Non-fluid h1 (fluid-type bar, 1.4.4 robustness): 2 — minor, fix soon.
- Borderline hamburger target (2.5.8): 2 — minor.
- Missing CTA disabled/loading states (H1): 2 — minor.
- LCP image not prioritized (CWV budget): 2 — minor performance risk.
- Marginal secondary-CTA contrast (1.4.3): 1 — cosmetic/advisory, currently passing.

Expected count: roughly 4 severity-3 items and 4–5 severity-2/1 items. A reviewer that returns zero severity-3 items has under-read the contrast and focus issues; a reviewer that flags more than ~9 distinct issues is likely inventing problems beyond what the text supports.

## Rubric score expectation

Scoring the 8 design-quality dimensions (1–5; target 4 = strong and shippable):

| Dimension | Current | Projected after fixes |
|---|---|---|
| Attention path & hierarchy | 4 | 4 |
| Composition & spacing | 4 | 4 |
| Typography craft | 3 | 4 |
| Color/state & contrast | 2 | 4 |
| Density & rhythm | 4 | 4 |
| Interaction polish & motion | 3 | 4 |
| Context & brand fit | 4 | 4 |
| Production readiness | 2 | 4 |

- Expected current overall: ~3.2/5 — the median of the assessable dimensions is 3.5, lowered to ~3.2 because two critical task dimensions (Color/state 2, Production readiness 2) drag below the median. The layout, spacing, and hierarchy are already strong; the page is dragged down by two contrast fails, incomplete focus styling, unspecified overlay semantics, and missing CTA/LCP production details.
- Projected after the Expected-critique fixes: ~3.9–4.0/5 — strong and shippable.
- A review that scores Color/state & contrast or Production readiness at 4 in the current state has missed the named failures and should be treated as a calibration miss.
