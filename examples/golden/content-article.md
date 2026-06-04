# Golden example: Long-form editorial article optimized for readability

A compact calibration example showing a strong (4/5) web answer for a readability-first editorial layout. Use it to judge what "shippable" looks like before reaching for a 5/5 polish pass.

## Prompt

```text
We publish long-form articles (2,000-4,000 words) on our marketing blog -
think deep dives with subheads, pull quotes, code-ish callouts, and the
occasional chart. Right now the body text is cramped, the line length runs
edge to edge on desktop, and people bounce. Give me the layout and CSS for
a readable article template: the reading column, type scale, spacing, and
the in-article elements (figures, pull quotes, callouts, footnotes). It has
to work from a 320px phone up to a wide desktop, be accessible, and not
tank Core Web Vitals. React/Next.js is fine.
```

## Golden output

```md
# Readable article template

The whole design is one decision repeated: protect the **reading column**.
Everything else - figures, quotes, asides - either sits inside that column
or deliberately breaks out of it, and nothing else competes with the prose
for attention.

## Layout: a named-grid reading column

Use a 3-track CSS grid so body text lands in a ~65ch measure while full-bleed
media and wide quotes can escape to the edges. Named grid lines keep authoring
declarative - a `<figure>` opts into `full-bleed` without touching the parent.

​```css
.article {
  --measure: 65ch;          /* ideal line length for prose */
  --gutter: clamp(1rem, 5vw, 2rem);

  display: grid;
  grid-template-columns:
    [full-start] minmax(var(--gutter), 1fr)
    [wide-start] minmax(0, 8rem)
    [text-start] min(var(--measure), 100% - 2 * var(--gutter)) [text-end]
    minmax(0, 8rem) [wide-end]
    minmax(var(--gutter), 1fr) [full-end];
}
.article > *           { grid-column: text; }   /* prose default */
.article > .wide       { grid-column: wide; }    /* pull quotes, tables */
.article > .full-bleed { grid-column: full; }
​```

`min(65ch, 100% - 2 * var(--gutter))` is the load-bearing line: it caps the
measure on desktop *and* guarantees a gutter at the 320px reflow floor
(WCAG 1.4.10 Reflow), so the layout never needs a horizontal scrollbar.

## Type scale and rhythm

Body is **1.125rem (18px)** - above the 16px floor because this is reading-first.
Fluid headings use `clamp()` with a `rem` term so they still scale when the user
zooms to 200% (WCAG 1.4.4 Resize Text).

​```css
.article {
  font-size: clamp(1.0625rem, 1rem + 0.3vw, 1.1875rem);
  line-height: 1.6;                 /* generous for long reads */
  text-wrap: pretty;                /* avoid orphans in paragraphs */
}
.article h2 { font-size: clamp(1.5rem, 1.2rem + 1.5vw, 2rem);   line-height: 1.25; }
.article h3 { font-size: clamp(1.25rem, 1.1rem + 0.8vw, 1.5rem); line-height: 1.3; }

/* Vertical rhythm: space comes from the element that follows. */
.article > * + *               { margin-block-start: 1.5rem; }
.article > * + :is(h2, h3)     { margin-block-start: 2.5rem; }  /* 40px before a head */
​```

Spacing follows the 4px scale (8 / 12 / 16 / 24 / 32 / 40px). Headings get more
space *above* than below so each one reads as the top of its section, not a
floating label - a direct application of the Law of Proximity.

## In-article elements

**Pull quote** (`.wide`) breaks the measure to signal "pause here," but stays
text - never an image of text:

​```html
<blockquote class="wide pull-quote">
  <p>The reading column is the product. Everything else is chrome.</p>
</blockquote>
​```

​```css
.pull-quote {
  border-inline-start: 4px solid var(--accent);
  padding-inline-start: 1.5rem;
  font-size: 1.375rem;
  line-height: 1.35;
}
​```

**Callout** carries an icon *and* a text label so meaning never rides on color
alone (WCAG 1.4.1 Use of Color). It is an `<aside>` with `role="note"`:

​```html
<aside class="callout callout--warn" role="note">
  <span class="callout__label"><svg aria-hidden="true">...</svg> Heads up</span>
  <p>Deprecated in v4. Migrate before the next release.</p>
</aside>
​```

**Figure** reserves space to keep CLS <= 0.1 - `aspect-ratio` plus intrinsic
`width`/`height` so nothing reflows when the image decodes:

​```html
<figure class="full-bleed">
  <img src="/chart.avif" width="1600" height="900"
       alt="Bounce rate fell from 58% to 31% after the redesign"
       loading="lazy" decoding="async" style="aspect-ratio: 16 / 9">
  <figcaption>Bounce rate, before vs. after. Source: internal analytics.</figcaption>
</figure>
​```

The `alt` states the *conclusion* of the chart, not "a chart" - a non-text
alternative that carries the same information (WCAG 1.1.1 Non-text Content).

**Footnotes** are real links, not tooltips, so they work by keyboard and on
touch. The back-reference returns focus to where the reader was:

​```html
<sup><a href="#fn-1" id="ref-1">1</a></sup>
...
<li id="fn-1">Source. <a href="#ref-1" aria-label="Back to reference 1">return</a></li>
​```

## Accessibility and states

- **Heading outline:** one `<h1>` (the title), then `<h2>`/`<h3>` with no
  skipped levels (WCAG 1.3.1) - a navigable structure for assistive-tech users.
- **Landmarks:** `<header>`, `<nav aria-label="On this page">`, `<main>`,
  `<article>`, `<footer>`. The table-of-contents nav uses
  `aria-current="location"` on the active section.
- **Focus:** every in-article link shows a 2px `:focus-visible` ring with a
  2px offset, contrast >= 3:1 against both the text and the page (WCAG 1.4.11
  Non-text Contrast); the sticky TOC never obscures the focused link (2.4.11).
- **Contrast:** body text is `#1a1a1a` on `#ffffff` (about 16:1), captions and
  metadata are `#595959` (about 7:1) - both clear AA (1.4.3 Contrast Minimum),
  captions still pass even though they read as "secondary."
- **Text spacing:** the layout survives the WCAG 1.4.12 overrides
  (line-height 1.5x, letter-spacing 0.12em, word-spacing 0.16em, paragraph
  2em) without clipping, because heights are content-driven, never fixed.
- **Targets:** TOC links and footnote markers get `min-height: 24px` with
  padding (WCAG 2.5.8 Target Size Minimum); inline prose links are exempt but
  still get a comfortable hit area via line-height.

​```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }   /* skip smooth-scroll on TOC jumps */
}
@media (forced-colors: active) {
  .callout { border: 1px solid CanvasText; }  /* keep edges in forced-colors */
}
​```

## Performance (Core Web Vitals)

- **LCP <= 2.5s:** the article's first heading or hero image is the LCP element.
  `preload` the above-the-fold heading font; serve body font with
  `font-display: swap` and a tuned `size-adjust` fallback so the swap doesn't
  shift layout (protects CLS).
- **CLS <= 0.1:** every `<img>`, `<figure>`, and embed reserves space via
  `aspect-ratio` / explicit dimensions; the TOC is sticky, not injected late.
- **INP <= 200ms:** the only interactivity is the TOC and footnote jumps -
  plain anchor navigation, no JS handler on the critical path. A reading-progress
  bar, if added, updates via `requestAnimationFrame` off a passive scroll
  listener, never synchronous layout reads in the handler.

​```jsx
// Next.js: ship the article as a Server Component - zero client JS for prose.
export default function Article({ source }) {
  return (
    <main>
      <article className="article">
        <MDXRemote source={source} components={{ Callout, Figure, PullQuote }} />
      </article>
    </main>
  );
}
​```

## Build order

1. Grid + measure + type scale (the readability core - ship this first).
2. Figures and footnotes with reserved space (locks in CLS).
3. Sticky TOC with `aria-current` + reduced-motion guard.
4. Callouts / pull quotes as MDX components.
```

## Design-quality notes

This response earns a strong, shippable mark across the dimensions that matter most for an editorial template.

**Quality target: 4/5**

- **Attention path & hierarchy (4/5):** the whole layout is organized around a
  single protected reading column, and the heading-spacing rule (more space
  above a head than below) reinforces section starts via the Law of Proximity.
  One clear job, one clear focus.
- **Typography craft (5/5):** 18px reading-first body, fluid `clamp()` heads
  with a `rem` term that survives 200% zoom, a ~65ch measure enforced by the
  `min()` trick, `text-wrap: pretty`, and a met 1.4.12 text-spacing override
  budget - all named and accounted for.
- **Composition & spacing (4/5):** named-grid breakout lanes (`text` / `wide` /
  `full`) are declarative and authorable; spacing rides the 4px scale. It stops
  short of 5/5 because the wide/full lane widths are fixed `8rem` rather than
  tied to a container query.
- **Color/state & contrast (4/5):** concrete contrast ratios for body *and*
  secondary text, color-independent callouts (icon + label, WCAG 1.4.1),
  `:focus-visible` rings with named 1.4.11 contrast, and forced-colors support.
- **Production readiness (4/5):** Server-Component delivery, CWV budgets tied to
  specific techniques (font preload + `size-adjust`, reserved media space,
  rAF-throttled scroll), and a sensible build order. Reads like something an
  engineer can ship Monday.

**What would push it to 5/5:** (1) make the breakout lanes container-query
driven so embedded contexts (a narrow sidebar render) reflow correctly rather
than relying on viewport width; (2) specify the exact `size-adjust` /
`ascent-override` numbers for the named fallback font instead of describing the
technique; (3) add the loading, empty (no figures), and error states for any
async embed - e.g., a chart that fails to load - so every in-article element has
a defined failure mode, not just the happy path.
