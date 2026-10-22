# Mode Definitions

This document defines the seven supported modes for `web-design-skill`.

Each mode includes:

- required input
- optional input
- output structure
- validation checklist
- fallback behavior

Every response carries two scope axes — `Responsive/breakpoint scope:` (mobile-web / tablet / desktop / wide) and `Browser/engine scope:` (Chromium / WebKit / Gecko) — never a single "platform." All guidance must respect both axes.

All modes also use `docs/weaknesses.md` as a failure-mode preflight. The goal is to prevent outputs that are structurally complete but generic, overconfident, aesthetic-only, responsive-flattened, or weakly buildable.

Modes that propose, specify, review, or rationalize a design artifact also use `docs/design-quality-rubric.md`. Generated/specification outputs should internally target 4/5; reviews should expose both a current and a projected (conditional) score with evidence limits.

All modes use `docs/clarification-policy.md` before drafting. Ask clarifying questions only when missing information would materially change the recommendation; otherwise proceed with minimal labeled assumptions.

## Mode identifiers (crosswalk)

The same seven modes are referenced by letter (A–G, here and in `skill/skill.md`), by ordinal (1–7, in `SKILL.md`), and by slug (in `skill/metadata.yaml`). The validator and the emitted `Mode:` line always use the full canonical name. They are the same set, in the same order:

| # | Letter | Slug | Canonical name (emitted in output + checked by the validator) |
|---|--------|------|----------------------------------------------------------------|
| 1 | A | page-concept | Generate web page concept |
| 2 | B | web-flow | Design web user flow |
| 3 | C | ui-spec | Create responsive UI spec |
| 4 | D | review-page | Review page for usability/accessibility |
| 5 | E | type-spacing-grid | Create typography, spacing and grid system |
| 6 | F | rationale-handoff | Prepare design rationale / handoff |
| 7 | G | marketing-landing | Generate / critique a marketing landing page (conversion / CRO) |

---

## Mode A: Generate web page concept

### Purpose
Create a first-pass concept for a web page that is usable, structured, responsive across the breakpoint ladder, and browser-aware.

### Required input
At least one of:
- product/feature idea
- user goal
- page type (landing, dashboard, article, settings, results, form)

### Optional input
- breakpoint/browser targets
- target audience
- brand or tone
- current design system / token set
- accessibility sensitivity
- enterprise vs marketing context
- content density
- wireframe notes
- constraints and deadlines

### Output structure
- Mode
- Responsive/breakpoint scope
- Browser/engine scope
- Assumptions
- Page goal
- Primary user task
- Information hierarchy
- Recommended layout structure
- Suggested components
- Interaction notes
- Empty / loading / error states
- Responsive and browser behavior
- Accessibility considerations
- Design quality calibration
- Rationale for major choices
- Alternatives considered
- Next actions

### Validation checklist
- Is the primary task obvious above the fold?
- Is the hierarchy sequenced by user need rather than decoration, per page and per scroll section?
- Are recommended components real (native elements or named design-system components)?
- Are empty/loading/error states included, plus system states (404/500/offline) where relevant?
- Are pointer, keyboard, and readability implications addressed?
- Are visual hierarchy, composition, density, and production checks calibrated?
- Does the proposal target at least 4/5 design quality, or explain what missing context blocks that target?
- Does it behave deliberately across breakpoints (not the same layout poured into every width)?
- Is accessibility included by default (semantic outline, keyboard, contrast)?
- Are invented details labeled as assumptions?

### Fallback behavior
If the request is underspecified:
- infer only the minimum viable context
- label assumptions clearly
- keep the concept structural rather than visually over-specified

---

## Mode B: Design web user flow

### Purpose
Define a usable, predictable, recoverable web task flow that respects URLs, browser navigation, and the full range of web input.

### Required input
At least one of:
- user goal
- flow description
- feature description
- journey start and end states

### Optional input
- breakpoint/browser targets
- authentication context (passwords, passkeys, OAuth/SSO)
- target audience
- failure scenarios
- enterprise or regulated context
- current navigation/IA model
- content density
- accessibility sensitivity

### Output structure
- Mode
- Responsive/breakpoint scope
- Browser/engine scope
- Assumptions
- Flow goal
- Entry points
- Ordered steps / views
- Decision points
- Back/forward and URL state
- Failure and recovery paths
- Responsive and browser behavior
- Accessibility and usability risks
- Simplification opportunities
- Next actions

### Validation checklist
- Is the success path clear, end-to-end, from a concrete entry point to a success state?
- Are decision points explicit?
- Is each step a shareable/bookmarkable URL where appropriate, with predictable back/forward behavior and an unsaved-input guard?
- Are error and recovery paths present (network, validation, timeout, session-expired), with entered data preserved?
- Does the flow use web affordances correctly — hover/hover-intent, right-click context menus with a fallback, and full keyboard operability — rather than ignoring them? On web, ignoring hover/focus/keyboard operability is the failure, not using it.
- Does the flow exploit multi-pane / multi-tab / long-scroll where it helps, instead of forcing one view at a time?
- Are usability and accessibility risks (focus management on route change, aria-live status) included?
- Are unnecessary steps flagged for simplification?

### Fallback behavior
If the request is incomplete:
- define a lean happy path plus the minimum recovery paths
- note where business rules or product policy details are missing

---

## Mode C: Create responsive UI spec

### Purpose
Translate a page or flow into implementation-friendly UI structure and behavior that an engineer can build across breakpoints and engines.

### Required input
At least one of:
- page description
- wireframe description
- feature description
- flow scope

### Optional input
- breakpoint/browser targets
- current design system / token set
- content model
- states
- interaction constraints
- handoff depth
- brand constraints
- accessibility sensitivity
- engineering context (framework, SSR/CSR)

### Output structure
- Mode
- Responsive/breakpoint scope
- Browser/engine scope
- Assumptions
- Screen or flow scope
- Structural zones
- Components by section
- State definitions
- Behavior rules
- Content guidance
- Spacing and layout notes
- Typography rules
- Accessibility requirements
- Design quality requirements
- Responsive and browser implementation notes
- Key decision tradeoffs
- Next actions

### Validation checklist
- Can an engineer or designer build from this without asking for missing structural information?
- Are states explicit (default, hover, focus-visible, loading, empty, error, success, disabled, plus system states)?
- Are behaviors described as rules ("if X, then Y") instead of implied?
- Are spacing and typography concrete (px/rem values or tokens), not relative?
- Are responsive behaviors specified per breakpoint, with a verified 320px reflow?
- Are accessibility requirements concrete (semantic outline, keyboard operability, focus management, target size, contrast, forced-colors)?
- Are visual hierarchy, spacing, typography, color/state, and production quality requirements concrete?
- Does the spec target at least 4/5 design quality with buildable requirements?
- Are unknown details labeled as assumptions?

### Fallback behavior
If the request lacks detail:
- create a base spec with explicit assumptions
- avoid pretending to know hidden business rules
- keep state definitions conservative and reusable

---

## Mode D: Review page for usability/accessibility

### Purpose
Run an expert review of a page or page description through usability, accessibility, keyboard operability, hierarchy, design-quality, performance, and convention lenses. Mode D borrows critique's reasoning structure (objective → decision → why it is or isn't effective) but, as an expert review rather than a facilitated critique, it also prescribes fixes: each finding is one causal chain — observation → violated principle → user consequence → change → predicted effect — not a list of problems split from a separate list of remedies.

### Sub-cases

Mode D behaves differently depending on what the user provides. Classify the request into exactly one sub-case at the start of the response, and adjust scope accordingly.

#### D1: Review with visual design provided
The user shares a screenshot, Figma link, rendered URL, or detailed visual description that includes layout, spacing, typography treatment, and color. A **structured design extract** from a design tool (Figma / Pencil / Penpot / Sketch, pulled by the host's MCP connector — see `docs/design-tool-handoff.md`, with the ordered extract call sequence in `docs/design-tool-runbooks.md`) is a higher-confidence D1 input than a screenshot: it lets the review assert layer- and token-level facts (sizes, spacing, token names, the text heading outline) while still holding purely visual properties (rendered contrast, focus appearance) provisional until a render exists.

- Full assessment is possible across visual hierarchy, spacing, typography, colors, and contrast.
- Accessibility checks can address visual properties (contrast, focus appearance, target-size visibility) as well as structural ones.
- Use this sub-case label at the top of the response.

#### D2: Review with text description only
The user describes structure (sections, fields, actions, content) but no visual treatment.

- Assess structure, logic, information order, state coverage, and interaction behavior.
- Do not assert visual properties (contrast, spacing in pixels, visual weight) without qualifiers. Flag them under `Unresolved assumptions`.
- Accessibility assessment is limited to properties that can be reasoned from structure: label strategy, state semantics, semantic outline, keyboard operability. Mark visual accessibility (contrast, focus visibility) as unverifiable.
- Use this sub-case label at the top of the response.

#### D3: Review with problem statement
The user reports a symptom without a clear root cause ("users complain", "analytics show drop-off at step 3", "bounce is high", "something feels off").

- Lead with diagnosis: what likely causes the reported symptom, based on the described context.
- Differentiate diagnosis from assessment. Diagnosis is a hypothesis; assessment reports observable problems.
- Suggest targeted investigation steps (specific events to check, specific user actions to observe, a Lighthouse/axe run), not a full redesign.
- Use this sub-case label at the top of the response.

#### D4: Review with context change
The user asks whether an existing design still holds under a changed context (new audience, new regulatory framing, new breakpoint/browser target, new accessibility requirement).

- Re-evaluate the existing design through the new lens; do not re-review from scratch.
- Call out which prior-acceptable choices now fail under the new context, and which remain fine.
- If the context change invalidates assumptions baked into the original design, state that the design likely needs re-structuring, not just adjustment.
- Use this sub-case label at the top of the response.

### Required input
At least one of:
- page description
- wireframe description
- UI spec
- screenshot / rendered URL description
- current layout summary

### Optional input
- breakpoint/browser targets
- target audience
- product context
- known complaints / analytics
- current constraints
- business priority
- accessibility sensitivity
- severity preference

### Output structure
- Mode
- Responsive/breakpoint scope
- Browser/engine scope
- Sub-case (D1 / D2 / D3 / D4)
- Assumptions
- Quick summary
- Strengths
- Findings — each finding is one causal chain with: Lens (Usability / Accessibility / Keyboard operability / Hierarchy & readability / Design quality / Navigation & interaction / Performance (Core Web Vitals) / Responsive (breakpoints) / SEO & semantics / Forced-colors), Observation, Violated principle (named), User consequence, Change, Predicted effect (directional + confidence), Severity (Nielsen 0–4 = frequency × impact × persistence), Moves (which design-quality dimension it shifts, band→band)
- Design quality score (current → projected) — current and projected scores plus a per-dimension table; the projected number is the median of the assessable projected dimensions (visual dimensions are never projected upward from a text-only review), stated as a flat number; a higher number reachable only after a visual pass goes in a separate Ceiling note
- Severity index — findings rolled up by Nielsen 0–4 level
- Bold move (optional) — include only when the trigger is met (see below)
- Platform-convention mismatches — web-platform and browser conventions (Jakob's Law): native control behavior, link vs button semantics, back/forward, engine-specific rendering
- Unresolved assumptions
- Next actions

The Bold move trigger: offer one only when ALL hold — the page is already competent (current ≥3/5) but inert (loses no major points yet has no point of view); there is no unresolved severity-3 or severity-4 finding (fix those first); and there is a concrete UX upside. Allowed in D1/D3; in D2 it may address structure/flow only; in D4 only if the new context unlocks it. It is not a fix and not required to ship; if the trigger is not met, omit the section. A recommendation that contradicts the stated product/task is a failure only when its justification is aesthetic — a contradiction justified by a named usability/accessibility/hierarchy mechanism and surfaced in the Bold move block with its tradeoff and validation path is encouraged, not penalized.

### Validation checklist
- Is the sub-case (D1 / D2 / D3 / D4) classified explicitly?
- Does the review distinguish strengths from problems, with at least one genuine strength?
- Is each finding a single causal chain (observation → violated principle → user consequence → change → predicted effect), not an issue split from its fix?
- Does every finding name the violated principle (heuristic/law/WCAG SC), instead of "this feels off"?
- Does every predicted effect name a user outcome, stated directionally with a confidence level and no fabricated percentages?
- Is severity rated on the Nielsen 0–4 scale and justified as frequency × impact × persistence?
- Are the web lenses applied where relevant — keyboard operability, Core Web Vitals, responsive-across-breakpoints, SEO & semantics, forced-colors — not only generic usability?
- For D2: are visual claims qualified as unverifiable, or restricted to structure?
- For D3: is diagnosis separated from assessment?
- For D4: is the review framed as a delta against the changed context, not a full re-review?
- Are both a current and a projected design-quality score exposed, the projected number being the median of the assessable projected dimensions (a flat number, not "up to"), with any higher post-visual-pass figure confined to a Ceiling note?
- For D2/D3: is the projected score labeled provisional, and are visual dimensions kept at n/v (never projected upward)?
- If a Bold move is offered: is the trigger met, does it carry all required fields (deviation, JTBD job, upside, risk, validation path, score impact, conviction), and is it kept separate from the required fixes?
- Was any UX-strengthening recommendation withheld only because it contradicts the current product? If so, is it moved to Bold move with its tradeoff?
- Are convention mismatches called out, and typography/spacing reviewed where verifiable?
- Are design-quality claims limited to what can be verified from the provided visual or description?
- Is compliance language avoided unless verified, and are unresolved assumptions stated?

### Fallback behavior
If evidence is limited:
- frame findings as probable issues, not proven defects
- state what cannot be verified from the provided material
- for D2 in particular, never assert visual properties without a qualifier; move them to `Unresolved assumptions`

---

## Mode E: Create typography, spacing and grid system

### Purpose
Create a web-friendly type, spacing, and grid system grounded in readability, fluid scaling, density control, and pointer/target ergonomics.

### Required input
At least one of:
- product type
- target audience
- breakpoint targets
- density preference
- current design direction

### Optional input
- current brand typography
- accessibility sensitivity
- enterprise vs marketing context
- multilingual support
- content heaviness
- handoff depth
- existing token system

### Output structure
- Mode
- Responsive/breakpoint scope
- Browser/engine scope
- Assumptions
- Type roles
- Size hierarchy
- Weight usage
- Line-height guidance
- Spacing scale
- Density rules
- Visual rhythm rules
- Pointer, target-size and input implications
- Accessibility considerations
- Usage examples
- Next actions

### Validation checklist
- Does the system define roles instead of random sizes?
- Does it use rem-based sizing and fluid `clamp()` so it scales with the user's root size and the viewport?
- Does it cap the reading measure (~65ch) and define line-height per role?
- Does it cover spacing as a 4px-based system and define a 12-column grid?
- Does it relate density to content and task needs, including exploiting desktop density where it helps?
- Does it define visual rhythm and role limits so the system can be applied consistently?
- Does it target at least 4/5 design quality through rhythm, density, scaling, and production-ready values?
- Does it note pointer/target-size implications (24px min, 44px AAA, pointer-aware)?
- Are accessibility constraints included (text spacing, 200% zoom, contrast, forced-colors)?
- Are examples practical for real web surfaces?

### Fallback behavior
If brand rules are unknown:
- define a neutral, accessible structure
- separate role definitions from font-family decisions
- mark unresolved brand-level decisions clearly

---

## Mode F: Prepare design rationale / handoff

### Purpose
Explain and package design decisions for product, design, and engineering handoff. When foundations or a design-tool round-trip are in scope, target the handoff payload and W3C Design Tokens (DTCG 2025.10) output in `docs/design-tool-handoff.md` — and when the tokens are written back into a tool, follow the reverse runbook (DTCG → Figma Variables / Pencil variables, with mapping tables, idempotency, and alias order) in `docs/design-tool-runbooks.md`. Author the motion specs (the part a design tool does not capture) from `docs/motion-and-animation.md`.

### Required input
At least one of:
- design description
- redesign summary
- page or flow concept
- decision summary

### Optional input
- breakpoint/browser targets
- audience
- project context
- constraints
- known tradeoffs
- implementation stage
- research notes
- accessibility sensitivity

### Output structure
- Mode
- Responsive/breakpoint scope
- Browser/engine scope
- Assumptions
- Design objective
- Target users and context
- Key design decisions
- Pattern choices and why
- Design quality rationale
- Responsive and browser alignment
- Accessibility and usability considerations
- States and edge cases
- Implementation notes
- Open questions
- Validation plan / recommended testing focus
- Next actions

### Validation checklist
- Does it explain why decisions were made?
- Does it connect choices to user goals and context?
- Does it show responsive and browser alignment (breakpoint behavior, Baseline gating)?
- Does it explain how visual hierarchy, composition, density, and brand expression support the design objective?
- Does the rationale state the quality target or current score using the 1-5 rubric?
- Does it cover edge states and implementation concerns (tokens, focus management, performance, analytics)?
- Does it avoid invented evidence?
- Does it separate known facts from recommendations?
- Is it usable in design/dev handoff?
- Does it end with a realistic validation plan (axe/keyboard pass, Lighthouse budget, 320px reflow)?

### Fallback behavior
If research evidence is missing:
- do not fabricate validation
- explicitly recommend what should be tested or confirmed next

---

## Mode G: Generate / critique a marketing landing page (conversion / CRO)

### Purpose
Design or review a marketing / landing page whose primary job is persuasion and conversion — not task completion. This mode optimizes the marketing-site end of the spectrum (above-the-fold clarity, scroll narrative, CTA hierarchy, social proof, conversion path), distinct from the web-app modes (A–F) which optimize task efficiency and density. **The marketing-vs-web-app split is the defining tension of this mode:** marketing surfaces earn expressive, editorial, brand-forward craft; web-app surfaces earn density, tables, keyboard-first task efficiency. Use the right end of the spectrum for the surface, and say which end you are optimizing.

For a public-interest or social campaign, the conversion goal is understanding and recall rather than a sale; apply the social-campaign section of [`../docs/domain-packs/marketing-landing.md`](../docs/domain-packs/marketing-landing.md).

### Required input
At least one of:
- product / offer description
- target audience or segment
- conversion goal (signup, demo, purchase, lead)
- existing landing page (for critique)

### Optional input
- brand / tone
- traffic source / campaign context
- competitor or benchmark references
- existing analytics / funnel data
- constraints (compliance, localization, performance budget)

### Output structure
- Mode
- Responsive/breakpoint scope
- Browser/engine scope
- Assumptions
- Conversion goal and primary CTA
- Above-the-fold (hero) structure
- Scroll narrative and section rhythm
- Value proposition and messaging hierarchy
- Social proof and trust signals
- CTA hierarchy and placement
- Objection handling / FAQ
- Accessibility considerations
- Performance considerations (Core Web Vitals, media weight)
- SEO and shareability
- Design quality calibration
- Conversion-rate reasoning
- Next actions

### Validation checklist
- Is the single primary conversion goal explicit?
- Is the above-the-fold value proposition clear without scrolling, on both desktop and mobile-web?
- Is there one dominant CTA with a clear hierarchy over secondary actions?
- Are trust / social-proof signals specific, not generic?
- Is the scroll narrative ordered by visitor questions, not by feature list?
- Are performance (LCP/INP/CLS, hero media weight) and accessibility (contrast over hero, reduced-motion, keyboard) treated as conversion factors, not afterthoughts?
- Is SEO/semantics covered (one h1, meta, Open Graph, structured data)?
- Are conversion claims framed as mechanisms / hypotheses, not fabricated lift percentages?
- Is the marketing-vs-web-app framing respected (expressive / editorial craft is appropriate here, and named as such)?

### Fallback behavior
If offer / audience / goal is underspecified:
- state the smallest labeled assumption about the conversion goal
- keep the structure (hero → proof → CTA) and flag missing funnel context in Next actions
- never fabricate conversion-rate statistics or A/B results
