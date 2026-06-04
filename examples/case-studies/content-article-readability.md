# Case study: Long-form article readability (measure, type scale, table of contents)

A bad-to-good calibration case for a long-form editorial article template:
a documentation guide or magazine feature that a reader works through top to
bottom and returns to via a table of contents. The target for the strong
response is a shippable **4/5** across the eight design-quality dimensions.

## Prompt

```text
We publish long technical guides (3,000-6,000 words) on our marketing site.
Right now they render as one wide column of text edge to edge on desktop and
people bounce. Reading feels exhausting and nobody scrolls past the fold.

Design the reading experience for an article template:
- the body type and measure so it is comfortable to read
- a fluid type scale for h1/h2/h3 and body
- a table of contents that helps people jump around a long piece
- how it behaves from a 320px phone up to a 1440px desktop

Stack is plain HTML/CSS with a little JS. Give me concrete values I can build,
not vibes. Accessibility matters - we get audited.
```

## Weak response

```md
Here's a clean reading layout for your articles.

**Typography**
- Use a nice serif like Georgia for the body, it feels editorial.
- Make the body text a comfortable size, around 18-20px.
- Headings should be bold and much bigger so they stand out - maybe 2-3x
  the body size.
- Add some line spacing so it breathes.

**Layout**
- Center the article and don't let it get too wide. A max-width keeps lines
  from running on forever.
- Add generous padding on the sides.
- On mobile it stacks into one column, on desktop you can put the table of
  contents on the left.

**Table of contents**
- List all the headings as links at the top of the article.
- Clicking a link jumps to that section with smooth scrolling.
- On desktop, make it sticky so it follows you down the page.

**Polish**
- Use a light off-white background instead of pure white, easier on the eyes.
- Highlight the current section in the TOC as you scroll.
- Add a reading-progress bar at the top.

This gives you a focused, distraction-free reading experience that should
keep people on the page longer.
```

## Why this is weak

- **Typography craft (2/5) - no measure, no scale, no rem.** "Around 18-20px"
  and "2-3x the body" is a vibe, not a system. There is no defined **measure**
  (the prompt's core ask), no modular ratio, and sizes are implied in `px`,
  which fights user font-size preferences and risks **WCAG 1.4.4 Resize text**.
  A "much bigger" heading with no `line-height` guidance produces the classic
  long-form failure: tight 1.1 leading on a wrapped h2.
- **Composition & spacing (2/5) - "generous padding" is unbuildable.** No
  spacing scale, no container width in numbers, no gutter values. "Don't let it
  get too wide" never names the ~65ch reading column, so the developer guesses
  and the measure ends up at 100-120 characters on a 1440px screen - exactly
  the fatigue the prompt described.
- **Attention path & hierarchy (2/5).** A serif body "because it feels
  editorial" is a taste assertion with no contrast or rendering rationale, and
  the heading hierarchy is described only by size multiplier. Nothing about the
  semantic heading outline (one `h1`, no skipped levels) that the TOC depends on.
- **Color/state & contrast (1/5) - skips the audit they asked about.** "Light
  off-white background, easier on the eyes" gives no hex values and no contrast
  ratio, so there is no **1.4.3** check (4.5:1 body). Links get no affordance
  beyond color (**1.4.1 Use of color**), and the TOC "highlight current section"
  relies on a tint alone with no non-color cue (**1.4.11 Non-text contrast**).
- **Interaction polish & motion (2/5) - scroll-jump and motion hazards.**
  "Smooth scrolling" is hard-coded with no `prefers-reduced-motion` escape
  (**2.3.3 Animation from interactions**), and a sticky scroll-spy TOC with
  in-page anchors gives no thought to **2.4.11 Focus not obscured** (a sticky
  header hiding the jumped-to heading) or to where keyboard focus lands after a
  TOC jump (**2.4.3 Focus order**).
- **Production readiness (1/5).** No font-loading strategy, so the swap from
  fallback to web serif causes layout shift (**CLS** budget 0.1 blown). No
  responsive behavior for the TOC below desktop beyond "stacks." No
  `:focus-visible`, no skip link, no loading/empty states. Fails Nielsen's
  *Visibility of system status* (where am I in the doc?) and *User control and
  freedom* (no way to opt out of motion).

## Strong response

```md
## Reading system: measure first, then the scale around it

The whole template is built around one constant - the **reading column** - and
everything else (scale, spacing, TOC) is derived from it.

### The reading column (measure)

- Body measure caps at **~65ch** (`max-width: 65ch`), inside the comfortable
  45-75 character target. At 16px body that is roughly 600-680px; we set the
  column to `min(65ch, 100% - 2rem)` so it never touches the viewport edge on a
  320px phone (the reflow floor for WCAG 1.4.10).
- Figures, code blocks and pull-quotes are allowed to **break out** wider than
  the text column (a wide / full-bleed grid track) so prose stays at 65ch while
  evidence gets room.

```css
.article {
  /* gutter | wide | reading column | wide | gutter, with bleed tracks */
  --measure: 65ch;
  --gutter: clamp(1rem, 4vw, 2rem);
  display: grid;
  grid-template-columns:
    [full-start] minmax(var(--gutter), 1fr)
    [wide-start] minmax(0, 8rem)
    [text-start] min(var(--measure), 100%) [text-end]
    minmax(0, 8rem) [wide-end]
    minmax(var(--gutter), 1fr) [full-end];
}
.article > *        { grid-column: text; }   /* prose at 65ch */
.article > figure   { grid-column: wide; }   /* media breaks out */
.article > .full    { grid-column: full; }
```

### Fluid type scale (rem-anchored clamp, ratio 1.25 major third)

Every `clamp()` carries a **rem term** so user zoom and browser font-size still
scale the type (passes 1.4.4 Resize text to 200% and 1.4.10 Reflow):

| Role | Size | line-height |
|------|------|-------------|
| body | `clamp(1rem, 0.95rem + 0.3vw, 1.125rem)` | 1.6 |
| h3   | `clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)` | 1.3 |
| h2   | `clamp(1.563rem, 1.4rem + 0.8vw, 1.953rem)` | 1.25 |
| h1   | `clamp(1.953rem, 1.7rem + 1.6vw, 2.986rem)` | 1.2 |
| caption | `0.875rem` | 1.5 |

- Body never drops below **16px (1rem)**. Long-form leading is **1.6** (looser
  than the 1.5 floor) because eyes travel a full 65ch line; headings tighten to
  1.2-1.3 so multi-line headings stay one visual block.
- Vertical rhythm on a 4px base: paragraph spacing `1.5rem` (24px), space above
  an h2 `3rem` (48px) / above h3 `2rem` (32px) - the "more space before than
  after" rule that binds a heading to the text it owns (Gestalt proximity).
- The grid already constrains line length, so no `max-width` on `<p>` is needed;
  we add `text-wrap: pretty` on headings and `hanging-punctuation: first` for
  editorial polish where supported.

### Type rendering and font loading (protects CLS)

- Body font `font-display: swap`; preload only the above-the-fold weight
  (`<link rel="preload" as="font" crossorigin>`), and declare a fallback with
  matched metrics (`size-adjust` / `ascent-override` on an `@font-face` for the
  system fallback) so the swap does not shift the article. CLS budget 0.1, LCP
  (the h1 + first paragraph) target <= 2.5s.
- Colors meet **1.4.3**: text `#1a1d23` on `#fbfbf9` is ~15:1; muted captions
  `#5b6270` on the same background is ~5.2:1 (still >= 4.5:1). Links carry an
  underline, not color alone (**1.4.1 Use of color**), and `:focus-visible`
  shows a 2px outline with 2px offset that meets **1.4.11** 3:1 against the page.

## Table of contents

Semantics first: the article is one `<h1>` then a strict `h2`/`h3` outline
(no skipped levels) - the TOC is generated from that outline, so the document
structure and the nav stay in sync.

```html
<nav class="toc" aria-labelledby="toc-heading">
  <h2 id="toc-heading">On this page</h2>
  <ol>
    <li><a href="#measure">The reading column</a>
      <ol><li><a href="#scale">Type scale</a></li></ol>
    </li>
    <!-- ... -->
  </ol>
</nav>
```

- It is a real `<nav>` landmark with an accessible name, containing an ordered
  list of in-page `<a href="#id">` links - native anchor navigation, keyboard
  operable for free, working with no JS at all.
- Each target heading has a matching `id`. We add
  `:target { scroll-margin-top: 5rem; }` so a jumped-to heading is **not hidden
  behind the sticky site header** (WCAG **2.4.11 Focus not obscured (minimum)**).
- After a TOC click we move focus to the section so screen-reader and keyboard
  users land where sighted users land: the target heading container has
  `tabindex="-1"` and we call `.focus()` on `hashchange` (satisfies **2.4.3
  Focus order**; nothing becomes a keyboard trap, **2.1.2**).
- **Scroll-spy without color-only:** the current section's link gets
  `aria-current="location"` plus a visible 3px left rule and a weight change -
  two non-color cues, not just a tint (**1.4.1**, **1.4.11**). The spy uses
  `IntersectionObserver`, never a per-scroll handler, to protect **INP <= 200ms**.
- TOC link targets are >= 24px tall (**2.5.8 Target size (minimum)**), spaced so
  adjacent anchors do not overlap their hit areas.

## Responsive behavior (320 -> 1440)

| Range | Reading layout | Table of contents |
|-------|----------------|-------------------|
| 320-767 | single column, `1rem` gutters, measure = `100% - 2rem` | collapsed into a native `<details>` at the top, summary "On this page" |
| 768-1023 (tablet) | centered 65ch column | inline `<details>` stays, or a sticky top bar |
| 1024-1439 | 65ch column, room for wide breakout figures | sidebar TOC in the left gutter, `position: sticky; top: 5rem` |
| 1440+ | column stays 65ch (we do NOT widen prose), figures use bleed tracks | sticky sidebar with scroll-spy |

- The TOC component decides its own form with a **container query**
  (`@container (min-width: 60rem)`) rather than a viewport breakpoint, so it can
  be reused in a narrow CMS preview pane and still collapse correctly.
- A skip link (`Skip to article`) precedes the TOC so keyboard users are not
  forced to tab through every anchor to reach the prose.

## Motion and states

- `html { scroll-behavior: smooth; }` is wrapped in
  `@media (prefers-reduced-motion: no-preference)` - reduced-motion users get
  instant jumps (**2.3.3**). The reading-progress bar is decorative
  (`aria-hidden`) and also disabled under reduced-motion.
- States covered: default, `:hover`, `:focus-visible`, `:active`, `:visited`
  for TOC links; loading uses a content skeleton sized to the 65ch column to
  avoid shift; an empty TOC (article with no `h2`) hides the `<nav>` entirely
  rather than rendering an empty box; `forced-colors` mode keeps the
  current-section rule via `border-color: currentColor` and a system color.

This is a strong, shippable answer (**4/5**): measure-first system, rem-anchored
fluid scale, an accessible TOC with focus management, and named CWV / WCAG
guardrails. It stops short of 5/5 because it does not spec a per-locale measure
(CJK character width differs from Latin ch) or a server-rendered TOC fallback
for no-JS scroll-spy parity.
```

## Why this is stronger

- **Typography craft (4/5).** The answer is organized around the **measure**
  (`min(65ch, 100% - 2rem)`) the prompt actually asked for, with a named modular
  scale (1.25 major third), every size in a **rem-anchored `clamp()`** so 1.4.4
  Resize and 1.4.10 Reflow hold, and per-role `line-height` (1.6 body for a long
  line, 1.2-1.3 headings). Vertical rhythm is on the 4px scale with the
  "more space above a heading than below" rule (Gestalt proximity).
- **Composition & spacing (4/5).** A concrete grid keeps prose at 65ch while
  letting figures break out - directly answering the "edge-to-edge wide column"
  fatigue. Gutters are `clamp()`'d, never "generous." Spacing is numeric
  (24/32/48px on the 4px base).
- **Color/state & contrast (4/5) - it does the audit.** Real hex values with
  stated ratios (~15:1 body, ~5.2:1 captions, both passing **1.4.3**), links
  underlined not color-only (**1.4.1**), focus outline meeting **1.4.11** 3:1,
  and a `forced-colors` fallback - the compliance the weak answer hand-waved.
- **Interaction polish & motion (4/5).** Smooth scroll gated on
  `prefers-reduced-motion` (**2.3.3**), `scroll-margin-top` so the target is not
  obscured by the sticky header (**2.4.11**), focus moved to the section on
  `hashchange` (**2.4.3**), and scroll-spy via `IntersectionObserver` to defend
  **INP**. Nielsen *Visibility of system status* (aria-current + visible rule)
  and *User control and freedom* (reduced-motion, native back/forward via real
  anchors) are both served.
- **Density & rhythm + context fit (4/5).** Desktop density is exploited where
  it pays (sidebar TOC in the gutter, breakout figures at 1024+) instead of
  flattening to a phone column, while prose deliberately stays 65ch at 1440+.
  The TOC uses a **container query** so the component is portable, not viewport-locked.
- **Production readiness (4/5).** Font-loading with `swap`, preload, and matched
  fallback metrics protects **CLS <= 0.1**; LCP and INP budgets are named;
  states (default/hover/focus/active/visited/loading/empty/forced-colors) and a
  skip link are specified. Honest 4-vs-5 boundary: no per-locale (CJK) measure
  and no no-JS scroll-spy parity.

## Regression checks

- Body text is **>= 16px (1rem)** and every font-size uses a **rem-anchored
  `clamp()`** (a rem or em term inside the clamp), so the page survives 200%
  zoom (1.4.4) and 320px reflow (1.4.10); a future answer must not regress to
  bare `px` or `vw`-only sizing.
- The prose **measure stays ~65ch** (45-75 characters) at every breakpoint up
  to 1440px+; widening the reading column to fill a wide desktop is a failure.
- The **table of contents is a real `<nav>` landmark of in-page anchors built
  from a clean `h1`/`h2`/`h3` outline** (one `h1`, no skipped levels), works
  without JS, applies `scroll-margin-top` so the target is not obscured
  (2.4.11), and moves focus to the section on jump (2.4.3).
- Body contrast is **>= 4.5:1** and the current-TOC-section indicator and links
  never rely on **color alone** (1.4.1 / 1.4.11) - at least one non-color cue
  (underline, border rule, weight) is present, including under `forced-colors`.
- Smooth scrolling and any progress / scroll animation are gated on
  `prefers-reduced-motion` (2.3.3), and scroll-spy uses `IntersectionObserver`
  (not a per-scroll handler) to keep **INP <= 200ms**; font loading uses
  `font-display: swap` + preload + matched fallback metrics to hold **CLS <= 0.1**.

Boundary: this is a SYNTHETIC calibration fixture for scoring article-reading
layouts; it is **not** validation against a shipped, real-world product, and the
contrast ratios, CWV figures, and scale values are illustrative targets to be
re-measured in a real build, not audited production numbers.
