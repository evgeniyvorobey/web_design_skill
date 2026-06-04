# Content / Publishing Domain Pack

Synthetic calibration material for content and publishing surfaces: articles and long-form reading, section fronts and feeds, paywalls and subscription flows, newsletters, comment threads, and the advertising that funds them. This pack shapes hierarchy, trust language, state coverage, responsive and browser behavior, and handoff checks. It is calibration guidance, not real-product validation.

## When To Use

Reach for this pack when the primary job of the surface is to deliver editorial or user-generated reading material and to convert or retain readers around it. Concretely:

- News sites, magazines, blogs, and knowledge bases where the article body is the product.
- Section fronts, topic hubs, and infinite or paginated feeds that route readers into stories.
- Metered paywalls, hard paywalls, registration walls, and subscription/upgrade flows.
- Newsletter capture, double opt-in confirmation, and preference/unsubscribe centers.
- Comment threads, reactions, highlights, and reader contributions.
- Ad-supported layouts: display slots, in-article units, sponsored/native placements.

Do not use this pack as the lead when the surface is primarily transactional commerce (use the ecommerce pack), a data-dense operational tool (use the webapp-dashboard pack), or a single conversion landing page (use the marketing-landing pack). A subscription checkout step inside a publication legitimately borrows from ecommerce; cite both packs in handoff.

## Primary User Jobs

Design the hierarchy around these jobs, roughly in order of frequency:

1. **Read one article end to end.** The reader arrived from search, social, or a newsletter and wants the body text with minimal friction. Time-to-readable text and reading comfort dominate.
2. **Scan and triage a front or feed.** The reader is deciding what to open. Headlines, decks/standfirsts, timestamps, and section labels carry the weight; thumbnails support but never replace text.
3. **Decide whether to subscribe.** The reader hit a meter limit or paywall and is weighing price against value. Clarity of what they get, what it costs, and how to cancel governs trust.
4. **Manage the relationship.** Existing subscribers update payment, change newsletter preferences, pause, or cancel. These flows must be findable and honest.
5. **Return for more.** Saved articles, "continue reading," related stories, and newsletter signup keep the reader in the ecosystem.
6. **Contribute or react.** Comment, applaud, highlight, or share. Secondary, but a trust and community signal.

## Trust And Safety Risks

Content and publishing surfaces carry specific credibility and consent hazards. Name them in review:

- **Sponsored content confusion.** Native ads and advertorials that read as editorial. Label them with a persistent, high-contrast "Sponsored" / "Paid partner content" marker that is not conveyed by color alone (WCAG 1.4.1). Disclosure must survive scroll and be present in the feed card and the article header.
- **Dark patterns at the paywall.** Pre-checked auto-renew, buried cancellation, "free trial" that silently converts, fake scarcity timers. State renewal terms, price after intro, and cancellation path before the reader pays. Cancellation must be reachable in comparable effort to signup.
- **Newsletter consent.** No pre-checked opt-in; use explicit double opt-in confirmation. Provide a working one-click unsubscribe and a granular preference center, not an all-or-nothing toggle.
- **Misinformation and provenance.** Show byline, publish and updated timestamps, corrections, and section/source. For syndicated or AI-assisted content, disclose it.
- **Ad-driven CLS and clickbait reflow.** Ads that inject after load shove the body and cause misclicks; reserve slot space. Avoid headlines that the body does not support.
- **Comment safety.** Spam, harassment, and PII in user content. Provide report, block, and moderation states, and rate-limit submission.
- **Tracking consent.** Personalized ads and analytics typically require a consent banner that does not trap focus, offers a genuine "reject all," and does not block reading content behind consent unlawfully.

Trust language should be plain: "Cancel anytime, effective at period end," "$X/month after your first month at $Y," "We will email you a confirmation link," "This article was updated on 5 June 2026." Avoid "risk-free" and unqualified superlatives.

## Common Web Surfaces

- **Article / story page** — `<article>` with one `<h1>`, byline block, hero media with reserved aspect ratio, reading column ~65ch, in-article ads, footnotes, share rail, related stories.
- **Section front / homepage** — editorial grid using the 12-column desktop grid, lead story, secondary wells, river of cards, ad rails.
- **Feed / topic hub** — paginated or progressively loaded list with load-more or numbered pagination; reserve space to avoid CLS.
- **Paywall / meter overlay** — inline gradient fade plus `<dialog>` or sticky panel with plan options.
- **Subscription / checkout flow** — plan picker, payment, confirmation, receipt.
- **Newsletter capture and preference center** — inline and modal capture, double opt-in confirmation page, granular preferences, unsubscribe.
- **Account / billing** — plan status, invoices, payment method, pause/cancel.
- **Search and archive** — query, filters, results with snippets and dates.
- **Comment thread** — composer, sorted replies, moderation and report controls.
- **Reader/print/offline view** — stripped reading mode, RSS, save-for-later.

## Hierarchy Guidance

The reading body is the protagonist. Everything else is supporting cast that must never out-shout the text.

- **Type and measure.** Body 18-20px (1.125-1.25rem) on article pages, never below 16px (1rem). Set measure to ~65ch via `max-inline-size: 65ch` on the prose container. Body `line-height: 1.5`; headings `line-height: 1.2-1.35`. Fluid headline with a rem anchor, e.g. `clamp(1.75rem, 1.2rem + 2.5vw, 3rem)`.
- **One h1, clean outline.** The article headline is the `h1`. Section subheads step down h2 -> h3 with no skipped levels so the document outline and assistive tech navigation hold (WCAG 1.3.1, 2.4.6, 2.4.10).
- **Standfirst and metadata.** Deck/standfirst at ~1.25rem under the headline; byline, section, and timestamps in a muted but AA-contrast block (4.5:1). Reading time and updated date build trust.
- **Vertical rhythm.** Use the 4px spacing scale: 24px between paragraphs is too much and 8px too little — target 16-24px paragraph spacing, 32-48px above subheads, 48-64px between major article sections.
- **Ad and chrome subordination.** In-article ad units sit in clearly bounded slots with reserved height and a small "Advertisement" label; they break the column rhythm deliberately but never mimic editorial type. Share rails and related-story modules use smaller type and lower contrast than the body.
- **Feed cards.** Headline is the strongest element, then deck, then timestamp/section; thumbnail supports. Entire card is one focusable link target where possible, with the headline as the accessible name. Keep card density honest: do not pad a thin feed, do not crush a rich one.
- **Paywall framing.** When the meter trips, fade the body with a readable gradient (not a hard cut mid-word that reads as a bug), then present the offer. The value proposition and price lead; the "maybe later" / login path stays visible and is not a near-invisible link.

## State And Recovery Requirements

Cover the full web state matrix per surface; missing states are the most common review failure here.

- **Article**: default; loading (content skeleton with reserved hero box to protect CLS <= 0.1); image lazy-load placeholder; embed/video failure fallback; metered-locked (paywall) vs unlocked; saved/unsaved; updated/corrected banner; 404 for a removed or moved story (offer search and section links, not a dead end).
- **Feed / front**: default; loading skeleton cards; empty (no stories in topic — suggest related topics); end-of-feed marker; load-more loading and load-more error with retry; offline (serve cached stories, label staleness).
- **Paywall / subscription**: meter remaining ("2 free articles left this month" via `aria-live` when it changes); plan selected; payment processing (disable submit, show progress, prevent double charge); payment declined (specific, recoverable message); success/receipt; already-subscribed (route to content, do not re-sell); session-expired during checkout (preserve plan selection on re-auth).
- **Newsletter**: default; submitting; success ("Check your inbox to confirm"); confirmation-pending; confirmed; invalid email (inline, `aria-describedby`); already-subscribed; unsubscribe success and resubscribe path.
- **Comments**: empty ("Be the first to comment"); submitting; posted; pending moderation; rejected/flagged; rate-limited; sign-in-required; edit/delete; report sent.
- **Global**: 500 (preserve nav and offer retry), offline, and forced-light/dark and reduced-data variants.

Recovery rule: every error tells the reader what happened, why if known, and the next action. Async results announce via `aria-live="polite"` (or `assertive` for errors). Never silently drop a failed newsletter or payment submission.

## Accessibility Notes

Anchor to named WCAG 2.2 AA criteria and APG patterns:

- **Contrast.** Body and metadata text 4.5:1, large headlines 3:1 (1.4.3); focus rings, card borders, and meter indicators 3:1 against adjacent colors (1.4.11). Sponsored labels and error states never rely on color alone (1.4.1).
- **Reflow and zoom.** Article and feed reflow to a single column at 320px with no horizontal scroll (1.4.10) and survive 200% browser zoom (1.4.4). Respect user text-spacing overrides (1.4.12) — do not clip pull quotes or captions.
- **Keyboard operability (2.1.1).** Logical tab order through headline, body links, share, and footer. Paywall and newsletter modals use native `<dialog>` or APG Dialog pattern: focus moves into the dialog, is trapped, ESC closes, and focus returns to the trigger. Skip-to-content link before the masthead. No keyboard trap in carousels or ad iframes.
- **Focus visibility (2.4.7, 2.4.11).** `:focus-visible` ring on every interactive element; sticky headers and cookie/consent bars must not obscure the focused element (2.4.11).
- **Targets (2.5.8).** Interactive controls at least 24x24px; share buttons, reaction taps, and pagination meet it, with 44px preferred (AAA 2.5.5) for reaction clusters.
- **Semantics and landmarks.** `header`/`nav`/`main`/`footer`; the story in `<article>`; comment list as a labeled region; figures with `<figcaption>`; `<time datetime>` for dates. Meter/limit announcements and "comment posted" use `aria-live`.
- **Media.** Captions for video, transcripts for audio/podcasts, meaningful `alt` for editorial images (empty `alt` for decorative). Respect `prefers-reduced-motion` for autoplaying hero or scroll effects.
- **Forced colors.** Support forced-colors / Windows High Contrast: paywall fades, sponsored badges, and meter UI must not vanish when system colors override; test that the offer remains legible.

## Responsive And Browser Notes

Breakpoint behavior on the mobile-first ladder (min-width: 320 / 360 / 480 / 640 / 768 / 1024 / 1280 / 1440 / 1920):

- **320-480 (reflow floor to large phone).** Single column. Body fills the viewport with comfortable side gutters (16px). Hero media uses `aspect-ratio` to reserve space. Ads stack inline between paragraphs with reserved height. Section fronts collapse to one card per row. Sticky subscribe bar stays slim and dismissible.
- **640-768 (tablet).** Two-column card grids on fronts; article stays single reading column capped at ~65ch even as the viewport widens — do not stretch measure. Share rail may dock to a horizontal bar.
- **1024-1280 (desktop).** Editorial 12-column grid: lead story spans more columns, wells and ad rails appear. Article gains an outer margin column for a sticky share/progress rail while the prose column holds ~65ch. Use container queries on cards so a card in a narrow rail and a card in a wide well restyle independently of viewport.
- **1440-1920+ (wide).** Cap content at ~1200-1440px; let background and full-bleed media breathe but keep the reading column fixed. Increase white space, not line length.

Browser and engine considerations:

- Test across Blink (Chrome/Edge), Gecko (Firefox), and WebKit (Safari). Validate `:focus-visible`, `<dialog>` behavior, container queries, and `text-wrap: balance/pretty` on headlines, with graceful fallback where unsupported.
- Font loading: `font-display: swap`, preload the above-the-fold body/headline font, and set fallback font metrics (size-adjust / ascent-override) to avoid layout shift when the webfont swaps — critical for CLS on text-heavy pages.
- Reserve space for every image, embed, and ad slot (`width`/`height` or `aspect-ratio`) so late-loading units do not shift the body. Lazy-load below-the-fold media; eager-load and `fetchpriority="high"` the LCP hero.
- Respect Reader modes, RSS, and print stylesheets; ensure the article degrades to clean, ad-free text. Honor `prefers-color-scheme` and `prefers-reduced-data`.
- Third-party ad and embed iframes are the top source of jank: sandbox them, constrain their size, and verify they cannot steal focus or trigger reflow that hurts INP.

Core Web Vitals budgets to hold: LCP <= 2.5s (usually the hero image or headline), INP <= 200ms (comment submit, paywall open, load-more), CLS <= 0.1 (the hardest target on ad-funded pages).

## Evidence And Compliance Boundaries

This pack is a synthetic, calibration-only playbook. It is a set of recommendations, not proof of compliance, safety, or business performance. Following it does not by itself establish legal compliance (privacy/consent law, accessibility regulation, advertising and subscription-disclosure rules), nor does it prove conversion lift, retention, or revenue outcomes.

- The accessibility guidance maps to WCAG 2.2 AA criteria but is not an audit; only testing with assistive technology and real users produces evidence, and even then it is not a guarantee of full compliance.
- Trust and disclosure patterns (paywall terms, native-ad labeling, consent, cancellation) reduce risk but are not a substitute for legal review in the jurisdictions you ship to.
- Inspiration galleries (Awwwards, Land-book, Mobbin Web) are never evidence for usability, accessibility, performance, or compliance — treat them as visual reference only.
- Any performance numbers here are budgets to verify in the field (RUM/lab), not measured proof for your specific build.

Treat every recommendation as a hypothesis to validate, and record the actual test, source, or measurement that supports each shipped decision.

## Design-Quality Traps

Common ways content surfaces score below 4/5 on the eight dimensions:

- **Measure drift (typography craft, density).** Letting the reading column stretch past ~75ch on desktop because the grid allows it; body text dropping below 16px in captions and footnotes.
- **CLS from ads and webfonts (production readiness).** Unreserved ad slots and unmetricked font swaps shoving the body after the reader starts reading.
- **Paywall as a wall, not a door (attention path).** A hard cut mid-sentence that reads as breakage, an invisible "log in" link, or a "no thanks" that is harder to find than "subscribe."
- **Sponsored ambiguity (context and brand fit, color/state).** Native units styled identically to editorial; disclosure carried by a faint color only.
- **Card hierarchy mush (composition, attention path).** Thumbnail louder than headline; equal weight on every card so nothing leads the front.
- **Missing states (production readiness).** No empty topic feed, no payment-declined recovery, no newsletter already-subscribed, no offline cache.
- **Motion overreach (interaction polish).** Parallax heroes and scroll-jacking that ignore `prefers-reduced-motion` and spike INP.
- **Comment afterthought (state coverage).** Composer with no submitting, rate-limited, or moderation-pending states.
- **Consent/cancel friction (trust).** Focus-trapping cookie banners and cancellation buried several screens deep.

## Handoff Checks

Engineering and editorial handoff is not done until:

- [ ] One `<h1>` per article; heading outline has no skipped levels; landmarks present (`header`/`nav`/`main`/`footer`, `<article>`).
- [ ] Reading column capped at ~65ch; body >= 16px (article body 18-20px); `line-height: 1.5` body, 1.2-1.35 headings; fluid type uses `clamp()` with a rem term.
- [ ] Spacing uses the 4px scale (4/8/12/16/24/32/48/64); values in rem/px only.
- [ ] All breakpoints in the ladder reviewed; single-column reflow at 320px with no horizontal scroll; 200% zoom holds.
- [ ] Hero, images, embeds, and every ad slot reserve space (`aspect-ratio` / `width`+`height`); LCP hero prioritized; below-fold media lazy-loaded.
- [ ] `font-display: swap`, above-the-fold font preloaded, fallback metrics set; CLS <= 0.1, LCP <= 2.5s, INP <= 200ms verified.
- [ ] Full state matrix delivered per surface (default, loading/skeleton, empty, error, success, disabled, 404/500/offline/session-expired where relevant).
- [ ] Paywall/newsletter modals are `<dialog>` or APG Dialog: focus trap, ESC, focus restore, scroll-lock, `aria-*` wired; meter changes announced via `aria-live`.
- [ ] Sponsored/native content labeled persistently and not by color alone (1.4.1); disclosure present in card and article header.
- [ ] Subscription terms (intro price, renewal, cancellation path) stated before payment; cancel reachable with effort comparable to signup; newsletter uses double opt-in and working unsubscribe.
- [ ] Contrast verified: text 4.5:1 (large 3:1), non-text 3:1; `:focus-visible` on all controls; focus not obscured by sticky chrome; targets >= 24px.
- [ ] Forced-colors / High Contrast and `prefers-reduced-motion` / `prefers-color-scheme` honored; Reader/print/RSS degrade cleanly.
- [ ] Tested on Blink, Gecko, and WebKit; third-party ad/embed iframes sandboxed and size-constrained.
- [ ] Boundaries acknowledged: this pack is recommendations, not proof of compliance — accessibility, legal, and performance claims are validated with real tests, not assumed.
