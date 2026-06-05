# Visual review fixture: Long-form content article, desktop reading column

> Synthetic fixture only. This file is a text stand-in for a screenshot or Figma
> frame. It exists so a Mode D reviewer can be calibrated against a known answer
> key. There is no rendered pixel buffer here; every value below is authored, not
> measured. Do not claim to have inspected real pixels, computed real contrast
> from an image, or run an automated checker — judge only from the prose.

## Review setup

A reader opens an editorial long-form article ("How container queries change the
component contract") on a marketing-adjacent engineering blog. The route is
`/articles/container-queries-component-contract`. The page is a single-column
reading experience with a sticky table-of-contents rail on the left at desktop, a
share/utility cluster, inline figures, pull quotes, code blocks, and a footnotes
section. The reviewer is asked to grade reading ergonomics, typographic craft,
and accessibility of the article surface — not the surrounding global nav.

Evaluate against WCAG 2.2 AA, the WAI-ARIA APG, Nielsen's 10 heuristics, and the
8 design-quality dimensions. Severity uses the Nielsen 0–4 scale.

## Page description

The viewport shows a content-first article template. From top to bottom:

- A slim global header (logo left, primary nav, search, "Subscribe" button right),
  56px tall, that scrolls away with the page (not sticky).
- An article hero: eyebrow category link ("Engineering"), the `h1` headline, a
  one-sentence standfirst/deck, then a byline row (author avatar 40px, author
  name link, role, publish date `2026-05-28`, "9 min read").
- Below the hero, a two-rail layout at >=1024px: a 240px left rail holding a
  sticky table of contents ("On this page") and a vertical share cluster
  (Copy link, X, LinkedIn, Email), and a centered reading column.
- The reading column: running body text, three `h2` section headers, several
  `h3` subheads, two inline `<figure>` images with captions, one
  `<figure>`-wrapped pull quote, two fenced code blocks (CSS), an inline callout
  ("Note") box, and an ordered footnotes list at the end.
- A footer-of-article block: tags row, author bio card, "Related articles"
  3-card grid, and a newsletter sign-up form.

The reading column is the subject. The left rail TOC is in scope; the global
header/footer chrome is explicitly out of scope.

## Viewport specs

Primary capture — **1280px desktop** (1280×900 logical, 12-col grid, 24px gutters,
margins ~96px each side):

- Page max content width: 1200px, centered.
- Left rail: fixed 240px column, `position: sticky; top: 24px` for the TOC.
- Reading column: width is **pinned at 760px** (not a `ch`-based measure). At the
  authored body size this yields roughly **88–92 characters per line** — wider
  than the ~65ch reading-comfort target.
- Gap between left rail and reading column: 64px.
- Right side of the reading column to page edge: ~136px of empty space (the
  column is not optically centered in the remaining area; it hugs the left rail).
- Inline figures span the full 760px column; pull quote is inset to 640px.

Secondary capture — **390px mobile-web** (390×844 logical, 16px page margins):

- Single column; left rail collapses. The TOC becomes a `<details>` disclosure
  ("On this page") placed under the deck, collapsed by default.
- Reading column = viewport minus margins = 358px. Body text reflows to ~38–42
  characters per line.
- Share cluster moves to a horizontal row under the byline.
- Code blocks scroll horizontally inside the column (no wrap), with a visible
  scrollbar track.

Reflow floor check: author asserts the layout reflows cleanly at 320px with no
horizontal page scroll except inside the code blocks and one wide figure.

## Visible hierarchy

1. `h1` headline (article title) — clearly the dominant element of the hero.
2. Deck/standfirst — secondary, larger than body, lighter weight.
3. Section `h2` headers — anchor the reading rhythm; each has a hover-revealed
   `#` anchor link.
4. Pull quote — visually loud, competes with `h2` for second-most-prominent.
5. Body paragraphs — the workhorse text.
6. Left-rail TOC — quiet until a section is active (active item bolded + accent
   left-border).
7. Captions, footnotes, metadata — quietest tier.

Heading outline as authored: one `h1`, then `h2` → `h3` → `h2` → `h3` → `h3` →
`h2`. No level is skipped. The author bio card heading at the end is marked up as
an `h2` ("About the author"), which is structurally correct but visually styled
identically to an `h3`, slightly muddying the outline's visual logic.

## Components

- **Reading column** — semantic `<article>` wrapping the content, with the body
  in flowing `<p>`, `<h2>`, `<h3>`, `<figure>`, `<blockquote>`, `<pre><code>`.
- **Table of contents** — `<nav aria-label="On this page">` containing an
  ordered list of in-page anchor links. Active section tracked via an
  IntersectionObserver and reflected with `aria-current="location"` on the active
  link. On mobile, wrapped in `<details>`.
- **Share cluster** — group of `<button>`/`<a>` controls. "Copy link" is a
  `<button>` that writes to clipboard and shows a transient "Copied" confirmation.
- **Inline figure** — `<figure>` + `<img>` + `<figcaption>`; images carry
  `width`/`height` attributes and `loading="lazy"` below the fold.
- **Pull quote** — `<figure>` with `<blockquote>` and `<figcaption>` attribution.
- **Callout / Note box** — a tinted container with a "Note" label and body text.
- **Code block** — `<pre><code>` with a language tag chip and a "Copy" button in
  the top-right corner of the block.
- **Footnotes** — ordered list; each note has a back-reference link `↩` returning
  to its citation; citations are superscript anchor links.
- **Newsletter form** — email `<input type="email">`, consent checkbox, submit
  `<button>`; has default/loading/success/error states.

## Typography

Type ramp (root `font-size: 100%` → 1rem = 16px; body uses a fluid clamp):

- Body paragraph: `clamp(1rem, 0.96rem + 0.2vw, 1.125rem)` → **18px** at 1280px,
  weight 400, **line-height 1.5** (27px), color `#3A3F47` on `#FFFFFF`.
  Paragraph spacing: 24px bottom margin. Measure is 760px / ~90ch (too wide).
- Deck/standfirst: 22px / line-height 1.4, weight 400, color `#5A6270`.
- `h1`: `clamp(2rem, 1.4rem + 2.4vw, 3rem)` → **48px** at 1280px, weight 700,
  line-height 1.15, letter-spacing -0.01em, color `#14181F`.
- `h2`: 30px, weight 700, line-height 1.25, 48px top margin / 16px bottom.
- `h3`: 22px, weight 600, line-height 1.3, 32px top / 8px bottom.
- Pull quote: 26px, weight 500, line-height 1.35, color `#14181F`, 32px vertical
  margins, inset to 640px with a 4px accent left-border.
- Figure caption: **13px**, weight 400, line-height 1.4, color `#8A909B`.
- Footnotes: 14px, line-height 1.5, color `#5A6270`.
- Code: monospace 14px, line-height 1.6, in a `#F5F6F8` block.
- TOC links: 14px, line-height 1.4; active item weight 600.

Font loading: a single variable serif for headings (preloaded, `font-display:
swap`) and the system UI sans stack for body and chrome. Fallback metrics
(`size-adjust`, `ascent-override`) are declared on the serif `@font-face` to hold
layout and avoid CLS during the swap.

Text-spacing (1.4.12) and resize-to-200% (1.4.4): author claims the layout
survives the 1.4.12 overrides and a 200% zoom without clipping, because line
lengths and containers use logical max-widths and the column is not height-capped.

## Color and state notes

Surface is light. Contrast pairs (authored, not measured):

- Body `#3A3F47` on `#FFFFFF`: ~10.4:1 — passes 1.4.3 AA for normal text.
- `h1` `#14181F` on `#FFFFFF`: ~17.8:1 — passes.
- Deck `#5A6270` on `#FFFFFF`: ~6.0:1 — passes AA normal text.
- **Figure caption `#8A909B` on `#FFFFFF`: ~3.2:1 — FAILS 1.4.3** (needs 4.5:1;
  13px is normal-sized text, not large text).
- **Inline link color `#5B8DEF` on `#FFFFFF`: ~3.2:1 — FAILS 1.4.3** for link
  text, and links in body are distinguished **by color only** (no underline,
  no other non-color cue) → **also fails 1.4.1 Use of Color**.
- Code text `#1F2430` on `#F5F6F8`: ~14:1 — passes.
- Accent/brand `#2F6FED` used for the "Subscribe" button and TOC active border;
  button label `#FFFFFF` on `#2F6FED`: ~4.7:1 — passes AA normal text.
- Focus ring (authored): 2px solid `#2F6FED` with a 2px white offset; against the
  white page the ring-to-background contrast is ~4.7:1 (passes 1.4.11 non-text
  3:1), and on the `#F5F6F8` code block the same ring is ~4.4:1 (still passes).

Dark mode and forced-colors: a `prefers-color-scheme: dark` theme is declared. A
`forced-colors: active` block is **not** declared; the author notes link
underlines are suppressed, which would make links indistinguishable in Windows
High Contrast mode (compounds the 1.4.1 issue).

## Interaction states

- **TOC links**: default, `:hover` (accent text), `:focus-visible` (2px ring),
  `aria-current="location"` active (bold + 4px left-border). Active state is
  conveyed by border + weight, not color alone — acceptable.
- **Anchor `#` links on `h2`**: appear on `:hover` of the heading only. They are
  in the tab order and show on `:focus-visible`, so keyboard users can reach them
  even though they are visually hover-gated.
- **Copy link / Copy code buttons**: default, hover, focus, active; success state
  swaps label to "Copied" for ~1.5s. The confirmation is announced via an
  `aria-live="polite"` region — non-visual users get feedback.
- **Inline links**: default, hover (author says "darkens"), focus-visible, visited.
  No underline in any non-focus state (see color notes — this is the core defect).
- **Images**: reserve space via `width`/`height` → no layout shift on load. A
  blurred low-res placeholder is shown while loading.
- **Newsletter form**: default, focus-visible on field, loading (button spinner +
  disabled), success ("Check your inbox" inline message, `aria-live`), error
  (field-level message tied via `aria-describedby`, `aria-invalid="true"`).
- **Reduced motion**: `prefers-reduced-motion: reduce` removes the smooth-scroll
  on TOC anchor jumps and the placeholder blur-up transition.
- Targets: TOC links are 14px text in a 32px-tall row → meet 2.5.8 (24px). Share
  buttons are 40×40 → meet 2.5.8 and approach the 2.5.5 AAA 44px guideline.

## Known constraints

- The reading column width is a hard 760px set by the template; it is not derived
  from a `ch` measure, so longer body type overflows the comfort range.
- The brand link color `#5B8DEF` is a fixed brand token the team is reluctant to
  change; the underline decision is a CSS choice, not a brand constraint.
- The caption gray `#8A909B` is shared with disabled-text styling elsewhere.
- The article template predates the design system's link-treatment guidance.

## Expected critique

A good reviewer SHOULD surface these, from this text alone:

1. **(Severity 3) Inline body links fail 1.4.1 Use of Color and 1.4.3 contrast.**
   Links are `#5B8DEF` (~3.2:1, under 4.5:1) and distinguished by color only with
   no underline or other cue. Fix: add an underline (or equivalent non-color
   affordance) and darken the link token to meet 4.5:1. This is the headline
   defect — it harms both low-vision and color-blind readers.
2. **(Severity 2–3) Figure captions fail 1.4.3.** `#8A909B` on white at 13px is
   ~3.2:1. Darken to at least a `#6B7280`-class gray (>=4.5:1) and/or do not go
   below 14px for body-adjacent text.
3. **(Severity 2) Reading measure is too wide.** ~88–92ch at 760px exceeds the
   ~65ch comfort target, hurting return-sweep and reading speed. Constrain the
   column to a `ch`/rem-based max (e.g. `max-width: 68ch`).
4. **(Severity 2) Missing `forced-colors` support + suppressed underlines** make
   links indistinguishable in Windows High Contrast mode; add a
   `@media (forced-colors: active)` treatment and keep link underlines.
5. **(Severity 1) Reading column is not optically centered** in the desktop
   canvas (~136px dead space on the right), making the page feel unbalanced.
   Either center the column in the post-rail area or widen gutters symmetrically.
6. **(Severity 1) "About the author" `h2` is visually styled like an `h3`,**
   weakening the visual-to-semantic mapping of the outline. Give document-level
   `h2`s a consistent visual weight or demote this to its true visual rank.

## Prohibited critique

Claims a reviewer must NOT make from this text alone — Synthetic fixture only,
no rendered image exists, so do not invent measured-pixel findings:

- **Do not claim** the body text contrast fails. Body `#3A3F47` on white is
  ~10.4:1 and passes; only captions and links fail.
- Do not claim the heading outline skips a level — the authored outline
  (`h1 → h2 → h3 → h2 → h3 → h3 → h2`) is valid with one `h1`.
- Do not claim images cause layout shift — `width`/`height` are set and space is
  reserved; CLS is explicitly mitigated.
- Do not claim there is no keyboard access to the heading anchor links — they are
  in tab order and appear on `:focus-visible`.
- Do not claim the copy/success confirmation is invisible to assistive tech — it
  is announced via `aria-live="polite"`.
- Do not invent INP/LCP numbers, font file sizes, or a real Lighthouse score;
  none were measured. Performance is described structurally only.
- Do not claim the TOC active state relies on color alone — it uses weight + a
  4px border in addition to color.

## Severity expectations

Using Nielsen's 0–4 severity scale (0 = not a problem, 4 = usability catastrophe):

- Inline link color-only + contrast failure: **3** (major — blocks/penalizes a
  measurable share of readers; high priority).
- Caption contrast failure: **2–3** (minor-to-major; legibility, affects every
  figure).
- Over-wide reading measure: **2** (minor usability — slows reading, not blocking).
- Missing forced-colors / underline suppression: **2** (minor, but compounds #1).
- Optical centering imbalance: **1** (cosmetic).
- `h2`/`h3` visual-rank mismatch: **1** (cosmetic).

No issue here rises to **4**; the link defect is the one that should be fixed
before ship.

## Rubric score expectation

Scored on the 8 design-quality dimensions (target 4/5 = strong and shippable):

| Dimension | Current | Projected (after fixes) |
| --- | --- | --- |
| Attention path & hierarchy | 4 | 4 |
| Composition & spacing | 3 | 4 |
| Typography craft | 3 | 4 |
| Color/state & contrast | 2 | 4 |
| Density & rhythm | 4 | 4 |
| Interaction polish & motion | 4 | 4 |
| Context & brand fit | 4 | 4 |
| Production readiness | 3 | 4 |

**Expected current overall: ~3.4/5.** The template's reading rhythm, motion, and
state coverage are already strong; the score is dragged down by the color/contrast
failures and the over-wide measure. **Projected after the Expected-critique fixes:
~4.0/5** and shippable. A reviewer landing far from this band (e.g. calling it
1/5, or 5/5 with no notes) has likely missed the link defect or hallucinated a
measured-pixel finding the fixture does not support.
