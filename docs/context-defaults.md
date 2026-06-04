# Context-Aware Defaults

These are starting-point defaults tuned to context, not rules. Apply the relevant ones, then override with anything the user states explicitly. When signals conflict, resolve with the precedence ladder at the bottom and surface the resolution in `Assumptions`.

Context has four dimensions: **audience × domain × platform/browser × use-context.**

---

## Audience defaults

| Audience | Type & spacing defaults | Interaction & density defaults |
|----------|-------------------------|--------------------------------|
| General consumer | 16px/1rem body, 1.5 line-height, ~65ch measure | comfortable density, generous tap/click targets (≥ 24px, prefer 44px), clear single primary action |
| Older adults / low vision | 18–20px body, higher contrast (aim 7:1 where feasible), larger targets (≥ 44px) | avoid hover-only affordances, persistent labels, forgiving error recovery, respect 200% zoom |
| Power users / professionals | 14–16px body, denser presets allowed | keyboard shortcuts + command palette, real data tables, multi-pane, hover row actions, exploit desktop density |
| Children | larger type, simple vocabulary, high contrast | large targets, minimal text entry, no dark patterns |
| Mixed / unknown | 16px/1rem body baseline | comfortable density, keyboard + pointer + touch all operable |

Audience defaults set the floor; never go below 16px body for primary content or below the 24px target-size minimum.

## Domain defaults

| Domain | Hierarchy & trust defaults | State & evidence defaults |
|--------|----------------------------|---------------------------|
| Marketing / landing | expressive, editorial craft; one dominant CTA; benefit-led headline | scroll narrative ordered by visitor questions; conversion claims as mechanisms, not lift % |
| Ecommerce | product clarity, price/availability prominent, trust signals near CTA | cart/checkout state coverage, error recovery, address/payment autocomplete |
| Content / publishing | reading-first: measure cap, type scale, generous rhythm | reading progress, subscription/paywall states handled honestly |
| Docs / dev portal | scannability, search, persistent sidebar + on-page TOC, code blocks | versioning, copy-to-clipboard, deep-linkable headings, zero-results search |
| Web app / dashboard | density and task efficiency; tables first-class; keyboard power-use | loading/empty/error per widget, optimistic UI, session-expired handling |
| Fintech / health / gov (high-trust) | restrained visual language, clarity over flair, explicit confirmations | strong error prevention/recovery; never claim compliance without verified evaluation |

Domain shapes hierarchy and trust language, not proof — see the packs in `docs/domain-packs/`.

## Platform / browser dimension

Web "platform" is two axes, not an OS:

- **Breakpoint set & strategy:** default mobile-first with a working layout down to 320px, scaling up the ladder (320 → 768 → 1024 → 1440+). Choose desktop-first only when the product is a desktop-dense web app and mobile-web is secondary — and still verify 320px reflow.
- **Browser/engine support matrix:** default to modern evergreen Chromium / WebKit / Gecko. Gate any non-trivial CSS/JS feature against `caniuse` / MDN Baseline and name a fallback. Call out engine-specific behavior (form controls, scrollbars, back-forward cache, font rendering) when it affects the design.
- **System preferences to honor by default:** `prefers-color-scheme` (provide a real dark theme), `prefers-reduced-motion` (provide a non-animated path), `forced-colors` (preserve focus/outlines), and a sensible print stylesheet for content/document pages.

## Use-context dimension

| Use-context | Defaults it forces |
|-------------|--------------------|
| Low bandwidth / slow CPU | lean payloads, lazy-load below the fold, protect LCP/INP; avoid heavy hero video |
| Keyboard-only / screen-reader | full keyboard operability, visible focus, focus management, skip links, correct semantics/landmarks |
| Wide viewport / large display | cap reading measure (~65ch), use whitespace and multi-column rather than stretched line length; exploit density for app surfaces |
| Anonymous-first vs returning-auth | anonymous: clarity, low-friction entry, deep-linkable; returning-auth: persistence, shortcuts, saved state, session-expired recovery |
| High-distraction / glance | strong first-glance hierarchy, large legible type, minimal required reading |

## Cross-dimension precedence ladder

When dimensions disagree, resolve in this order (highest wins):

1. **Safety and accessibility constraints** — never traded away for aesthetics or density.
2. **Regulated domain constraints** (finance, health, government) — clarity, error prevention, honest evidence.
3. **Use-context constraints** (low bandwidth, keyboard-only/screen-reader, wide-viewport, anonymous-first).
4. **Audience constraints** (older adults, power users, children).
5. **Breakpoint/browser defaults** (the platform axes above).

State the resolution in `Assumptions` so the user can correct a misclassification. Example: a dense data table (audience: power users) for a regulated finance product (regulated domain) keeps the density but adds the stronger confirmation, error-prevention, and contrast the regulated tier requires — the regulated constraint outranks the density default, but neither overrides the accessibility floor.
