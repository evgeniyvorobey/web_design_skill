# web_design_skill

`web-design-skill`: a website UI/UX design skill (responsive web, marketing and landing pages, web apps) for Claude Code and Codex. It is prompt-and-docs plus Python validators; the one script that touches a browser is the optional `scripts/rendered_qa.py`.

## Layout

- `SKILL.md`: canonical entrypoint and core workflow. `skill/modes.md` and `skill/templates.md` carry the modes and output templates; `skill/skill.md` is the expanded maintainer reference, not the entrypoint.
- `.claude/skills/web-design-skill/SKILL.md`: thin wrapper that lists the supporting files by `${CLAUDE_SKILL_DIR}/../../../` paths. A new runtime doc goes into that list too.
- `.claude/agents/web-design-judge.md`: the independent judge for `/web-design-skill --judge` (`docs/judged-mode.md`).
- `docs/`: workflow, foundations, quality system, domain packs, design-tool handoff, rendered QA.
- `examples/`: calibration corpus; `examples/evals/` holds the score-graded rubric fixtures.
- `scripts/`: validators, version bumper, rubric judge runner and its oracle, installer.

## Changing the skill

1. Edit, then run the three validators, all green before a commit:
   `python3 scripts/validate_repo.py`, `python3 scripts/run_rubric_judge.py --dry-run`, `python3 scripts/validate_release.py`.
   `validate_repo.py` checks required files and required phrases in several docs; a new doc goes into `REQUIRED_FILES`.
2. The validators check structure. For output quality, score drafts against `docs/evals.md` and `docs/design-quality-rubric.md` with `scripts/run_rubric_judge.py` (contract in `docs/llm-judge-runner.md`); that run needs a model.
3. Each change ships as a version: `python3 scripts/bump_version.py major|minor|patch` (policy in `docs/versioning.md`), a CHANGELOG entry, and the version in the commit subject, as in `git log`.

## Source of truth and copies

This repo is the source of truth. After a change, report which copies need a sync and leave the sync to the owner.

- `~/.claude/skills/web-design-skill/`: a separate git clone of this repo (full tree), loaded globally. It syncs by `git pull` there once the change is on `origin/main`.
- `~/.claude/agents/web-design-judge.md`: a plain copy of `.claude/agents/web-design-judge.md`.
