# Worked example: Typography, spacing and grid system (Mode E)

## Example prompt

```text
Use the web-design-skill.

Create a typography, spacing and grid system for a documentation website (reference docs + guides).

Inputs:
- Audience: developers, frequent scanning + deep reading
- Breakpoints: mobile-web through wide desktop
- Browsers: evergreen engines
- Constraints: long-form readability, code blocks, sidebar nav + on-page TOC, accessibility-sensitive
```

## Example output

```md
Mode: Create typography, spacing and grid system
Responsive/breakpoint scope: Mobile-web (320px) through wide desktop
Browser/engine scope: Evergreen Chromium / WebKit / Gecko
Assumptions:
- A variable sans for UI/body and a monospace for code; no decorative display face needed.
- Tokens feed a CSS custom-property theme with a light and dark mode.
- Content is authored in Markdown, so heading levels map directly to the type scale.

## Type roles
- Display: page hero on landing/guide intros
- Page title (h1): one per page
- Section title (h2) and Subsection (h3/h4): document outline
- Body: prose
- Secondary body / caption: notes, captions, metadata
- Label: UI controls, nav
- Code (mono): inline and block code

## Size hierarchy
- Body: 16px / 1rem (never below) — long-form bumps to 1.0625rem (17px)
- h1: fluid `clamp(1.75rem, 1.5rem + 1.2vw, 2.5rem)` (28→40px)
- h2: `clamp(1.375rem, 1.25rem + 0.6vw, 1.75rem)` (22→28px)
- h3: 1.25rem (20px); h4: 1.125rem (18px)
- Caption/label: 0.875rem (14px); inline code: 0.9375rem (15px)

## Weight usage
- 400 (regular) for body; 600 (semibold) for headings and labels; 700 reserved for emphasis within headings
- Avoid more than three weights to keep the hierarchy stable

## Line-height guidance
- Body: 1.6 (long-form reading); UI/labels: 1.4
- Headings: 1.2–1.3; code blocks: 1.5
- Tighter than 1.4 on body fails comfortable reading; looser than 1.3 on large headings wastes vertical rhythm

## Spacing scale
- 4
- 8
- 12
- 16
- 24
- 32
- 48
- 64

## Density rules
- Comfortable is the default for prose; a compact preset (one step tighter) applies to the sidebar nav and metadata tables.
- Code blocks get 16px internal padding and 24px block margin so they read as distinct objects.
- Exploit desktop width with a persistent sidebar + on-page TOC rather than hiding navigation behind a toggle.

## Visual rhythm rules
- Quality target: 4/5 — consistent vertical rhythm and a capped measure; 5/5 adds validated localization and print styles.
- Vertical rhythm in multiples of 8: 8 between tight pairs, 16 between paragraphs, 32 before an h2, 48 before a major section.
- Reading column capped at ~72ch (docs run wider than marketing prose); body measure never exceeds 75ch on wide screens.
- Section spacing and heading scale repeat identically across reference and guide templates.

## Pointer, target-size and input implications
- Interactive targets (nav links, TOC items, copy-code buttons) meet 24px minimum (WCAG 2.5.8); primary controls reach 44px (2.5.5 AAA).
- Pointer-aware: `@media (pointer: coarse)` increases nav/TOC hit areas and spacing; `(pointer: fine)` allows the denser desktop sidebar.
- Inputs (the search field) use a 16px font to avoid mobile zoom-on-focus; ≥ 8px between adjacent TOC targets.

## Accessibility considerations
- All sizes in `rem` so the system honors the user's root size and scales cleanly to 200% zoom.
- Text spacing (WCAG 1.4.12) survives user overrides without clipping; headings keep a logical outline (one h1, no skipped levels).
- Body and code contrast ≥ 4.5:1 in both themes; code-token colors re-checked in dark mode and under `forced-colors`.
- Focus-visible styling on every nav/TOC/code-copy control; reduced-motion removes any TOC scroll animation.

## Usage examples
- Global header / nav: label role at 0.875rem semibold, 44px target rows
- Article body / long-form reading column: 1.0625rem body, 1.6 line-height, 72ch max
- Code block: 0.9375rem mono, 1.5 line-height, 16px padding, copy button top-right
- On-page TOC: caption role, compact density, `aria-current` on the active section
- Metadata table: 0.875rem, tabular figures, compact row height

## Next actions
- Emit the scale as CSS custom properties and verify the `clamp()` ranges at 320px and 1920px.
- Run a contrast pass on code-token colors in dark mode and under forced-colors.
- Add a print stylesheet so reference pages export cleanly.
```
