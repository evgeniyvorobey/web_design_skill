# Self-review

This document defines the mandatory self-review pass every skill response must undergo before being returned.

Self-review is the single highest-impact lever for output quality. Without it, LLM responses drift toward plausible-sounding but shallow output — visible structure, weak substance. With it, most low-quality outputs are caught before the user ever sees them.

Self-review runs inside the workflow as **Step 10: Self-review against the quality bar**, after the draft is complete and before it is returned.

---

## How to run self-review

1. Produce the full mode-specific draft using the template.
2. Silently answer every prompt in the relevant section below.
3. If any answer is "no" or "not sure", revise the draft.
4. Only return the response after every applicable prompt has a confident "yes".

Do not echo the self-review prompts in the response. Do not add a "self-review passed" footer. Self-review is internal quality control, not user-facing content.

Do not skip self-review to save tokens. A response that fails self-review is a regression; a response that passes is the floor, not the ceiling.

---

## Universal self-review prompts (run for every mode)

### Specificity
- Could this exact response have been written with **no** information about the user's product, domain, or audience? If yes, rewrite with the provided context.
- Have I replaced every instance of vague language ("modern", "clean", "intuitive", "appropriate spacing", "good contrast") with a concrete claim?
- If I removed the `Mode:` and the two scope axes (`Responsive/breakpoint scope:`, `Browser/engine scope:`), would a reader still be able to tell which mode this is? If not, structure is weak.

### Clarification policy
- Did I apply `docs/clarification-policy.md` before deciding to ask questions or proceed?
- If I asked questions, are there three or fewer and are they genuinely blocking?
- If I proceeded with assumptions, are they minimal, labeled, and safe?
- Did I avoid asking cosmetic or preference questions before task, breakpoint/browser, safety, accessibility, or implementation blockers?
- If clarification blocks a reliable artifact, did I offer a fast path when a provisional draft would still be useful?

### Known weakness prevention
- Which weakness pattern from `docs/weaknesses.md` is most likely in this task, and did I actively prevent it?
- Does the draft resemble template completion without real decisions? If yes, add choices, rejected alternatives, and reasons.
- Did I avoid the common regression trio: generic output, first-idea bias, and happy-path-only design?
- If the task involves review or handoff, did I prevent visual overclaim and weak buildability?

### Substance
- Does every recommendation have a reason tied to user goal, task, accessibility, readability, performance, or implementation — not aesthetic preference?
- For a recommendation that changes a design, did I state its intended effect, not just the change itself?
- For each major design decision, have I named at least one alternative and said why it was rejected?
- Are there any sentences that could be deleted without losing information? Delete them.

### Honesty
- Have I claimed any web standard, browser behavior, research finding, or accessibility compliance that I cannot source or that was not provided?
- Have I made a visual claim (contrast, spacing value, typography treatment) when only a text description was provided? If yes, move it to `Unresolved assumptions`.
- Have I echoed a user-provided compliance claim (for example, "WCAG AA") as fact? If yes, add the "cannot independently verify" qualifier.

### Context fit
- Have I applied the relevant defaults from `docs/context-defaults.md` (audience, domain, breakpoint/browser, use-context)?
- When context signals conflicted, did I resolve them using the documented precedence (safety/accessibility > regulated domain > use-context > audience > breakpoint/browser) and surface the resolution in `Assumptions`?
- Did I apply a generic default where a context-specific one would have been more appropriate?

### Heuristic grounding
- For each major decision, can I name the heuristic that justifies it (Fitts, Hick, Doherty, Miller, Jakob, Zeigarnik, goal-gradient, peak-end, Nielsen, Gestalt)?
- If I cited a heuristic, is the citation doing work, or is it decorative? Remove decorative citations.
- Did I miss a red flag from `docs/heuristics.md` that applies to this page or flow?

### Pattern selection
- Did I pick each pattern (navigation, overlay, list/grid/table, form pattern, feedback surface, search, auth) using the decision matrix in `docs/patterns-catalog.md`, or did I default to my first instinct?
- Did I cite the losing alternative for every pattern-level choice?
- Am I inventing a novel pattern where an established one fits? If yes, revert unless the input truly has no fit.
- For Mode D reviews: did I check every pattern the design uses against the matching entry's red flags?

### Design quality calibration
- If the response proposes, specifies, reviews, or rationalizes a design artifact, did I apply the relevant lenses from `docs/design-quality.md`?
- Did I apply the 1-5 rubric from `docs/design-quality-rubric.md`?
- For generated/specification outputs, would the draft score at least 4/5? If not, did I revise the weak dimension or state the missing input?
- For Mode D reviews, did I expose both a current and a projected (conditional) design-quality score with a reason and evidence limits?
- Did I define the intended attention path rather than only listing components?
- Did I translate visual quality into concrete mechanisms (size, spacing, alignment, color role, density, motion, state treatment, tokens)?
- Did I avoid using "premium", "clean", "modern", "delightful", or "polished" as unexplained taste words?
- Equal-height + internal-alignment check: for any row of peer cards/tiles/columns, do they share a height *and* do their internal rows line up across siblings — title, description, and CTA each on a shared baseline (subgrid / shared row tracks) — so a title that wraps to a different number of lines doesn't shove that card's body and button out of line? Footer-only pinning (`margin-top: auto`) is not enough when titles/bodies vary in length. If one tile is intentionally emphasized, is that carried by color/border/badge/scale, not by accidental height variance?
- Inert-page test: if this page lost its logo and brand color, would it still be distinguishable from a competitor's template? If not, flag it as inert (3/5 with an upside note), not a quiet 4/5.

### Web platform self-checks
- Does the design behave deliberately across the breakpoint ladder, and did I verify a 320px reflow and 200% zoom rather than pouring one layout into every width (responsive flattening)?
- Is everything keyboard operable — logical tab order, visible `:focus-visible`, focus managed on route/overlay change, dialogs focus-trapped with focus restored, skip link present, ESC closes overlays — and did I avoid hover-only actions?
- Did I respect both web meanings of "keyboard": input *type* (inputmode/type) and operability (focus/tab)?
- Did I consider performance (LCP candidate prioritized, layout shift prevented, INP-friendly interactions) against the Core Web Vitals budget?
- Did I cover SEO & semantics where relevant (one h1, heading outline, landmarks, metadata/Open Graph on marketing/content surfaces)?
- Did I check forced-colors / high-contrast survival and a real dark theme where relevant?
- For any motion I proposed: does each animation serve a functional purpose (feedback, orientation, state change, status), or did I animate high-frequency/keyboard actions, dense tables, or forms where stillness is better? Is every animation `transform`/`opacity`-only with a `prefers-reduced-motion` fallback and named easing/duration tokens, per `docs/motion-and-animation.md`?
- If a design came from or is going to a design tool: did I consume the structured extract as a high-confidence input (not just "a screenshot"), and — if I emitted tokens — are they valid DTCG 2025.10 (object color/dimension, aliases, theming), every value tokenized, with vendor data kept in `$extensions`, per `docs/design-tool-handoff.md`? If I described pulling the design or writing tokens back, did I follow the concrete READ/REVERSE call sequences in `docs/design-tool-runbooks.md` (real tool names, DTCG↔native mapping, idempotency by name, alias targets before referrers) and keep the boundary — the skill sequences/reasons, the host's MCP connector executes the I/O?

### Inspiration handling
- If I used inspiration sources, are they clearly separated from UX rationale, web conventions, accessibility requirements, and compliance language?
- Did I use production-flow references (Mobbin Web, Page Flows, Refero) for journey/pattern benchmarking before craft galleries or moodboards?
- Did I avoid presenting Awwwards, Land-book, Dribbble, Behance, Pinterest, or award examples as proof that a design is usable, accessible, performant, or correct?
- If the user did not ask for inspiration and it does not materially help, did I leave it out?

### Completeness
- Are all relevant edge states addressed (default, loading, empty, error, plus 404/500/offline/session-expired where relevant)?
- Does the `Next actions` section contain specific, testable actions — not "test it", "iterate", "validate"?
- For multi-breakpoint outputs, have I specified behavior changes across the ladder where they actually differ, and shared the structure where they align?

### Readability of the response itself
- Can a designer skim this response in under 2 minutes and extract the 3 most important decisions?
- Are sections ordered by decision priority, not template default?
- Is the response too long? If so, the structure is hiding thin content; cut and strengthen.

---

## Mode-specific self-review prompts

### Mode A: Generate web page concept
- Is the primary user task singular and obvious above the fold, or did I list three parallel tasks?
- Is the information hierarchy ordered by what the user needs to decide or do first, not by visual prominence?
- Are the suggested components real (native elements or named design-system components)?
- Have I addressed what happens when the page has zero data, partial data, stale data, and full data?
- Did I commit to one layout and specify how it adapts across breakpoints, rather than describing three possible layouts without choosing?

### Mode B: Design web user flow
- Does the flow run end-to-end from a concrete entry point to a success state?
- Are URLs shareable where appropriate, and is back/forward behavior defined, with an unsaved-input guard?
- Have I defined recovery for at least network failure, validation error, and session expiry, with entered data preserved?
- Does the flow correctly use web affordances — hover/hover-intent, right-click context menus with a fallback, and full keyboard operability — and manage focus on route change? (Ignoring these is the failure on web, not using them.)
- Does the flow use multi-pane / long-scroll / multi-tab where it helps, instead of forcing one view at a time?
- Are any invented business rules labeled as assumptions?

### Mode C: Create responsive UI spec
- Can an engineer begin implementation without asking clarifying structural questions?
- Are states defined beyond "default" — at minimum default, loading, empty, error, plus system states where relevant?
- Are spacing and typography values concrete (tokens, px, rem), not relative ("more", "tighter")?
- Are responsive behaviors specified per breakpoint with a verified 320px reflow, rather than one layout duplicated?
- Does the spec reference a design system (named or assumed), or does it invent component names without grounding?

### Mode D: Review page for usability/accessibility
- Did I classify the sub-case (D1 visual / D2 description only / D3 problem statement / D4 context change) at the top?
- For D2 (description only): did I avoid asserting visual properties (contrast, spacing values, visual weight)?
- Did I find at least one genuine strength?
- Is each finding a single causal chain (observation → violated principle → user consequence → change → predicted effect), with no issue split from its fix?
- Does every finding name the violated principle, and does every predicted effect name a user outcome (directional + confidence)?
- Did I apply the web lenses where relevant — keyboard operability, Core Web Vitals, responsive-across-breakpoints, SEO & semantics, forced-colors?
- Is severity rated 0–4 (Nielsen = frequency × impact × persistence) based on user impact, not visual taste?
- For a rendered or visual (D1) artifact, did I check whether peer cards/tiles in a row have ragged, content-driven heights *and* whether their internal rows (title, description, CTA) fail to line up across cards (a Gestalt similarity/continuity finding), and rate it by user impact — usually cosmetic-to-minor — rather than skipping it as "just polish"? (For a D2 description-only review, do not assert heights or alignment unless they are stated.)
- Did I expose both a current and a projected score, with the projection conditional, capped at 4/5 unless resilience is named, and labeled provisional for D2/D3?
- If a Bold move is present: is its trigger met, all fields complete, and kept separate from required fixes — and did I withhold any UX-strengthening move only because it contradicts the product (if so, move it here)?

### Mode E: Create typography, spacing and grid system
- Are type roles named (Display, Title, Body, etc.), not just a list of sizes?
- Does the scale use rem and fluid `clamp()` so it honors the user's root size and scales to 200% zoom, with a capped measure?
- Is the spacing scale systematic (4px base) and the grid defined?
- Did I state minimum target size (24px / 44px AAA) and pointer-aware sizing?
- If multilingual was requested, did I address script-specific adjustments (CJK, Arabic, Devanagari)?

### Mode F: Prepare design rationale / handoff
- Does every "Key design decision" have an alternative that was considered and rejected, with reason?
- Is the rationale connected to the specific design in question, or does it read like a generic essay?
- Does the validation plan specify what to test and how (method, metric, acceptance — axe/keyboard pass, Lighthouse budget, 320px reflow), not just "test with users"?
- Are open questions genuinely open (blocking or undecided), not filler?

### Mode G: Generate / critique a marketing landing page (conversion / CRO)
- Is there a single primary conversion goal and one dominant CTA, with secondary actions visually subordinate?
- Is the above-the-fold value proposition clear without scrolling on both desktop and mobile-web?
- Is the scroll narrative ordered by visitor questions, not a feature list?
- Are performance (LCP/INP/CLS, hero media weight) and accessibility (contrast over hero, reduced-motion, keyboard) treated as conversion factors?
- Are conversion claims mechanisms/hypotheses, never fabricated lift percentages, and is the marketing-vs-web-app split named?

---

## When self-review finds a problem

If self-review fails on any prompt:

1. Do not patch the surface. Address the root cause.
2. If the draft cannot be fixed with light edits, rewrite the affected section from scratch.
3. Re-run self-review after the fix.

If self-review cannot pass because the input is underspecified:

1. Reduce the scope of the response to what the input supports.
2. Move unsupported claims to `Unresolved assumptions`.
3. Strengthen `Next actions` to pull the missing information from the user.

Do not return a response that fails self-review with a disclaimer. Fix it or narrow it.

---

## Integration with other quality mechanisms

Self-review complements, but does not replace:

- **Guardrails** (`docs/guardrails.md`): hard rules that must never be violated.
- **Evals** (`docs/evals.md`): external scoring criteria for regression tests.
- **Mode validation checklists** (`skill/modes.md`): structural contracts per mode.
- **Quality bars** (`docs/quality-bars.md`): concrete thresholds self-review checks against.
- **Known weaknesses** (`docs/weaknesses.md`): recurring failure modes and prevention checks.

The flow is: draft → self-review (internal) → response returned → evals (external, automated or manual).

---

## Maintenance

When a new failure mode is observed in the field, add a corresponding self-review prompt here. The goal is that every regression caught in eval should trigger a new self-review prompt to prevent recurrence.

Keep prompts answerable in one pass — yes/no or short-answer. Self-review must be fast to run, or it will be skipped.
