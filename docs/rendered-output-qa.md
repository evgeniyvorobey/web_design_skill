# Rendered Output QA

This is an **optional workflow** that runs only after a design exists as a rendered artifact — an HTML page, a deployed URL, a prototype, a screenshot, or a recording. It does not block normal design generation: when no artifact exists, list rendered QA as a next action and move on.

Where the design modes reason about a described or proposed design, rendered-output QA inspects what the browser actually painted. On web, the primary tool is **Playwright** (cross-browser, scriptable, captures DOM + screenshots + the accessibility tree), backed by **axe-core** for automated accessibility and Lighthouse for performance. Tooling output here is first-class evidence about a specific build (see [`sources.md`](sources.md)) — but a clean automated run is a recommendation to verify, not a compliance verdict.

Emit a structured report conforming to the `rendered-output-qa/v1` schema in [`../examples/rendered-output-qa/report-schema.json`](../examples/rendered-output-qa/report-schema.json); a filled example is in [`../examples/rendered-output-qa/sample-report.json`](../examples/rendered-output-qa/sample-report.json).

## Artifact classification

Classify the artifact before inspecting: deployed URL, local HTML/dev server, prototype, screenshot, or recording — plus the responsive/breakpoint and browser/engine scope it represents. A live URL or dev server supports the full Playwright sweep; a single screenshot supports only static layout and contrast observations, with everything else marked unverified.

## Layout, overlap and reflow (320px)

Drive a real browser across the **breakpoint ladder** (320 / 360 / 768 / 1024 / 1280 / 1440 / 1920) and capture issues that only appear once rendered:

- element **overlap** and z-index collisions
- **clipping** of content by fixed/sticky containers
- **text overflow** / truncation and broken wrapping
- horizontal scroll where there should be none; sticky-header overlap of focused content
- the **320px reflow** (WCAG 1.4.10): no two-dimensional scrolling for vertical content, plus a usable 200% zoom
- SSR/hydration mismatches that shift layout after load (a CLS source)

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
