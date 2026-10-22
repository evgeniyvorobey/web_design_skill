# Rendered Output QA

This is an **optional workflow** that runs only after a design exists as a rendered artifact — an HTML page, a deployed URL, a prototype, a screenshot, or a recording. It does not block normal design generation: when no artifact exists, list rendered QA as a next action and move on.

Where the design modes reason about a described or proposed design, rendered-output QA inspects what the browser actually painted. On web, the primary tool is **Playwright** (cross-browser, scriptable, captures DOM + screenshots + the accessibility tree), backed by **axe-core** for automated accessibility and Lighthouse for performance. Tooling output here is first-class evidence about a specific build (see [`sources.md`](sources.md)) — but a clean automated run is a recommendation to verify, not a compliance verdict.

Emit a structured report conforming to the `rendered-output-qa/v1` schema in [`../examples/rendered-output-qa/report-schema.json`](../examples/rendered-output-qa/report-schema.json); a filled example is in [`../examples/rendered-output-qa/sample-report.json`](../examples/rendered-output-qa/sample-report.json).

## Artifact classification

Classify the artifact before inspecting: deployed URL, local HTML/dev server, prototype, screenshot, or recording — plus the responsive/breakpoint and browser/engine scope it represents. A live URL or dev server supports the full Playwright sweep; a single screenshot supports only static layout and contrast observations, with everything else marked unverified.

## Layout, overlap and reflow (320px)

Drive a real browser across the **breakpoint ladder** (320 / 360 / 768 / 1024 / 1280 / 1440 / 1920) and capture issues that only appear once rendered. The ladder is where screenshots go; layout breaks live *between* its rungs, so add two geometry-only passes:

- **Width sweep** — step the width by 10–20px from 320 to 1920 and record geometry only (no screenshots). A nav label that wraps at 1180px passes every ladder rung and still ships broken.
- **Height sweep** — pair the widths with heights 667, 720 and 800, plus a landscape phone (844×390). The `h1` and the primary CTA land inside the first viewport at every pair; a 1280×720 laptop is a common miss when every check runs at 900px tall.

Capture at every width:

- element **overlap** and z-index collisions
- **clipping** of content by fixed/sticky containers
- **text overflow** / truncation and broken wrapping
- horizontal scroll where there should be none; sticky-header overlap of focused content
- **uneven peer-tile heights and internal misalignment**: cards, tiles, or columns that are peers in one row rendering at mismatched heights with ragged bottom edges, *or* whose internal rows don't line up across siblings — titles, descriptions, and CTAs starting at different heights because one title wrapped to more lines — instead of sharing both height and row tracks (a Gestalt similarity/continuity break — usually cosmetic-to-minor, but a real `observed` finding, not to be skipped)
- **single-line labels**: nav links, buttons, tags and badges render on one line (`el.getClientRects().length === 1` for inline boxes, or a height within one line box). A label that wraps to two lines at a mid width is an `observed` finding.
- **edge alignment**: every block with a background, border or shadow ends on the content column edge. A block with an offset (hard) shadow ends inside the column by exactly its shadow offset; a plain block stops short of the edge only when it is meant to. Ragged right edges at phone widths usually come from one compensation rule applied to every block.
- the **320px reflow** (WCAG 1.4.10): no two-dimensional scrolling for vertical content, plus a usable 200% zoom
- SSR/hydration mismatches that shift layout after load (a CLS source)

## Lazy media and engine differences

Scroll each section into view, wait for the network to settle, then assert every `<img>` has `complete && naturalWidth > 0`. A check that runs before the scroll passes on images that never load. Run it in WebKit as well as Chromium: WebKit leaves a `loading="lazy"` image unloaded when its box is zero-sized before load, so the image never counts as visible (the fix is in [`quality-bars.md`](quality-bars.md) under Performance).

## Motion smoothness and the device check

Headless engines report no scroll jank, so a green run says nothing about smoothness. Record a Chromium trace (`devtools.timeline` category) during a scripted scroll and count `Paint` events: a large layer that repaints on every scroll frame is a finding (the usual cause is a gradient or filter driven by a custom property; see [`motion-and-animation.md`](motion-and-animation.md) §6). Then confirm every scroll-linked animation on a real iOS Safari device; without a device, mark smoothness `unverified`.

## Built output

Run the sweep against the files that ship (minified, comment-stripped, with production URLs), not against the source tree. Build steps break things the source never shows: a minifier, a stripped attribute, a placeholder domain left in `og:image`.

## Targets and pointer

Measure rendered interactive controls against the **target size** bars: 24px minimum (WCAG 2.5.8), 44px for primary/coarse-pointer (2.5.5). Flag undersized or overlapping targets and insufficient spacing. Sample text and UI-component contrast against the rendered background and flag any **contrast risk** below 4.5:1 (text) or 3:1 (non-text) — as a risk to verify, not a verdict.

## State coverage

Render and capture each state the artifact exposes: default, hover, focus-visible, active, loading, empty, error, success, disabled, plus web system states (404, 500, offline, session-expired) where reachable. Mark any state that could not be triggered as unverified rather than assuming it works.

## Accessibility behavior (keyboard, focus, reduced motion)

- Run **axe-core** and report violations (rule, impact, nodes).
- Capture the **focus order** by tabbing through the page; flag focus lost on route/overlay change, missing visible focus, focus not restored after a dialog closes, and keyboard traps.
- Render under `prefers-reduced-motion: reduce` and flag animations, parallax, or auto-advancing carousels that still run.
- Render under **forced-colors** (`forced-colors: active`) and `prefers-color-scheme: dark`; flag disappearing outlines, shadow-only state, and broken contrast.

## Performance (Core Web Vitals)

Capture Lighthouse / Core Web Vitals hints: the LCP element and timing, CLS sources (unsized media, layout-shifting fonts), and long tasks affecting INP. Budget LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1; flag a heavy LCP image, render-blocking webfonts, or layout-shifting media.

## Severity caps and evidence labels

Label every finding with an evidence tier — `observed` (seen in a render), `measured` (a tool number), `inferred`, or `user_supplied` — and a severity. A confirmed rendered overlap, clipping, overflow, failed 320px reflow, or focus-order break can cap an otherwise strong written design until fixed; record the cap and feed it back into the Mode D score. Never assert a visual property as `measured` when it was only `inferred` from a description.

## Playwright workflow

[`../scripts/rendered_qa.py`](../scripts/rendered_qa.py) runs the geometry passes from this document in Chromium and WebKit: the width sweep, the height sweep for the first viewport, single-line labels, edge alignment, horizontal overflow, lazy media after scroll, and the scroll `Paint` count. It writes JSON findings and exits non-zero on a failure. Screenshots, axe-core and the focus-order walk stay with the ladder pass below.

```bash
uv run --with playwright python3 scripts/rendered_qa.py dist/site \
  --cta ".hero .btn" --edges "main section .card, main section figure"
```

```js
// Resize across the ladder, screenshot, run axe, capture focus order, emulate media.
for (const width of [320, 360, 768, 1024, 1280, 1440, 1920]) {
  await page.setViewportSize({ width, height: 900 });
  await page.screenshot({ path: `shot-${width}.png`, fullPage: true });
  // overlap / clipping / text overflow via bounding boxes
  // const results = await new AxeBuilder({ page }).analyze();  // axe-core
  // tab through and record document.activeElement for the focus order
}
// page.emulateMedia({ forcedColors: 'active' }); dark; reducedMotion: 'reduce'
```

Run the same sweep across the engines in the browser/engine scope (Chromium, WebKit, Gecko). Confirmed issues become evidence: a Mode D review backed by a rendered artifact can assert visual properties a text-only review cannot.
