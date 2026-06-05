# Design-Tool Runbooks — read/extract & reverse-write call sequences

This doc is the **concrete, executable companion** to [`design-tool-handoff.md`](design-tool-handoff.md). The handoff doc holds the *conceptual contract* — the neutral "design extract" input schema (§1), the DTCG 2025.10 token output (§2), the Dev-Mode-style handoff payload (§3), and thin vendor profiles (§4). This doc holds the *runbooks*: exact, ordered tool-call sequences a host model can run, step by step, to pull a design out of a tool and normalize it into the neutral schema, or to take a DTCG `.tokens.json` and write it back as native variables.

Each runbook is **both documentation and directly runnable**: every step names the exact tool or REST endpoint, its inputs, what it returns, and the normalize action that maps the result onto the neutral schema or native model. Figma and Pencil are covered in full (READ + REVERSE); Penpot and Sketch are runbook-lite, with the call surface marked where it is connector-dependent or unverified.

## The boundary this layer keeps

The skill **reasons and orchestrates**; the **host's MCP connector executes the I/O**. The skill never opens a `.fig` or `.pen` file or calls a vendor API itself — it sequences the calls, supplies the inputs, and normalizes the outputs. The runbooks below are the orchestration the skill reasons about; the host's loaded connector (the official Figma MCP, the Pencil MCP, a REST client, …) is what actually runs each numbered call. Where no connector is available, a screenshot or rendered URL is the fallback input, with the usual evidence limits (rendered pixels, runtime/INP, real focus behavior stay unverifiable). This is the same honest boundary the whole interop layer keeps — the runbooks make the call sequence explicit without ever claiming the skill is the connector.

## How a runbook is structured

Every step is written as:

> **N. Action** — `tool_or_endpoint` (inputs) → *what it returns*. **Normalize:** how the result maps onto the neutral schema (§1 of the handoff doc) or, for reverse, onto the native model.

A READ runbook ends at a populated **neutral design-extract** (handoff §1) the modes can consume. A REVERSE runbook starts from a DTCG `.tokens.json` (handoff §2) and ends at native variables verified back in the tool. "Resolve aliases first" and "match by name for idempotency" are load-bearing — they appear in every reverse runbook and are spelled out per tool.

### DTCG features the runbooks emit (and deliberately avoid)

The runbooks emit only the **portable reference form** — a curly-brace alias string `"{group.token}"` as the whole `$value` — because that is what every target in scope resolves: Figma Variables (`VARIABLE_ALIAS`), Pencil variables (resolved to a concrete value), Penpot/Tokens Studio, and the downstream Style Dictionary pipeline. They do **not** emit `$ref` (JSON-Pointer aliases), `$root`, or `$extends` — although those are *normative in 2025.10*, design-tool round-trips and the Style-Dictionary / Tokens-Studio pipeline have thin and uneven support for those forms, so a token that used them would not round-trip into Figma or Pencil. Keeping to the curly-brace alias keeps every emitted artifact maximally interoperable. The durable DTCG contract (object `color`/`dimension`, the `typography` composite, theming, `$extensions`) lives in [`design-tool-handoff.md`](design-tool-handoff.md) §2 — anchored on **DTCG 2025.10**, the first stable release (a *Final Community Group Report*, 28 Oct 2025 — not a formal W3C Recommendation).

---

## Shared mapping tables (DTCG ↔ native)

These tables are referenced by both reverse runbooks. They are the **reverse mapping** from a DTCG `$type` to each tool's native representation. (Read runbooks invert the same rows: native value → DTCG.)

### Type mapping: DTCG `$type` → Figma → Pencil

| DTCG `$type` (and `$value` shape) | Figma variable (`resolvedType` + value) | Pencil variable (`set_variables`) |
|---|---|---|
| `color` — object `{colorSpace, components, alpha, hex}` | `COLOR` — RGBA object `{r, g, b, a}`, every channel **0–1**. From an sRGB DTCG token the `components` are already 0–1; if only `hex` is present, parse and divide each channel by 255; `alpha` maps to `a`. Non-sRGB spaces (display-p3, oklch) convert to sRGB or fall back to `hex`. | `{type: "color", value: "#rrggbb"}` — a **hex string**, not a DTCG object. Resolve the token to its `hex` (or convert components → hex). |
| `dimension` — object `{value, unit}` (`px` or `rem`) | `FLOAT` — a bare number. Resolve to **px** (`rem` → ×16, or the project root size). Set scope `WIDTH_HEIGHT` / `GAP` / `CORNER_RADIUS` / `FONT_SIZE` / `LINE_HEIGHT` / `LETTER_SPACING` per use. | `{type: "number", value: <px number>}` — resolve `rem` to px (note the assumed root size as a caveat). |
| `number` — JSON number | `FLOAT` — the number; scope `OPACITY` / `ALL_SCOPES` per use. | `{type: "number", value: <number>}` |
| `fontWeight` — number 1–1000 or keyword | `FLOAT` — the numeric weight (map keyword → number, e.g. `bold` → 700); scope `FONT_WEIGHT`. | `{type: "number", value: <weight>}` |
| `fontFamily` — string or array (stack) | `STRING` — the primary family (or a CSS stack string); scope `FONT_FAMILY`. | `{type: "string", value: "<family or stack>"}` |
| `boolean` | `BOOLEAN` — the boolean. | `{type: "boolean", value: <bool>}` |
| `duration` `{value, unit}` / `cubicBezier` `[x1,y1,x2,y2]` | No native variable type for motion. Carry as a `FLOAT` (ms) or keep in the handoff motion spec; do not invent a variable type. | No native variable type. Keep in the handoff motion spec. |
| `typography` (composite) | **Decompose** — Figma has no composite-typography variable. Emit one variable per sub-field (`fontFamily`→STRING, `fontSize`→FLOAT, `fontWeight`→FLOAT, `letterSpacing`→FLOAT, `lineHeight`→FLOAT) and/or build a Text Style that binds them. | **Decompose** — bind a text node's `fontFamily`/`fontSize`/`fontWeight`/`letterSpacing`/`lineHeight` fields to individual `$variables`; there is no composite typography variable. |
| `shadow` / `border` / `transition` / `gradient` / `strokeStyle` (composite) | **Decompose** into the underlying color + float variables and apply via an effect/stroke style; no single composite variable. | **Decompose**; apply via node properties bound to the underlying `$variables`. |

### Alias mapping: `{group.token}` → native reference

| DTCG | Figma (Plugin API) | Figma (REST) | Pencil |
|---|---|---|---|
| `"$value": "{color.brand.primary}"` | `figma.variables.createVariableAlias(targetVar)` → `{type: "VARIABLE_ALIAS", id}`, then `setValueForMode(modeId, alias)` | `value: {type: "VARIABLE_ALIAS", id}` where `id` is the target's real id **or** a `tempId` created earlier in the same POST | **Resolve to a concrete value.** Pencil binds variables into *properties* via a `$name` reference, but a variable *definition* takes a concrete primitive — flatten the alias chain to its terminal `hex`/number/string before writing. |

**Alias resolution order (every reverse runbook):** create/define the **target before the referrer**. Topologically sort the token graph — primitives first, then semantic, then component — so a `VARIABLE_ALIAS` (Figma) always points at an id that already exists, and so a Pencil resolve never chases an undefined token. Figma's REST POST lets a referrer reference a target's `tempId` *created earlier in the same payload*; a variable may not alias itself or form a cycle.

### Modes & themes mapping

| DTCG theming | Figma | Pencil |
|---|---|---|
| One value-set per theme-axis value (e.g. `mode: light` / `mode: dark`) | Collection **modes**: `collection.addMode("Dark")` → `modeId`; write each theme's value with `setValueForMode(modeId, value)` (REST: a `variableModes` entry + per-mode `variableModeValues`). | Themed array: `value: [{value, theme: {mode: "light"}}, {value, theme: {mode: "dark"}}]`. Theme axes/values **auto-register** — do not declare themes separately. |

### Figma scopes & code syntax

- **Scopes** gate where a variable is offered in the UI. Pick from the `resolvedType`-valid set: COLOR → `ALL_FILLS`, `FRAME_FILL`, `SHAPE_FILL`, `TEXT_FILL`, `STROKE_COLOR`, `EFFECT_COLOR`; FLOAT → `CORNER_RADIUS`, `WIDTH_HEIGHT`, `GAP`, `OPACITY`, `STROKE_FLOAT`, `FONT_WEIGHT`, `FONT_SIZE`, `LINE_HEIGHT`, `LETTER_SPACING`, …; STRING → `FONT_FAMILY`, `FONT_STYLE`, `TEXT_CONTENT`; or `ALL_SCOPES`.
- **Code Syntax** is what makes Dev Mode surface a variable as `var(--name)`. Set `WEB` to the CSS custom-property name (`--color-action-primary`) so the round-trip matches the skill's `color.action.primary → --color-action-primary → var(--color-action-primary)` convention. Keys are exactly `WEB`, `ANDROID`, `iOS` (lowercase `i`).

---

## Figma runbooks

Figma is the default target (~70–83% share). URLs decode as `figma.com/design/:fileKey/:name?node-id=:nodeId` — extract `fileKey` and `nodeId`, converting `-` → `:` in the node id (`1-2` → `1:2`). For a branch URL `figma.com/design/:fileKey/branch/:branchKey/:name`, use `branchKey` as the file key.

### Figma — READ runbook (extract → neutral schema)

MCP-first; the REST steps are the Enterprise alternative when the MCP connector is absent.

1. **Resolve the target** — parse the Figma URL → `fileKey` + `nodeId`. No node id in the URL → ask the user for a node-specific link (the MCP read tools require a concrete node).
2. **Confirm auth/plan** — `whoami` (no inputs) → the authenticated handle, email, and plan tier. Tier `enterprise` means the REST Variables endpoints (step 6) are reachable; otherwise rely on the MCP path. **Normalize:** record nothing user-facing; this only chooses the path.
3. **Map the structure** — `get_metadata` (`fileKey`, optional `nodeId`) → an XML overview: node ids, layer types, names, positions, sizes. Omit `nodeId` to list the document's top-level pages, then drill in. **Normalize:** seed `nodes[]` — each element's `id` (strip any `/`), `type` (lower-case the UPPERCASE Figma enum: `FRAME`→`frame`, `TEXT`→`text`, `INSTANCE`→`instance`), `name`, and `box {x, y, w, h}` from the position/size.
4. **Pull the token surface** — `get_variable_defs` (`fileKey`, `nodeId`) → the variable name→value map used on that subtree, e.g. `{"icon/default/secondary": "#949494", "space/md": 16}`. **Normalize:** map each `/`-delimited Figma name to a dotted DTCG path (`icon/default/secondary` → `icon.default.secondary`); attach it as the `tokenRef` on the fill/size it resolves, and add it to the extract's `variables` (as DTCG — see the type table). A node value with **no** matching variable is a raw literal → flag it as a **rogue (un-tokenized) style** in review.
5. **Get per-node design context** — `get_design_context` (`fileKey`, `nodeId`) → reference code + a screenshot + contextual metadata (the richest single call: layout, text content, fills, component references). **Normalize:** fill each node's `layout {mode, gap, padding, justify, align}`, `text {content, style{fontFamily, fontSize, fontWeight, lineHeight, letterSpacing, align}}`, `fills[]` (with `tokenRef` from step 4), and `component {isOrigin, ref, overrides}`.
6. **(Enterprise REST alternative)** — when no MCP connector is loaded and the user is a Full member of an Enterprise org (OAuth scope `file_variables:read`):
   - `GET /v1/files/:fileKey` → the node model `DOCUMENT → CANVAS → FRAME → …` with UPPERCASE enums (mirror of steps 3–5 from the file tree).
   - `GET /v1/files/:fileKey/variables/local` → `meta.variables{}` (keyed by `VariableID`) and `meta.variableCollections{}` (keyed by collection id, carrying `modes[]` + `defaultModeId`). Each variable has `resolvedType`, `valuesByMode`, `scopes[]`, `codeSyntax{WEB,ANDROID,iOS}`. **Normalize:** a COLOR `valuesByMode` value `{r,g,b,a}` (0–1) → DTCG `color` object; a `{type:"VARIABLE_ALIAS", id}` → DTCG `"{path}"` (look the id up in `meta.variables` for its dotted name); collection `modes[]` → the extract's `themes`; ids/keys/scopes → `$extensions["com.figma"]`.
7. **Capture renders & provenance (optional)** — `get_screenshot` (`fileKey`, `nodeId`, `maxDimension`) → a PNG for visual QA (hold contrast/focus *provisional* until rendered); `get_libraries` (`fileKey`) and `search_design_system` → library/component origin. **Normalize:** attach screenshot as the D1 render evidence; record library provenance under `$extensions`.
8. **Emit the neutral extract** — assemble `source {tool:"figma", fileKey, extractedAt}`, `themes`, `variables` (DTCG), and `nodes[]`. Hand it to Mode D as a high-confidence D1 input: assert layer/token facts confidently; hold purely visual properties provisional until a render exists.

### Figma — REVERSE runbook (DTCG tokens → Figma Variables)

Input: a DTCG `.tokens.json` (handoff §2). Two write paths — **Path A (`use_figma`)** is the default and is **not** Enterprise-gated; **Path B (REST)** is the Enterprise alternative. Pick by what the host has loaded and the user's plan. Apply the [type table](#shared-mapping-tables-dtcg--native) and the alias-order rule throughout.

**Pre-step (both paths) — flatten & order the token set:** resolve `$type` defaults from group `$type`; expand each token to `{dottedName, resolvedType, perModeValues, isAlias, aliasTarget, scope, cssVarName}`; **topologically sort** primitives → semantic → component so every alias target is created before its referrer.

#### Figma reverse — Path A: `use_figma` Plugin API (default, not Enterprise-gated)

`use_figma` runs JavaScript in the Figma plugin sandbox with the `figma` global, and the Plugin API can author variables directly — so this path works for **anyone who can edit the file** (no Enterprise/REST gate; the only tier limit is `addMode()`'s mode-count cap on free files).

1. **Load the skill** — the `/figma-use` skill is **MANDATORY** before calling `use_figma`; load it first.
2. **Get-or-create the collection (idempotent)** — in the `use_figma` `code`: `const cols = await figma.variables.getLocalVariableCollectionsAsync(); let col = cols.find(c => c.name === "Brand") || figma.variables.createVariableCollection("Brand");`
3. **Get-or-create one mode per theme axis value** — `col.modes.find(m => m.name === "Light")?.modeId ?? col.addMode("Light")` (wrap `addMode` in try/catch for the tier cap). The collection's default mode covers a single-theme token set.
4. **Get-or-create each variable by name + collection** — `const vars = await figma.variables.getLocalVariablesAsync("COLOR"); let v = vars.find(x => x.name === name && x.variableCollectionId === col.id) || figma.variables.createVariable(name, col, "COLOR");` — pass the **collection object** (passing a collection id is deprecated).
5. **Set the per-mode value** — literal: `v.setValueForMode(modeId, {r, g, b, a})` (channels 0–1) for COLOR, a number for FLOAT, a string for STRING. Alias: `v.setValueForMode(modeId, figma.variables.createVariableAlias(targetVar))` → `{type:"VARIABLE_ALIAS", id}`.
6. **Set Code Syntax & scopes** — `v.setVariableCodeSyntax("WEB", "--color-brand-primary")` (so Dev Mode shows `var(--color-brand-primary)`); `v.scopes = ["ALL_FILLS", "STROKE_COLOR"]` (a `resolvedType`-valid set).
7. **Repeat in topological order** — primitives first (concrete values), then semantic/component variables that alias them.

Worked, idempotent `use_figma` `code` (gets-or-creates, sets RGBA 0–1, code syntax, scopes, and an alias):

```javascript
// runs in the Figma plugin sandbox (global `figma`); load /figma-use first.
async function getOrCreateCollection(name) {
  const cols = await figma.variables.getLocalVariableCollectionsAsync();
  return cols.find(c => c.name === name) || figma.variables.createVariableCollection(name);
}
function getOrCreateMode(col, modeName) {
  const m = col.modes.find(x => x.name === modeName);
  return m ? m.modeId : col.addMode(modeName); // may throw on free-file mode cap
}
async function getOrCreateVar(name, col, type) {
  const vars = await figma.variables.getLocalVariablesAsync(type);
  return vars.find(v => v.name === name && v.variableCollectionId === col.id)
      || figma.variables.createVariable(name, col, type); // pass the collection OBJECT
}
async function run() {
  const col = await getOrCreateCollection("Brand");
  const light = getOrCreateMode(col, "Light");
  // primitive first (alias target must exist before the referrer)
  const primary = await getOrCreateVar("color/brand/primary", col, "COLOR");
  primary.setValueForMode(light, { r: 0, g: 0.4, b: 0.8, a: 1 }); // DTCG components 0..1
  primary.setVariableCodeSyntax("WEB", "--color-brand-primary");
  primary.scopes = ["ALL_FILLS", "STROKE_COLOR"];
  // semantic alias -> primitive
  const action = await getOrCreateVar("color/semantic/action", col, "COLOR");
  action.setValueForMode(light, figma.variables.createVariableAlias(primary));
  action.scopes = ["ALL_FILLS"];
}
run();
```

#### Figma reverse — Path B: REST `POST /v1/files/:key/variables` (Enterprise)

When the host has no plugin connector but the user is a Full member of an Enterprise org (OAuth scope **`file_variables:write`** + edit access). The endpoint is a single **atomic** bulk call — build the whole payload, send once (any validation error → HTTP 400, nothing persists).

1. **(Optional) read current state** — `GET /v1/files/:key/variables/local` to find existing collection/mode/variable ids so the POST can `UPDATE` rather than duplicate.
2. **Build the four action arrays** — `variableCollections[]`, `variableModes[]`, `variables[]` each take `action: "CREATE" | "UPDATE" | "DELETE"` plus an `id` (an existing real id, or an arbitrary `tempId` unique within the body). `variableModeValues[]` has **no** action (it is an upsert): `{variableId, modeId, value}`.
   - collection CREATE: `{action:"CREATE", id:"tmpCol", name:"Brand", initialModeId:"tmpLight"}`
   - mode CREATE: `{action:"CREATE", id:"tmpDark", name:"Dark", variableCollectionId:"tmpCol"}`
   - variable CREATE: `{action:"CREATE", id:"tmpPrimary", name:"color/brand/primary", resolvedType:"COLOR", variableCollectionId:"tmpCol"}`
   - mode value (literal): `{variableId:"tmpPrimary", modeId:"tmpLight", value:{r:0, g:0.4, b:0.8, a:1}}`
   - mode value (alias): `{variableId:"tmpAction", modeId:"tmpLight", value:{type:"VARIABLE_ALIAS", id:"tmpPrimary"}}` — references a `tempId` created **earlier** in the same payload (alias order).
3. **POST once** — `POST /v1/files/:key/variables` with that body → `{status, error, meta:{tempIdToRealId:{...}}}`. **Map** each `tempId` to its real id from `meta.tempIdToRealId` for any follow-up.
4. **Set scopes & code syntax** — include `scopes` and `codeSyntax{WEB:"--name"}` on the variable CREATE/UPDATE objects so Dev Mode surfaces `var(--name)`.

```json
{
  "variableCollections": [
    { "action": "CREATE", "id": "tmpCol", "name": "Brand", "initialModeId": "tmpLight" }
  ],
  "variableModes": [
    { "action": "UPDATE", "id": "tmpLight", "name": "Light", "variableCollectionId": "tmpCol" }
  ],
  "variables": [
    { "action": "CREATE", "id": "tmpPrimary", "name": "color/brand/primary", "resolvedType": "COLOR", "variableCollectionId": "tmpCol", "scopes": ["ALL_FILLS"], "codeSyntax": { "WEB": "--color-brand-primary" } },
    { "action": "CREATE", "id": "tmpAction", "name": "color/semantic/action", "resolvedType": "COLOR", "variableCollectionId": "tmpCol", "scopes": ["ALL_FILLS"] }
  ],
  "variableModeValues": [
    { "variableId": "tmpPrimary", "modeId": "tmpLight", "value": { "r": 0, "g": 0.4, "b": 0.8, "a": 1 } },
    { "variableId": "tmpAction", "modeId": "tmpLight", "value": { "type": "VARIABLE_ALIAS", "id": "tmpPrimary" } }
  ]
}
```

#### Figma reverse — idempotency, alias order, verify

- **Idempotency.** Re-running must not duplicate. Path A matches by `(name, variableCollectionId)` via the async getters before `create*`. Path B reads `variables/local` first and uses `action:"UPDATE"` with the real id for anything that already exists (matching by name + collection); only genuinely new tokens get `CREATE` + a `tempId`. Treat the variable **name** (and, for the round-trip, the `codeSyntax.WEB` value) as the identity key.
- **Alias order.** Create primitives before semantics before components; a Path-B alias may reference an earlier `tempId` in the same payload, never a later one; no self-alias / cycle.
- **Verify.** Re-call `get_variable_defs` on a node bound to the new variables (or `GET …/variables/local`) and confirm the names, per-mode values, and `codeSyntax`. Dev Mode shows `var(--name)` **only** when Code Syntax is set — if it is missing, the round-trip is incomplete.
- **Gating reminder.** Path A (`use_figma`) is not Enterprise-gated; Path B (REST) is. If neither is available (no plugin connector, non-Enterprise), the honest fallback is a Tokens Studio import the user runs — say so rather than implying the skill wrote the file.

---

## Pencil runbooks

The `.pen` file is **opaque/encrypted via the connector** — never `Read`/`Grep` it. **A file must be OPEN in the editor**, or every Pencil MCP call errors with *"A file needs to be open in the editor."* Node ids never contain `/`.

### Pencil — READ runbook (extract → neutral schema)

1. **Confirm a file is open & get the schema** — `get_editor_state` (`include_schema: true`) **first** → the authoritative `.pen` schema (format version `2.13`), the current selection, and essential design info. The schema is required before any other Pencil call is trustworthy. **Normalize:** set `source {tool:"pencil", extractedAt}`.
2. **Pull variables & themes** — `get_variables` (`filePath`) → the file's `variables` map (`{name: {type, value}}`, colors as hex strings, themed values as `[{value, theme}]` arrays) and the `themes` axes (`{mode: ["light","dark"]}`). **Normalize:** themes axes → the extract's `themes`; each variable → a DTCG token (color hex → DTCG `color` object with `hex` + sRGB components; number → `dimension` or `number`; string → `fontFamily`/`string`); a themed array → per-mode value-sets.
3. **Walk the node tree** — `batch_get` (`filePath`, `patterns`/`nodeIds`, `readDepth`, `searchDepth`, `resolveVariables`) → matching nodes and their children; start from the top level, then drill into ids shown as `"..."`. Use `patterns:[{reusable:true}]` to list component origins. **Normalize:** each node → a neutral node — `id` (no `/`), `type` (`frame|group|text|rectangle|ellipse|image|icon|ref|…`), `box`, `layout {mode: none|vertical|horizontal, gap, padding, justify (justifyContent), align (alignItems)}` plus `fit_content`/`fill_container` sizing, `text {content, style{fontFamily, fontSize, fontWeight, letterSpacing, lineHeight, align (textAlign)}}`, and `fills` carrying a `tokenRef` for any `$name`-bound property (a raw literal is a rogue-style signal). A `ref` node → `component {isOrigin:false, ref, overrides}` with the `descendants` slash-path overrides.
4. **Check layout health & capture renders (optional)** — `snapshot_layout` (`problemsOnly`) → layout problems to flag in review; `get_screenshot` (`nodeId` or `"document"`) / `export_nodes` → renders for visual QA. `get_guidelines` lists task guides/styles. **Normalize:** attach renders as D1 evidence; record layout problems as findings.
5. **Emit the neutral extract** — the assembled `source` + `themes` + `variables` (DTCG) + `nodes[]`, ready for Mode D as a high-confidence input.

### Pencil — REVERSE runbook (DTCG tokens → pencil variables)

Input: a DTCG `.tokens.json`. Pencil variable *definitions* hold **concrete primitives**; binding into nodes happens via a `$name` reference in properties (definition-level variable→variable aliasing has no defined resolution and is treated as unsupported). So the reverse path **resolves every alias** to its terminal value before writing.

#### Pencil reverse — write sequence, idempotency, verify

1. **Resolve & flatten the token set** — for each DTCG token compute its terminal concrete value: `color` → `hex` string (convert non-sRGB to sRGB hex; Pencil colors are hex, **not** DTCG objects); `dimension`/`number`/`fontWeight` → a bare number (resolve `rem`→px, noting the assumed root size); `fontFamily` → a string (primary family or a CSS stack); `boolean` → boolean. **Fully resolve `{group.token}` aliases** to the target's concrete value — do not pass `$name` as a variable *value*.
2. **Shape multi-theme tokens** — a DTCG token with per-mode values → a Pencil themed array `value: [{value:"#F8F5F0", theme:{mode:"light"}}, {value:"#1A1A1A", theme:{mode:"dark"}}]`. Theme axes auto-register; do not declare themes separately. Names **must not** start with `$`.
3. **Write the variables** — `set_variables` (`filePath`, `variables`, `replace:false`) where `variables` is the name-keyed map of `{type, value}`. Default `replace:false` **merges by name** — re-running updates in place rather than duplicating. Only use `replace:true` to wipe-and-replace the whole set.
4. **Apply variables into the design (optional)** — `batch_design` (`filePath`, `input`) to bind the new variables into nodes via `$name` references (e.g. a frame's `fill: "$color.semantic.action"`, `gap: "$dimension.space.md"`). Get the `batch_design` input grammar from `get_editor_state(include_schema:true)` first.
5. **Verify** — `get_variables` (`filePath`) and confirm names, types, resolved values, and per-theme entries match the source tokens. Pencil has no auto-save — remind the user to save.

```json
// set_variables payload — colors as hex, dimensions as numbers, aliases pre-resolved, a themed pair
{
  "filePath": "designs/dashboard.pen",
  "replace": false,
  "variables": {
    "color.brand.primary":   { "type": "color",  "value": "#0066cc" },
    "color.semantic.action": { "type": "color",  "value": "#0066cc" },   // {color.brand.primary} resolved
    "dimension.space.md":    { "type": "number", "value": 16 },
    "font.weight.bold":      { "type": "number", "value": 700 },
    "font.family.sans":      { "type": "string", "value": "Inter, system-ui, sans-serif" },
    "color.surface.bg": {
      "type": "color",
      "value": [
        { "value": "#ffffff", "theme": { "mode": "light" } },
        { "value": "#111418", "theme": { "mode": "dark"  } }
      ]
    }
  }
}
```

**Idempotency:** `set_variables` with `replace:false` keys by variable name, so a re-run with the same names is a no-op-or-update, never a duplicate — match by name. **Boundary:** the host's Pencil MCP runs `set_variables`/`batch_design` against the open file; the skill resolves the DTCG, builds the payload, and reasons about the result — it never opens the `.pen` itself.

---

## Penpot — runbook-lite

Penpot is the open-source / self-host, DTCG-leaning option — the first major tool to integrate the W3C design-tokens format (built with Tokens Studio). The call surface is **connector-dependent**: there is no standardized cross-tool tokens MCP, and a dedicated REST tokens-import endpoint is still "coming soon." Treat the host (an export the user runs, the personal-access-token REST API, or the partially-shipped plugin Tokens API) as what hands the skill the file.

- **READ (extract):** the host provides Penpot's **token JSON export** (Tokens panel → Tools → export; single file, or a multifile folder of one JSON per set plus `$themes.json` + `$metadata.json`). It uses DTCG keys (`$value`/`$type`/`$description`) but **Tokens-Studio value conventions** — a bare hex string (`"$value": "#f44336"`), unit strings (`"$value": "2px"`), Tokens-Studio type names (`borderRadius`/`spacing`/`fontFamilies` rather than DTCG `dimension`/`fontFamily`), and a non-DTCG `$themes`/`$metadata`/sets envelope. **Normalize** is thin but **not** a no-op: convert each value to the DTCG object shape (`color` → `{colorSpace, components, hex}`, `2px`/`16px` → `dimension {value, unit}`), collapse the Tokens-Studio type names to DTCG `$type`, resolve `{reference}` aliases, and evaluate any math expressions (DTCG cannot carry them). Penpot Sets → DTCG theming; Penpot components → the neutral node layer, not tokens.
- **REVERSE (write):** import the DTCG `.tokens.json` via the Tokens panel (import accepts a ZIP, a single JSON, or a multifile folder), or the plugin **Tokens API** (read/write tokens — note reported gaps in programmatic theme/set attachment). Convert DTCG object values back to the Tokens-Studio conventions Penpot reads on import (hex strings, `"16px"` unit strings, TS type names). **Verify** by re-exporting and diffing names/values. **Caveat:** the exact field-level fidelity of composite typography/shadow on Penpot export/import is unverified — confirm against a real export before relying on it.

## Sketch — runbook-lite

Sketch is Mac-only (~7% primary-tool share) — a thin profile. It exports tokens natively but in **Amazon Style Dictionary** format, **not** W3C DTCG, so the adapter does a genuine **format conversion**, not just normalization.

- **READ (extract):** the host provides a Sketch token export — Mac app: *Document Details → Export Design Tokens*; web app: *Color Variables → Export*. Color tokens export as CSS or JSON; Layer Styles and Text Styles as JSON only. The JSON is Style-Dictionary-shaped. **Normalize / convert:** Style Dictionary → DTCG — map **Color Variables → `color`**, **Text Styles → `typography`** (composite), **Layer Styles → `color`/`shadow`/`border`** per the style's properties. **Symbols do NOT export as tokens** — map Symbols to the neutral component/node layer.
- **REVERSE (write):** there is no documented DTCG-import path; Sketch's write surface is its native styles/variables, and its MCP server (Sketch 2025.2.4+, `run_code` over the SketchAPI) is Sketch-specific scripting, **not** a documented tokens endpoint. The honest reverse profile is: convert DTCG → Sketch Color Variables / Text Styles via the host's scripting connector if present, else hand the user a Style-Dictionary build and have them apply it. **Mark the write call surface as unverified** — do not imply a turnkey DTCG-import.

---

## Worked round-trip: `tokens.tokens.json` → Figma + Pencil

Take the example token file [`../examples/design-tool/tokens.tokens.json`](../examples/design-tool/tokens.tokens.json) (`color.brand.primary` = sRGB `[0, 0.4, 0.8]`/`#0066cc`; `color.semantic.action` = `"{color.brand.primary}"`; `dimension.space.md` = `16px`; `font.weight.bold` = `700`; `font.family.sans` = a stack; a `typography` composite). The reverse runbooks produce:

**Figma (Path A, `use_figma`)** — topological order, idempotent:

```javascript
const col = await getOrCreateCollection("Brand");          // get-or-create
const light = getOrCreateMode(col, "Light");
const primary = await getOrCreateVar("color/brand/primary", col, "COLOR");
primary.setValueForMode(light, { r: 0, g: 0.4, b: 0.8, a: 1 });   // components already 0..1
primary.setVariableCodeSyntax("WEB", "--color-brand-primary");     // Dev Mode -> var(--color-brand-primary)
primary.scopes = ["ALL_FILLS", "STROKE_COLOR"];
const action = await getOrCreateVar("color/semantic/action", col, "COLOR");
action.setValueForMode(light, figma.variables.createVariableAlias(primary)); // {color.brand.primary}
const md = await getOrCreateVar("dimension/space/md", col, "FLOAT");
md.setValueForMode(light, 16); md.scopes = ["GAP", "WIDTH_HEIGHT"];
// font.weight.bold -> FLOAT 700 (scope FONT_WEIGHT); font.family.sans -> STRING (scope FONT_FAMILY);
// typography composite -> decompose into the fontSize/fontWeight/fontFamily/lineHeight variables above.
```

**Pencil (`set_variables`)** — aliases resolved, colors as hex, dimensions as numbers:

```json
{
  "filePath": "designs/app.pen",
  "variables": {
    "color.brand.primary":   { "type": "color",  "value": "#0066cc" },
    "color.semantic.action": { "type": "color",  "value": "#0066cc" },
    "dimension.space.md":    { "type": "number", "value": 16 },
    "font.weight.bold":      { "type": "number", "value": 700 },
    "font.family.sans":      { "type": "string", "value": "Inter, system-ui, sans-serif" }
  }
}
```

Both writers are idempotent (match by name), resolve/order aliases (primitive `color.brand.primary` before the `color.semantic.action` referrer), and leave the I/O to the host connector. A round-trip is **complete** only when a re-READ (`get_variable_defs` / `get_variables`) returns the same names and values — and, for Figma Dev Mode, when Code Syntax makes them surface as `var(--…)`.

---

## Caveats & honest-boundary checklist

- **Figma write gating.** `use_figma` (Plugin API) is **not** Enterprise-gated — it works for any editor; the REST `POST /v1/files/:key/variables` path needs `file_variables:write` + a Full seat in an Enterprise org. State which path was used; if neither is available, say a Tokens Studio import is the fallback.
- **Idempotency (don't duplicate on re-run).** Match collections/variables by **name** (Figma: name + collection id, plus `codeSyntax.WEB`; Pencil: name with `replace:false`); use `UPDATE` over `CREATE` for anything that exists. Never blind-create.
- **Alias resolution order.** Create/define targets before referrers (topological: primitives → semantic → component). Figma aliases use `VARIABLE_ALIAS`; Pencil resolves aliases to concrete values (no definition-level aliasing). No cycles.
- **Modes/themes.** Figma collection modes ↔ Pencil themed arrays ↔ DTCG theme axes — one value per theme per token.
- **DTCG portability.** Emit object `color`/`dimension`, the `typography` composite, and curly-brace `{group.token}` aliases; never emit `$ref`/`$root`/`$extends` (normative in 2025.10, but uneven round-trip support across tools). Anchor on 2025.10 (handoff §2).
- **The boundary.** The skill **reasons and sequences** these calls; the **host's MCP connector executes** the file/API I/O. The runbooks are executable orchestration, not a claim that the skill opens `.fig`/`.pen` or calls the API itself. Where no connector exists, fall back to a screenshot/URL with the usual evidence limits — and say so.

See also: [`design-tool-handoff.md`](design-tool-handoff.md) (the conceptual contract), [`motion-and-animation.md`](motion-and-animation.md) (the motion specs a design tool does not capture, authored in Mode F), and [`self-review.md`](self-review.md) (the design-tool self-review gate).
