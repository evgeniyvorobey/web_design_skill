# Visual review fixture: SaaS pricing comparison table (desktop 1280px)

## Review setup

Synthetic fixture only. This is a text description that stands in for a screenshot or Figma frame so a Mode D visual reviewer can be calibrated against a known answer key. There is no live DOM, no real CSS, and no rendered pixels — only the prose below. A correct review reasons strictly from the stated values and flags the issues listed under **Expected critique** at roughly the stated severities, while avoiding everything under **Prohibited critique**.

Do not claim anything that depends on evidence not present in this text (computed contrast beyond the pairs given, actual font files, real animation timing, measured INP, or screen-reader output). If a fact is not written here, treat it as unknown, not as a defect.

## Page description

A marketing pricing page for a fictional SaaS product, "Cadence", rendered at a 1280px desktop viewport. The page centers a four-plan pricing comparison: **Free**, **Starter ($19/mo)**, **Growth ($49/mo)**, and **Scale ($129/mo)**. Below the four plan cards sits a long feature-comparison table with 28 feature rows grouped into 5 sections (Core, Collaboration, Automation, Security, Support). A monthly/annual billing toggle sits above the cards. The "Growth" plan is visually promoted as the recommended plan.

The reading flow top-to-bottom is: skip link (visually hidden until focus) -> sticky top nav -> h1 + subhead -> billing toggle -> 4 plan cards -> comparison table -> FAQ accordion -> footer.

## Viewport specs

- **Primary viewport:** 1280px x 900px desktop (breakpoint ladder: 1280 desktop tier). Container max-width 1200px, centered, with 40px gutters (so content column is 1120px wide).
- **Secondary viewport (referenced only):** 390px mobile-web for the responsive note in **Known constraints**. At 390px the 4 cards stack to a single column and the comparison table switches to a per-plan stacked layout.
- **Grid:** 12-column desktop grid, 24px gutters. The 4 plan cards each span 3 columns (so 4 x 3 = 12). The comparison table spans all 12 columns.
- **Plan card dimensions:** each card 264px wide x 420px tall, 24px internal padding, 16px gap between cards.
- **Comparison table:** first column (feature name) 360px wide and sticky-left; the 4 plan columns are 190px each. Header row is sticky-top at offset 64px (below the 64px sticky nav). Row height 48px; section header rows 40px.

## Visible hierarchy

1. **h1** — "Pricing that scales with your team" (one h1 on the page).
2. **Subhead** (paragraph, not a heading) — "Start free. Upgrade when you outgrow it. Cancel anytime."
3. **Billing toggle** — segmented control: "Monthly" | "Annual (save 20%)".
4. **4 plan cards**, each with an **h3** plan name, price, a CTA button, and a short feature list (6 bullet items per card).
5. **h2** — "Compare all features".
6. **Comparison table** with 5 **section header rows** (styled as bold cells spanning the row, not real headings) and 28 feature rows. Cells use a check glyph, an em dash for "not included", or a short text value (e.g., "5 seats", "Unlimited").
7. **h2** — "Frequently asked questions" with a 6-item accordion (native `<details>`/`<summary>`).
8. **footer** with 4 link columns.

Heading outline as described: h1 -> h3 (x4) -> h2 -> h2. **There is a skipped level: the page jumps from h1 to h3 on the plan cards with no intervening h2** (the "Compare all features" h2 appears only after the cards).

## Components

- **Sticky top nav** (`<header>` + `<nav>`): logo, 4 nav links, "Log in" text link, "Start free" primary button. Height 64px, sticky at top, subtle bottom border.
- **Billing toggle**: implemented as two `<button>`s in a segmented control with `role="group"`. Selected state shown by a filled pill behind the active label.
- **Plan card**: `<article>` containing h3, price block, CTA `<button>`, and a `<ul>` of 6 features. The "Growth" card is the promoted card — it has a 2px accent border, a small "Most popular" badge pinned to the top edge, and is drawn 8px taller than its siblings, breaking card baseline alignment.
- **CTA buttons**: "Get started" (Free), "Start free trial" (Starter, Growth, Scale). Growth's CTA is the only filled/primary button; the other three are outline/secondary. Button height 40px, horizontal padding 16px.
- **Comparison table** (`<table>` with `<thead>`/`<tbody>`): sticky first column and sticky header row. Cells render a check glyph (included) or em dash (excluded). The check glyph is the ONLY signal for inclusion in boolean rows — no text label, no `aria-label` mentioned.
- **FAQ accordion**: native `<details>`/`<summary>`, 6 items, single-open not enforced (multiple can be open).
- **Footer**: 4 columns of links, copyright row, locale switcher.

## Typography

- **Body / table cells:** 16px (1rem), line-height 1.5, system UI stack.
- **h1:** clamp(2rem, 1.5rem + 2.5vw, 3rem) — at 1280px this resolves to ~3rem (48px), line-height 1.2, weight 700.
- **Subhead:** 1.125rem (18px), line-height 1.5, weight 400.
- **h2 ("Compare all features", "Frequently asked questions"):** 1.75rem (28px), line-height 1.3, weight 600.
- **h3 (plan names):** 1.25rem (20px), line-height 1.3, weight 600.
- **Price (large):** 2.25rem (36px), weight 700, with a 0.875rem (14px) "/mo" suffix.
- **Plan card feature list:** 0.875rem (14px), line-height 1.5.
- **"Most popular" badge text:** 0.6875rem (11px), uppercase, letter-spacing 0.04em, weight 600.
- **Table section header text:** 0.8125rem (13px), uppercase, weight 700.
- **Legal/footnote under prices** ("Billed annually" caption): 0.75rem (12px), line-height 1.4.
- Measure: the FAQ answer paragraphs run the full 1120px content width (~140 characters per line at 16px), far past the ~65ch reading target.

## Color and state notes

Stated contrast pairs (treat these as ground truth for this fixture):

- **Body text** #1F2933 on #FFFFFF = **14.8:1** (passes 1.4.3 AA for normal text).
- **h1** #0B1220 on #FFFFFF = **18.7:1** (passes).
- **"Most popular" badge** text #FFFFFF on accent #3B82F6 = **3.7:1** — text is 11px, so it is "normal" text and needs 4.5:1. **Fails 1.4.3 AA.**
- **Primary button label** #FFFFFF on #2563EB = **5.2:1** (passes for normal text).
- **Secondary/outline button** label #2563EB on #FFFFFF = **5.2:1** (passes); its 1px border #93C5FD on #FFFFFF = **1.8:1** (the border is the only thing delimiting the control — **fails 1.4.11 non-text contrast 3:1**).
- **Muted helper text** ("Cancel anytime") #8A94A6 on #FFFFFF = **3.1:1** — **fails 1.4.3 AA.**
- **Table em-dash "not included"** glyph #C4CDD9 on #FFFFFF = **1.6:1** — **fails 1.4.11** (it is meaningful non-text content distinguishing excluded features).
- **Annual savings indicated only by green** check color #16A34A vs the monthly state — color is the sole differentiator on the toggle's "save 20%" emphasis. Potential **1.4.1 use of color** concern (see Expected critique for the exact scope).
- **Focus ring:** 2px solid #2563EB at 2px offset on buttons and links = **5.2:1** against white (passes 1.4.11). Focus ring color is stated; focus IS visible.

## Interaction states

- **Buttons:** default, hover (darken 8%), :focus-visible (2px ring described above), active, disabled (none disabled on this page).
- **Billing toggle:** selected vs unselected; selection persists via `?billing=annual` URL param (URL-as-shareable-state). Keyboard: arrow keys move between the two options, Enter/Space activates.
- **Plan card CTA:** loading state on click shows a spinner inside the button and sets `aria-busy="true"` (stated).
- **Comparison table:** header row and first column are sticky; no sort, no row selection (static marketing table — acceptable for this context). Hover highlights the full row with a #F3F6FA background.
- **FAQ `<summary>`:** focusable, expands on Enter/Space/click, rotates a chevron.
- **Reduced motion:** `prefers-reduced-motion` is NOT mentioned for the chevron rotation or button transitions (unknown — see Prohibited critique).

## Known constraints

- This is a marketing page, not an app surface; the comparison table is intentionally read-only (no sort, filter, or row-select). Density is deliberately moderate, not dashboard-dense.
- At the 390px mobile-web viewport the cards stack and the table reflows to per-plan stacks; that mobile layout is out of scope for this 1280px review except where reflow at 320px (1.4.10) is logically implied.
- Brand accent is blue (#2563EB / #3B82F6 family); green (#16A34A) is used only for positive/included emphasis.
- The page sets `width`/`height` on the logo and card media; CLS-relevant boxes are reserved (stated).

## Expected critique

A good reviewer should surface most of these. Severity uses the Nielsen 0–4 scale (see **Severity expectations**).

1. **(Sev 3) "Most popular" badge fails text contrast.** White on #3B82F6 = 3.7:1 at 11px normal text; needs 4.5:1 (WCAG 1.4.3). The promoted plan's badge is the least readable label on the page — fix the accent or darken to the #2563EB token (≈5.2:1).
2. **(Sev 3) Boolean inclusion relies on a check glyph alone.** Included vs excluded is conveyed only by check-vs-em-dash with no text/`aria-label` and the em dash is #C4CDD9 (1.6:1). This implicates 1.4.1 (use of color/shape alone) AND 1.4.11 (non-text contrast 3:1) for the meaningful glyphs. Add visible text ("Included"/"Not included") or accessible names and raise glyph contrast.
3. **(Sev 3) Muted helper text "Cancel anytime" at 3.1:1 fails 1.4.3.** Darken #8A94A6 to at least a #6B7280-class value to reach 4.5:1.
4. **(Sev 2) Outline/secondary button border fails non-text contrast.** #93C5FD border at 1.8:1 is below the 3:1 required by 1.4.11 for the control boundary; the 4.5:1 label is borderline but the control edge is effectively invisible. Strengthen the border token.
5. **(Sev 2) Heading outline skips a level (h1 -> h3).** Plan cards use h3 with no enclosing h2, violating the logical outline expected under semantic HTML / 1.3.1. Either promote the cards' grouping to an h2 or restructure.
6. **(Sev 2) Annual-savings emphasis may be color-only.** If "save 20%" is distinguished from the monthly option purely by green, that risks 1.4.1; the text label "Annual (save 20%)" is present, so scope this narrowly to the *emphasis styling*, not the label itself.
7. **(Sev 2) FAQ answer measure is too long.** ~140ch lines at full 1120px width hurt readability (typography craft; ~65ch target). Constrain the answer column to ~65ch.
8. **(Sev 1) Promoted card breaks baseline alignment.** Growth card is 8px taller, so the 4 CTAs no longer sit on a shared baseline — minor composition/rhythm issue.
9. **(Sev 1) Sticky header offset coupling.** Table header sticks at 64px to clear the 64px nav; note as a fragile magic-number coupling worth a CSS variable, not a defect per se.

## Prohibited critique

A reviewer must NOT make these claims from this text alone:

- **Do not claim** the focus indicator is missing or invisible — a 2px #2563EB ring at 5.2:1 is explicitly stated as present and passing 1.4.11.
- Do not claim body text or h1 contrast fails — they are 14.8:1 and 18.7:1 (passing).
- Do not claim there is no skip link — a visually-hidden-until-focus skip link is stated in the reading flow.
- Do not claim the billing toggle is not keyboard operable — arrow-key navigation and Enter/Space activation are stated.
- Do not invent INP/LCP/CLS numbers or assert a performance failure; only box-reservation (CLS-relevant) is stated as handled, and no timings are given.
- Do not claim `prefers-reduced-motion` is mishandled — it is unmarked/unknown, not stated as broken.
- Do not claim the table needs sort/filter/row-select; it is intentionally a read-only marketing table per **Known constraints**.
- Do not claim a sticky action bar or any overlay is present — none is described.
- Do not claim target sizes fail without basis: button height is 40px and the segmented control labels are normal buttons; 2.5.8 AA (24px) is met and nothing states otherwise (do not assert the 44px AAA bar as a failure).
- Do not claim missing alt text on images; image accessible names are not described either way (unknown).

## Severity expectations

Nielsen severity scale (0 = not a problem, 1 = cosmetic, 2 = minor, 3 = major, 4 = catastrophic):

- **Sev 3 (major):** badge text contrast (#1), boolean-by-glyph + low-contrast em dash (#2), muted helper text contrast (#3). These block real comprehension/readability and touch named WCAG AA criteria.
- **Sev 2 (minor):** outline button border (#4), skipped heading level (#5), color-only annual emphasis (#6), over-long FAQ measure (#7).
- **Sev 1 (cosmetic):** broken card baseline (#8), sticky-offset magic number (#9).
- **Sev 0:** anything in **Prohibited critique** — reporting those counts against the reviewer.
- No **Sev 4** issues are present; a reviewer asserting a catastrophic/blocker defect is over-calling.

## Rubric score expectation

Scores are 1–5 per dimension (target 4 = strong and shippable).

| Dimension | Current | Projected after fixes |
|---|---|---|
| Attention path & hierarchy | 3 | 4 |
| Composition & spacing | 3 | 4 |
| Typography craft | 3 | 4 |
| Color/state & contrast | 2 | 4 |
| Density & rhythm | 4 | 4 |
| Interaction polish & motion | 3 | 4 |
| Context & brand fit | 4 | 4 |
| Production readiness | 3 | 4 |

**Expected current overall: ~3.0/5.** The dominant drag is **Color/state & contrast (2/5)** driven by the three Sev-3 contrast/use-of-color findings plus the non-text border. **Projected after addressing the Expected critique: ~4/5** across the board — strong and shippable. A review landing far above (claiming 4–5 now) or far below (flagging Sev-4 blockers) this band is miscalibrated against this **Synthetic fixture only**.
