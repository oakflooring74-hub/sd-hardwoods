# Live Visual Conversion Audit — sdhardwoods.com

**Date:** 2026-08-13
**Scope:** Read-only visual audit of the live website. No code, content, wording, SEO, or functionality evaluated or changed. Business objective context: increase qualified phone calls and contact-path (call / text-photos / email) actions, without increasing unqualified inquiries. Owner reports the former site had more prominent CTAs and produced more medium/smaller-job inquiries; treated as context, not proof.
**Method:** URLs taken from the live `https://www.sdhardwoods.com/sitemap.xml` (13 canonical HTML pages; image/asset URLs excluded). Rendered captures via headless Chrome at desktop **1440×900** and mobile **360×800**, 100% zoom, plus a 500×800 diagnostic capture. Full-page tall-window captures used for top-to-bottom inspection. Screenshots stored outside the repository (local temp directory). Each finding below separates **Evidence** (directly observed) from **Interpretation**.

---

## 1. URLs audited, grouped by shared template

All 13 sitemap pages were audited. Every page shares the same header (logo + name, CALL number, email, red header button) and footer (dark card with red text contact links + copyright). Groups below are by body layout.

| Group | URLs |
|---|---|
| **T1 — Homepage (unique body)** | `/` |
| **T2 — Short contact page** | `contact_us.html` |
| **T3 — Short about page** | `about_us.html` |
| **T4 — Long-form content pages** (hero + CTA pair, mixed text/photo sections) | `blog.html`, `deep-cleaning-hardwood-floors-san-diego.html`, `floor-assessments-inspections.html` |
| **T5 — Project gallery pages** (hero + CTA pair, long before/after photo rows) | `recent_project_photo_gallery_1.html`, `recent_project_photo_gallery_2.html`, `recent_project_photo_gallery_3.html`, `recent_project_photo_gallery_4.html`, `recent_project_gallery_5.html`, `solid_wood_floor_photo_gallery.html` |
| **T6 — Videos page** | `videos_of_refinishing_process.html` |

## 2. Representative pages fully audited (desktop fold + full page, mobile fold + full page)

- T1: `/` (homepage)
- T2: `contact_us.html`
- T4: `floor-assessments-inspections.html`
- T5: `recent_project_photo_gallery_1.html`
- T6: `videos_of_refinishing_process.html`

All remaining URLs received desktop-fold, mobile-fold, and full-page scans; `about_us.html` and `recent_project_gallery_5.html` noted as variants (below).

## 3. Bottom-line visual assessment

**Desktop:** Professional, consistent, credible. On all 13 pages the header contact cluster and a hero CTA pair are visible within the first 900 px. The visual problems are pacing and competition, not absence: pages are extremely long (homepage ≈ 17,500 px, of which roughly 10,000 px is one photo gallery; galleries/videos run 5,500–13,000 px), conversion CTAs are sparse in the long middle stretches, there is no persistent/sticky contact action, and the bright red "primary action" color is shared with dozens of non-conversion elements (video watch buttons, text links, photo watermarks). Which contact action gets the primary red treatment flips between templates (and between desktop and mobile headers).

**Mobile (360×800):** One systematic defect dominates: **every page renders wider than a 360 px viewport**, clipping the right side of the header CTA, the hero's secondary button, and body text (mid-word cutoffs). At 500 px width everything fits cleanly. On text-heavy pages the first hero CTA lands at or below the first viewport edge even before accounting for the clipping. Mobile is where the owner-reported weakness in inbound actions is most visually plausible.

**Overall:** The site visually reads as a portfolio first and a contact funnel second. That plausibly contributes to the reported lead-mix change (interpretation, not proof), most strongly on mobile.

## 4. CTA-reachability summary

**Desktop (1440×900) — all pages:**
- Header (top of every page): large white `CALL 858-699-0072` (plain text styling, not button-styled), small grey `Text Floor Photos / sandiegohardwoods@gmail.com` line, and a bright red button — all above the fold site-wide.
- Hero CTA pair (red primary + gold-outline secondary) visible above the fold on all 13 pages (approx. y 380–700). On the homepage the red hero button is fully visible (~y 790–850) and the gold call button straddles the fold edge (~y 870–900, partially cut).
- Mid-page: red CTA band partway down on homepage, blog, deep-cleaning; assessments page repeats the CTA pair inside its "Free Phone & Photo Assessment" card and at the bottom. Gallery and video pages carry essentially no conversion CTA between the hero and the footer across thousands of px of photos/videos.
- Footer (every page): red text links (`Text Photos | Call | email`) — on long pages these sit 6,000–17,000 px down.

**Mobile (360×800):**
- Header: hamburger `Menu` + red `Call 858-…` button — **right portion clipped off-screen on every page** (overflow defect). A partial red call button remains visible/tappable at top.
- First hero CTA visible within the first 800 px viewport: `contact_us` (~y 470), `about` (~y 585), galleries 1/2/5, `solid_wood`, `deep-cleaning` (~y 565–745, red primary only; gold secondary clipped by the overflow).
- First hero CTA at or below the fold edge: homepage (fully below fold), `blog`, `videos`, `floor-assessments-inspections` (edge), gallery 3 (edge), gallery 4 (below).
- After the hero, the next conversion CTA on gallery/videos/assessment pages is typically near the bottom of pages 17,000–20,000 px tall.

## 5. Site-wide findings

**S1 — Mobile horizontal overflow at 360 px (critical).**
- *Evidence:* In every 360×800 capture, all pages are clipped on the right: header red button reads "Call 8…", hero gold button half off-screen, paragraph text cut mid-word. At 500×800 the same pages fit perfectly (verified on homepage). Affects: all 13 URLs, mobile only, full page height.
- *Interpretation:* The layout's effective minimum width sits somewhere between 361–500 px, so small phones (360 CSS px is a common Android width) get horizontal scrolling and partially hidden CTAs. This is the single largest reachability problem observed. Captures are headless-browser renderings; confirm on a physical 360 px device before prioritizing fixes.

**S2 — No persistent contact action on long pages.**
- *Evidence:* In full-page captures, contact actions appear at the hero, on some mid-page red bands (home/blog/deep-cleaning/assessments), and in the footer; nothing follows the scroll. Pages run ≈ 5,500–17,500 px desktop and up to ≈ 20,000 px mobile.
- *Interpretation:* A user deep in a gallery, the videos page, or the homepage photo grid has no visible next step without scrolling to the very end or back to the top. (See §8: sticky-header behavior could not be conclusively verified from static captures.)

**S3 — Primary-action treatment is inconsistent across templates and devices.**
- *Evidence:* On homepage, assessments, contact, and videos pages the **red primary button is the text-photos action** and gold-outline is call. On about, blog, deep-cleaning, and all gallery pages the **red primary button is the call action** and gold-outline is text-photos. The header's red button is text-photos on desktop but call on mobile.
- *Interpretation:* "Red = the thing we most want you to do" means different things on different pages, which weakens the learned visual cue and splits emphasis between the two contact paths rather than backing one.

**S4 — The red action color is diluted by non-conversion uses.**
- *Evidence:* The videos page shows a red `▶ Watch Video` button on every one of dozens of video cards; red is also used for body/footer text links (`Call 858-699-0072`, email, deep-cleaning links) and for the `SAN DIEGO HARDWOODS` watermark across gallery photos; the nav carries a red-icon `Watch on YouTube` pill.
- *Interpretation:* The strongest visual signal on the site frequently leads to YouTube or to nowhere clickable, competing with — and on the videos page vastly outnumbering — the conversion CTAs.

**S5 — Outbound video content gets near-equal billing with contact actions in high-value regions.**
- *Evidence:* Homepage desktop hero: a large YouTube embed occupies the entire right half of the above-the-fold area, with a `Watch Our Work on YouTube` button beneath it; the nav's only pill-styled item is `Watch on YouTube`.
- *Interpretation:* In the most valuable viewport on the site, an exit path to YouTube competes visually with the call/text actions.

**S6 — Extreme page length buries lower content and footer CTAs.**
- *Evidence:* Homepage gallery runs ≈ y 3,800–14,200 (~89 numbered photos); homepage content ends ≈ 17,500 px desktop / ≈ 19,500+ px mobile. Gallery pages 1–4 ≈ 8,000–13,000 px desktop; videos ≈ 12,800 px; mobile versions up to ≈ 20,000 px.
- *Interpretation:* Post-gallery sections (gallery cross-links, assessments promo, project cards, footer CTA links) are effectively unreachable for many users; long unbroken photo scrolls have no action prompts.

**S7 — Letterboxed gallery cards.**
- *Evidence:* Homepage gallery grid contains cards with large empty dark areas above/below the photo (e.g., cards #72, #77), where landscape images sit in portrait-shaped cards.
- *Interpretation:* Minor polish defect; reads as broken/unfinished in an otherwise strong proof section. (Possible capture artifact — see §8 — but the pattern is consistent with real letterboxing.)

## 6. Page-specific findings and outliers

**Homepage `/` (T1)**
- *Evidence (desktop):* Fold shows header cluster, large serif H1, two intro paragraphs, red `Text Photos` button fully visible, gold call button ~partially cut at the fold edge; YouTube embed fills the right column. *Evidence (mobile 360):* No hero CTA within the first viewport at all — the fold is consumed by the eyebrow line, H1 and two paragraphs; only the clipped header call button is present.
- *Interpretation:* On mobile, the homepage delays any contact action further than any other page; on desktop the fold works but shares its attention with the video.

**Contact page (T2)** — strongest conversion layout.
- *Evidence:* Short page (≈ 1,900 px desktop / ≈ 2,600 px mobile). Hero CTA pair high (~y 380 desktop / ~y 470 mobile), followed by three numbered contact-path cards with red action links (text, call, email) and a response-time card.
- *Interpretation:* This is the template the rest of the site most benefits from pointing to; nothing material to flag beyond the site-wide mobile overflow.

**Assessments page (T4 outlier in a good sense)**
- *Evidence:* Hero CTA pair above fold; "Free Phone & Photo Assessment" card repeats the pair immediately below; then a long pricing/FAQ middle (≈ y 2,000–10,000 desktop) with no conversion CTA until the "Ready to Get Started?" section and footer. Mobile ≈ 17,500 px.
- *Interpretation:* Structure matches the business goal (free phone/photo path framed as the first step). The long CTA-free middle on mobile is the weak stretch.

**Blog and deep-cleaning (T4)**
- *Evidence:* Red CTA bands appear at intervals through the body on desktop. On mobile, blog's first CTA sits just below the first viewport; deep-cleaning's is at ~y 690–745 (visible, gold clipped).
- *Interpretation:* Acceptable mid-page CTA presence; mobile intro stack pushes the first action down.

**Gallery pages 1–4 + solid wood (T5)**
- *Evidence:* Hero + CTA pair + info card, then unbroken before/after photo rows with captions to the footer (gallery 1 ≈ 12,900 px desktop / ≈ 19,000 px mobile). No conversion CTA between hero and the bottom band/footer. Gallery 4's longer intro pushes its mobile CTA fully below the first viewport. Shared-template findings S1–S4, S6 apply.
- *Interpretation:* These are proof pages; the proof is thorough but the long middle offers no next step.

**Gallery 5 (T5 outlier)**
- *Evidence:* Different body: five numbered case studies (#81–#85) with side-by-side before/after pairs and a pagination bar (`← Prev 1 2 3 4 5 · Gallery 5 of 5 · Next →`, Next disabled). Much shorter (≈ 5,500 px); CTA button row and footer reachable.
- *Interpretation:* The paginated case-study format paces better than the endless-rows format of galleries 1–4; pagination is only present here.

**Videos page (T6)**
- *Evidence:* Featured embed, then a grid of dozens of video cards each with a red `▶ Watch Video` button and a gold `Watch on YouTube` link; ≈ 12,800 px desktop / ≈ 20,000 px mobile. Conversion CTAs at hero and bottom only.
- *Interpretation:* The page with the most red buttons on the site uses none of them for contact — maximum CTA-color competition (see S4).

**About page (T3)**
- *Evidence:* Short (≈ 3,400 px desktop); hero CTA pair above fold, video embed, mid-page red button, closing CTA pair, footer. Red primary here is the call action.
- *Interpretation:* No material issues beyond site-wide items.

## 7. Prioritized potential improvements (conceptual, visual only — no wording, code, or structural changes implied)

1. **Make the layout fit 360 px phones without horizontal scrolling** so the header call button, both hero buttons, and body text are fully inside the viewport. (Direct reachability fix; highest impact.)
2. **Add one persistent, quiet contact action that follows the scroll** (at minimum on mobile; consider desktop for the very long pages), so a next step always exists mid-gallery/mid-page.
3. **Pick one primary contact action and give it the red treatment everywhere** — same action, same color, desktop and mobile, header and hero — while keeping the secondary path visible but visually subordinate.
4. **Reserve the bright red for conversion actions only**; recolor/restyle video watch buttons and non-action red accents to a quieter treatment so red reliably means "contact us".
5. **Fix the pacing of the longest pages**: fewer inline photos or periodic visual action prompts inside long galleries (the gallery-5 paginated case-study pattern already paces better), so footer CTAs and lower sections are not buried under 10,000+ px of photos.
6. **Raise the first mobile CTA on text-heavy pages** (homepage, blog, videos, gallery 4) by tightening the vertical space the centered intro stack consumes at small widths — spacing/typography-scale adjustments only.
7. **Reduce the visual weight of outbound YouTube elements** (nav pill, homepage hero embed/button) relative to the contact actions in the same regions.
8. **Clean up letterboxed gallery cards** so photos fill their frames (minor polish).

## 8. Could not inspect reliably

- **Sticky/fixed header behavior while scrolling** — static tall-window captures cannot confirm whether any header/CTA element sticks; none was observed floating mid-page, but live scrolling was not simulated.
- **Opened states**: nav dropdowns (Services / Project Galleries / Videos carets) and the mobile hamburger menu; hover/focus states; gallery lightbox behavior. These require interaction, which was out of scope for the capture method.
- **Physical-device confirmation of the 360 px overflow** — findings are from headless Chrome at 360×800 and 500×800; real-device rendering (and any viewport-meta scaling behavior) should be verified before acting on S1.
- **Below-fold lazy-load completeness** — captures used a virtual time budget; a few gallery cards showed empty/letterboxed areas (S7) that could partly be capture artifacts rather than shipped rendering.
- **Below-13,000 px content on the first pass** — the homepage exceeded the initial 13,000 px capture height; it was re-captured at 20,000 px (content ends ≈ 17,500 px). All other pages fit their captures.

---

*Audit performed read-only. No files modified, no code run against the site, no wording/SEO/functionality evaluated. Screenshots kept outside the tracked repository.*
