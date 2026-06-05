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

**An AI skill that turns vague design requests into structured, accountable web UI/UX guidance** — page concepts, user flows, responsive specs, accessibility reviews, type/spacing systems, and engineering handoff. It exists to replace generic "make it modern" advice with decisions you can defend: every recommendation is tied to a usability principle, a WCAG criterion, a breakpoint, or a measured budget — never taste alone.

Runs as a **Claude Code** skill (`/web-design-skill`), as a **Codex / OpenAI** skill, or as a **system prompt** for the Claude API or any LLM. It reasons over text, screenshots, and structured design extracts; when a design-tool connector is loaded it can also read a Figma/Pencil file and write design tokens back.

Current version: **1.3.0** — see [`CHANGELOG.md`](CHANGELOG.md).

## What it does

Give it a page, a screenshot, a flow, or a one-line idea. It classifies the request into one of **seven modes**, fills the gaps with *labeled* assumptions (instead of inventing facts), and returns a structured artifact that names its scope, its evidence, and its risks.

- **Evidence-first, not decorative** — guidance is grounded in web-platform conventions, Nielsen heuristics, WCAG 2.2 AA, and Core Web Vitals; inspiration galleries are kept behind a firewall and never used as proof of usability or compliance.
- **Two explicit scope axes** on every answer — `Responsive/breakpoint scope:` (320 → 1920+) and `Browser/engine scope:` (Chromium / WebKit / Gecko) — so nothing is silently flattened to one device or engine.
- **Severity-tiered reviews** — each finding is a causal chain (observation → violated principle → user consequence → fix → predicted effect + confidence), scored on Nielsen 0–4 and rolled into a current→projected design-quality number.
- **Calibrated quality bar** — a 1–5 rubric with hard caps (responsive-flattening, keyboard-inoperability) and a mandatory self-review pass before anything is returned.
- **Design-tool round-trip** — consume a structured design extract as a high-confidence review input, and emit W3C **DTCG 2025.10** tokens you can write back into Figma/Pencil. See [`docs/design-tool-runbooks.md`](docs/design-tool-runbooks.md).

## Quick start

```bash
git clone https://github.com/evgeniyvorobey/web_design_skill.git ~/web-design-skill
cd ~/web-design-skill
./scripts/install.sh                 # installs into ~/.claude/skills/web-design-skill (symlink)
```

Then, in Claude Code:

```text
/web-design-skill review this pricing page for usability and accessibility
```

That's it. The skill auto-classifies the request, states its assumptions, and returns a structured review. Other install options:

```bash
./scripts/install.sh --scope project   # install into the current project's .claude/ instead of globally
./scripts/install.sh --method copy      # self-contained copy instead of a symlink
./scripts/install.sh --status           # show where it is installed
./scripts/install.sh --uninstall        # remove it
```

For Codex / OpenAI and Claude API integration, see [`docs/commands.md`](docs/commands.md). You don't have to name the skill — it triggers on design intent (e.g. *"redesign this checkout"*, *"is this form accessible?"*).

## Usage examples

Every output opens with its `Mode`, both scope axes, and labeled `Assumptions`, then the mode-specific sections. Full worked input/output pairs live in [`examples/`](examples/); here are trimmed previews.

### Review a page (Mode D)

```text
Use the web-design-skill. Review this account settings page (text description only):
- one long single-column form: profile, email, password, notifications, danger zone
- all fields rendered at once; a single "Save" fixed at the page bottom
- "Delete account" is a red link inside the form, right above Save
- inline errors appear only after pressing Save; no focus styling mentioned
Constraints: accessibility-sensitive, keyboard users common.
```

→ returns a severity-ordered critique with fixes and a score (trimmed):

```md
Mode: Review page for usability/accessibility
Responsive/breakpoint scope: Assumed desktop + mobile-web (not specified)
Browser/engine scope: Assumed evergreen engines (not specified)
Sub-case: D2 — text description only

## Quick summary
Structure is recoverable but risky: one giant form with a single bottom Save mixes
low-stakes edits with an irreversible delete, defers all validation to submit, and
gives no focus styling. Biggest risks: accidental destructive action, keyboard inoperability.

## Findings
### F1 — Destructive action adjacent to Save  · Severity 4 (catastrophic)
Observation → violated principle → user consequence → fix → predicted effect…

Design quality: 2/5 now → 4/5 projected after F1–F4.
```

Full version: [`examples/review-page.md`](examples/review-page.md).

### Generate a concept, flow, spec, or system

The same `Use the web-design-skill.` prefix drives every other mode — give it the goal, breakpoints, browsers, and constraints:

```text
Design a web page concept for a "Project overview" page in a SaaS PM app.
Goal: understand status at a glance and act on what's blocked. Desktop-first, down to 320px.
Constraints: dense status data, keyboard-operable, existing tokens, accessibility-sensitive.
```

```text
Generate a marketing landing page for "Cadence" (automated standup updates).
Goal: free-trial signups. Audience: eng managers. Constraints: fast LCP, reduced-motion, SEO.
```

```text
Turn this into a responsive UI spec: an admin "Users" page with a searchable, sortable,
selectable data table and bulk actions. Thousands of rows; keyboard power-users; existing tokens.
```

Worked outputs: [page concept](examples/generate-page.md) · [user flow](examples/web-flow.md) · [UI spec](examples/ui-spec.md) · [type/spacing/grid](examples/type-spacing-grid.md) · [marketing landing](examples/marketing-landing.md) · [rationale/handoff](examples/rationale-handoff.md).

### Round-trip with a design tool (Figma / Pencil / Penpot / Sketch)

With a design-tool MCP connector loaded in your host, the skill orchestrates the calls and reasons over the result — it never opens the file itself (the connector does the I/O):

```text
Use the web-design-skill. Pull node 1:2 from this Figma file as a structured extract and
review it, then emit the foundations as DTCG tokens and write them back as Figma Variables.
```

It runs the ordered READ runbook (`get_metadata` → `get_variable_defs` → `get_design_context`) into the neutral extract, reviews it as a high-confidence input, then the REVERSE runbook (DTCG → Figma Variables via the Plugin API, or Pencil variables via `set_variables`). Without a connector, paste a screenshot or an extract and it works from that. See [`docs/design-tool-runbooks.md`](docs/design-tool-runbooks.md) and the conceptual contract in [`docs/design-tool-handoff.md`](docs/design-tool-handoff.md).

### Higher-confidence mode

Append `--judge` to run an independent judge pass that scores the draft against the rubric and revises below-target answers before returning:

```text
/web-design-skill --judge review this onboarding flow
```

## Modes

| # | Mode | Use when |
|---|------|----------|
| A | Generate web page concept | First-pass page/view concept with structure, hierarchy, components, states. |
| B | Design web user flow | Ordered steps, decision points, URL/history, recovery paths. |
| C | Create responsive UI spec | Implementation-ready structure across breakpoints, with states and tokens. |
| D | Review page for usability/accessibility | Severity-tiered critique with causal findings and fixes. |
| E | Create typography, spacing & grid system | Type roles, fluid scale, spacing, grid, density. |
| F | Prepare design rationale / handoff | Decisions, tradeoffs, tokens, validation plan. |
| G | Generate / critique a marketing landing page | Above-the-fold, scroll narrative, CTA hierarchy, social proof, conversion. |

## How it works

Every request runs the same pipeline (full version in [`docs/workflow.md`](docs/workflow.md)):

1. **Classify** the request into exactly one primary mode.
2. **Identify context** — product, user goal, audience, density, accessibility sensitivity ([`docs/context-defaults.md`](docs/context-defaults.md)).
3. **Determine scope** — the responsive and browser/engine axes, stated explicitly.
4. **Clarify or assume** — ask up to 3 blocking questions, otherwise proceed with *labeled* assumptions ([`docs/clarification-policy.md`](docs/clarification-policy.md)).
5. **Draft** against the foundations — quality bars, patterns, heuristics, domain pack.
6. **Self-review** — a mandatory pass ([`docs/self-review.md`](docs/self-review.md)) that checks keyboard operability, contrast, responsive reflow, state coverage, and the inspiration-vs-evidence firewall before returning.

## What it's good at — and what it isn't

Honest scope matters more than hype, so here it is plainly.

**Good fit**

- Structured **reviews** of a page/flow with prioritized, causal, fixable findings.
- **Spec & handoff** work: turning a concept into implementation-ready structure, states, tokens, and acceptance criteria across breakpoints.
- **Accessibility-aware** reasoning (WCAG 2.2 AA, keyboard operability, forced-colors, reduced-motion) as a design-time check.
- **Conventions & tradeoffs**: which pattern to reach for, why, and what it costs — grounded in web-platform behavior, not trends.
- **Design-token round-trips** in valid DTCG 2025.10, with idempotent write-back runbooks for Figma/Pencil.

**Not a good fit / known limits**

- **It is not pixel-perfect rendering.** It reasons from text, DOM, screenshots, or structured extracts — it does not see sub-pixel layout, real font rendering, or runtime contrast unless you give it concrete values. Visual claims stay *provisional* until a render exists.
- **Guidance, not a compliance guarantee.** Accessibility output is a strong design-time starting point, not a substitute for testing with real screen readers (VoiceOver/NVDA/JAWS), keyboard-only runs, and a contrast checker. It will not claim conformance it cannot verify.
- **It doesn't run, deploy, or screenshot your site, or open a `.fig`/`.pen` itself.** Those I/O steps belong to your host's tools/MCP connector; the skill orchestrates and reasons. The optional [rendered-output QA](docs/rendered-output-qa.md) workflow is Playwright-first and host-driven.
- **Rubric scores are model-judged, not deterministic.** The 1–5 number is a calibrated estimate to compare drafts and target a bar — two runs can differ slightly. Use it as a gradient, not a certificate.
- **Scope is web.** Responsive web, marketing/landing, and web apps — not native iOS/Android, print, or email-client HTML.
- **It will ask or assume, not invent.** Missing flows, states, or policies are surfaced as labeled assumptions or blocking questions rather than fabricated.

## What's inside

- **Skill spine:** [`SKILL.md`](SKILL.md) (entrypoint), [`skill/modes.md`](skill/modes.md), [`skill/templates.md`](skill/templates.md), [`docs/workflow.md`](docs/workflow.md).
- **Foundations:** [`docs/quality-bars.md`](docs/quality-bars.md), [`docs/sources.md`](docs/sources.md), [`docs/heuristics.md`](docs/heuristics.md), [`docs/patterns-catalog.md`](docs/patterns-catalog.md), [`docs/context-defaults.md`](docs/context-defaults.md), [`docs/principles.md`](docs/principles.md), [`docs/guardrails.md`](docs/guardrails.md).
- **Quality system:** [`docs/design-quality.md`](docs/design-quality.md), [`docs/design-quality-rubric.md`](docs/design-quality-rubric.md), [`docs/weaknesses.md`](docs/weaknesses.md), [`docs/self-review.md`](docs/self-review.md), [`docs/evals.md`](docs/evals.md).
- **Design-tool interop & motion:** [`docs/design-tool-handoff.md`](docs/design-tool-handoff.md) (neutral extract + DTCG 2025.10 tokens), [`docs/design-tool-runbooks.md`](docs/design-tool-runbooks.md) (per-tool READ/REVERSE call sequences for Figma, Pencil, Penpot, Sketch), and [`docs/motion-and-animation.md`](docs/motion-and-animation.md) (the motion layer).
- **Calibration corpus:** [`docs/golden-examples.md`](docs/golden-examples.md) + [`examples/golden/`](examples/golden/); [`docs/synthetic-case-studies.md`](docs/synthetic-case-studies.md) + [`examples/case-studies/`](examples/case-studies/); [`docs/visual-review-fixtures.md`](docs/visual-review-fixtures.md) + [`examples/visual-review-fixtures/`](examples/visual-review-fixtures/); the five web domain packs in [`docs/domain-packs/`](docs/domain-packs/index.md); and the rubric fixtures in [`examples/evals/`](examples/evals/) with the upgrade example [`examples/rubric-before-after.md`](examples/rubric-before-after.md).
- **Inspiration (non-authoritative):** [`docs/inspiration-sources.md`](docs/inspiration-sources.md), [`docs/visual-benchmark-playbooks.md`](docs/visual-benchmark-playbooks.md), [`docs/benchmark-report-format.md`](docs/benchmark-report-format.md).
- **Rendered-output QA (optional, Playwright-first):** [`docs/rendered-output-qa.md`](docs/rendered-output-qa.md) + [`examples/rendered-output-qa/`](examples/rendered-output-qa/).
- **Tooling:** the LLM-as-judge runner [`scripts/run_rubric_judge.py`](scripts/run_rubric_judge.py) (documented in [`docs/llm-judge-runner.md`](docs/llm-judge-runner.md)) that powers `--judge` mode, the repo validator, and deterministic release validation in [`scripts/validate_release.py`](scripts/validate_release.py).

## Validation

The repo is self-validating — structure, links, content depth, and rubric calibration are all checked deterministically (no API keys required):

```bash
python3 scripts/validate_repo.py                # structure, links, hygiene, content-depth checks
python3 scripts/run_rubric_judge.py --dry-run   # rubric fixture coverage
python3 scripts/validate_release.py             # version/tag sanity + judge self-tests
```

Design quality is calibrated against the score-graded fixtures in [`examples/evals/`](examples/evals/) and the before/after example in [`examples/rubric-before-after.md`](examples/rubric-before-after.md). Release automation is documented in [`docs/release-automation.md`](docs/release-automation.md).

## Security & trust

This skill is prompt-and-docs plus a few **Python validation/release scripts** (no network calls, no secrets). As with any skill you install, read what runs: the scripts under [`scripts/`](scripts/) and the wrapper in [`.claude/`](.claude/). The skill performs no file or network I/O of its own — any reading of your design files or sites happens through your host's tools/MCP connectors, under your control.

## Versioning & contributing

Semantic versioning, adapted for a prompt-and-docs skill ([`docs/versioning.md`](docs/versioning.md)). Bumps go through [`scripts/bump_version.py`](scripts/bump_version.py); every release must pass `scripts/validate_release.py`. Changes are documented in [`CHANGELOG.md`](CHANGELOG.md). Issues and PRs are welcome — run the three validators above before opening one.

## License

MIT — see [`LICENSE`](LICENSE).
