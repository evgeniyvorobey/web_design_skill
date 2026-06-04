# Changelog

All notable changes to `web-design-skill` are documented here. This project follows [Semantic Versioning](https://semver.org/) adapted for a prompt-and-documentation skill (see [`docs/versioning.md`](docs/versioning.md)).

## [0.1.0] - 2026-06-05

### Iteration 1 — mechanical transfer (chassis + scaffold)

Initial transfer of the domain-agnostic chassis and methodology from [`mobile-design-skill`](../mobile-design-skill) v1.16.0 into a standalone website-design skill. The web domain layer is **stubbed**; Iteration 2 authors it (see [`ITERATION_2_HANDOFF.md`](ITERATION_2_HANDOFF.md)).

**Carried verbatim (methodology / chassis):**
- Eval/judge runner, oracle, both CI workflows, `validate_release.py`, `bump_version.py`, `install.sh`.
- Core methodology: principles, workflow, guardrails, clarification policy, self-review, weaknesses, evals, the 1–5 design-quality rubric scoring mechanics, and the Mode D review engine.
- `docs/proposals/review-mode-upgrade.md` (Mode D crown-jewel spec) — ported in Iteration 2.

**Re-framed for web (contract):**
- Slug `mobile-design-skill` → `web-design-skill`; judge agent `mobile-design-judge` → `web-design-judge`.
- Mode titles re-framed for web; added a 7th mode — **Generate / critique a marketing landing page (conversion / CRO)**.
- `Platform scope: iOS/Android` → two axes: `Responsive/breakpoint scope:` + `Browser/engine scope:`.
- Packaging (Claude Code wrapper, judge agent, `agents/openai.yaml`, logos) repointed to the web slug.

**Stubbed (authored in Iteration 2), each marked `TODO(iteration-2)` / `INVERSION-WATCH`:**
- Foundations: `quality-bars`, `sources`, `inspiration-sources`, `context-defaults`, `heuristics`, `patterns-catalog`, `design-quality`, `rendered-output-qa`, `visual-benchmark-playbooks`.
- 5 web domain packs (marketing-landing, ecommerce, content-publishing, docs-dev-portal, webapp-dashboard) replacing the 6 mobile packs.
- Calibration corpus: 7 golden examples, 12 case studies, 6 visual-review fixtures, 7 worked examples, anti-patterns, benchmark-report, rubric-before-after.
- 5 eval fixtures (minimal placeholders covering scores {1..5}; calibrated web scores in Iteration 2).

**Validator:** `scripts/validate_repo.py` re-pointed (`REQUIRED_FILES` → web set); content-depth checks gated behind `WDS_STRICT` (off in Iteration 1, default-on in Iteration 2).

### Not yet done (Iteration 2)
The 9 semantic inversions (hover/keyboard/right-click red-flags, anti-density, one-screen-at-a-time, platform-flattening cap, touch targets, tooling-last, offline-default, the two-axis split) are marked `INVERSION-WATCH` and must be consciously flipped — not renamed — when the web content is authored.
