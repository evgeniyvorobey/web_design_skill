# Changelog

All notable changes to `web-design-skill` are documented here. This project follows [Semantic Versioning](https://semver.org/) adapted for a prompt-and-documentation skill (see [`docs/versioning.md`](docs/versioning.md)).

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
| 5 | "platform-flattening cap (3/5)" | "responsive-flattening cap" (no behavior across breakpoints, hover/focus ignored, no 320px reflow) — in `weaknesses.md` + `validate_repo.py` |
| 6 | Touch target 44pt / 48dp + thumb-zone | WCAG 2.5.8 (24px) / 2.5.5 (44px AAA) + pointer-aware `@media (pointer: coarse\|fine)`; Fitts via cursor travel + screen edges/corners; thumb-zone deleted |
| 7 | "keyboard" = on-screen keyboard TYPE | Two web meanings kept separate: input *type* (inputmode/type) vs *operability* (tab order, focus-visible, focus management, trap+restore, skip links); operability dominates |
| 8 | "tooling last" (sources Tier 5) | Tooling is **first-class evidence** (Lighthouse/PSI/CrUX, axe-core/WAVE, Playwright, BrowserStack), re-tiered up |
| 9 | "offline as a default state" | PWA / service-worker **conditional**, paired with 404 / 500 / session-expired states |

A repo-wide grep for leaked mobile-sign tokens (`thumb`, `FAB`, `safe-area`, `44pt`, `48dp`, `one screen at a time`, `tooling…last`, `offline…default`) returns only intentional contrastive mentions (the flips above and lines like "offline is conditional, **not** a default").

## [0.1.0] - 2026-06-04

### Iteration 1 — mechanical transfer (chassis + scaffold)

Initial transfer of the domain-agnostic chassis and methodology from the upstream mobile design skill into a standalone website-design skill: eval/judge runner, oracle, CI workflows, release validation, version bumper, installer, the Claude Code wrapper, the judge agent, and `agents/openai.yaml`. The mode contract was re-framed for web and the web domain layer was scaffolded as stubs, authored in v1.0.0.
