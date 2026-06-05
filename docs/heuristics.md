# Heuristics Catalog

This catalog is the named-law engine behind web design generation and Mode D reviews. Every entry gives the law, a concrete web application, and a red flag you can quote verbatim in findings. Web physics stay constant throughout: 16px / 1rem minimum body text, a measure near 65ch, a 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 spacing scale, WCAG 2.2 AA, full keyboard operability, Core Web Vitals targets (LCP <= 2.5s, INP <= 200ms, CLS <= 0.1), and simultaneous mouse + keyboard + touch input on the same page.

The web is multi-pane, multi-tab, and long-scroll. Pages are deep-linkable, resizable, zoomable, and printed. Nothing here assumes a fixed viewport or a single forward path; design for reflow, back/forward navigation, and parallel tabs.

---

## Interaction laws (Fitts, Hick, Doherty)

**Fitts's Law** (Paul Fitts, 1954). Time to acquire a target grows with cursor travel distance and shrinks with target size: `MT = a + b * log2(D/W + 1)`. On the web this is about cursor travel + hit-area size + the four screen edges and four corners, which are effectively infinitely deep because the pointer stops at them — no overshoot is possible. Apply it: make primary actions large and close to where the eye already is; pin global navigation, scroll-to-top, and account menus to edges/corners so they are cheap to hit; give links and buttons a hit area of at least 24x24 CSS px (44px for touch-first); keep destructive and primary actions far apart so a fast pointer cannot conflate them. Red flag: a 16px icon-only control with no padding floating in mid-canvas, a primary CTA stranded far from its supporting copy, or "click here" links smaller than the line they sit in.

**Hick's Law** (Hick & Hyman, 1952). Decision time grows with the number and complexity of choices: `RT = b * log2(n + 1)`. Web application: cap top-level navigation to a scannable set (group the rest behind a clear "More" or mega-menu with headed columns); structure pricing as 3-4 plans with one highlighted recommendation rather than a 9-column matrix; stage long settings behind tabs or sections. Red flag: a 14-item flat top nav, a pricing page with eight equally weighted columns, or a filter sidebar dumping 40 ungrouped checkboxes with no headings or search.

**Doherty Threshold** (Doherty & Thadani, 1982). Productivity rises sharply when system response stays under 400ms because the user and machine never wait on each other. Web application: keep interaction latency in the Doherty band and tie it to Core Web Vitals — target INP <= 200ms for input responsiveness; if real work exceeds ~400ms, acknowledge within 100ms with optimistic UI, a spinner, a skeleton, or a disabled-with-progress button so the user is never staring at a dead control. Red flag: a form submit that freezes with no feedback for two seconds, a filter that silently re-runs with no loading affordance, or INP regularly over 200ms because handlers block the main thread.

**F-pattern and Z-pattern scanning** (Nielsen Norman Group eye-tracking). Users do not read web pages; they scan. Dense text blocks are read in an F (two horizontal sweeps near the top, then a vertical scan down the left); sparse, designed pages (landing/marketing) are scanned in a Z from top-left to a focal CTA. Web application: front-load the value proposition and key terms in the first two lines and at the start of headings and list items; place the primary CTA on the Z's terminal; left-align body copy so the scan anchor is stable. Red flag: the offer buried in paragraph three, headings that start with filler ("Welcome to our..."), or centered long-form body text that destroys the F-scan's left edge.

**Above-the-fold priority.** The portion visible before any scroll on the dominant viewport sets first-glance comprehension and bounce. Web application: ensure the hero communicates what this is and what to do next without scrolling on common viewports (test ~1366x768 desktop and ~390px-wide handheld); never gate the core message behind a full-viewport decorative banner; below the fold, keep scrolling cheap and continuous (the page is long-scroll, not paginated reveals). Red flag: a 100vh hero image with the headline and CTA pushed entirely below the fold, or a cookie/consent layer that obscures the primary content above the fold.

**Miller's Law** (George Miller, 1956). Working memory holds roughly 7 +/- 2 chunks, and reliable chunking is closer to 3-5. Web application: chunk navigation into labeled groups; segment long forms and checkout into named steps; break long numbers (phone, card, IBAN) into visual groups via input formatting. Red flag: a flat 20-link footer with no column headings, or an account number rendered as one unbroken 16-digit string.

**Jakob's Law** (Jakob Nielsen, 2000). Users spend most of their time on other sites, so they expect yours to work the same way. Web application: logo top-left links home; primary nav across the top or in a recognized hamburger pattern; cart top-right; search as a labeled field; underlined or clearly styled links; form submit on the right/end. Honor platform and ARIA Authoring Practices conventions for widgets. Red flag: a non-clickable logo, a "menu" hidden behind a custom gesture, links that look like body text, or a tab widget that does not respond to arrow keys.

**Tesler's Law** (Larry Tesler, conservation of complexity). Every system has irreducible complexity; the only question is who absorbs it — the system or the user. Web application: handle messy reality server-side (parse pasted phone numbers/dates in any format, normalize addresses, auto-detect currency/locale) rather than forcing the user into a rigid input mask. Move complexity into smart defaults and inference, not onto the form. Red flag: rejecting a card number because the user typed spaces, or demanding a date in exactly `MM/DD/YYYY` when the field could parse what was typed.

**Goal-gradient effect** (Clark Hull, 1932). Motivation increases as a perceived goal gets closer. Web application: show a step indicator on multi-step forms and checkout ("Step 2 of 3"); pre-fill the first step so the user starts with apparent progress; give endowed progress on loyalty/onboarding ("2 of 5 done" rather than "0 of 3"). Red flag: a 4-step checkout with no progress indicator, so each "Next" feels like it could be endless.

**Zeigarnik effect** (Bluma Zeigarnik, 1927). People remember and feel pulled to complete unfinished tasks. Web application: surface incomplete state — a profile-completion meter, a "resume where you left off" banner, saved-but-unsubmitted draft indicators, a cart badge with item count. Red flag: an onboarding checklist with no visible completion state, so users forget what is left and abandon.

**Peak-end rule** (Daniel Kahneman). People judge an experience by its most intense moment and its end, not its average. Web application: invest in the success peak (a confirmation page that is genuinely useful — order summary, next steps, tracking) and the recovery peak (a helpful error, not a dead end); end flows on a clear, positive, actionable note. Red flag: a checkout that ends on a bare "Thank you" with no order number or next step, or an error screen that is the harshest moment with no path forward.

---

## Cognitive heuristics

**Cognitive load — intrinsic vs extraneous** (John Sweller, Cognitive Load Theory). Intrinsic load is the difficulty of the task itself; extraneous load is everything the interface adds on top. Web application: strip extraneous load — consistent layout, one primary action per view, plain labels, no decorative motion competing with reading, defaults that remove decisions. Spend the user's attention budget on the real task. Red flag: three competing CTAs of equal weight, autoplaying carousels next to a form, jargon labels, or a layout that reshuffles between similar pages.

**Recognition over recall** (Nielsen heuristic 6, applied broadly). Recognizing an option is far cheaper than recalling it from memory. Web application: keep navigation and current location visible (persistent nav, breadcrumbs, active-state highlighting); offer a command palette (Cmd/Ctrl-K) that lets users find actions by name instead of memorizing menu paths; show recently used and suggested items; label icons. Red flag: icon-only toolbars with no labels or tooltips, a wizard that hides previously entered values, or deep settings reachable only by remembering an exact path.

**Progressive disclosure** (Jakob Nielsen / Joseph Hutchins). Show the common, simple options first; reveal advanced ones on demand. Web application: default forms to essential fields with an "Advanced options" disclosure; use "Show more" on long lists; expand detail in accordions, drawers, or detail panes rather than dumping everything at once. Red flag: a 30-field form with every advanced setting visible to first-time users, or a settings page with no grouping or defaults.

**Postel's Law / robustness principle** ("be conservative in what you send, liberal in what you accept"). Web application: accept input in any reasonable shape and normalize it — strip spaces and dashes from card and phone numbers, parse dates and currencies flexibly, trim whitespace, accept upper/lowercase emails — while emitting clean, consistent output. This is Tesler's Law made concrete at the input layer. Red flag: validation that rejects `(415) 555-0100` because it wanted `4155550100`, or an email field that fails on a trailing space.

**Serial position effect** (Hermann Ebbinghaus — primacy and recency). Items at the start and end of a list are remembered best; the middle sags. Web application: place the most important nav items, plans, or actions first and last; put the recommended pricing plan at an anchor position; order menu items so destructive or rare actions sit in the low-attention middle, not the recency slot where a tired user clicks. Red flag: the primary plan buried in the middle of a pricing row, or "Delete account" as the last, most-remembered item in a menu.

---

## Nielsen 10

Jakob Nielsen's 10 usability heuristics (1994), each with a web application and a web red flag.

1. **Visibility of system status.** Web application: reflect every state — loading skeletons and spinners with sensible timing, optimistic UI, toast/inline confirmations, progress bars, `aria-live="polite"` regions so screen readers hear async updates, disabled-with-progress submit buttons. Red flag: a button that does nothing visible after click, an async list that pops in with no loading state, or status changes announced only visually.

2. **Match between system and the real world.** Web application: use the user's language and mental models — "Cart", "Checkout", "Sign in" over internal jargon; real-world ordering (calendar weeks, currency formats by locale); icons that match conventions (trash = delete). Red flag: "Commit transaction" on a buy button, server error codes shown to end users, or date formats that ignore locale.

3. **User control and freedom.** Web application: respect Back/Forward and deep-linkable URLs so the browser's own controls work; provide visible Undo (especially after delete), Cancel, and Close; let ESC dismiss modals and overlays; never trap the user in a flow. Red flag: a modal with no close button that also ignores ESC and backdrop click, a delete with no undo, or a SPA that breaks the browser Back button.

4. **Consistency and standards.** Web application: follow Jakob's Law and the ARIA Authoring Practices Guide (APG) for widget behavior; reuse one button hierarchy, one form pattern, one icon set across the product; identical components look and behave identically. Red flag: three different primary-button styles across pages, a custom dropdown that ignores APG keyboard semantics, or "Save" meaning different things in different views.

5. **Error prevention.** Web application: prevent errors before they happen — inline validation as the user leaves a field, sensible input types and `inputmode`, smart defaults, confirmation on destructive/irreversible actions, disabling submit until requirements are met (with the reason shown). Red flag: validation that only fires on submit and dumps a wall of errors, a destructive action with no confirmation, or a free-text field where a constrained picker belongs.

6. **Recognition rather than recall.** Web application: keep options, current location, and prior input visible — persistent nav, breadcrumbs, autocomplete, recently viewed, a command palette for discoverable actions. Red flag: forcing users to remember a code or path between steps, or icon-only controls with no labels.

7. **Flexibility and efficiency of use.** Web application: serve novices and experts on the same page — keyboard shortcuts with a discoverable cheat sheet, a command palette (Cmd/Ctrl-K), bulk actions, saved filters/views, type-ahead. Accelerators must not break the basic path. Red flag: a power tool with no keyboard support, or shortcuts that exist but are undocumented and conflict with browser defaults.

8. **Aesthetic and minimalist design.** Web application: every element earns its place; use the spacing scale and whitespace to group and prioritize; one clear focal point per section; remove decoration that competes with the task. Minimalist means low noise, not low information. Red flag: competing CTAs, autoplaying carousels, dense unstructured walls of text, or decorative imagery that pushes the real content below the fold.

9. **Help users recognize, diagnose, and recover from errors.** Web application: error messages in plain language that say what went wrong and how to fix it, placed at the field that failed; helpful 404 pages with search and navigation back into the site; 500 pages with a retry and a way to report; inline recovery rather than dead ends. Red flag: "An error occurred", a raw stack trace, or a 404 that is a blank page with no way back.

10. **Help and documentation.** Web application: contextual help where it is needed — inline hints, tooltips on ambiguous fields, an empty-state that teaches, searchable docs, and links to support; ideally the product is usable without docs, with help one click away when needed. Red flag: no empty-state guidance, no contextual hints on a complex field, or help that requires leaving the task and hunting a separate site.

---

## Gestalt

Gestalt principles (Wertheimer, Koffka, Köhler) describe how people group visual elements. On the web they govern layout, cards, grids, and whitespace.

- **Proximity.** Elements placed close together are read as a group. Web application: use the 4/8/16/24/32 spacing scale so intra-group gaps are smaller than inter-group gaps — a label hugs its input, sections breathe apart. Red flag: uniform spacing everywhere, so a form field's label appears equally tied to the field above and below it.

- **Similarity.** Elements that share color, shape, or size are perceived as related. Web application: give all primary actions one consistent style, all links one treatment, all cards one shape; signal "same kind of thing" through visual sameness. Red flag: three visually different buttons that all do the same class of action, or links that vary style page to page.

- **Common region.** A shared bounded container groups its contents even across distance. Web application: cards, panels, fieldsets, and subtly tinted backgrounds bind related controls; use a `<fieldset>`/region per logical group. Red flag: related settings scattered with no container while unrelated ones share a card.

- **Continuity.** The eye follows aligned edges and lines. Web application: align to a grid and a consistent baseline so the gaze flows down a column; left-align form labels and inputs to a shared edge; give peer cards/tiles in a row a shared height so their bottom edges resolve on one line (grid/flex `stretch`), and align the content *inside* them across siblings — title, body, and footer/CTA each on a shared baseline — with subgrid (shared row tracks), not just by pinning the footer with `margin-top: auto`. Red flag: ragged, unaligned fields and cards that break the column the eye is trying to follow; a row of peer cards with mismatched heights and ragged bottom edges; titles, descriptions, or buttons that don't line up across sibling cards because one title wraps to more lines, so each card's body and CTA start at a different height.

- **Closure.** The mind completes implied shapes from partial cues. Web application: let a row of cards bleed slightly past the fold or viewport edge to signal "scroll for more"; use partial borders or implied grids instead of boxing everything. Red flag: a horizontally scrollable row with no peek of the next item, so users never discover it scrolls.

- **Figure-ground.** People separate a foreground figure from its background. Web application: use elevation, contrast, blur/scrim, and whitespace so modals, dropdowns, and the active focal element read as foreground; meet AA contrast so the figure stays legible. Red flag: a modal with no backdrop scrim that blends into the page, or low-contrast cards that fight the background.

---

## Form heuristics (Wroblewski)

From Luke Wroblewski, *Web Form Design* (2008) and ongoing research. Forms are where conversion is won or lost.

- **Single-column layout.** One field per row, top to bottom, so the path is unambiguous. Web application: stack fields in a single column; only pair tightly coupled fields on one row (city/state, expiry/CVC) when it does not break the scan. Red flag: a multi-column form where the eye zigzags and users skip fields.

- **Top-aligned labels.** Labels sit directly above their input. Web application: top-align for fastest completion and clean reflow to narrow viewports; always use a real `<label>` (placeholders are not labels). Red flag: placeholder-only fields whose label vanishes on focus, or left-aligned labels that wrap and misalign at 320px.

- **Minimize fields.** Every field costs completion. Web application: ask only for what you need now; defer optional data to after conversion; merge fields (full name over first/last when possible); infer rather than ask. Red flag: requiring phone, company, and job title to download a one-pager.

- **Smart defaults.** Pre-select the most likely value. Web application: detect country from locale, default to the recommended plan, pre-fill known data, set sensible quantities — while keeping every default editable. Red flag: an empty country dropdown defaulting to "Afghanistan" alphabetically, or no default on a field where one is obvious.

- **Inline validation.** Validate as the user finishes a field, not only on submit. Web application: confirm valid input and flag errors at the field on blur (not on every keystroke), with a clear message and matching `aria-invalid`/`aria-describedby` for assistive tech. Red flag: errors revealed only after submit, or red text with no programmatic association for screen readers.

- **Action vs secondary buttons.** The primary action must dominate; secondary/destructive actions must recede. Web application: one visually dominant primary button per form; style "Cancel"/"Back" as low-emphasis (text or outline); never give two equal-weight buttons. Red flag: "Submit" and "Cancel" rendered identically, or a destructive button styled like the primary.

- **Autocomplete and input types.** Let the browser and OS do the work. Web application: set correct `autocomplete` tokens (`email`, `cc-number`, `street-address`, `one-time-code`), correct `type`/`inputmode` so the right keyboard appears, and allow password managers. Red flag: `type="text"` on an email or numeric field, missing `autocomplete`, or markup that blocks autofill and password managers.

---

## Severity crosswalk (Nielsen 0-4 to 1-5 cap)

Severity is a function of **frequency x impact x persistence**: how often users hit the issue, how badly it hurts the task when they do, and whether it blocks them or has a workaround. Nielsen's 0-4 severity scale maps to the design-quality 1-5 caps so that the worst *unresolved* finding sets the ceiling. This crosswalk is the engine Mode D reviews use to turn findings into a score; it is kept consistent with the caps in `docs/design-quality-rubric.md`.

| Nielsen severity | Meaning | Frequency x impact x persistence | Design-quality cap (if unresolved) |
|---|---|---|---|
| 0 | Not a usability problem | Cosmetic disagreement; no task effect | No cap from this finding |
| 1 | Cosmetic only | Rare or trivial; noticed, not blocking; easy workaround | Caps at **5/5** (cannot claim "resilient"); note it |
| 2 | Minor usability problem | Low frequency or low impact; recoverable with effort | Caps at **4/5** |
| 3 | Major usability problem | Frequent or high impact; degrades the primary task; awkward workaround | Caps at **3/5** |
| 4 | Usability catastrophe | Frequent and blocking, or data-loss / accessibility-barrier / trust-breaking; no workaround | **Fail**, or caps at **1-2/5** |

Rules of use:

- The lowest cap among unresolved findings wins; resolving a finding (or specifying the fix that meets the cap's condition) lifts only that cap.
- A severity-4 is treated as a P0-class issue: it makes the response Fail or holds the score at 1-2/5 until fixed — never quietly averaged away.
- A severity-3 holds the score at 3/5 even when every other dimension is strong; a beautiful page with one major usability break is not a 4/5.
- A severity-2 holds at 4/5; a clean sweep with no finding above severity-1 is required to reach 5/5, alongside the resilience evidence the rubric demands.
- Accessibility barriers (keyboard inoperability, contrast failures, screen-reader dead ends) escalate severity because they are persistent and total for affected users — score them at least severity-3, often severity-4.

---

## How to apply

1. **Cite the heuristic by name in findings.** Name the law and what it predicts, then the specific web evidence: "Fitts's Law — the 16px icon-only delete control has no padding and sits mid-canvas, so it is slow and error-prone to hit." Naming makes the critique teachable and checkable rather than a matter of taste.

2. **Use the red flags as a Mode D violation checklist.** Walk the page against the red flags in each section; every red flag you confirm is a candidate finding. Assign each confirmed finding a Nielsen severity via frequency x impact x persistence, then apply the crosswalk above to derive the score cap.

3. **When two heuristics conflict, name both and resolve by context.** Conflicts are normal — name the tension explicitly and decide by the page's job, not by picking a favorite:
   - *Hick's Law vs recognition over recall*: fewer visible choices speed decisions, but hiding options forces recall. Resolve by frequency — keep common actions visible, disclose the long tail behind a labeled menu or command palette.
   - *Aesthetic-minimalist vs visibility of system status*: minimalism wants less chrome, status wants feedback. Resolve toward feedback whenever absence would leave the user uncertain.
   - *Progressive disclosure vs recognition over recall*: hiding advanced options reduces load but can bury features. Resolve by audience — defaults for novices, a visible, discoverable path (disclosure label, search, palette) for experts.
   - *Minimize fields vs error prevention / Tesler*: fewer fields convert better, but some validation needs data. Resolve by moving complexity into the system — infer, default, and parse flexibly rather than adding fields or strict masks.

   State the winning principle and why the context favors it, so the resolution is auditable.
