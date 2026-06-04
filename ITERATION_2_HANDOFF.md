# ITERATION 2 HANDOFF — bring `web-design-skill` to production-ready (v1.0.0)

> **How to use this file:** open a **fresh Claude Code session from inside this directory**
> (`/Users/evgeniyvor/Documents/web_design_skill`) and paste the prompt below (everything inside the
> fenced block) as your first message. It is self-contained and assumes no memory of the transfer session.

---

````text
# TASK: Author Iteration 2 of the web-design skill — bring it to production-ready (v1.0.0)

You are working inside /Users/evgeniyvor/Documents/web_design_skill. This is a Claude Code / Codex
"skill" repository (slug: web-design-skill). Assume you have ZERO memory of any prior conversation —
everything you need is below or in the repo.

## 0. Ground truth before you start
Verify the repo state: run `git -C . status` and `ls -la`. The reusable CHASSIS and a STANDALONE
skeleton should be present (scripts/run_rubric_judge.py, oracle, CI workflows, scripts/validate_release.py,
bump_version.py, install.sh, .claude/ wrapper + judge agent + agents/openai.yaml, and the validator
scripts/validate_repo.py with data constants already pointed at the web file set).
- METHODOLOGY and the Mode D engine were copied ~verbatim from the mobile skill. The CONTRACT is
  web-reframed (modes: page concept / web flow / responsive UI spec / review page / type+spacing+grid /
  rationale-handoff, PLUS a 7th marketing/landing/CRO mode whose headings exist but body is STUBBED).
  `Platform scope:` was mechanically split into `Responsive/breakpoint scope:` + `Browser/engine scope:`.
- ALL DOMAIN content is STUBBED with `TODO(iteration-2)` and `INVERSION-WATCH` markers: quality-bars,
  sources, inspiration-sources, context-defaults, heuristics, patterns-catalog, design-quality bands,
  rendered-output-qa, visual-benchmark-playbooks, all domain packs, all golden examples, all case studies,
  all visual-review fixtures, the 5 eval fixtures (placeholders satisfying {1..5}), anti-patterns, the
  6 worked examples, and docs/proposals/review-mode-upgrade.md.
- If any skeleton file is missing or the tree is empty, STOP and report what is missing — do not invent
  the chassis.
Reference repo (READ-ONLY, for structure/methodology shape ONLY): ../mobile-design-skill (v1.16.0). You
may read it to see HOW a section is structured. NEVER copy mobile bodies, numbers, or examples into web
files. Author all web content FRESH.
Find your work queue: `grep -rn "TODO\|INVERSION-WATCH" docs skill examples scripts`.

## 1. Non-negotiable discipline
- AUTHOR FRESH. Do not copy mobile prose, mobile numbers (pt/dp/sp), mobile examples, or mobile source
  lists. The only things identical to mobile are the METHODOLOGY and the Mode D REVIEW ENGINE (see §2).
- KEEP VERBATIM (engine — do not "improve"): the causal Finding chain (Observation → Violated principle →
  User consequence → Change → Predicted effect + confidence → Severity Nielsen 0-4 → Moves); the flat-median
  projected score capped 4/5 until a visual pass; the gated Bold move with JTBD grammar + kill criterion;
  the generative method (JTBD → HMW → Crazy8s → SCAMPER → converge → mechanism); the inspiration-vs-evidence
  firewall; the 1-5 rubric mechanics + 8 dimensions; the clarification policy; the weakness preflight; the
  D1-D4 sub-cases. Only the LENS ENUM and the NAMED PRINCIPLES inside findings become web.
- CONSCIOUSLY FLIP THE 9 INVERSIONS (§2). Renaming is NOT flipping — reverse the SIGN/SEMANTICS.
- Do not loosen any validator check to make it pass. Re-point checks to web; keep depth thresholds.

## 2. The 9 inversions you must FLIP (not rename)
1. `Platform scope: iOS|Android` overloaded two web axes → keep the split into `Responsive/breakpoint
   scope:` + `Browser/engine scope:` in EVERY mode template, modes.md, and metadata.yaml; all guidance
   respects both axes.
2. Mode B fail-conditions, docs/evals.md, docs/self-review.md treat "hover, right-click, keyboard-first"
   as RED FLAGS. On web these are REQUIRED. Flip the sign: the failure is IGNORING hover/focus/keyboard
   operability.
3. "one-screen-at-a-time" heuristic → web is multi-pane / multi-tab / long-scroll.
4. SaaS pack "avoid desktop table shrinkage / anti-density" → web should EXPLOIT desktop density (real
   tables, multi-pane, hover-actions, keyboard shortcuts).
5. "platform-flattening cap (3/5)" → recast as "responsive-flattening cap" (no behavior across breakpoints,
   hover/focus ignored, no 320px reflow). Update the literal string in docs/weaknesses.md AND
   scripts/validate_repo.py (WEAKNESS_REQUIRED_PATTERNS).
6. touch-target 44pt/48dp + thumb-zone → WCAG 2.5.8 (24px) / 2.5.5 (44px AAA) + pointer-aware
   `@media (pointer: coarse|fine)`; Fitts via cursor travel + screen edges/corners. Delete thumb-zone.
7. "keyboard" = mobile on-screen keyboard TYPE (inputmode) vs web keyboard OPERABILITY — keep separate;
   operability (tab order, focus-visible, focus management, trap+restore, skip links) dominates on web.
8. "tooling last" (sources Tier 5) → on web, tooling is FIRST-CLASS evidence (Lighthouse/PSI/CrUX,
   axe-core/WAVE, Playwright, BrowserStack). Re-tier it up.
9. "offline as a default state" → web = PWA / service-worker-CONDITIONAL; pair with 404/500/
   session-expired states.
Maintain an inversion ledger (one row per inversion: file:line before → after). Finish with a grep
proving zero leaked mobile-sign tokens.

## 3. Web knowledge to USE (do not re-derive)
FOUNDATIONS ("physics"): 16px/rem baseline + fluid type `clamp()` + ~65ch measure; breakpoint ladder
~320/360->768->1024/1280->1440->1920+ + container queries + max content width; units px/rem/em/ch/vw/dvh
(delete pt/dp/sp + safe-area/FAB/app-bar); WCAG 2.2 web SCs: 1.4.10 reflow@320px, 1.4.4 resize 200%,
1.4.12 text spacing, 2.5.8 target size 24px (2.5.5 44px AAA), 2.4.11 focus not obscured, 1.4.1 use of
color, 1.4.11 non-text contrast, forced-colors; Core Web Vitals (LCP/INP/CLS) + font-loading (FOUT/FOIT)
+ image art-direction as quality bars and a review lens.
INPUT + A11Y: simultaneous mouse+keyboard+touch; hover/hover-intent, cursor, right-click, drag-with-
fallback; keyboard operability (WCAG 2.1.1): tab order, focus-visible, focus management on route/overlay
change, focus-trap+restore, skip links, command palette; semantic HTML + heading outline (one h1) +
landmarks + WAI-ARIA APG patterns + aria-live.
NAV/PATTERNS (rebuild, no mobile analog): top-nav/sidebar/mega-menu/breadcrumb/footer + History API +
URL-as-shareable-state + back/forward + beforeunload + scroll restoration; web overlays
`<dialog>`/popover/off-canvas/side-sheet (ESC+scroll-lock+ARIA); data tables first-class (sort/sticky-
header/keyboard nav/row-select+bulk/virtualization/density/responsive collapse); button hierarchy +
sticky footers (NO FAB); WebAuthn/passkeys/OAuth/SSO/autocomplete one-time-code; web push via service
workers; 12-col grid + desktop whitespace doctrine; long-scroll narrative + section rhythm + scroll-
triggered motion.
SOURCES (re-author tiers): Tier1 web platform = WHATWG HTML + WAI-ARIA APG + MDN + web.dev/CWV (replacing
Apple HIG / Material-as-OS / Android Nav). WCAG 2.2 promoted to primary (drop the "applying WCAG to
mobile" doc). Tier3 design systems: IBM Carbon, Shopify Polaris, Atlassian, Microsoft Fluent (web),
Material Web/M3 web, Ant Design, Salesforce Lightning, GitHub Primer + utility stack Tailwind + shadcn/ui
+ Radix; GOV.UK/NHS/USWDS/Fluent stronger. Tier4: Baymard e-commerce/checkout (web), NN/g web + IA, Luke
Wroblewski Web Form Design (promote). Legal: Section 508, EAA / EN 301 549. Browser data: caniuse / MDN
Baseline / Browserslist. TOOLING first-class (not last): Lighthouse/PSI/CrUX, axe-core/WAVE, Playwright,
BrowserStack.
INSPIRATION (rebalance): Awwwards promoted to primary web craft (keep perf/reduced-motion/contrast/
keyboard caveats); add Land-book, SiteInspire, Godly, Lapa Ninja, SaaS Landing Page, httpster, One Page
Love, Mobbin Web, Refero; replace Apple Design Awards craft playbook with CSS Design Awards / FWA / Webby;
demote/drop Pttrns and UI Sources.
7th MODE (marketing/landing/CRO): conversion + persuasion + above-the-fold + scroll narrative + CTA
hierarchy + social proof + the marketing-site-vs-web-app optimization split (expressive/editorial craft
vs density/task/tables/keyboard-first).
NEW DOMAIN PACKS (already named as stubs): marketing-landing, ecommerce, content-publishing,
docs-dev-portal, webapp-dashboard (5).

## 4. Deliverables, by phase, with acceptance criteria
A. WEB FOUNDATIONS — quality-bars, context-defaults, design-quality, usage. Author the physics above.
   Accept: no pt/dp/sp/thumb-zone/safe-area/FAB token survives grep; CWV thresholds present. (single-threaded)
B. WEB PATTERNS + HEURISTICS — patterns-catalog (largest), heuristics, design-quality. Each pattern =
   mechanism + when-to-use + failure mode. Tables first-class; APG referenced. (fan-out by pattern family)
C. TRAP AUDIT — flip all 9 inversions (§2) with the ledger. Accept: grep proves zero leaked tokens.
   (single-threaded, highest care — this is the correctness core)
D. 7th-MODE CONTENT — fill the marketing/CRO mode (contract + template + metadata) and the
   marketing-landing pack; make the marketing-vs-app split explicit. (single-threaded)
E. WIRE NEW LENSES — add CWV/performance, keyboard operability, SEO/semantics + heading outline,
   responsive-across-breakpoints, forced-colors to the universal lenses (docs/workflow.md, skill.md) AND
   the Mode D `Lens:` enum (modes.md + templates.md). Keep the Finding engine verbatim. (single-threaded)
F. CALIBRATION CORPUS — 7 web golden examples, 5 web domain packs, 12 case studies, 6 visual-review
   fixtures, and the 5 eval fixtures (examples/evals/rubric-score-{1..5}.json) with CALIBRATED web
   expected scores. Keep the JSON schema (required fields + 8 dimensions); rewrite prompt/response/
   expected_* to web; demonstrate web caps (responsive-flattening, keyboard-inoperability) at scores 1-2;
   a true 5/5 web spec cites rem/clamp values, breakpoints, focus management, INP/CLS budgets, axe-clean,
   320px reflow. Accept: {1..5} coverage; dimension medians match expected_score; inter-fixture
   monotonicity. (fan-out the corpus; SINGLE-THREADED calibration pass for the 5 eval fixtures — one
   consistent grader sets all 5 scores)
G. MODE D WEB PORT — translate/port docs/proposals/review-mode-upgrade.md so its file:line citations and
   worked example land on a WEB screen; re-derive the worked Finding chain on a web artifact; swap the
   de-risk checklist to web a11y (axe/WAVE, keyboard pass, 320px reflow, forced-colors). Keep the engine's
   claims intact. Update anti-patterns to web traps (modal w/o focus-trap, off-canvas table, hover-only
   actions). (single-threaded)
H. RE-ENABLE + TIGHTEN VALIDATOR; RUN JUDGE — in scripts/validate_repo.py the content-depth checks are
   gated behind WDS_STRICT (and a STRICT constant). Re-point every guarded check to web: MODE_REQUIREMENTS
   keys (6 web modes + 7th), the must_contain regexes (drop dp|pt|sp; the 44pt.*48dp rule -> 24px / 2.5.8 /
   44px; rebase the rhythm scale to your web spacing scale), VISUAL_BENCHMARK_REQUIRED_PATTERNS (web set:
   Awwwards + the new galleries + CSS Design Awards/FWA/Webby + the two firewall sentences),
   WEAKNESS_REQUIRED_PATTERNS ("platform flattening" -> "responsive flattening"), GOLDEN_EXAMPLE_AREAS,
   DOMAIN_PACK_FILES, SYNTHETIC_CASE_STUDY_FILES, VISUAL_REVIEW_FIXTURE_FILES, the section lists, and the
   eval_pack lists in skill/metadata.yaml (still point at mobile filenames). Then default STRICT to True
   (remove the WDS_STRICT gate). In scripts/run_rubric_judge.py confirm "web" in the judge prompt. Run the
   judge calibration. Accept: `python3 scripts/validate_repo.py` exits 0 with all content-depth checks
   ACTIVE; `python3 scripts/run_rubric_judge.py --dry-run` green; oracle/command self-tests green; nothing
   loosened. (single-threaded)
I. PRODUCTION HARDENING + SHIP — rewrite docs/rendered-output-qa.md for web with Playwright first-class
   (resize across the breakpoint ladder, axe-core, 320px reflow, focus-order capture, CWV/Lighthouse hints,
   forced-colors) + update the JSON schema/sample; rewrite README and CHANGELOG; make the slug
   web-design-skill consistent everywhere; bump metadata.yaml + README badges + .claude wrapper to v1.0.0
   (use scripts/bump_version.py if supported, else edit + validate); run `python3 scripts/validate_release.py`;
   create the v1.0.0 git tag. (single-threaded)

## 5. How to parallelize
Use a Workflow / subagents for the breadth-heavy fan-out: Phase B pattern families (navigation, overlays,
tables, forms/auth, motion/scroll, a11y/keyboard) then one reconcile pass; Phase F golden examples + 5 packs
+ case studies + visual fixtures against a shared "web foundations + rubric" brief. Keep SINGLE-THREADED
(correctness core, do yourself): Phase A constants, Phase C trap-audit ledger, Phase E lens wiring, the
Phase F eval-fixture calibration pass, Phase G proposal port, Phase H validator, Phase I release.

## 6. Definition of Done (all must hold before shipping)
- `python3 scripts/validate_repo.py` exits 0 with all content-depth checks RE-ENABLED and web-re-pointed
  (no skips, no loosened thresholds; the WDS_STRICT gate removed / defaulted on).
- `python3 scripts/run_rubric_judge.py --dry-run` passes; oracle + external-command self-tests pass.
- 5 eval fixtures cover {1..5} with calibrated web expected scores; web caps demonstrated; scores monotonic.
- Trap-audit ledger shows all 9 inversions flipped; grep for mobile-sign tokens
  (thumb|FAB|safe-area|44\s?pt|48\s?dp|one screen at a time|tooling.*last|offline.*default) returns only
  intentional contrastive mentions.
- No mobile body text copied verbatim (engine/methodology identical BY DESIGN; all domain bodies web-authored).
- 7 modes live (6 ported + marketing/CRO), each with full required sections + web must_contain.
- New lenses (CWV, keyboard operability, SEO/semantics, responsive-across-breakpoints, forced-colors) wired
  into universal lenses + the Mode D Lens enum.
- Sources re-tiered and inspiration rebalanced exactly as in §3.
- Rendered-output-QA is web + Playwright-first.
- README + CHANGELOG rewritten; slug web-design-skill consistent; v1.0.0 in metadata/badges/wrapper.
- `python3 scripts/validate_release.py` green; v1.0.0 git tag created.

Work phase by phase. After each phase, run the validator and report a short diff of what changed and which
acceptance criteria now pass. Do not mark the task done until every Definition-of-Done box holds.
````
