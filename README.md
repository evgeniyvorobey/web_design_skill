<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo-light.svg" alt="Website Design Skill" width="640">
  </picture>
</p>

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-1.3.0-blue">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="status" src="https://img.shields.io/badge/status-production--ready-brightgreen">
</p>

# Website Design Skill

A reusable AI skill that helps generate, review, structure, and justify **website** UI/UX design decisions for responsive web (desktop, tablet, mobile-web), marketing/landing pages, and web apps.

Works as a Claude Code skill (`/web-design-skill`), as a Codex / OpenAI skill, and as a system prompt for the Claude API or any LLM integration.

Current version: **1.3.0** — see [`CHANGELOG.md`](CHANGELOG.md).

## What this skill does

It enforces a practical, evidence-first framework for web design decisions, built for product work rather than decorative advice:

- **Seven modes** — every request is classified into exactly one: web page concept, web user flow, responsive UI spec, page review, type/spacing/grid system, handoff rationale, or marketing landing page (conversion/CRO).
- **Two scope axes** — `Responsive/breakpoint scope:` and `Browser/engine scope:`, so guidance respects both the breakpoint ladder (320 → 1920+) and the target engines (Chromium/WebKit/Gecko).
- **Web foundations** — a 16px/rem type baseline with fluid `clamp()` and ~65ch measure, a 4px spacing scale, WCAG 2.2 AA success criteria (reflow at 320px, target size, contrast, forced-colors), keyboard operability, and Core Web Vitals budgets. See [`docs/quality-bars.md`](docs/quality-bars.md).
- **The Mode D review engine** — causal Findings (observation → violated principle → user consequence → change → predicted effect + confidence → Nielsen 0–4 severity → score moves), a current→projected design-quality score, and a gated Bold move.
- **A 1–5 design-quality rubric** with caps (responsive-flattening, keyboard-inoperability) and median scoring — see [`docs/design-quality-rubric.md`](docs/design-quality-rubric.md) — plus a weakness preflight ([`docs/weaknesses.md`](docs/weaknesses.md)), hard guardrails, a mandatory self-review, a clarification policy ([`docs/clarification-policy.md`](docs/clarification-policy.md)), and an inspiration-vs-evidence firewall.

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

Run an independent judge pass with `/web-design-skill --judge ...` (judged mode). See [`docs/commands.md`](docs/commands.md) for Codex / Claude API integration.

## What's inside

- **Skill spine:** [`SKILL.md`](SKILL.md) (entrypoint), [`skill/modes.md`](skill/modes.md), [`skill/templates.md`](skill/templates.md), [`docs/workflow.md`](docs/workflow.md).
- **Foundations:** [`docs/quality-bars.md`](docs/quality-bars.md), [`docs/sources.md`](docs/sources.md), [`docs/heuristics.md`](docs/heuristics.md), [`docs/patterns-catalog.md`](docs/patterns-catalog.md), [`docs/context-defaults.md`](docs/context-defaults.md), [`docs/principles.md`](docs/principles.md), [`docs/guardrails.md`](docs/guardrails.md).
- **Quality system:** [`docs/design-quality.md`](docs/design-quality.md), [`docs/design-quality-rubric.md`](docs/design-quality-rubric.md), [`docs/weaknesses.md`](docs/weaknesses.md), [`docs/self-review.md`](docs/self-review.md), [`docs/evals.md`](docs/evals.md).
- **Design-tool interop & motion:** [`docs/design-tool-handoff.md`](docs/design-tool-handoff.md) (neutral extract + DTCG 2025.10 tokens), [`docs/design-tool-runbooks.md`](docs/design-tool-runbooks.md) (per-tool READ/REVERSE call sequences for Figma, Pencil, Penpot, Sketch), and [`docs/motion-and-animation.md`](docs/motion-and-animation.md) (the motion layer).
- **Calibration corpus:** [`docs/golden-examples.md`](docs/golden-examples.md) + [`examples/golden/`](examples/golden/); [`docs/synthetic-case-studies.md`](docs/synthetic-case-studies.md) + [`examples/case-studies/`](examples/case-studies/); [`docs/visual-review-fixtures.md`](docs/visual-review-fixtures.md) + [`examples/visual-review-fixtures/`](examples/visual-review-fixtures/); the five web domain packs in [`docs/domain-packs/`](docs/domain-packs/index.md); and the rubric fixtures in [`examples/evals/`](examples/evals/) with the upgrade example [`examples/rubric-before-after.md`](examples/rubric-before-after.md).
- **Inspiration (non-authoritative):** [`docs/inspiration-sources.md`](docs/inspiration-sources.md), [`docs/visual-benchmark-playbooks.md`](docs/visual-benchmark-playbooks.md), [`docs/benchmark-report-format.md`](docs/benchmark-report-format.md).
- **Rendered-output QA (optional, Playwright-first):** [`docs/rendered-output-qa.md`](docs/rendered-output-qa.md) + [`examples/rendered-output-qa/`](examples/rendered-output-qa/).
- **Tooling:** the LLM-as-judge runner [`scripts/run_rubric_judge.py`](scripts/run_rubric_judge.py) (documented in [`docs/llm-judge-runner.md`](docs/llm-judge-runner.md)), the repo validator, and deterministic release validation in [`scripts/validate_release.py`](scripts/validate_release.py).

## Validation

```bash
python3 scripts/validate_repo.py                # structure, links, and content-depth checks
python3 scripts/run_rubric_judge.py --dry-run   # rubric fixture coverage
python3 scripts/validate_release.py             # version/tag sanity + self-tests
```

## License

MIT — see [`LICENSE`](LICENSE).

## Rubric eval pack

Design quality is calibrated against the score-graded fixtures in [`examples/evals/`](examples/evals/) and the before/after upgrade example in [`examples/rubric-before-after.md`](examples/rubric-before-after.md). The LLM-as-judge runner (`scripts/run_rubric_judge.py`, documented in [`docs/llm-judge-runner.md`](docs/llm-judge-runner.md)) provides provider-agnostic semantic rubric calibration and powers judged mode (`/web-design-skill --judge`). Release automation is documented in [`docs/release-automation.md`](docs/release-automation.md).
