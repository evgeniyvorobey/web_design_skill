<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo-light.svg" alt="Website Design Skill" width="640">
  </picture>
</p>

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-0.1.0-blue">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="status" src="https://img.shields.io/badge/status-iteration--1--transfer-orange">
</p>

# Website Design Skill

A reusable AI skill that helps generate, review, structure, and justify **website** UI/UX design decisions for responsive web (desktop, tablet, mobile-web), marketing/landing pages, and web apps.

Works as a Claude Code skill (`/web-design-skill`), as a Codex / OpenAI skill, and as a system prompt for the Claude API or any LLM integration.

Current version: **0.1.0** — see [`CHANGELOG.md`](CHANGELOG.md).

> **⚠️ Iteration 1 — transfer skeleton (v0.1.0).**
> This repository is a **hybrid clone** of [`mobile-design-skill`](../mobile-design-skill): it carries that skill's domain-agnostic chassis and methodology verbatim, and re-frames the contract for the web. The **web domain layer is currently STUBBED** — quality bars, sources, patterns, heuristics, the calibration corpus, and the Mode G (marketing/CRO) content are placeholders marked `TODO(iteration-2)`. The skill installs and classifies requests into one of 7 modes, but does **not yet give production-grade web advice**. Iteration 2 authors the web content; see [`ITERATION_2_HANDOFF.md`](ITERATION_2_HANDOFF.md).

## What this skill does

It enforces a practical framework for web design decisions, built for product work rather than decorative advice. It carries from the mobile skill:

- **Six web-reframed modes + a 7th marketing/CRO mode** — every request is classified into exactly one: web page concept, web user flow, responsive UI spec, page review, type/spacing/grid system, handoff rationale, or marketing landing page (conversion/CRO).
- **Two scope axes** — `Responsive/breakpoint scope:` and `Browser/engine scope:` (replacing the mobile `Platform scope: iOS/Android`).
- **The Mode D review engine** — causal Findings (observation → violated principle → user consequence → change → predicted effect + confidence → Nielsen 0–4 severity → score moves), before/after design-quality score, and a gated Bold move.
- **A 1–5 design-quality rubric** with caps and median scoring, a weakness preflight, hard guardrails, a mandatory self-review, and an inspiration-vs-evidence firewall.
- **An LLM-as-judge runner, judged mode (`--judge`), validators, and release automation** — all domain-agnostic.

## Modes

| # | Mode | Use when |
|---|------|----------|
| A | Generate web page concept | First-pass page/view concept with structure, hierarchy, components, states. |
| B | Design web user flow | Ordered steps, decision points, URL/history, recovery paths. |
| C | Create responsive UI spec | Implementation-ready structure across breakpoints, with states and tokens. |
| D | Review page for usability/accessibility | Severity-tiered critique with causal findings and fixes. |
| E | Create typography, spacing & grid system | Type roles, fluid scale, spacing, grid, density. |
| F | Prepare design rationale / handoff | Decisions, tradeoffs, validation plan. |
| G | Generate / critique a marketing landing page (conversion / CRO) | Above-the-fold, scroll narrative, CTA hierarchy, social proof, conversion. |

## Install (Claude Code)

```bash
git clone <this-repo> ~/web-design-skill
cd ~/web-design-skill
./scripts/install.sh
```

Then in Claude Code:

```text
/web-design-skill review this pricing page for usability and accessibility
```

See [`docs/commands.md`](docs/commands.md) for Codex / Claude API integration.

## Architecture

Mirrors `mobile-design-skill`: `SKILL.md` (canonical entrypoint) + `skill/` (modes, templates, metadata) + `docs/` (workflow, methodology, quality bars, sources, patterns, domain packs) + `examples/` (golden, case studies, visual fixtures, eval fixtures) + `scripts/` (validators, judge runner, install) + `.claude/` (Claude Code wrapper + judge agent).

## Validation

```bash
python3 scripts/validate_repo.py        # structural checks (Iteration 1)
WDS_STRICT=1 python3 scripts/validate_repo.py   # full content-depth checks (Iteration 2)
python3 scripts/validate_release.py
```

## License

MIT — see [`LICENSE`](LICENSE).

## Rubric eval pack

Design-quality is calibrated against score-graded fixtures in `examples/evals/` and the before/after upgrade example in [`examples/rubric-before-after.md`](examples/rubric-before-after.md). (Iteration 1: placeholders; Iteration 2 authors calibrated web scores.)

The LLM-as-judge runner (`scripts/run_rubric_judge.py`, documented in [`docs/llm-judge-runner.md`](docs/llm-judge-runner.md)) provides provider-agnostic semantic rubric calibration and powers judged mode (`/web-design-skill --judge`).
