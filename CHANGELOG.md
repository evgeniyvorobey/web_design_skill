# Changelog

All notable changes to `web-design-skill` are documented here. This project follows [Semantic Versioning](https://semver.org/) adapted for a prompt-and-documentation skill (see [`docs/versioning.md`](docs/versioning.md)).

## [1.5.0] - 2026-10-22

Lessons from shipping a one-page social-campaign landing (static HTML/CSS/JS, Chromium + WebKit QA). Automated checks on the fixed breakpoint ladder passed while the client still found bugs between the rungs, on real iOS Safari, and in the build. This release closes those gaps.

### Added — Rendered QA between the ladder rungs
- `docs/rendered-output-qa.md`: **Width sweep** (10–20px steps, geometry only) and **Height sweep** (667/720/800 plus landscape phone, h1 and primary CTA in the first viewport); **single-line labels** and **edge alignment** (offset-shadow blocks end inside the column by exactly the offset); lazy media checked after scrolling, in WebKit; scroll `Paint` count from a Chromium trace plus a mandatory real iOS Safari device check; QA runs on the **Built output**, not the source.
- `scripts/rendered_qa.py`: geometry runner for the passes above in Chromium and WebKit. Emits `checks` in the `rendered-output-qa/v1` checkResult shape; exit code 1 on a failure. Calibrated on a real build: it caught a wrapped nav label, a ragged column edge, lazy logos that never loaded, and a background repainting on every scroll frame, with no false positives after tuning.
- `docs/guardrails.md` §16 *Use brand marks from the source file*: extract the vector, verify by pixel overlay, no silent redraws.
- `docs/domain-packs/marketing-landing.md` *Public-Interest And Social Campaigns*: conversion as understanding and recall; facts not offers (no sale vocabulary such as "−50%" stickers); sources at the claim; partner logo grid; imagery consent; social-advertising law routed to counsel. Pointer added to Mode G in `skill/modes.md`.
- `docs/patterns-catalog.md` *Full-page preloader / splash*: avoid on static pages, state the LCP cost before building one.

### Changed
- `docs/motion-and-animation.md`: one code path per engine for scroll-driven motion; `overflow: clip` instead of `hidden` so `view()` keeps following the page; *Paint once, move the layer*; *Pause ambient loops during scroll*; device verification; 21st.dev added to the build resources with a port-to-CSS rule for non-React stacks.
- `docs/quality-bars.md`: lazy media needs dimensions before load (WebKit skips zero-size lazy images); variable-font subsetting by axes and scripts.
- `docs/patterns-catalog.md` *Top horizontal nav*: inline nav only from the width where every label fits on one line; red flag for mid-width wrapping.
- `docs/design-quality.md` dimension 2: shared column edges with offset-shadow compensation on the shadowed element.
- `docs/domain-packs/marketing-landing.md`: stat captions match the source definition, paired numbers share base and period; static logo grid up to about a dozen logos; concrete consent-mode checklist; static-host launch checklist (`404.html`, staging `noindex`, absolute OG URLs at build time).
- `docs/weaknesses.md` #11: clean-build prevention check for code handoffs.
- `scripts/validate_repo.py`: requires the new rendered-QA and motion patterns and `scripts/rendered_qa.py`.
- `README.md`: lists the geometry runner and states the browser/network scope it uses when invoked.

## [1.4.0] - 2026-06-05

### Added — Equal-height peer tiles + internal cross-card alignment
- Closed a real gap: the skill had no rule that **peer cards/tiles/columns in a row should share a height *and* align their internal content across siblings**, so generated layouts (and reviews of them) let each card size to its own content — producing ragged bottom edges, misaligned footer CTAs, and titles/descriptions/buttons that start at different heights when one title wraps to more lines. The fix lands the rule across both the generation and the review/QA surfaces so it is produced *and* caught.
- **Generation rule** — `docs/patterns-catalog.md` §3 *Card collection*: expanded the mechanism, failure mode, and red-flag list. Equal card height via direct grid/flex children + default `align-items: stretch`; **internal alignment** so title, body, and footer/CTA each sit on a shared baseline across cards via **subgrid** (shared row tracks: `grid-template-rows: subgrid; grid-row: span 3`, Baseline since 2023), with `flex-direction: column` + `margin-top: auto` or per-section `min-height` named as the fallback where subgrid is out of the browser/engine scope (it pins only the footer, not the title/body boundary); single-card emphasis carried via color/border/badge/equal-amount scale, never by ragged content-driven height.
- **Quality bar** — `docs/quality-bars.md` §*Spacing, grid and breakpoints*: new "Equal-height peer tiles + internal alignment" bar (height via stretch; internal title/body/CTA baselines via subgrid) so workflow step 9 checks it as a concrete floor.
- **Heuristic grounding** — `docs/heuristics.md` Gestalt *Continuity*: peer-tile height alignment is now named, with a quotable red flag, so Mode D findings can cite it (Gestalt similarity + continuity) instead of treating it as taste.
- **Design-quality lens** — `docs/design-quality.md` dimension 2 *Composition & spacing*: equal-height peer tiles added to the alignment mechanisms.
- **Calibration pair** — `examples/anti-patterns.md` #7 *Ragged-height card row*: Bad/Good pair with the concrete CSS mechanism.

### Changed — Review now catches ragged card heights and internal misalignment
- `docs/heuristics.md` Gestalt *Continuity* and `docs/design-quality.md` dimension 2: extended to name internal cross-card alignment (title/body/CTA on shared baselines via subgrid), with a quotable red flag, so Mode D can cite it.
- `docs/self-review.md`: universal design-quality prompt and Mode D prompt now cover both shared height *and* internal-row alignment (a title wrapping to a different number of lines must not shove that card's body/CTA out of line), with the D2 description-only guard that heights/alignment are not asserted unless stated.
- `docs/rendered-output-qa.md`: layout check is now "uneven peer-tile heights and internal misalignment" (titles/descriptions/CTAs not on shared baselines), a real `observed` finding (not to be skipped).
- `docs/weaknesses.md` #9 *Weak design-quality calibration*: failure signal and prevention check now cover internal-row misalignment and the subgrid fix.
- `docs/evals.md`: conditional content-validation checks for Mode A (generation addresses equal-height *and* internal cross-card alignment) and Mode D (a D1 review surfaces ragged heights and misaligned internal rows; a D2 review does not assert them unless stated).
- `examples/anti-patterns.md` #7 *Ragged-height card row*: Good rewrite now uses subgrid for internal title/body/CTA alignment, with the flex/`min-height` fallback named.

## [1.3.0] - 2026-06-05

### Added — Runbook-level design-tool profiles & the reverse token-write path
- New `docs/design-tool-runbooks.md`: the concrete, executable companion to the conceptual `design-tool-handoff.md`. Where the handoff doc holds the *contract* (neutral extract schema, DTCG 2025.10 output, Dev-Mode handoff payload, thin profiles), the runbooks doc holds **exact, ordered call sequences** a host model can run step by step — every step names the real tool/endpoint, its inputs, what it returns, and the normalize action. Grounded in fresh verified research against official docs (developers.figma.com Plugin + REST API, docs.pencil.dev, Penpot/Sketch token docs) plus the live MCP tool schemas in-session.
- **READ runbooks (extract → neutral schema):** Figma (`whoami` → `get_metadata` → `get_variable_defs` → `get_design_context` → `get_screenshot`/`get_libraries`, or the Enterprise REST path `GET /v1/files/:key` + `GET …/variables/local` with `file_variables:read`) and Pencil (`get_editor_state(include_schema:true)` → `get_variables` → `batch_get` → `snapshot_layout`), each ending at a populated handoff-§1 extract.
- **REVERSE runbooks (DTCG `.tokens.json` → native variables):** Figma via **two paths** — Path A `use_figma` (Plugin API `figma.variables.*`, verified **not** Enterprise-gated, `/figma-use` skill mandatory) and Path B REST `POST /v1/files/:key/variables` (`file_variables:write`, Enterprise, atomic `tempIdToRealId` payload) — and Pencil via `set_variables` (hex-string colors, aliases pre-resolved, themed arrays) then `batch_design`.
- **Exact DTCG↔native mapping tables:** DTCG `color` object ↔ Figma RGBA `{r,g,b,a}` 0–1 ↔ Pencil hex; `dimension`/`number`/`fontWeight`/`fontFamily`/`typography` (decomposed); aliases `{group.token}` ↔ Figma `VARIABLE_ALIAS` ↔ Pencil resolved-to-concrete; DTCG theme axes ↔ Figma collection modes ↔ Pencil themed arrays; Figma scopes + Code Syntax (`var(--…)`). Plus a worked round-trip from `examples/design-tool/tokens.tokens.json`.
- **Runbook-lite** profiles for Penpot (Tokens-Studio-flavored DTCG export — adapter normalizes values + resolves `{reference}` aliases; call surface connector-dependent) and Sketch (Amazon Style Dictionary export, not W3C DTCG — adapter does a format conversion; write surface unverified).
- **Caveats covered:** Figma Enterprise REST write-gating vs. the ungated Plugin path, idempotency (match by name / collection / `codeSyntax.WEB`; `UPDATE` over `CREATE`; Pencil `replace:false` merge), alias resolution order (topological: targets before referrers, no cycles), and the honest boundary — the skill sequences/reasons, the host's MCP connector executes the I/O. The runbooks emit only the portable `{group.token}` alias and never `$ref`/`$root`/`$extends` (they would not round-trip).

### Changed
- `docs/design-tool-handoff.md` §4: each vendor profile (Figma, Pencil, Penpot, Sketch) now points at its runbook, and §5 points the Mode C/F reverse-write path at it; the conceptual contract is otherwise intact. Penpot/Sketch profile text corrected to the verified token-export reality (Penpot = Tokens-Studio-flavored, needs normalization; Sketch = Style Dictionary format, needs conversion).
- Wired the runbooks doc into `SKILL.md` (load list), `skill/skill.md`, `skill/metadata.yaml` (`design_tool_interop.runbooks`), `skill/modes.md` (Mode D read + Mode F handoff), and `docs/self-review.md` (design-tool gate now covers the READ/REVERSE call sequences, idempotency, and the boundary).
- Enforced by a new `validate_runbooks_layer()` in `scripts/validate_repo.py` (requires the real call names — `get_variable_defs`, `get_design_context`, `get_editor_state`, `set_variables`, `batch_design`, `POST /v1/files`, `file_variables:write` — plus the reverse mapping, idempotency, alias ordering, and honest boundary, with reference-file wiring); `docs/design-tool-runbooks.md` added to `REQUIRED_FILES`. No existing check or depth threshold was loosened.

### Fixed — senior-review pass
- **DTCG `$ref`/`$root`/`$extends` rationale corrected.** `docs/design-tool-handoff.md` previously called these "draft-only" features of the moving `/TR/drafts/` preview. Re-verified against the stable spec (designtokens.org/TR/2025.10/format/ §6.2/§6.4/§6.6): they are **normative in 2025.10** (`$ref` is MUST-support). The skill still does not emit them — now on the correct **portability** grounds (uneven round-trip support across design tools, Tokens Studio, and Style Dictionary), aligning handoff.md with the framing already in `design-tool-runbooks.md`. The recommended portable form remains the curly-brace `{group.token}` alias.
- **Validator hardened (no loosening).** `validate_runbooks_layer()` now adds rule-binding assertions on top of the keyword presence checks — RGBA stated as 0–1 (not 0–255), alias targets before referrers, Pencil colors as hex — plus a minimum numbered-step count and minimum length, so a keyword-stuffed stub or a flipped correctness rule no longer passes.
- **README repository map** now lists the design-tool interop (`design-tool-handoff.md`, `design-tool-runbooks.md`) and motion (`motion-and-animation.md`) layers, which the "What's inside" section had omitted.
- Dropped a stray empty `()` after the no-input `whoami` step in the Figma READ runbook.

## [1.2.0] - 2026-06-05

### Added — Design-tool interop & handoff layer
- New `docs/design-tool-handoff.md`: a durable, **tool-agnostic** interop layer so the skill can consume designs from any design tool and emit handoff the tool can read back — without binding to a vendor. Anchored on the **W3C Design Tokens (DTCG) format, version 2025.10** (its first stable release, 28 Oct 2025), grounded in fresh verified research.
- **Input side:** a neutral "design extract" schema (nodes, layout, text, fills, token refs, components/states) that any tool's MCP output maps onto. A structured extract is a **higher-confidence Mode D (D1) input than a screenshot** — the review can assert layer/token facts (sizes, spacing, token names, heading outline) while holding purely visual properties provisional.
- **Output side:** DTCG 2025.10 tokens (the modern object `color`/`dimension` shapes, aliases `{group.token}`, the `typography` composite, theming) plus a Dev-Mode-style handoff payload (tokens, component/state map, measurements, a11y annotations, responsive notes, motion specs, edge cases). Downstream pipeline `DTCG → Style Dictionary → CSS custom properties / Tailwind` with the `var(--…)` convention. A concrete example lives in `examples/design-tool/tokens.tokens.json`.
- **Thin vendor profiles:** Figma (Variables REST/Dev Mode/MCP, `resolvedType` → `$type` mapping, Enterprise-gating caveat), Pencil/`.pen` (opaque-via-MCP, format v2.13 node/variable model), Penpot (DTCG-native, self-host), Sketch, Framer (published-site input); Builder.io/Visual Copilot as a design-to-code step; Adobe XD noted as legacy/discontinued.
- **Honest boundary:** the skill reasons (review/spec/handoff/tokens); the **host's MCP connector** does the file/API I/O — the skill never opens `.fig`/`.pen` itself. Wired into Mode D (D1 input), Mode F (handoff target), SKILL.md, skill/skill.md, metadata, and self-review; enforced by a new `validate_design_tool_layer()` (doc patterns + valid DTCG example + reference wiring) and added to `REQUIRED_FILES`.

## [1.1.0] - 2026-06-05

### Added — Motion & animation layer
- New `docs/motion-and-animation.md`: a first-class motion layer so the skill proposes animation **only where it earns its place** (feedback, orientation, state change, status) and never on high-frequency/keyboard actions, dense tables, or forms.
- Grounded in fresh web research (2024–2025), with verified facts: an easing palette of exact `cubic-bezier()` tokens (corrected Material 3 Standard vs Emphasized; IBM Carbon productive/expressive), a duration scale, spring-vs-tween guidance, and the CSS → WAAPI → View Transitions → CSS scroll-driven → library build ladder with **current Baseline status** per API (View Transitions same-document Baseline Oct 2025; cross-document and scroll-driven animations *not* Baseline → progressive enhancement; Web Animations API + `linear()` Baseline; GSAP now fully free incl. former Club plugins).
- Performance rules (animate `transform`/`opacity` only; protect INP/CLS) and accessibility rules (`prefers-reduced-motion` with a *reduced* alternative, not just off; WCAG 2.2.2/2.3.1/2.3.3), plus a tiered wow-effect resource list (learn / build / inspire: animations.dev, Josh Comeau, web.dev; Motion, hover.dev, Lottie, Rive; Codrops, Awwwards, Godly).
- A "Motion plan" output shape for Modes A/C/F/G and a Mode D motion lens that flags both missing functional motion and over-animation.
- Wired into `SKILL.md`, `skill/skill.md`, `skill/metadata.yaml`, `quality-bars.md`, `design-quality.md`, `self-review.md`, `workflow.md`, and `inspiration-sources.md`; enforced by a new `validate_motion_layer()` check and added to `REQUIRED_FILES`.

### Fixed
- Workflow step-numbering desync: `docs/workflow.md` is aligned to the canonical 11-step scheme (a dedicated "Step 3: Determine scope" was added), and the cross-references in `docs/self-review.md` (now "Step 10") and `skill/skill.md` (now "workflow Step 8") were corrected.

## [1.0.0] - 2026-06-05

### Iteration 2 — production-ready web skill

The web domain layer is fully authored. Every mode, foundation, calibration fixture, and the Mode D review engine now produce production-grade web guidance. Content-depth validation (`WDS_STRICT`) is on by default and passes.

**Web foundations (authored fresh):**
- `quality-bars` — 16px/rem type baseline, fluid `clamp()`, ~65ch measure, the 4px spacing scale, the breakpoint ladder (320 → 1920+), WCAG 2.2 AA success criteria (1.4.10 reflow@320px, 1.4.4 resize 200%, 1.4.12 text spacing, 2.5.8/2.5.5 target size, 2.4.11 focus, 1.4.1 use of color, 1.4.11 non-text contrast, forced-colors), and Core Web Vitals budgets (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1).
- `sources` (re-tiered for the open-web stack), `inspiration-sources` (rebalanced for web galleries), `context-defaults`, `principles`, `guardrails`, `design-quality`, `heuristics`, and the `patterns-catalog` (navigation, overlays, data tables first-class, forms/auth, feedback, states, search, responsive divergence).

**Modes & engine:**
- Seven web modes live (page concept, web flow, responsive UI spec, page review, type/spacing/grid, rationale/handoff, and the new **marketing landing / CRO** mode with the marketing-vs-web-app split).
- The Mode D review engine (causal Finding chain, Nielsen 0–4 severity, flat-median current→projected score, gated Bold move) is preserved verbatim and re-pointed to web; `docs/proposals/review-mode-upgrade.md` ported to a web artifact.
- New universal + Mode D lenses wired in: keyboard operability, Core Web Vitals, responsive-across-breakpoints, SEO & semantics, and forced-colors.

**Calibration corpus:** 7 golden examples, 5 web domain packs, 12 synthetic case studies, 6 visual-review fixtures, 7 worked examples, web anti-patterns, a benchmark report, the rubric before/after, and 5 calibrated eval fixtures (scores {1..5}, medians matching expected scores, monotonic, web caps demonstrated at 1–2 and a true 5/5 at the top).

**Production hardening:** `rendered-output-qa` rewritten Playwright-first with a web `rendered-output-qa/v1` schema + sample; README, CHANGELOG, and packaging copy rewritten for web; validator content-depth checks re-pointed to web and defaulted on; release validation green.

### Inversion ledger — the 9 mobile→web traps consciously flipped (not renamed)

| # | Before (mobile sign) | After (web) |
|---|----------------------|-------------|
| 1 | `Platform scope: iOS\|Android` (one overloaded axis) | Split into `Responsive/breakpoint scope:` + `Browser/engine scope:` in every template, mode, and metadata |
| 2 | Hover / right-click / keyboard-first treated as red flags | Required on web; the failure is **ignoring** hover/focus/keyboard operability |
| 3 | "one-screen-at-a-time" heuristic | Web is multi-pane / multi-tab / long-scroll |
| 4 | SaaS "avoid desktop density / table shrinkage" | **Exploit** desktop density: real tables, multi-pane, hover actions, keyboard shortcuts |
| 5 | "platform-flattening cap (3/5)" | "responsive-flattening cap" — the 3/5 cap lives in `design-quality-rubric.md` + the `heuristics.md` severity crosswalk (severe no-reflow form is P1 → 2/5); the weakness is named in `weaknesses.md` and the literal pattern is enforced in `validate_repo.py` (`WEAKNESS_REQUIRED_PATTERNS`) |
| 6 | Touch target 44pt / 48dp + thumb-zone | WCAG 2.5.8 (24px) / 2.5.5 (44px AAA) + pointer-aware `@media (pointer: coarse\|fine)`; Fitts via cursor travel + screen edges/corners; thumb-zone deleted |
| 7 | "keyboard" = on-screen keyboard TYPE | Two web meanings kept separate: input *type* (inputmode/type) vs *operability* (tab order, focus-visible, focus management, trap+restore, skip links); operability dominates |
| 8 | "tooling last" (sources Tier 5) | Tooling is **first-class evidence** (Lighthouse/PSI/CrUX, axe-core/WAVE, Playwright, BrowserStack), re-tiered up |
| 9 | "offline as a default state" | PWA / service-worker **conditional**, paired with 404 / 500 / session-expired states |

A repo-wide grep for leaked mobile-sign tokens (`thumb`, `FAB`, `safe-area`, `44pt`, `48dp`, `one screen at a time`, `tooling…last`, `offline…default`) returns only intentional contrastive mentions (the flips above and lines like "offline is conditional, **not** a default").

## [0.1.0] - 2026-06-04

### Iteration 1 — mechanical transfer (chassis + scaffold)

Initial transfer of the domain-agnostic chassis and methodology from the upstream mobile design skill into a standalone website-design skill: eval/judge runner, oracle, CI workflows, release validation, version bumper, installer, the Claude Code wrapper, the judge agent, and `agents/openai.yaml`. The mode contract was re-framed for web and the web domain layer was scaffolded as stubs, authored in v1.0.0.
