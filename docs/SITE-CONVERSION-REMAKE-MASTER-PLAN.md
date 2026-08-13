# San Diego Hardwoods — Site Conversion Remake Master Plan

**Current status:** Revision-2 visual proof approved; full implementation executed through the build/ generator (all 13 pages regenerated, all six gates verified locally) — awaiting owner preview review; no commits or deploys made
**Last updated:** 2026-08-13

---

## Business objective

Transform the site from a portfolio-first experience into a lead-funnel-first experience while retaining portfolio depth, credibility, all existing content and established Google presence. Target character: **premium craftsmanship with direct-response clarity — simple at first glance, deep by choice.** Dominant conversion category: **direct contact**, with **Call** and **Text Floor Photos** as equal peer actions; email visually secondary; galleries as the primary exploration path.

## Authoritative source documents

1. `docs/LIVE-VISUAL-CONVERSION-AUDIT-2026-08-13.md` — completed live visual audit (authoritative audit record; do not alter)
2. This document — canonical project record

## Owner-confirmed facts

- Legacy site was simpler, billboard-like, with a much more prominent phone/contact path; it reliably produced worthwhile medium and smaller job inquiries.
- Multiple real callers said they saw the phone number and called/texted without exploring the site.
- Current site feels like a premium portfolio; produces a different lead mix.
- Calling and texting are equally important: calling reaches a real person fast; texting enables floor photos and speeds evaluation. They are **equal peer actions**.
- Galleries are the primary exploration path. Homepage gallery must appear **substantially earlier** with **greater visual presence**. All **89 photographs remain**, with clear numbering retained (existing overlay or cleaner replacement). Lightbox: larger size, fullscreen option, closes by clicking outside.
- Owner believes the gallery is currently buried under dense introductory material.
- YouTube/video = supporting proof, not a primary destination.
- Dark-and-gold look is attractive but possibly too fancy/boutique — owner concern to weigh, not proven causation.
- Desired personality: established, trustworthy, skilled, professional — and direct, approachable, easy to contact.
- Services range: repairs, deep cleaning, maintenance → custom restoration, new flooring. **100% dust-containment is a core differentiator and must remain visually prominent.**

## Locked SEO/content requirements

Locked absent explicit owner approval: all live URLs/filenames, sitemap destinations, canonicals/redirects, H1–H3 wording and levels, body wording, titles/metadata, schema, internal-link destinations, image URLs, alt text/captions, forms/contact destinations, phone number and business identity. No deleting or rewriting indexed content. Section **repositioning is allowed**, but any material DOM/content-order change must be flagged for SEO/accessibility/functional risk. All substantive content stays available, visible and crawlable. Homepage gallery + all 89 photos remain; all gallery pages and URLs remain. Hiding/collapsing/paginating/"show more" is **not approved** — presentable only as labeled options with tradeoffs, requiring owner approval. New containers/controls/nav aids may be proposed if they reuse existing approved wording; genuinely new wording must be flagged separately as unapproved. All pages ultimately share one visual system, color system and CTA hierarchy.

## Confirmed header behavior (owner-supplied; corrects audit uncertainty)

Full initial desktop header: identity, phone info, Text Floor Photos action, primary nav. After slight scroll it is replaced by a much smaller sticky header: identity, Menu, phone number, Text Floor Photos and Call — Free Assessment controls. **A persistent sticky header exists** — but owner judges the reduced state visually insufficient: it must remain space-efficient yet keep phone number, Call and Text unmistakable, same hierarchy on desktop and mobile. The initial viewport performs the main billboard function; the sticky state must not be oversized/obstructive.

## Concise audit synthesis (from the authoritative audit)

- **S1 (critical):** Site-wide horizontal overflow at 360×800 — header call button, secondary hero button and body text clipped on every page; fits cleanly at 500px.
- **S3:** Primary red action flips between templates (Text on home/assess/contact/videos; Call on about/blog/clean/galleries) and between desktop (Text) and mobile (Call) headers.
- **S4:** Signal red diluted — dozens of red "Watch Video" buttons, red text links, red photo watermarks, red-icon YouTube nav pill.
- **S5:** YouTube gets near-equal billing in high-value regions (homepage hero embed, nav pill).
- **S6:** Extreme page length (homepage ≈17,500px desktop / ≈19,500px mobile, gallery ≈ y3,800–14,200) buries lower sections and footer CTAs; gallery/video pages carry no conversion CTA between hero and footer.
- **S7:** Letterboxed gallery cards (empty dark regions) on the homepage grid.
- Contact page = strongest existing conversion layout; gallery 5's paginated case-study format paces best of the galleries.
- Desktop folds are otherwise strong: header contact cluster + hero CTA pair above the fold on all 13 pages.

## Visual-direction options

Shared commitments in **all** directions (locked unless noted): Call and Text Floor Photos rendered as equal-weight peer actions; the digits of the phone number always immediately readable as text near the actions (never only inside a button); email reduced to a quiet text link; one reserved action color used **only** for direct-contact controls; video elements restyled as supporting proof (no action color, no nav pill); the 360px overflow eliminated via genuinely fluid small-screen layout; compact sticky header carries identity + readable number + both peer actions; all 89 homepage photos remain with clear numbering; lightbox per owner spec (larger view, fullscreen option, click-outside close); dust-containment differentiator stays visually prominent. Moving the homepage gallery earlier is a **DOM/content-order change — flagged** in each direction; wording unchanged.

---

### Direction 1 — "Workshop Billboard" (recommended)

1. **Character:** Warm, light, confident trade craftsmanship — paper-and-walnut rather than velvet-and-gold. Reads as an established tradesman who answers the phone, not a showroom. Directly answers the owner's boutique concern and the billboard history without becoming dated or loud.
2. **Color roles:** Background warm off-white/paper with soft walnut-toned section bands; primary text near-black walnut ink; **direct-contact action color: the existing signal red, reserved exclusively for Call/Text** (continuity with current brand equity); secondary/accent: muted wood-bronze used sparingly for trust marks (est. 1990, Bona, dust-containment badge) — gold survives only as this quiet craft accent.
3. **Desktop first viewport:** One billboard band: the preserved brand lockup (logo, "San Diego Hardwoods," exact tagline "San Diego's Finest Hardwood Floor Specialist Since 1990" — see binding owner decisions), the phone number set very large as live text, twin solid red Call / Text peer buttons directly under it, and one dust-containment proof mark. No video in the first viewport; a single strong project image anchors the right side.
4. **Mobile first viewport:** Full brand lockup (logo, name, exact tagline — per binding owner decisions), large readable number, full-width twin stacked peer buttons, dust-containment badge — all inside 360px with nothing clipped. Gallery preview begins within the first scroll.
5. **Full header:** Taller "contact masthead" — identity left; contact block right (number prominent as text + twin buttons); simple text nav beneath, no pill styling, YouTube removed from nav.
6. **Sticky transition:** On scroll the masthead collapses to a slim light bar: identity, phone number as readable text, and the twin red peer buttons; identical hierarchy on mobile. Space-efficient, non-obstructive, unmistakable.
7. **Call/Text parity:** Identical solid red buttons, same size/shape, always adjacent — Call first, Text second, reading order consistent site-wide.
8. **Number readability:** Number appears as plain large text in masthead, sticky bar, and footer — tappable but never dependent on button chrome.
9. **Gallery discovery without competing:** A numbered "Recent projects" index strip sits directly below the hero on the homepage and links to gallery pages; styled in neutral walnut, never red, so exploration is obvious but subordinate to contact.
10. **Homepage + 89 photos:** Gallery section moved up to immediately after the services overview (flagged DOM reorder); presented as a bold numbered masonry wall with noticeably larger tiles; contact band repeated before and after the gallery so pacing never strands the visitor. Long intro text stays (locked wording) but follows the gallery.
11. **Deep-scroll contact access:** Slim sticky bar (point 6) plus a repeated neutral contact band at the end of each major section on gallery/assessment/video pages.
12. **YouTube as supporting proof:** Videos gathered into one clearly labeled proof section; plain dark buttons. Per binding owner decision, the homepage hero video is removed only from the first viewport and relocated into this supporting-proof section with its existing embed destination preserved — not replaced by a text link — integrated so it does not look out of place.
13. **360px fix:** Fluid single-column small-screen layout, no fixed-min-width elements; twin buttons stack full-width; header contact block wraps instead of overflowing. (Verify on owner's Samsung — see Open decisions.)
14. **Cross-template consistency:** Same masthead, sticky bar, color roles, CTA pair and section rhythm on all 13 pages; only body content differs.
15. **Advantages/tradeoffs/risks:** Strongest billboard clarity and approachability; red exclusivity restores signal value; light theme maximizes contrast/accessibility headroom. Tradeoffs: largest departure from current brand look; some users' positive association with the premium dark style is retired. Risks: homepage gallery reorder = DOM-order change (SEO risk to review at implementation); none of the changes touch wording, headings or URLs.

### Direction 2 — "Modern Heritage" (evolutionary)

1. **Character:** Keeps a refined dark identity but demotes luxury to structure: a dark forest-espresso header and section dividers over warm cream content areas — two-tone rhythm instead of all-dark velvet. For an owner who wants funnel clarity without abandoning existing brand equity.
2. **Color roles:** Background cream content fields alternating with deep espresso bands; primary text near-black on cream / warm white on dark; **direct-contact action color: the signal red, reserved for Call/Text only**; secondary/accent: restrained antique brass for trust marks and heading flourishes (gold explicitly retained but subordinate).
3. **Desktop first viewport:** Split billboard — left slab carries identity, large phone number text and twin red peer buttons on cream; right carries one dark-framed current project image with dust-containment badge. Nav in a thin dark strip above.
4. **Mobile first viewport:** Cream slab stacks: identity, number, twin full-width red buttons, badge; dark elements become thin separators.
5. **Full header:** Dark bar with identity + nav; beneath it the cream contact band with number and twin actions — contact reads as its own tier, not inside the nav.
6. **Sticky transition:** Collapses to the dark bar alone, now carrying readable number text + twin compact red buttons; same arrangement mobile.
7. **Call/Text parity:** Twin identical red solids, fixed order Call → Text everywhere.
8. **Number readability:** Large live text in the contact band, sticky bar, footer.
9. **Gallery discovery:** Numbered chapter cards (extending the gallery-5 case-study pattern) appear early on the homepage; neutral brass-on-dark styling, no red.
10. **Homepage + 89 photos:** Gallery moved to second position (flagged DOM reorder), organized into numbered project chapters with larger lead images instead of one continuous grid; contact band between chapters keeps pacing; full count retained.
11. **Deep-scroll access:** Sticky dark bar + end-of-section contact bands; gallery chapters each end with the quiet band.
12. **YouTube demoted:** Single "videos" proof chapter, dark-framed thumbnails, plain buttons; no red, no nav pill.
13. **360px fix:** Same fluid small-screen discipline as Direction 1; dark/cream bands stack naturally without fixed widths.
14. **Consistency:** Two-tone band system applies identically to all templates; gallery pages adopt the chapter pattern.
15. **Advantages/tradeoffs/risks:** Lowest visual discontinuity; retains premium cues for high-end jobs while hierarchy becomes funnel-first. Tradeoffs: boutique feeling reduced but not eliminated — weaker answer to the owner's concern than Direction 1; two-tone system is more design-sensitive to execute well. Same flagged DOM-reorder risk.

### Direction 3 — "Jobsite Signal" (boldest)

1. **Character:** Utilitarian confidence — the visual language of jobsite signage and workwear: stark light field, heavy condensed type, big numerals. The most distinctive, least generic-contractor option; deliberately anti-boutique.
2. **Color roles:** Background bright off-white; primary text ink black; **direct-contact action color: high-visibility safety amber for the Call/Text pair** (red retired entirely to break the dilution habit); secondary/accent: dusty cedar brown for rules, numbering and proof marks.
3. **Desktop first viewport:** True billboard: condensed uppercase display headline hierarchy (locked wording, new scale), phone number as the largest element on screen, twin amber peer buttons, dust-containment rendered as a bold rectangular "spec badge."
4. **Mobile first viewport:** Number + twin amber full-width buttons fill the lower half of the first screen; nothing else competes.
5. **Full header:** Flat utilitarian top bar — identity as a strong wordmark, nav as plain uppercase text items, contact block right with number text + twin amber buttons.
6. **Sticky transition:** Slim ink-black bar, amber twin buttons, white number text; identical on mobile.
7. **Call/Text parity:** Identical amber blocks, fixed Call → Text order.
8. **Number readability:** Number is the typographic hero of masthead, sticky bar and footer.
9. **Gallery discovery:** A numbered index grid (big cedar numerals + thumbnails) directly under the hero; reads like a project ledger.
10. **Homepage + 89 photos:** Gallery moved up (flagged DOM reorder) as a large-tile numbered ledger grid, interleaved every ~2 rows with a thin amber contact strip so no scroll depth lacks an action.
11. **Deep-scroll access:** Sticky bar plus the interleaved contact strips on gallery/video/assessment pages.
12. **YouTube demoted:** Plain thumbnail list under a proof heading; buttons in ink black.
13. **360px fix:** Same fluid discipline; condensed type scales down cleanly; amber pair stacks full-width.
14. **Consistency:** One flat, border-light system across all pages; numbering motif unifies galleries, sections and footer.
15. **Advantages/tradeoffs/risks:** Maximum immediacy and distinctiveness; strongest small-phone legibility. Tradeoffs: furthest from current identity; risks feeling austere or overly aggressive to some premium prospects; amber-on-white requires care for contrast compliance (dark text on amber passes). Same flagged DOM-reorder risk.

---

## Recommended direction

**Direction 1 — "Workshop Billboard."** Reasoning: (a) the audit shows the core failures are hierarchy and signal dilution, not content — Direction 1 fixes both most decisively (red reserved for contact, billboard masthead, gallery pulled forward); (b) the owner-confirmed lead history says people called straight off a prominent number — Direction 1 makes the number the persistent typographic centerpiece on every device; (c) it is the strongest answer to the boutique concern while staying contemporary and craft-specific, avoiding both the dated legacy look and a generic contractor template; (d) it preserves all locked content, the full 89-photo portfolio and every URL. Direction 2 is the fallback if the owner wants to retain dark-premium equity; Direction 3 if the owner wants maximum differentiation and accepts the boldest departure.

## Direction 1 — mobile design commitments (owner-requested confirmation, 2026-08-13)

Recorded at owner request prior to direction selection. These take effect only if Direction 1 is selected; they bind the later implementation plan.

- **Mobile is first-class, not compressed desktop.** The phone layout is its own composition: single-column hierarchy ordered for glance-and-thumb use (identity → number → twin actions → proof badge → gallery preview), with desktop scaled up from it.
- **Width coverage.** One fluid phone layout spanning the 360px baseline and common larger phones (~390/414/430px): no fixed min-widths, no clipped content, buttons and text reflow rather than overflow at any width in that range; tablet gets an intermediate two-column step rather than a stretched phone layout.
- **Complete Call/Text visibility.** Twin solid red peer buttons, full-width and stacked, both fully visible inside the first viewport at 360–430px. Neither button is clipped, hidden or deprioritized.
- **Readable phone number.** The digits appear as large live text directly above the twin buttons in the first mobile viewport, again in the sticky bar and footer — tappable, but never existing only inside a button.
- **Non-obstructive sticky controls.** The mobile sticky bar is a slim single row (identity, number text, twin compact actions) budgeted to roughly a tenth of viewport height; it never covers content, never expands without a deliberate tap, and carries the same hierarchy as desktop.
- **Navigation.** The hamburger opens a simple full-height menu panel of large touch rows listing the existing nav items; no YouTube item in nav; the panel never hides the Call/Text pair below it when closed.
- **Touch targets.** All interactive elements — twin CTAs, sticky controls, menu rows, gallery tiles, lightbox controls — meet current comfortable touch-target standards (approx. 44px minimum).
- **Gallery discovery on mobile.** The numbered project index appears within the first scroll; tiles are large and numbered; the full 89-photo wall follows the services overview per the flagged reorder.
- **Lightbox (owner spec binding).** Opens at near-fullscreen size on phones, offers a fullscreen option, displays the existing photo numbering, and closes by tapping outside the image as well as via a visible close control.

**Still undecided (non-blocking; resolved during implementation planning, not before direction selection):** exact sticky-bar height tuning, lightbox gesture details (e.g., swipe between photos), menu panel animation, precise tablet breakpoint values, and on-device verification on the owner's Samsung (360px overflow + sticky feel).

## Binding owner decisions recorded at direction selection (2026-08-13)

Issued by the owner together with the Direction 1 selection. These bind the implementation plan and override any conflicting wording in the Direction 1 description above.

- **Brand lockup preserved.** The existing header lockup — the current logo, "San Diego Hardwoods," and the exact tagline **"San Diego's Finest Hardwood Floor Specialist Since 1990"** — is preserved as-is. The tagline must not be replaced with alternate wording (this supersedes the "Est. 1990 • San Diego County" line in Direction 1 point 3). The full lockup stays prominent in the initial desktop and mobile masthead; the compact sticky state may omit **only the tagline** when necessary for space.
- **Hero video relocated, not removed.** The current homepage hero video is removed **only from the first viewport**, not from the website. Its existing video/embed destination is preserved, and it is relocated into a clearly labeled supporting-proof section below the primary billboard/contact experience (refines Direction 1 point 12). It must be integrated so it does not look out of place or weird in the new design.

## Functional questions and owner answers

None blocking. The owner-confirmed header behavior, equal Call/Text priority, gallery/lightbox requirements and locked-content list supplied everything material to the directions above. Non-blocking verification item recorded below.

## Decision log

- 2026-08-13 — Live visual audit completed and accepted as authoritative evidence base (`docs/LIVE-VISUAL-CONVERSION-AUDIT-2026-08-13.md`).
- 2026-08-13 — Owner confirmed: sticky header exists but is visually insufficient; Call and Text are equal peer actions; gallery must move earlier with all 89 photos and numbering; lightbox spec (larger, fullscreen option, click-outside close); YouTube demoted to supporting proof; dust-containment must stay prominent.
- 2026-08-13 — Three visual directions presented; Direction 1 recommended. Awaiting owner selection. (Agent recommendation — not yet an approved decision.)
- 2026-08-13 — Owner requested confirmation that Direction 1 treats mobile as first-class; mobile design commitments recorded (see dedicated section). Direction selection still pending.
- 2026-08-13 — **Owner selected Direction 1 ("Workshop Billboard"), including its recorded mobile design commitments.** The mobile design commitments section is now binding on the implementation plan. Directions 2 and 3 are retired. No implementation authorized yet.
- 2026-08-13 — **Owner issued binding decisions on the brand lockup and hero video** (see dedicated section): the existing header lockup — logo, "San Diego Hardwoods," and the exact tagline "San Diego's Finest Hardwood Floor Specialist Since 1990" — is preserved and stays prominent in the initial desktop and mobile masthead; the hero video is removed only from the first viewport and relocated, destination/embed preserved, into a supporting-proof section below the billboard/contact experience, styled so it does not look out of place.
- 2026-08-13 — Implementation-planning phase authorized and completed (documentation only). Planning-time owner decisions: dark mode removed entirely (light-only site); homepage gallery moves to immediately after the dust-containment section; hero video relocates into the dust-containment section (embed destination + VideoObject preserved); baked-in photo watermarks left untouched; explore bar (scroll hint) removed site-wide per owner direction. Full plan: `docs/2026-08-13-direction-1-implementation-plan.md`. **Awaiting owner approval of the plan.**
- 2026-08-13 — **Visual Proof checkpoint executed** (owner-directed): shared visual system (light-only tokens, billboard masthead, twin-red sticky bar, drawer/footer, lightbox spec) and homepage composition built in the generator only (`build/chrome/*`, assembly scripts, `build/data/index/main_content.html`) and regenerated into the local non-production `index.html`. Six+ proof captures taken via headless Chrome at 1440×900 and 360×800 (fold, sticky, full-page, gallery wall, lightbox desktop/mobile); zero horizontal overflow at all captured widths; 89 badges, both VideoObject blocks, and the relocated hero embed verified in built output. Captures stored outside the repo (local temp). Uncommitted; other 12 pages not yet regenerated. **Awaiting owner approval or revision of the visual proof.**
- 2026-08-13 — **Owner reviewed the visual proof; revision 1 applied and re-captured.** Owner decisions: (a) masthead branding enlarged (logo 96px, name 40px, tagline 17px) and phone number enlarged in Palatino serif (~46px desktop / 35px mobile) — the number was confirmed to already be a `tel:` link; (b) mobile masthead email removed as clutter (remains in drawer/footer/contact page); (c) hero kicker hidden on ≤1020px only (owner-approved; remains in DOM, crawlable, visible on desktop); (d) deep-cleaning section moved above the 89-photo gallery — supersedes the earlier "directly after dust containment" placement; new order: hero → index strip → Free Assessment → dust containment + video → deep cleaning → gallery → Bona band → …; (e) sticky bar reworked: bigger brand, wide centered serif number, wider twin Call/Text buttons; (f) legacy Turbify/Yahoo stylesheet links approved for removal (presentation-only, no SEO impact) — removed from all build scripts and the homepage head. The full-page "duplication" the owner asked about was confirmed to be a Playwright fullPage stitching artifact, not a page defect (DOM verified: 1 hero, 1 H1, 89 badges; clean single-render capture shows one coherent page). Still uncommitted; awaiting owner approval or further revision.
- 2026-08-13 — **Revision 2 applied and re-captured.** Owner decisions: (a) the deep-cleaning section's own trailing CTA button row removed as a duplicate — the neutral contact band directly above the gallery is now the single CTA at that junction; (b) hero photo no longer cropped (was `object-fit:cover` square-ish) — renders at natural aspect ratio, top-aligned flush with the H1, taking its natural length; (c) owner raised the mixed bold/non-bold sentence styling as questionable-looking — discussed; the bold runs are existing approved content from the live site (locked wording/emphasis), retained as-is unless the owner orders a content-level change. Overflow remains 0px at all captured widths; 89 badges intact. Still uncommitted; awaiting owner approval or further revision.
- 2026-08-13 — **Owner correction to revision 2(b): the natural-length hero photo is DESKTOP ONLY.** On mobile (≤920px) the hero photo is cropped to a fixed 420px height (`object-fit:cover`) so it doesn't run excessively long; desktop keeps the full natural-length rendering. Verified by capture (`r2-mobile-herophoto-360.png`). **Standing rule from the owner: never apply a desktop-directed change globally to mobile — desktop and mobile compositions are decided separately.** Still uncommitted.
- 2026-08-13 — **Owner approved the revision-2 visual proof and the implementation plan** (including the §9 DOM-reorder SEO-risk acknowledgement). **Full implementation executed the same day** through the build/ generator only, per the plan's gated sequence: (1) dark-mode remnants removed (`darkmode_boot_scripts.html` + `scrollhint_and_toggle.html` partials deleted, drawer-theme CSS removed, videos-page `body.darkmode` rules removed, `theme-color` → `#f8f4ec` on all pages) and 360px overflow verified at 6 widths × 13 pages = 0px; (2) chrome verified across all six templates (lockup + tagline once per page, twin red Call→Text in masthead/sticky/drawer at all widths, no YouTube in nav/drawer, no inline red on mailto); (3) homepage verified (89 badges, both VideoObject blocks, video mounted in dust section, approved r2 section order); (4) gallery pages 1–4 + 5 + solid wood: twin red CTA pairs, G3–4 video-cta neutralized + twin pair, neutral contact bands after every 4th project card and at module-list end (G1:5, G2:6, G3:3, G4:5), module grids enlarged with light matting and single-column on phones, figure/img/h3 counts byte-identical to live, lightbox spec verified behaviorally (larger view, fullscreen button, `#N · n / total` counter, outside-click + Esc close); (5) videos page: `.vid-watch` → ink, `.vid-flag--short` → neutral, hero/bottom pairs → twin red, contact band after library grid, filter + modal verified functional; about/blog/deep-cleaning/contact/assessments: every CTA row normalized to twin red Call→Text, assessments Email button quieted, contact-page mailto red removed; red reserved to contact controls site-wide; (6) QA sweep: zero horizontal overflow (13 pages × 6 widths), zero missing internal link targets, titles/H1s byte-identical on all 13 pages, sitemap URL+image set identical (13 URLs / 352 images), robots/_headers/_redirects untouched, 52 fold+sticky captures reviewed. All changes uncommitted; analytics smoke test deferred to preview (gtag is production-host-gated by design). **Awaiting owner confirmation to deploy the noindexed `redesign` preview for owner review + Samsung on-device check.**

## Open decisions

1. ~~Owner to select a visual direction (1, 2 or 3)~~ — **Resolved 2026-08-13: Direction 1 selected**, including its mobile design commitments.
2. **Visual Proof checkpoint (owner-directed, 2026-08-13):** before full implementation, a partial non-production build of Direction 1 (shared visual system + homepage composition only) is captured at specified desktop/mobile/sticky/full-page/lightbox views for owner approval or revision. No commits, no production, no page-specific work beyond the homepage. Anything simulated or incomplete is identified when the proof is presented.
3. Non-blocking verification: confirm whether the 360px overflow is visible on the owner's Samsung device (audit S1 was captured via headless browser at 360×800).
4. Direction 1 selected: homepage gallery reorder is a flagged DOM/content-order change requiring explicit owner acknowledgement of SEO-risk review at implementation time. **Risk review written** (implementation plan §9); owner acknowledgement requested as part of plan approval.
5. Any genuinely new wording discovered during implementation (e.g., labels for new nav aids) must be flagged for owner approval at that time.

## Last completed work

Read-only live visual audit of all 13 sitemap pages (desktop 1440×900, mobile 360×800) → audit document delivered. Visual-direction phase: three directions + recommendation recorded; owner selected Direction 1 (2026-08-13) with binding mobile, lockup and hero-video decisions recorded here. Implementation-planning phase (2026-08-13): targeted inspection of the build pipeline (chrome partials, assembly helpers, per-page build scripts) and a full implementation plan with 13-URL coverage matrix delivered at `docs/2026-08-13-direction-1-implementation-plan.md`. No site changes made.

## Next authorized action

Owner reviews the completed implementation. With owner confirmation: deploy the noindexed `redesign` preview Worker for owner review (including the analytics smoke test and the Samsung on-device check), then commit at checkpoints the owner approves. No production cutover in this phase.

## Implementation status

**Implementation complete locally (uncommitted).** All 13 pages regenerated from the build/ generator per `docs/2026-08-13-direction-1-implementation-plan.md`; all six execution gates verified (see decision log, 2026-08-13 final entry). Nothing committed or deployed; production cutover remains out of scope.
