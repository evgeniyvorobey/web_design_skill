# Marketing / Landing Domain Pack

A conversion-focused playbook for marketing sites and standalone landing pages: hero-to-CTA flows, pricing pages, lead-capture forms, paid-traffic landers, and product launches. It shapes hierarchy, trust language, state coverage, responsive and browser behavior, and handoff so the page sells without sacrificing accessibility, performance, or honesty.

## When To Use

Use this pack when the primary job of the surface is persuasion and conversion rather than ongoing task completion:

- A standalone landing page behind a paid campaign (search, social, display) where a single primary action dominates: "Start free trial", "Book a demo", "Get the report".
- A marketing home page or product page that funnels toward sign-up, contact, or purchase.
- A pricing page where plan comparison and the upgrade CTA are the conversion event.
- A lead-capture or waitlist page with a short form and an email/SMS gate.
- A launch or event page with a countdown, registration, and social proof.

Do NOT use this pack as the authority for the authenticated product itself (use the web-app pack), for documentation, or for transactional checkout flows where payment and order state dominate. A landing page hands off to those surfaces; it is not those surfaces.

## Primary User Jobs

Visitors arrive cold, skeptical, and fast-bouncing. Their jobs, roughly in funnel order:

1. **Orient in under five seconds** — "What is this, who is it for, is it relevant to me?" The above-the-fold hero must answer the value proposition before any scroll.
2. **Assess credibility** — "Can I trust this company with my email, money, or time?" Logos, testimonials, ratings, security and privacy signals.
3. **Compare and qualify** — "Is this better than my current option or a competitor? Which plan fits me?" Feature blocks, comparison tables, pricing tiers.
4. **Reduce risk before committing** — "What happens after I click? Can I back out? Is it free, is there a contract?" CTA microcopy, guarantees, FAQ.
5. **Convert** — complete the primary action: submit the form, start the trial, schedule the call.
6. **Recover or defer** — if not ready, capture a lighter commitment (newsletter, save for later) rather than losing them entirely.

Design the page so each scroll depth answers the next question. A visitor who scrolls is asking to be convinced; do not make them hunt.

## Trust And Safety Risks

Marketing pages are where overclaiming, dark patterns, and data-collection abuse concentrate. Treat these as first-class risks, not afterthoughts:

- **Overclaiming and unsubstantiated stats.** "10x faster", "Join 50,000 teams", "#1 platform". Every quantified claim needs a verifiable source or it becomes a legal and reputational liability. Mark the source in copy or footnote.
- **Fabricated or unattributed social proof.** Stock-photo "customers", invented testimonials, logo walls of companies that never bought. Attributable name + role + company, or do not show it.
- **Forced urgency and false scarcity.** Fake countdown timers that reset on reload, "Only 2 left!" on infinite digital goods, persistent "Sale ends today" banners. These are deceptive-pattern risks and erode trust on the second visit.
- **Confirmshaming and manipulative opt-outs.** Decline links worded as "No thanks, I hate saving money". Avoid; the negative option must be neutral and equally clickable.
- **Pre-checked consent and bundled marketing opt-in.** Consent for marketing email/SMS must be unchecked by default and separable from the core action. Bundling violates common consent expectations (GDPR/ePrivacy-style regimes) and damages deliverability.
- **Hidden costs and bait pricing.** "Free" that requires a card, "from $9" where $9 is unattainable, auto-renew buried in fine print. Disclose card requirement, renewal terms, and the realistic price near the CTA.
- **Data over-collection at the gate.** Asking for phone, company size, and job title to download a one-pager. Every extra field lowers conversion and raises privacy exposure. Collect only what the next step needs.
- **Consent and tracking.** Analytics, pixels, and session replay must respect a consent banner and Global Privacy Control / Do Not Track signals where applicable. Do not fire marketing tags before consent in regulated regions.

State in copy what the user is agreeing to, who receives their data, and how to opt out. Honesty is a conversion strategy on the return visit.

## Common Web Surfaces

Concrete components and page regions this pack governs:

- **Hero** — `h1` value proposition, supporting subhead, primary CTA, optional secondary CTA (`<button>` for in-page action, `<a>` for navigation), hero media with reserved aspect ratio.
- **Sticky header / top-nav** — logo, anchor links to sections, persistent CTA; collapses to a disclosure menu (`<button aria-expanded>`) on narrow viewports.
- **Social-proof strip** — customer logos, star rating, "Trusted by" count, press mentions.
- **Feature blocks** — alternating media/text rows, icon grids, benefit-led headings.
- **Testimonial cards / carousel** — quote, attributable name/role/avatar; carousel built as an APG-conformant pattern with accessible controls, not auto-advancing without pause.
- **Comparison / pricing table** — tiered plans, feature matrix, "Most popular" highlight, monthly/annual toggle.
- **Lead form / waitlist** — name, email, consent checkbox, submit; inline validation; success and error states.
- **FAQ** — native `<details>`/`<summary>` accordion, one question per disclosure.
- **CTA band** — repeated mid-page and end-of-page conversion prompts.
- **Footer** — secondary nav, legal links (Privacy, Terms), company info, newsletter sign-up.
- **Overlays** — exit-intent or scroll-triggered offer in a `<dialog>` (modal), cookie/consent banner (non-modal, focus-manageable), promo bar.

## Hierarchy Guidance

Conversion lives and dies on a single dominant path. Enforce it:

- **One primary action per viewport.** The hero CTA is the loudest element: highest contrast, largest target, most weight. Secondary CTAs ("See how it works", "Talk to sales") are visually subordinate — outline or ghost style, never matching the primary's emphasis.
- **One `h1`, clean outline.** The `h1` carries the value proposition. Section headings are `h2`; sub-points `h3`. Never skip levels for styling; size with fluid type (`clamp(2rem, 1.5rem + 2.5vw, 3.5rem)` for the hero, body steady at 16px / 1rem minimum). Decorative eyebrows above the `h1` are `<p>` or `<span>`, not heading levels.
- **F-pattern and Z-pattern for scanners.** Lead each block with the benefit, not the feature name. Front-load the value in the first ~65ch of every paragraph; most visitors read headings and the first line only.
- **Repeat the CTA at decision points.** Place the primary action after the hero, after the proof, after pricing, and in the final band — so a convinced visitor never has to scroll back. Keep the label and destination identical across repetitions.
- **Contrast and color are not the only signal.** Per WCAG 1.4.1 Use of Color, the primary CTA must differ from secondary by more than hue — size, weight, fill, and position carry the hierarchy so it survives grayscale and color-vision differences.
- **Above-the-fold discipline.** Value prop, one supporting line, primary CTA, and at least a sliver of the next section to signal scrollability — visible at 360px wide and at 768px without scrolling the fold offscreen.

## State And Recovery Requirements

A landing page is more stateful than it looks. Cover the full set, not just the happy path:

- **CTA / button states** — default, hover, `:focus-visible` (visible ring, never `outline: none` without a replacement), active, loading (spinner or disabled-with-label after submit to prevent double-submit), disabled (with a reason; never a dead disabled button with no explanation).
- **Form states** — empty/default, focused, inline validation error (tied to the field via `aria-describedby`, announced, error text + icon not color alone), success, and a global submit error.
- **Submission outcomes** —
  - *Success:* confirmation message or redirect to a thank-you state; do not silently clear the form. Announce via `aria-live="polite"`.
  - *Server / network error:* "Something went wrong, try again" with the entered values preserved — never wipe a filled form on failure.
  - *Validation error:* focus moves to the first invalid field; summary list at top for multi-field forms.
  - *Duplicate / already-subscribed:* friendly "You're already on the list" rather than a hard error.
  - *Rate-limited / spam-flagged:* graceful message, no leak of internal detail.
- **Loading / skeleton** — reserve space for async-loaded testimonials, pricing, or media so there is no layout shift (CLS budget <= 0.1).
- **Empty / fallback** — if a dynamic logo wall, review feed, or inventory count fails to load, hide the region cleanly rather than showing a broken empty box.
- **Offline / failed third party** — the page must still render and the form must still describe a fallback (e.g., "email us at...") if a script CDN or form provider fails.
- **Page-level errors** — branded 404 (mistyped campaign URL) and 500 pages that keep the primary CTA reachable; expired-offer state for time-boxed promos that explains the offer ended and points to a current one; session-expired handling for any gated download link.
- **Post-consent** — once a cookie banner is dismissed, persist the choice; do not re-prompt every navigation.

## Accessibility Notes

Apply WCAG 2.2 AA across the page; conversion and accessibility reinforce each other:

- **Contrast (1.4.3 / 1.4.11).** Body and CTA text at 4.5:1, large text (>=24px or >=18.66px bold) at 3:1, button fills and input borders at 3:1 against their background. Hero text over imagery needs a scrim or solid plate — gradient overlays must be tested at the lightest pixel under the text.
- **Use of color (1.4.1).** Errors, required fields, "popular" plan, and selected toggle states use icon/text/shape in addition to color.
- **Keyboard operability (2.1.1, 2.4.11).** Logical tab order top-to-bottom; visible `:focus-visible` on every interactive element; skip link to `main`; no keyboard trap. Sticky headers must not obscure the focused element (2.4.11 Focus Not Obscured) — add `scroll-margin-top` so anchored focus targets clear the sticky bar.
- **Overlays.** Exit-intent and offer modals use `<dialog>` semantics: focus moves in on open, ESC closes, focus returns to the trigger on close, background scroll is locked, and the rest of the page is inert. Cookie banners should be reachable and dismissible by keyboard before they block interaction.
- **Forms.** Every input has a visible, persistent `<label>` (placeholder is not a label); `inputmode="email"` / `type="email"` / `autocomplete="email"` for the email field; consent checkbox is a real `<input type="checkbox">` with an associated label; errors announced via `aria-live`.
- **Target size (2.5.8).** Interactive targets at least 24x24 CSS px with adequate spacing; aim for ~44px on the primary CTA and on `pointer: coarse` devices.
- **Motion.** Honor `prefers-reduced-motion` for scroll animations, parallax, auto-advancing carousels, and counters; provide a non-animated equivalent. Carousels never auto-rotate without a visible pause/stop control.
- **Reflow & resize (1.4.10, 1.4.4, 1.4.12).** Single-column at 320px with no horizontal scroll; usable at 200% zoom; layout survives a text-spacing bookmarklet without clipping CTAs.
- **Forced colors.** Test in forced-colors / Windows High Contrast mode — CTAs defined only by `background-color` can vanish; keep a `border` and account for `forced-color-adjust` so buttons stay visible.
- **Semantics & landmarks.** `header`, `nav`, `main`, `footer`; decorative hero images get empty `alt=""`; meaningful media gets descriptive `alt`. One `h1`, no skipped levels for the SEO and screen-reader outline both.

## Responsive And Browser Notes

Mobile-first, with the conversion path intact at every step of the breakpoint ladder:

- **320px (reflow floor):** single column, hero CTA full-width or near it, nav collapsed to a disclosure menu, pricing tiers stacked vertically, comparison table switches to per-plan cards or a horizontally scrollable region with a sticky first column and a visible scroll affordance.
- **360 / 480px:** comfortable single column; CTA remains reachable and at least ~44px tall; logo strip wraps to 2-3 per row.
- **640 / 768px (tablet):** two-column feature rows begin; pricing tiers may sit side-by-side; sticky header can show inline anchor links. Use container queries on cards (testimonials, pricing) so a card reflows based on its own column width, not just the viewport.
- **1024 / 1280px (desktop):** 12-column grid, max content width ~1200-1440px, reading column ~65ch so paragraphs do not stretch unreadably wide. Hero may go split-layout (copy left, media right). Exploit the width for a full comparison matrix rather than collapsing it.
- **1440 / 1920px+ (wide):** cap line length and center the container; let background fill, content stays bounded. Avoid stretching the `h1` measure past readability.

Browser / engine considerations:

- **`<dialog>` and `popover`** — broadly supported across current Chromium, WebKit (Safari), and Gecko (Firefox); provide a focus-trap and scroll-lock fallback for older engines and test ESC/backdrop dismissal in each.
- **`:focus-visible`, `:has()`, container queries, `clamp()`** — current-engine baseline; if a campaign targets legacy browsers, gate enhancements with `@supports` and keep a functional fallback.
- **Sticky positioning** — verify `position: sticky` headers against iframe-embedded form widgets and against `overflow` ancestors that silently break sticking.
- **Font loading** — `font-display: swap`, preload the above-the-fold display font, and set fallback metric overrides (`size-adjust`, `ascent-override`) so the hero `h1` does not reflow and inflate CLS.
- **Core Web Vitals** — LCP <= 2.5s (the hero image/heading is usually the LCP element: preload it, serve responsive `srcset` with AVIF/WebP, set `width`/`height`); INP <= 200ms (defer non-critical marketing scripts and tag managers); CLS <= 0.1 (reserve space for banners, embeds, and late-loading proof). Heavy third-party tags are the usual CWV killers on landers — load them lazily and after consent.
- **Reduced-data** — consider lighter hero media when `prefers-reduced-data` is set.

## Evidence And Compliance Boundaries

This pack is a set of synthetic, calibration-grade recommendations for shaping marketing and landing-page design. It is **not** proof of anything, and it is not real-product validation.

- The guidance here is **not proof of legal compliance, accessibility conformance, privacy/consent compliance, advertising-standards compliance, security, or business performance.** Following it does not certify that a page meets WCAG 2.2 AA, GDPR/ePrivacy/CAN-SPAM/CCPA, FTC endorsement and advertising rules, or any other regime.
- Conversion claims, lift percentages, and "best practice" framings here are heuristics, not measured outcomes. Real performance requires your own instrumented A/B tests, analytics, and statistical validation on real traffic — this document provides none and is no proof of business results.
- Accessibility notes name criteria to design against; actual conformance requires audit with assistive technology, automated and manual testing, and ideally testing with disabled users. The pack is a checklist, not a conformance statement or proof of compliance.
- Trust, claim-substantiation, and consent guidance is general and not legal advice. Quantified marketing claims, testimonials, pricing disclosures, and data-collection practices must be reviewed by qualified legal and compliance counsel for the jurisdictions you operate in.
- Inspiration galleries (Awwwards, Land-book, Mobbin Web, Dribbble) are **never evidence** for usability, accessibility, performance, or compliance. They show aesthetics, not validated outcomes. Treat authoritative specs (WCAG, WAI-ARIA APG, MDN, web.dev, the relevant regulators) as the sources of record.

Use this pack to raise the floor of design quality and to ask the right questions. Treat every empirical claim as a hypothesis to verify, and route every compliance question to the people accountable for it.

## Design-Quality Traps

Common ways marketing pages score below 4/5 on the quality dimensions:

- **Hero with no clear value proposition** — clever tagline, no statement of what it is or who it is for. Fails attention-path and orientation.
- **Two co-equal CTAs** — "Start trial" and "Watch demo" at identical weight split attention and depress conversion. One must win.
- **Low-contrast hero text over a busy image** — looks premium in the mock, fails 1.4.3 on real photos. Always test the lightest pixel.
- **Carousel as a content dump** — auto-advancing, no pause, hides 80% of content most users never see. Prefer a static grid; if a carousel, make it APG-conformant.
- **Centered long-form body copy** — paragraphs centered and stretched past ~65ch are unreadable. Left-align body, cap measure.
- **Pricing table that collapses to an unusable narrow view** — feature matrix flattened into ambiguous stacked rows. Reflow into per-plan cards instead.
- **Fake urgency** — countdown that resets, "limited spots" on unlimited goods. Erodes trust and risks deceptive-pattern scrutiny.
- **Cookie banner that traps focus or blocks the page indefinitely** — and re-prompts on every navigation.
- **Decorative animation without `prefers-reduced-motion`** — parallax and number counters that ignore the user's setting.
- **Layout shift from late-loading proof and tag managers** — logos and banners popping in push the CTA down as the user reaches for it.
- **Form asking for ten fields to gate a PDF** — friction far exceeds the value exchanged; conversion craters.
- **Inconsistent CTA label/destination across repeated bands** — "Get started" here, "Sign up free" there, going to different routes, confusing the funnel.

## Handoff Checks

Before handing a marketing/landing page to engineering, confirm:

- [ ] **One `h1`**, clean heading outline (`h1` -> `h2` -> `h3`, no skipped levels), landmarks present (`header`/`nav`/`main`/`footer`), skip link to `main`.
- [ ] **Primary CTA** is unambiguously dominant by size + weight + fill + position (not color alone); label and destination are documented and identical across every repeated band.
- [ ] **Full breakpoint specs** at 320 / 360 / 480 / 640 / 768 / 1024 / 1280 / 1440, including how the pricing/comparison table and sticky nav reflow; no horizontal scroll at 320px.
- [ ] **All states designed**: button (default/hover/focus-visible/active/loading/disabled), form (default/focus/error/success), success/error/duplicate/rate-limited submission outcomes, skeleton/empty/offline, plus 404 / 500 / session-expired / expired-offer.
- [ ] **Form spec**: visible labels, `type`/`inputmode`/`autocomplete` per field, consent checkbox unchecked by default and separated from the core action, inline + summary error pattern with `aria-live`, values preserved on failure.
- [ ] **Contrast tokens** verified — text 4.5:1, large text/UI 3:1, hero scrim included; checked in forced-colors mode.
- [ ] **Overlay spec** for any modal/exit-intent/cookie banner: focus move-in, ESC close, focus restore, scroll-lock, background inert, persistence of consent choice.
- [ ] **Motion spec** with `prefers-reduced-motion` fallbacks; no auto-advancing carousel without a pause control.
- [ ] **Performance budget** stated: LCP element identified and preloaded, image `srcset`/dimensions/`aspect-ratio` set, fonts with `swap` + preload + metric overrides, third-party/marketing tags deferred and gated behind consent; CLS-reserved space called out.
- [ ] **Claim substantiation** noted: every stat, logo, and testimonial has a documented source and attribution; pricing discloses card requirement and renewal terms near the CTA.
- [ ] **Consent / privacy** behavior specified: which tags fire pre- vs post-consent, GPC handling, opt-out path, and links to Privacy/Terms in the footer.
- [ ] **Tracking handoff** clean: analytics/conversion events named and mapped to CTAs and form submit, with URL-as-shareable-state for campaign params (UTMs) preserved through navigation.
