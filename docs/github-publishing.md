# GitHub Publishing Kit

Ready-to-use GitHub metadata and launch copy for `web-design-skill`. Use it when creating the repository, filling the GitHub "About" section, and preparing a public release.

---

## Recommended repository description

Primary GitHub repository description:

`Reusable AI skill for Claude Code / Codex that generates, reviews, and structures website UI/UX decisions for responsive web, marketing/landing pages, and web apps.`

Shorter variant:

`Reusable Claude Code / Codex skill for practical website UI/UX design and review.`

---

## Suggested topics

Recommended GitHub topics:

- `ai-skill`
- `codex`
- `claude-code`
- `prompt-engineering`
- `web-design`
- `web-ui`
- `web-ux`
- `responsive-design`
- `accessibility`
- `core-web-vitals`
- `design-system`
- `ux-review`
- `ui-spec`
- `product-design`
- `design-ops`

Tighter core set:

- `ai-skill`
- `codex`
- `claude-code`
- `web-design`
- `web-ux`
- `responsive-design`
- `accessibility`
- `design-system`

---

## Release title

Recommended release title:

`v1.0.0 — Production-ready web release`

Alternative:

`v1.0.0 — Website Design Skill`

---

## Release notes

Recommended release text:

```md
## Website Design Skill

`web-design-skill` is a reusable AI skill for Claude Code / Codex focused on practical website design work.

It helps generate, review, structure, and justify website UI/UX decisions for:

- responsive web (desktop, tablet, mobile-web)
- marketing / landing pages
- web apps

### What it supports

- web page concepts
- web user flows
- responsive UI specs
- usability and accessibility reviews
- typography, spacing and grid systems
- design rationale and handoff
- marketing / landing page (conversion / CRO)

### What is included in this release

- canonical `SKILL.md` entrypoint for Codex
- Codex UI metadata in `agents/openai.yaml`
- expanded prompt pack in `skill/`
- supporting documentation in `docs/`
- worked examples and a calibration corpus in `examples/`
- repository validation script and GitHub Actions workflow

### Quality bar

This skill prioritizes:

- usability over decoration
- accessibility and keyboard operability by default
- responsive behavior across the breakpoint ladder
- performance (Core Web Vitals) as a design constraint
- implementation-friendly output
- clearly labeled assumptions
- a durable source hierarchy (WHATWG HTML, WAI-ARIA APG, WCAG 2.2) over trend-driven advice

### Notes

- Screenshots are not included in this repository.
- Worked examples and the calibration corpus are provided instead to show the expected structure and output quality.
```

---

## Recommended README intro for GitHub visitors

```md
Reusable AI skill for Claude Code / Codex that helps product teams generate, review, and hand off website UI/UX decisions for responsive web, marketing/landing pages, and web apps.
```

Alternative:

```md
Practical website UI/UX skill for Claude Code / Codex with structured outputs for flows, page concepts, UI specs, accessibility reviews, and handoff.
```

---

## Positioning notes

- Present it as a reusable skill, not a generic prompt dump.
- Emphasize web product design, accessibility, keyboard operability, responsive behavior, and performance.
- Be explicit that Claude Code supports `/web-design-skill` through the bundled `.claude/skills/` wrapper.
- Describe Codex support as standard skill compatibility.
- Use worked examples as the substitute for screenshots.
- Keep the value proposition operational: structured outputs, strong guardrails, and implementation usefulness.

Avoid over-positioning it as visual inspiration, generic design-thinking advice, aesthetic trend guidance, or screenshot-driven portfolio material.
