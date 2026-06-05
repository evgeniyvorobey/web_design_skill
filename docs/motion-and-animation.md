# Motion and Animation

This layer makes the skill propose **tasteful, performant, accessible** motion — and **only where it earns its place**. Animation is generated from a known palette of capabilities (easing tokens, durations, spring, and a CSS→WAAPI→library build ladder), never sprinkled everywhere for spectacle.

Use it whenever a mode proposes, specifies, or reviews interaction polish (Modes A, C, F, G, and — in Mode D — findings filed under the Design quality or Performance (Core Web Vitals) lens that move the "Interaction polish & motion" rubric dimension). It complements the motion bars in [`quality-bars.md`](quality-bars.md) and the "interaction polish & motion" dimension in [`design-quality.md`](design-quality.md).

Core doctrine: **a great animation is felt, not noticed.** It serves comprehension (feedback, orientation, continuity, status), not decoration. If a motion does not map to a functional purpose below, the default is **no animation**.

---

## 1. The appropriateness gate (animate only where it helps)

Before adding any motion, pass it through this gate. Most UI should be **mostly still**.

### Functional purposes that justify motion
1. **Feedback** — confirm the system registered an action (a panel slides in rather than popping); most valuable when a static change could be missed.
2. **State change** — communicate a transition between modes/views (expand/collapse, toggle fill, loading → ready, icon morph).
3. **Orientation & continuity** — show where you are and where you came from (overlays, drawers, push/pop nav, shared-element "grow into detail"); prevents disorientation, especially on small viewports.
4. **Focus / attention** — draw the eye to one meaningful change without extra copy (a newly added row settling once).
5. **Relationships** — show what spawned what (menu from its trigger, result from its source).
6. **Progress / system status** — loaders, skeletons, and progress for work that takes more than ~1s.

### Animate — YES (subtle, fast, purposeful)
- Modal / dialog / sheet / drawer enter & exit; menu/popover reveal.
- Expand/collapse (accordion, `<details>`), toggle/checkbox/switch state.
- Shared-element / continuity transitions into a detail view.
- Navigation transitions that signal hierarchy and direction (forward vs back).
- Loading / progress / skeletons for waits over ~1s.
- One or two **hero moments** on a marketing/landing page (see Mode G).

### Animate — NO (or strongly restrain)
- **High-frequency and keyboard-initiated actions** — typing, command palette, hotkeys, save, repeated utility clicks. Repeated motion makes an action feel slow and is the #1 over-animation trap. *Never animate keyboard-initiated commands.*
- **Dense dashboards and data tables** — sorting, filtering, row/cell re-layout. Prioritize density, legibility, and performance over motion.
- **Forms** — field-to-field transitions, or validation that animates instead of simply appearing where it's needed.
- **Anything encountered repeatedly in a session** — repeated motion becomes a roadblock that lengthens task time.
- **Above-the-fold core content** — never animate the logo, headline, or primary value proposition; reveal-on-scroll of body text delays reading and gets ignored as ad-like.
- **Auto-playing / scroll-jacking / parallax** by default — bad for usability and accessibility; gate behind clear intent and reduced-motion.

> The frequency rule: **the more often a user repeats an action, the less it should be animated.** Restraint is the mark of mature motion design.

---

## 2. Duration

- Working range **100–500ms**; **100–400ms** covers almost all UI. Beyond ~500ms a transition starts to feel like a drag (web.dev / NN/g).
- Simple feedback (toggle, checkbox): **~100ms** — feels like direct manipulation.
- Modal / dialog / sheet enter: **200–300ms**.
- Reserve **~400ms** for large elements / large travel only.
- **Duration scales with travel and size:** small elements move faster, large surfaces slower.
- **Asymmetric enter/exit:** things should leave slightly faster than they arrive (e.g., enter 300ms, exit 200–250ms).

Reference duration scales: Material 3 short 50/100/150/200, medium 250/300/350/400, long 450/500/550/600, extra-long 700–1000ms. IBM Carbon (productive) fast-01 70ms, fast-02 110ms, moderate-01 150ms, moderate-02 240ms, slow-01 300ms, slow-02 400ms.

---

## 3. Easing curves (the palette)

**Never use `linear` for UI movement** — it looks mechanical. Match the curve to the motion's direction:

- **Entering / appearing → ease-out** (fast start, gentle settle; feels responsive).
- **Exiting / disappearing → ease-in** (gentle start, accelerate away).
- **Moving between two on-screen positions → ease-in-out / "standard"**.
- **`linear` is correct only for continuous/looping motion** — spinners, marquees, indeterminate progress.

### Generic, safe defaults (Material-derived "standard" set)
| Role | `cubic-bezier()` |
|------|------------------|
| Enter (ease-out) | `cubic-bezier(0, 0, 0.2, 1)` |
| Move (standard / ease-in-out) | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Exit (ease-in) | `cubic-bezier(0.4, 0, 1, 1)` |
| Continuous (linear) | `linear` |

### Design-system tokens (use when you want a defensible, accessible default)
**Material 3** (note: the value commonly mislabeled "emphasized" is actually M3 **Standard**):
- Standard `cubic-bezier(0.2, 0, 0, 1)` · Standard-decelerate (enter) `cubic-bezier(0, 0, 0, 1)` · Standard-accelerate (exit) `cubic-bezier(0.3, 0, 1, 1)`.
- Emphasized (for hero moments) is a two-arc curve, not a single bezier; CSS approximates its decelerate portion as `cubic-bezier(0.05, 0.7, 0.1, 1)` (and emphasized-accelerate `cubic-bezier(0.3, 0, 0.8, 0.15)`).

**IBM Carbon v11** — *productive* (utilitarian UI) vs *expressive* (notable moments):
- Productive: standard `cubic-bezier(0.2, 0, 0.38, 0.9)` · entrance `cubic-bezier(0, 0, 0.38, 0.9)` · exit `cubic-bezier(0.2, 0, 1, 0.9)`.
- Expressive: standard `cubic-bezier(0.4, 0.14, 0.3, 1)` · entrance `cubic-bezier(0, 0, 0.3, 1)` · exit `cubic-bezier(0.4, 0.14, 1, 1)`.

Default to a **standard/productive** curve for app and utility surfaces; reserve **emphasized/expressive** for the rare hero moment. (Avoid the legacy Carbon v10 curves like `cubic-bezier(0.5, 0, 0.1, 1)` — superseded.)

### Spring-like easing in CSS — the `linear()` function
CSS `linear()` (Baseline widely available since 2023: Chrome/Edge 113, Firefox 112, Safari 17.2) approximates springs and bounces with multivariate points, e.g. a gentle overshoot. Use it for spring feel without JS; generate the points with a tool (Josh Comeau's generator, the `linear()` easing generators) rather than by hand.

---

## 4. Spring vs tween (duration-based)

- **Tween (duration + easing curve):** discrete, one-shot transitions — enter/exit, expand/collapse, fades. Predictable; the default for most UI.
- **Spring (physics):** interactive, gesture-driven, interruptible, or continuous motion — drag, swipe, layout reflow, anything that should react naturally to velocity. Springs have no fixed duration; they settle.

Motion's modern, intuitive spring API is **duration-based**: set `bounce` (default `0.25`; `0` = no overshoot, higher = bouncier) and a `duration`, no physics tuning needed. The classic physics config (widely cited default) is `stiffness: 100, damping: 10, mass: 1`. Rule of thumb: **spring for interactive/gesture/layout, tween for discrete enter/exit.**

---

## 5. Build mechanism — CSS → WAAPI → library (in that order of preference)

Pick the lightest tool that does the job. Animate from this capability ladder:

1. **CSS `transition` (default)** — for state changes on `:hover`, `:focus-visible`, `:active`, toggled classes, `[data-state]`. Baseline, zero JS, cheapest. Use for ~80% of UI motion.
2. **CSS `@keyframes`** — for multi-step or looping motion (spinners, pulse, shimmer skeletons).
3. **Web Animations API — `element.animate()`** — Baseline widely available (cross-browser since ~2020). The no-dependency **JS** primitive when you need to animate dynamically, sequence, or **interrupt/reverse** an animation (e.g., a half-open drawer the user grabs back). Prefer it over hand-rolled `requestAnimationFrame` loops.
4. **View Transitions API** — for shared-element / page-to-page continuity:
   - *Same-document (SPA)* — Baseline **Newly available (Oct 2025)**: Chrome/Edge 111+, Safari 18+, Firefox 144+ (`document.startViewTransition()`). Automates the FLIP technique for you. Firefox lacks view-transition *types* initially.
   - *Cross-document (MPA, `@view-transition { navigation: auto }`)* — **not Baseline**: Chromium 126+ and Safari 18.2+, not Firefox. Treat as **progressive enhancement** — non-supporting engines snap without animation (graceful).
5. **CSS scroll-driven animations (`animation-timeline: scroll()/view()`)** — **NOT Baseline (Limited availability):** Chromium 115+ and Safari 26, Firefox behind a flag (~85% global). Use only as progressive enhancement, always wrapped in `@supports (animation-timeline: scroll())` with a non-animated fallback; never make core content depend on it. (A JS polyfill exists but runs on the main thread and defeats the perf win — use sparingly.)
6. **Libraries — only when the above don't suffice:**
   - **Motion** (motion.dev, formerly Framer Motion) — MIT, hybrid engine that uses native WAAPI where possible; `layout` prop is FLIP under the hood; springs, gestures, scroll. For React/JS/Vue apps with rich interaction.
   - **GSAP** — now **100% free including all former Club plugins** (SplitText, MorphSVG, DrawSVG, ScrollSmoother, MotionPath), commercial use included (April 2025, under Webflow). For complex timelines, text effects, SVG, and award-grade marketing motion.
   - **Lottie / dotLottie** — MIT runtimes; pre-rendered vector animations (loaders, onboarding, icon illustration). Prefer `.lottie` over large JSON; provide a static fallback for reduced-motion.
   - **Rive** — interactive, state-machine-driven animation when you need genuine real-time interactivity (hover/drag/state-reactive) beyond Lottie's pre-rendered model.

Name the chosen mechanism and its scope in the spec/handoff, and gate any non-Baseline feature against `caniuse`/MDN Baseline with a fallback (see [`sources.md`](sources.md)).

---

## 6. Performance (motion must stay at 60fps and protect Core Web Vitals)

- **Animate only `transform` and `opacity`** — they run on the compositor thread and hold 60fps even on low-end devices. Use `transform: translate/scale/rotate` for movement/resize and `opacity` for show/hide.
- **Never animate layout/paint properties** for motion: `top/left/width/height/margin` (trigger layout), `background-color/box-shadow/color` (trigger paint) — these cause jank.
- **`will-change`** only on confirmed jank, on elements truly about to animate; add/remove via JS for infrequent changes — leaving it on permanently wastes GPU memory.
- **Core Web Vitals:** motion must not regress **INP** (≤ 200ms — keep handlers light, don't block the main thread) or **CLS** (≤ 0.1 — never animate layout; reserve space). Entrance animations on the LCP element can delay LCP — don't gate the hero behind a reveal.

---

## 7. Accessibility (reduced-motion is mandatory, and it means *reduced*, not just off)

- **Honor `prefers-reduced-motion: reduce`** for everyone who asks. The right pattern is to **replace** large motion (translate/scale/parallax) with an instant or **opacity-only** change — not necessarily to remove all feedback. Color/opacity state changes are not "motion" and may remain.
- Never **gate content behind motion**; the page must be fully usable with animation off.
- Remove parallax, auto-advancing carousels, and scroll-jacking under reduced-motion; provide pause/stop controls for anything that moves for more than 5s (WCAG 2.2.2). Respect WCAG 2.3.1 (no flashing > 3×/s) and 2.3.3 Animation from Interactions (AAA).
- Motion must never replace a non-color or text cue, and focus/keyboard operability must survive every transition (focus moves to the opened dialog; restores on close).

The canonical shape:

```css
.panel { transition: transform 240ms cubic-bezier(0, 0, 0.2, 1), opacity 240ms; }
@media (prefers-reduced-motion: reduce) {
  /* keep the state change legible, drop the travel */
  .panel { transition: opacity 120ms linear; transform: none; }
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; }
}
```

---

## 8. How a mode should propose motion

When a mode (A/C/F/G) packages interaction polish, emit a compact **Motion plan**, not "add animations":

```md
## Motion plan
- Where: [the 1–3 surfaces that earn motion + the functional purpose each serves]
- Where NOT: [explicitly: high-frequency/keyboard actions, tables, forms — left still]
- Tokens: [duration + named easing curve per transition, e.g. "drawer enter 240ms ease-out cubic-bezier(0,0,0.2,1); exit 200ms ease-in"]
- Mechanism: [CSS transition / @keyframes / WAAPI / View Transitions / library — and why]
- Reduced-motion: [the fallback — opacity/instant]
- Performance: [transform/opacity only; INP/CLS safe]
```

A Mode D review should flag both **missing** functional motion (no feedback on a slow action) and **over-animation** (motion on tables, forms, or keyboard actions) — under the Design quality or Performance (Core Web Vitals) lens — and reflect it in the "Interaction polish & motion" rubric dimension.

---

## 9. Resources — where to find new, wow-effect motion patterns

Every resource below optimizes for visual impact, **not your constraints**. Before shipping anything sourced here, re-check the firewall: **`prefers-reduced-motion` fallback, keyboard/focus operability, and `transform`/`opacity`-only performance.** Inspiration is never evidence (see [`inspiration-sources.md`](inspiration-sources.md)).

**Tier 1 — Learn (principles + production technique):**
- **Emil Kowalski — animations.dev** (paid course) and the free essay **"Great animations"** (emilkowal.ski/ui/great-animations) — the best short reference on taste: <300ms, ease-out, transform/opacity only, interruptible, reduced-motion, never animate keyboard actions.
- **Josh Comeau** (joshwcomeau.com/animation) — rigorous free explainers (easing, springs, FLIP, CSS `linear()`).
- **web.dev / MDN** (web.dev/learn/accessibility/motion, MDN `prefers-reduced-motion`) — the authoritative performance + accessibility guardrails. Cross-check every flashy demo against these.

**Tier 2 — Build (copy-paste, production-oriented; still audit a11y/perf):**
- **Motion — motion.dev/examples** — 378+ examples across React/JS/Vue, copy-paste, MIT.
- **hover.dev** — animated React + Tailwind sections (heroes, pricing, navs, cards) on Motion/JS.
- **Lottie / LottieFiles** — pre-rendered vector animations; MIT runtimes; prefer `.lottie`.
- **Rive** — interactive state-machine animation.
- **CodePen** — vast technique pool; unvetted — scratch material, never paste blind.

**Tier 3 — Inspire (look and feel; not code to copy):**
- **Codrops / Tympanus** (tympanus.net/codrops) — bleeding-edge tutorials + demos (GSAP, scroll-driven, WebGL/shaders). Adapt, don't lift — most demos ship no reduced-motion/perf fallback.
- **Awwwards** (/websites/animation, /websites/motion, /websites/gsap) — award-grade motion in the wild; spectacle over performance — inspiration only.
- **Godly** (godly.website) — hand-curated, animated thumbnails preview motion before you click; motion-forward.
- **Refero / Mobbin** — real product screens and flows (mostly static; pattern reference, not motion code).

**Safe defaults (anchor restrained, accessible motion here first):**
- **Material 3 motion** (m3.material.io) and **IBM Carbon motion** (carbondesignsystem.com) — tokenized easing/duration scales and a reduced-motion stance. Reach for Tier 3 only when a wow moment is genuinely warranted.
