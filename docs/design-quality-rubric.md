# Design Quality Rubric

This document turns design quality into a 1-5 scoring system. Use it to raise the quality of proposed designs, not only to critique existing ones.

The rubric complements:

- `docs/design-quality.md` for quality dimensions and mechanisms
- `docs/weaknesses.md` for recurring failure modes
- `docs/quality-bars.md` for numeric thresholds
- `docs/evals.md` for external response evaluation
- `docs/golden-examples.md` for compact taste and domain calibration examples
- `docs/synthetic-case-studies.md` for synthetic bad-to-good calibration cases
- `docs/domain-packs/index.md` for domain-specific risk and trust calibration
- `docs/visual-review-fixtures.md` for text-only review calibration
- `docs/rendered-output-qa.md` for optional QA when a rendered artifact exists
- `examples/evals/` for score-calibrated rubric fixtures
- `examples/rubric-before-after.md` for a weak-to-strong upgrade example
- `scripts/run_rubric_judge.py` and `docs/llm-judge-runner.md` for semantic judge calibration

---

## When to score

Score design quality when the response:

- proposes a page concept
- creates a responsive UI spec
- reviews a page or page description
- creates a typography, spacing and grid system
- prepares a rationale or handoff
- proposes or critiques a marketing / landing page (Mode G)

Mode B user flows normally do not need a visual quality score unless page pacing, progress feedback, or transition quality materially affects the flow.

---

## Output rule

For generated or specified design artifacts, the score is primarily internal:

- target **4/5** before returning the answer
- if the draft scores **3/5 or below** and the missing context is not blocking, revise the design before returning
- if missing input prevents a 4/5 recommendation, state the limitation in `Assumptions` or `Unresolved assumptions`

For reviews, expose both a current and a projected score. The projection is conditional and is derived from the improvement ladder below — never asserted as achieved:

```md
- Current: [1-5]/5 — [short evidence-based reason; "provisional" for D2/D3 text-only]
- Projected: [1-5]/5 — the median of the assessable projected dimensions once the listed fixes land; conditional: requires those fixes AND the named assumptions to hold. State a flat number, not "up to". For D2/D3, provisional — visual dimensions stay unassessable (n/v) and are never projected upward.
- Ceiling note: with a visual pass confirming [x], the ceiling is [1-5]/5 (capped at 4/5 unless resilience is named).
```

The projected score is the median of the assessable (non-`n/v`) projected dimensions, not the sum of per-dimension gains; a cap lifts only when the specific fix that meets its condition is present; a P0/Fail is never projected up to a number; and a higher figure reachable only after a visual pass belongs in `Ceiling note`, never in the projected number.

For generation, specs, typography systems, and handoff, expose the target only when useful:

```md
- Quality target: 4/5 — production-ready direction with remaining validation notes.
```

Do not let the score replace the reasoning. The score is a compression of the critique, not the critique itself.

---

## 1-5 score levels

| Score | Label | Meaning |
|-------|-------|---------|
| 1/5 | Broken or misleading | The design obscures the primary task, invents unsupported claims, violates hard guardrails, or creates serious accessibility/usability risk. |
| 2/5 | Structurally weak | The screen or recommendation has visible structure, but hierarchy, state handling, platform fit, or evidence boundaries are weak enough that users or implementers will struggle. |
| 3/5 | Acceptable baseline | The design can work, but it is mostly competent rather than strong. It handles the main task and basics, but lacks sharper hierarchy, stronger state coverage, or production-ready details. |
| 4/5 | Strong and shippable | The design is specific to the task and context, has clear hierarchy, usable density, concrete states, accessibility-aware decisions, platform alignment, and buildable mechanisms. |
| 5/5 | Excellent and resilient | The design is not just shippable; it anticipates edge cases, adapts across platform/context/accessibility settings, preserves brand without weakening semantics, and is ready for design-system scaling. |

---

## Dimension scoring

Score each relevant dimension from 1-5.

| Dimension | 1-2 signals | 3 signals | 4-5 signals |
|-----------|-------------|-----------|-------------|
| Attention path and hierarchy | unclear first glance; competing focal points; no dominant element above the fold | main task visible but secondary hierarchy is rough; per-section hierarchy on long pages is weak | first glance, second glance, and action path are deliberate per viewport and per scroll section |
| Composition and spacing | grouping depends on decoration or breaks with text-spacing overrides; ad-hoc gaps | spacing mostly works but lacks rhythm or a consistent grid | spacing scale, grid, alignment, and responsive placement across the breakpoint ladder communicate structure |
| Typography craft | ad-hoc sizes, weak readability, runaway measure, too many styles | basic roles exist; measure and line-height roughly right | role-based scale, `clamp()` sizing, ~65ch measure, line-height, and font-loading (swap/no-CLS) are deliberate |
| Color, state, and contrast | color carries meaning alone or fails contrast | semantic colors mostly present; one theme considered | color roles, non-color cues, real dark theme, forced-colors survival, and full state colors are defined |
| Density and rhythm | density fights the task; desktop space wasted or cramped | density is acceptable | density matches task and viewport — exploits desktop density where it helps — and repeats predictably across components |
| Interaction polish and motion | missing feedback; motion hides problems or jacks scroll | basic feedback exists | hover/focus-visible/active/loading/success/error feedback is clear, fast, and reduced-motion-aware |
| Context and brand fit | visual language contradicts trust, domain, or the marketing-vs-app spectrum | broadly appropriate | brand supports task and trust through tokens, fits its end of the marketing↔app spectrum, without overriding semantics |
| Production readiness | vague handoff; no tokens/states/QA; no perf or a11y budget | enough to discuss | token-ready values, component/state mapping, breakpoint behavior, semantic outline, CWV budget, and axe/keyboard QA are present |

---

## Caps and hard limits

Apply these caps before calculating the final score:

- Any P0 weakness from `docs/weaknesses.md` makes the response **Fail**, not a score.
- Any P1 weakness caps score at **2/5** until fixed.
- Missing empty/loading/error states where relevant caps generated concepts and UI specs at **3/5**.
- Unsupported accessibility compliance claims make the response **Fail**.
- Visual assertions from text-only review input cap Mode D score confidence; label the score as provisional or restrict it to structural quality.
- Aesthetic-only recommendations cap the design-quality score at **2/5** until translated into task, accessibility, or implementation mechanisms.
- Responsive flattening caps responsive outputs at **3/5**: the same layout poured into every breakpoint with no behavior change, hover/`:focus-visible` operability ignored, or no working 320px reflow.
- Keyboard inoperability — focus not visible, focus lost on route/overlay change, a modal without focus trap + restore, or actions reachable only by hover — caps at **2/5** until fixed.
- An inert screen — competent on all dimensions but failing the inert-screen test in `docs/design-quality.md` — caps at **3/5** with an upside note (not a quiet 4/5) until it carries at least one owned distinctive asset or a justified signature moment.

---

## Final scoring method

1. Score all relevant dimensions.
2. Apply caps and hard limits.
3. Use the median dimension score as the starting point.
4. Lower the final score if one critical dimension is weaker than the median and affects the primary task.
5. Raise to 5/5 only when resilience is demonstrated across states, accessibility settings, platform behavior, and implementation handoff.

Do not average away a serious flaw. A beautiful 5/5 visual direction with 2/5 state handling is not a 4/5 design; it is a risky design with polish.

---

## Improvement ladder

Use this ladder when a draft is below the target:

- 1 → 2: remove misleading claims, fix hard guardrails, define the actual user task
- 2 → 3: clarify hierarchy, add states, qualify assumptions, remove aesthetic-only advice
- 3 → 4: add concrete mechanisms, alternatives, responsive/browser notes, accessibility behavior, and production checks
- 4 → 5: add resilience — 320px reflow, dark theme + forced-colors, text-spacing/200% zoom, tokenization, CWV budget, localization, and design-system scaling

For most skill outputs, **4/5 is the default target**. Use 5/5 as a stretch target when the user provides enough context for strong system-level guidance.

---

## Self-review prompt

Before returning a design artifact, silently answer:

- What score would I give this draft before revision?
- Which dimension prevents it from reaching 4/5?
- Can I raise that dimension with the information already available?
- If not, did I state the missing input clearly?
- Did I avoid using the score as a substitute for concrete design mechanisms?

If the draft is below 4/5 and can be improved without inventing facts, revise it before returning.

---

## Eval calibration pack

The repository includes score-calibrated fixtures in `examples/evals/`:

- `rubric-score-1.json` — broken or misleading response
- `rubric-score-2.json` — structurally weak response
- `rubric-score-3.json` — acceptable baseline response
- `rubric-score-4.json` — strong and shippable response
- `rubric-score-5.json` — excellent and resilient response

Each fixture defines:

- prompt
- response excerpt
- expected score
- verdict
- cap or hard limit
- dimension scores
- failed dimensions
- improvement suggestions

Use these fixtures when tuning prompts, judging generated responses, or adding LLM-as-judge tests.

For human calibration, use `examples/rubric-before-after.md`. It shows the upgrade path from a 2/5 template-complete UI spec to a 4/5 shippable spec.

For taste and domain calibration, use `docs/golden-examples.md` and `examples/golden/`. These examples show compact 4/5-style patterns for marketing landing, ecommerce PDP + checkout, content article, docs / dev portal, web-app dashboard, web form, and settings / account.

For broader synthetic calibration, use `docs/synthetic-case-studies.md` and `examples/case-studies/`. These cases show plausible weak responses, stronger 4/5 responses, and regression checks across web domains and modes. They are not real-world validation.

For domain-aware calibration, use `docs/domain-packs/index.md` and `docs/domain-packs/`. Domain packs raise quality by improving hierarchy, state coverage, trust language, and handoff checks for marketing/landing, ecommerce, content/publishing, docs/dev-portal, and web-app/dashboard. They do not prove compliance or business impact.

For review calibration, use `docs/visual-review-fixtures.md` and `examples/visual-review-fixtures/` to test whether Mode D reviews avoid unsupported visual claims from text-only evidence.

For implemented UI, use `docs/rendered-output-qa.md` and `examples/rendered-output-qa/` as an optional post-design QA layer. Rendered overlap, clipping, overflow, or state failures can cap an otherwise strong written design until fixed.

For semantic runner calibration, use:

```bash
python3 scripts/run_rubric_judge.py --dry-run
```

See `docs/llm-judge-runner.md` for the provider-agnostic JSONL contract.

For live semantic calibration, use the runner's external-agent command path instead of storing provider keys in the repository.
