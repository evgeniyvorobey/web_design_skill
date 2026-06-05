# Design-Tool Interop & Handoff

This layer lets the skill **consume designs from any design tool** and **emit handoff the tool can read back** — without binding to any one vendor. It is a neutral contract: a tool-agnostic input schema + a standards-based output, with **thin vendor profiles** (Figma, Pencil, Penpot, Sketch, Framer) on top.

**Boundary (read this first).** This is a prompt-based skill: it cannot open a `.fig` or `.pen` file or call a vendor API itself. The **host's MCP connector** does the I/O (extracts the design, pushes the tokens); the skill does the **reasoning** — reviewing the extract (Mode D), specifying it (Mode C), and producing the handoff + tokens (Mode F). The two compose; the skill never claims to read or write a tool's files. Where no connector is available, a screenshot or rendered URL is the fallback input, with the usual evidence limits.

The durable anchor is the **W3C Design Tokens Community Group (DTCG) format, version 2025.10** — its first *stable* release (a *Final Community Group Report*, 28 Oct 2025). DTCG is an open, vendor-neutral community standard (a Community Group Report, not a formal W3C Recommendation — phrase it that way). Anchor on **2025.10**. Emit the **portable curly-brace alias** (`{group.token}` — the spec's recommended reference syntax) and do **not** emit `$ref` (JSON-Pointer aliases), `$root`, or `$extends`: those are *normative in 2025.10*, but design tools, Tokens Studio, and the Style Dictionary pipeline have thin/uneven round-trip support for them, so a token using them would not round-trip back into a tool. (Treat the moving `/TR/drafts/` preview as ahead-of-stable.)

---

## 1. The input side — a neutral "design extract" schema

Whatever tool the host pulls from, normalize it to this minimal, vendor-neutral shape so the modes never depend on a tool's native model:

```jsonc
// design-extract (neutral) — what a host's MCP connector should hand the skill
{
  "source": { "tool": "figma|pencil|penpot|sketch|framer", "fileKey": "…", "extractedAt": "…" },
  "themes": { "mode": ["light", "dark"] },          // theming axes, if any
  "variables": { /* normalize to DTCG tokens — see §2 */ },
  "nodes": [
    {
      "id": "…",                 // unique; never contains "/"
      "type": "frame|group|text|rectangle|ellipse|image|icon|instance|…",
      "name": "Buy box",
      "box": { "x": 0, "y": 0, "w": 360, "h": 480 },
      "layout": { "mode": "vertical", "gap": 16, "padding": [24,16,24,16],
                  "justify": "start", "align": "stretch" },
      "text": { "content": "Add to cart",
                "style": { "fontFamily": "Inter", "fontSize": 16, "fontWeight": 600,
                           "lineHeight": 1.5, "letterSpacing": 0, "align": "center" } },
      "fills": [ { "kind": "solid", "tokenRef": "color.action.primary", "hex": "#0066cc" } ],
      "component": { "isOrigin": false, "ref": "Button/primary",
                     "overrides": { "label": "Add to cart" } },
      "states": ["default","hover","focus-visible","disabled"],
      "children": [ /* … */ ]
    }
  ]
}
```

Rules for the adapter:
- **Token-first:** every fill/size/type value that resolves to a variable carries a `tokenRef` (its DTCG path); only un-tokenized values carry a raw literal — and a raw literal is a **"rogue style" signal** to flag in review.
- **Names:** map a tool's `/`-delimited variable names (`color/action/primary`) to the dotted DTCG path (`color.action.primary`); node `id`s must not contain `/`.
- **Provenance:** keep the tool's native ids/keys under `$extensions` (see §2), never in the neutral fields, so the contract stays tool-neutral.

### How Mode D ingests an extract (stronger than a screenshot)
A **structured design extract** is a higher-confidence D1 input than a screenshot: the skill can assert layer-level facts it cannot from pixels — exact sizes, spacing, token names, the heading outline from text nodes, whether values are tokenized, component/state coverage. Still mark as **unverifiable** anything the extract does not contain: rendered pixels, runtime/INP, actual contrast (unless concrete colors are given — then compute it), and focus behavior (unless states/interactions are described). A D1 review backed by an extract may score the structural and token dimensions confidently and hold the purely visual ones at provisional until a render is available.

---

## 2. The output side — design tokens in DTCG 2025.10

Emit foundations as a `.tokens.json` file (media type `application/design-tokens+json`; extension `.tokens` or `.tokens.json`). A token is any JSON object with a `$value`; a group is an object without one. Reserved keys are all `$`-prefixed: `$value` (required), `$type`, `$description`, `$extensions` (vendor data, reverse-domain keys), `$deprecated`. Names are case-sensitive and must not contain `$`, `{`, `}`, or `.`. Reference another token by its dotted path: `"{group.token}"`.

**2025.10 value shapes (note the breaking, modern object forms — not bare strings):**

| `$type` | `$value` shape (exact) |
|---------|------------------------|
| `color` | `{ "colorSpace": "srgb", "components": [r,g,b], "alpha": 0–1, "hex": "#rrggbb" }` — an **object**, not a bare hex (2025.10 added CSS Color 4 spaces: `srgb`, `display-p3`, `oklch`, …; keep `hex` as a fallback) |
| `dimension` | `{ "value": 16, "unit": "px" }` (`px` or `rem`) — an **object**, not `"16px"` |
| `fontFamily` | string or array (fallback stack) |
| `fontWeight` | number 1–1000 or keyword (`"bold"`) |
| `number` | JSON number |
| `duration` | `{ "value": 200, "unit": "ms" }` |
| `cubicBezier` | `[x1, y1, x2, y2]` |
| `typography` (composite) | `{ "fontFamily", "fontSize"(dimension), "fontWeight", "letterSpacing"(dimension), "lineHeight"(number) }` |
| `shadow` (composite) | `{ "color", "offsetX", "offsetY", "blur", "spread" }` (object or array; note `offsetX/offsetY`, not `x/y`) |
| `border`, `transition`, `gradient`, `strokeStyle` | composite per spec |

**Theming:** 2025.10 supports light/dark/brand variants without duplicating files; emit one resolved token set per theme axis value (e.g. `mode: light|dark`), or carry mode value-sets under `$extensions`. A minimal example lives in [`../examples/design-tool/tokens.tokens.json`](../examples/design-tool/tokens.tokens.json).

**Downstream pipeline (what the host runs):** `design tool → DTCG .tokens.json → Style Dictionary → platform outputs`. Style Dictionary (Amazon) transforms the tokens into **CSS custom properties**, a **Tailwind config**, iOS/Android, etc. So the skill's job is to emit clean, aliased DTCG; the convention to target is `color.action.primary → --color-action-primary → var(--color-action-primary)`. Flag any hardcoded (non-tokenized) value as a defect, since it cannot round-trip.

---

## 3. The handoff payload (Mode F output target)

Modern handoff is **Dev-Mode-native and live** — the static "export a spec doc" (Zeplin-era) flow is dead. The skill's Mode F handoff should mirror what Dev Mode + annotations + tokens collectively expose, tool-agnostically:

1. **Overview / intent** — feature, user flow context.
2. **Ready-for-dev scope** — a per-screen/per-component status flag mirroring Dev Mode's `Ready for dev` / `Completed`.
3. **Design tokens (foundations)** — the DTCG set from §2, as name + resolved value + `var(--…)` reference, grouped by category (color, typography, spacing, radius, stroke, shadow, opacity, breakpoint).
4. **Component & state map** — props/variants and every state (default, hover, focus-visible, active, loading, empty, error, success, disabled).
5. **Measurements / redlines** — layout, spacing, sizing from the spacing scale.
6. **Accessibility annotations** — semantic role, name, focus order, contrast pairs, target sizes, reduced-motion.
7. **Responsive / breakpoint notes** — behavior across the ladder; 320px reflow.
8. **Interaction & motion specs** — easing/duration tokens, triggers, reduced-motion. **This is the skill's value-add: motion is *not* auto-captured by Dev Mode**, so the skill should author it from [`motion-and-animation.md`](motion-and-animation.md).
9. **Assets** — export-ready icons/images.
10. **Edge cases + acceptance criteria** — empty/error/loading and the 404/500/offline/session-expired states.

---

## 4. Vendor profiles (thin shims)

Each profile is just: how the host gets data IN, how the native model maps to the neutral schema (§1) and DTCG (§2), and the caveats. Priority reflects 2025 usage. The profiles here are the **conceptual** mapping; the **concrete, ordered call sequences** (exact tool names, inputs, returns, and the reverse-write path) live in [`design-tool-runbooks.md`](design-tool-runbooks.md) — a numbered READ runbook and a numbered REVERSE (DTCG → native variables) runbook per tool. Each profile below points at its runbook.

### Figma (dominant — the default target)
- **In:** the official Figma MCP/Dev Mode (`get_variable_defs`, `get_code`, `get_design_context`, `get_metadata`) or the REST API: `GET /v1/files/:key` (object model `DOCUMENT → CANVAS → FRAME → …`, UPPERCASE node enums) and `GET /v1/files/:key/variables/local` (returns modes; OAuth `file_variables:read`).
- **Variables → DTCG:** a `Variable` has `resolvedType` ∈ `COLOR|FLOAT|STRING|BOOLEAN`, `valuesByMode`, `scopes`, `codeSyntax{WEB,ANDROID,iOS}`. Map COLOR (RGBA 0–1) → DTCG `color`; FLOAT → `dimension` (scopes `CORNER_RADIUS/WIDTH_HEIGHT/GAP/FONT_SIZE/LINE_HEIGHT/LETTER_SPACING`) or `number`/`fontWeight`; STRING → `fontFamily` (scope `FONT_FAMILY`) or `string`; a per-mode `VariableAlias {type:"VARIABLE_ALIAS", id}` → DTCG `"{path}"`; collection modes → DTCG theming; ids/keys/scopes → `$extensions["com.figma"]`.
- **Caveat:** the **variables REST endpoints are Enterprise-plan-gated**; outside Enterprise, rely on the Dev Mode MCP or a Tokens Studio export. Dev Mode surfaces variables as `var(--…)` only when **Code Syntax** is set.
- **Runbook:** [`design-tool-runbooks.md`](design-tool-runbooks.md) → *Figma READ* (`get_metadata` → `get_variable_defs` → `get_design_context`, or REST `GET …/variables/local`) and *Figma REVERSE* (DTCG → Variables via `use_figma` Plugin API — **not** Enterprise-gated — or REST `POST /v1/files/:key/variables`).

### Pencil (`.pen`)
- **In:** the Pencil MCP only — `get_editor_state(include_schema:true)`, `get_variables`, `export_nodes`, `get_screenshot`, `batch_get`. The `.pen` file is **opaque/encrypted via the connector** (never `Read`/`Grep` it), and a file must be open in the editor.
- **Model (format version "2.13"):** a JSON `Document { version, themes{axis:[values]}, imports, variables, children }`. Nodes have `id` (no `/`), `type` (`frame|group|text|rectangle|ellipse|image|icon|ref|script|…`), `x/y`, and `reusable?` (true = component origin); frames carry `layout` (`none|vertical|horizontal`), `gap`, `padding`, `justifyContent`, `alignItems`, and `fit_content`/`fill_container` sizing; a `ref` node is a component instance with `descendants` overrides (slash-path). Map `themes` axes → DTCG theming, `variables` → DTCG tokens, the node tree → the neutral §1 schema.
- **Runbook:** [`design-tool-runbooks.md`](design-tool-runbooks.md) → *Pencil READ* (`get_editor_state(include_schema:true)` → `get_variables` → `batch_get`) and *Pencil REVERSE* (DTCG → `set_variables`, aliases resolved to concrete hex/number values, then `batch_design`).

### Penpot (open-source / self-host)
- **In:** Penpot's API/export; it is **standards-leaning** — the first platform to integrate the DTCG design-tokens format (built with Tokens Studio). Its token export uses DTCG keys but Tokens-Studio value conventions (bare hex, `"16px"` strings, TS type names, a `$themes`/`$metadata` envelope), so the adapter normalizes values to the DTCG object shapes and resolves `{reference}` aliases. The right profile when the team wants no vendor lock-in or self-hosting.
- **Runbook:** [`design-tool-runbooks.md`](design-tool-runbooks.md) → *Penpot runbook-lite* (connector-dependent; convert the Tokens-Studio-flavored export to/from DTCG object shapes).

### Sketch (Mac)
- **In:** Sketch's native token export (Document Details → Export Design Tokens), in the **Amazon Style Dictionary** format — not W3C DTCG — so the adapter does a format conversion, not just normalization. Smaller share (~7%) but worth a thin profile for Mac-first teams. Map Color Variables → DTCG `color`, shared Text Styles → `typography`, Layer Styles → `color`/`shadow`/`border`; symbols → components (not tokens).
- **Runbook:** [`design-tool-runbooks.md`](design-tool-runbooks.md) → *Sketch runbook-lite* (Style Dictionary ↔ DTCG conversion; write call surface unverified).

### Framer (design → live site)
- **In:** Framer's output is a **hosted site/CMS**, not code or a token file — so this profile is about consuming a *published URL* (treat as a rendered artifact for Mode D / rendered-output QA) rather than extracting tokens. Capture its CMS/responsive behavior, not a `.tokens.json`.

### Builder.io / Visual Copilot (design-to-code)
- The **design → framework code** path: a host can run Visual Copilot to turn a Figma frame into component code; the skill then reviews/specs the result. Use it as a code-generation step the skill audits, not a token source.

### Legacy / out of scope
- **Adobe XD** — effectively discontinued (maintenance mode since 2023); treat only as a legacy import source, no live profile. **Webflow** — a site builder, not a token/handoff source; optional thin note only.

---

## 5. How the modes use this layer

- **Mode D (review):** accept a structured design extract (§1) as a high-confidence D1 input; assert layer/token facts; hold purely visual dimensions provisional until a render exists; flag rogue (un-tokenized) values.
- **Mode C (spec) / Mode F (handoff):** emit the handoff payload (§3) and, when foundations are in scope, a DTCG `.tokens.json` (§2). When the tokens are to be written **back** into a tool, follow the reverse runbook in [`design-tool-runbooks.md`](design-tool-runbooks.md) (Figma Variables / Pencil variables — mapping table, write-call sequence, idempotency, alias order). Author the motion specs from [`motion-and-animation.md`](motion-and-animation.md) — they are the part a design tool does not capture.
- **Self-review:** if a design tool / extract was provided, did I consume it as structured input (not just "a screenshot")? If I emitted tokens, are they valid DTCG 2025.10 (object color/dimension, aliases, theming) and is every value tokenized? Did I keep vendor data in `$extensions` and stay tool-neutral?

The skill stays a *design-and-reasoning* layer that **composes with** whatever connector the host has; it never pretends to be the connector.
