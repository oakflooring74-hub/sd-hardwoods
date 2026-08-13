# Direction 1 "Workshop Billboard" — Implementation Plan

**Date:** 2026-08-13
**Status:** Draft for owner approval. No code, content, configuration or assets have been changed. Implementation begins only after explicit owner approval of this plan.
**Authoritative inputs:** `docs/SITE-CONVERSION-REMAKE-MASTER-PLAN.md` (Direction 1 + mobile commitments + binding owner decisions), `docs/LIVE-VISUAL-CONVERSION-AUDIT-2026-08-13.md`, and the owner answers recorded below.

---

## 1. Owner decisions recorded during planning (2026-08-13)

1. **Dark mode removed entirely.** The site becomes light-only. The dark-default boot script, the `body.darkmode`/`html.sdh-dark` variable overrides, and the drawer theme toggle are all removed.
2. **Homepage gallery placement:** the 89-photo gallery moves to immediately **after the dust-containment section** (order: hero → Free Phone & Photo Assessment → dust containment → gallery → deep cleaning → Bona band → …). Flagged DOM reorder — see §9.
3. **Hero video placement:** the current hero YouTube embed (`zKs_lbzRd5E`, youtube-nocookie, "Dust-Contained Refinishing") is removed from the first viewport and relocated **into the dust-containment section**, embed destination and VideoObject JSON-LD preserved. It shows exactly that process, so it reads as proof, not decoration.
4. **Baked-in photo watermarks left untouched.** The "SAN DIEGO HARDWOODS" watermarks are inside the image files (no code overlay exists to restyle). Red dilution is addressed everywhere code controls it; image files are not reprocessed in this phase.
5. **Explore bar (scroll hint) removed** — owner direction given during planning: it does nothing good for the current site and would pollute the revised one. The `scrollhint_and_toggle.html` partial and its two injection points are removed.

## 2. Locked constraints (from the master plan — unchanged)

All URLs/filenames, titles/metadata, H1–H3 wording and levels, body wording, schema, canonicals, internal-link destinations, image URLs, alt text/captions, phone number and business identity stay byte-identical. New containers/controls reuse only existing approved wording ("Call 858-699-0072", "Text Floor Photos", "Text Photos for a Free Assessment", "True 100% Dust Containment", existing gallery/section headings). No hiding/collapsing/paginating content. All 89 homepage photos remain, numbered. The one approved DOM/content-order change is the homepage gallery move (§9).

## 3. Build mechanics (how changes land)

All 13 root HTML pages are generated artifacts. Implementation edits the generator, never the generated files:

- **Shared chrome:** `build/chrome/site_css.html` (design tokens + components), `top.html` (masthead/nav/mini-header/drawer), `footer.html`, `lightbox.html`, `darkmode_boot_scripts.html`, `scrollhint_and_toggle.html`, `analytics.html` (untouched).
- **Per-page bodies:** `build/scripts/pages/build_*.py`, `build/scripts/common/build_page.py` (galleries 3–4), `build/scripts/common/assemble_page.py`, and `build/data/index/main_content.html` (homepage body).
- **Regenerate:** `python build/scripts/build_all.py`, then review `git diff` before any commit (README quirk #1: homepage regeneration produces a small expected diff from later CSS refinements — review, then accept deliberately).
- **Preview/QA:** headless-Chrome captures at 360/390/430/768/1440 px on a scratch install outside the repo (per build/README convention); push to `redesign` deploys the noindexed preview Worker. No production deploy path exists yet — nothing in this phase can reach production.

## 4. Workstream A — Design tokens and global CSS (`chrome/site_css.html`)

- Light-only palette per Direction 1: warm off-white/paper canvas (existing `--canvas:#f8f4ec` family fits), near-black walnut ink, **signal red `--cta-red:#b3261e` reserved exclusively for direct-contact controls**, muted wood-bronze (existing `--brass` family) reserved for trust marks (Est. 1990 line, Bona, dust-containment badge).
- Delete the `html.sdh-dark, body.darkmode` override block and every `body.darkmode` descendant rule across all partials and page-level CSS (videos page has its own dark rules in `build_videos.py` PAGE_CSS).
- Delete `chrome/darkmode_boot_scripts.html` and its injection in `assemble_page.py` / `build_page.py`; delete the `.drawer-theme` toggle button from `top.html`. Update `<meta name="theme-color" content="#4b2e06">` to the new light canvas tone (flagged: a browser-UI metadata attribute only — no wording, ranking or indexation impact).
- **360px overflow fix (audit S1, critical):** diagnose the effective min-width (suspects: the legacy Turbify stylesheets still linked on every page — `assets/legacy-css/mc_global.195798.css`, `theme.css`, `beforenafter_1.css` — and any fixed-width component rules). Fix with genuinely fluid rules: no fixed min-widths, `min()`/`clamp()` sizing, wrapping flex rows. Verify at 360/390/414/430 px that nothing clips.
- **Legacy CSS link removal (candidate, verification-gated):** after the site's own CSS fully covers layout, remove the three legacy Turbify `<link>` tags from head assembly and confirm zero visual regression by before/after capture. If any regression appears, keep the links and fix the overflow in our own CSS instead. Decision made at implementation on evidence, not assumed.
- `.btn-outline` becomes the neutral walnut/bronze secondary style for all non-contact links (deep-cleaning links, gallery navigation, video links). `.btn-call` (red) is used **only** for tel:/sms: actions.
- Fix S7 letterboxing cosmetically: gallery card background moves from dark to the light canvas tone, so `object-fit:contain` empty areas read as intentional matting instead of broken dark boxes. No cropping (no `object-fit:cover`) — preserves every photo fully.

## 5. Workstream B — Masthead, nav, sticky bar, drawer, footer (`chrome/top.html`, `chrome/footer.html`)

**Masthead (billboard, desktop):** preserved brand lockup left (logo + "San Diego Hardwoods" + exact tagline "San Diego's Finest Hardwood Floor Specialist Since 1990" — binding owner decision, unchanged wording); contact block right: phone number set very large as live tappable text, **twin identical solid red buttons — Call first, Text Floor Photos second — directly under it**, email reduced to a quiet plain text link. Dust-containment proof mark (small bronze badge, existing "True 100% Dust Containment" wording) sits in the masthead/hero region.

**Masthead (mobile, 360–430px):** full lockup (tagline included) → large readable number as live text → twin full-width stacked red peer buttons, both fully visible in the first viewport. Nothing clipped; blocks wrap, never overflow.

**Nav band:** existing items and dropdowns unchanged, pill styling removed; **the outbound `.nav-youtube` pill is removed from the nav** (YouTube demotion; the internal Videos page link stays in the Videos dropdown). The one outbound "Watch Our Work on YouTube ↗" item inside the Videos dropdown is also removed for consistency — flagged here as a nav-content reduction (an outbound convenience link, not indexed content; the videos page itself keeps all its YouTube links).

**Sticky mini-header:** slim light bar — identity (logo + name, tagline omitted here only, per binding decision), phone number as readable text, and **twin compact red Call / Text buttons** (today it carries Call red + Text outline and hides Text under 900px — that ends; both actions present at all widths, hierarchy identical to desktop). Target ≈ a tenth of viewport height; never covers content (existing slide-in behavior and IntersectionObserver trigger retained).

**Drawer (mobile menu):** existing panel structure retained; remove the theme toggle (dark mode retired), remove the YouTube footer link and the outbound YouTube item in the Videos group (mobile commitment: no YouTube item in nav); twin Call/Text CTAs at top stay, restyled twin red; all rows ≥44px touch targets (already near-compliant; verify).

**Footer:** phone number as plain large tappable text plus the twin red peer actions; email link loses its inline red (`style="color:var(--cta-red)"`) and becomes a quiet neutral link; all existing footer wording unchanged.

**Red dilution cleanup in chrome/bodies:** inline `style="color:var(--cta-red)"` on tel:/sms: text links may stay red (they are contact controls); the same styling on **mailto:** links (homepage cards, footer, contact page) becomes neutral — email is visually secondary per the master plan.

## 6. Workstream C — Homepage (`build_homepage.py` + `data/index/main_content.html`)

Current section order: hero (copy + video) → Free Phone & Photo Assessment → dust containment → deep cleaning → Bona band → 89-photo gallery → gallery-nav → specialists/services → assessments → recent projects.

Planned changes:

1. **New billboard hero.** Left: existing kicker, H1, both intro paragraphs (locked wording, untouched), then the phone number as very large live text and the twin red Call / Text peer buttons (replacing today's red-Text/outline-Call pair). Right: one strong existing project photo (chosen from already-hosted gallery images — no new assets) with the dust-containment badge. The `hero-note` paragraph stays. No video in the first viewport.
2. **Hero video relocated** into the dust-containment section (owner decision): same `youtube-nocookie.com/embed/zKs_lbzRd5E` destination, same JS-mounted iframe pattern and parameters, same thumbnail, and the existing VideoObject JSON-LD block moves with it verbatim. Styled inside the section's card rhythm so it reads as proof of the dust-containment claim.
3. **Gallery moved up** to immediately after the dust-containment section (owner decision, flagged DOM reorder — §9). Heading, lede, all 89 figures, `#1–#89` badges, alt text and captions unchanged. Tiles rendered noticeably larger (grid `minmax` raised; light-canvas matting per Workstream A).
4. **"Recent projects" index strip** directly below the hero: a compact neutral-walnut numbered strip linking to the six gallery pages, reusing the existing approved gallery-nav wording ("Recent Project Gallery 1…5", "Solid Wood Floor Gallery"). Never red. This is a new nav aid using existing approved wording — no new wording introduced.
5. **Contact pacing:** a repeated neutral contact band (twin red buttons + large number, existing wording only) immediately before and immediately after the gallery wall, so no scroll depth strands the visitor.
6. **Intro text stays** (locked): the deep-cleaning section, Bona band, specialists/services, assessments and recent-projects sections all remain, in their current relative order, below the gallery.
7. The hero's old red-primary-Text / outline-Call assignment and the mid-page red-Call band (main_content lines 135–138) are normalized to the twin-red-peer pattern everywhere on the page.

## 7. Workstream D — Gallery pages 1–4 (`build_gallery1.py`, `build_gallery2.py`, `common/build_page.py`)

- Hero CTA pair → twin red Call / Text peers (currently red Call + outline Text).
- Galleries 3–4 carry a mid-page video section whose `video-cta` red button and red strong-text are restyled to the neutral/twin pattern.
- **Deep-scroll contact access:** a repeated slim neutral contact band (existing wording only) inserted between project module rows at a fixed cadence (proposal: after every 4th project card) and at the end of the module list — today these pages have no conversion CTA between hero and footer across 8,000–13,000 px. New containers, existing wording.
- The `.gallery` two-column module grids get the same larger-tile / light-matting treatment; gallery-progress bar styling moves to neutral walnut/bronze (its active dot is currently walnut — fine).
- Before/after figures, captions, module headings, counts: untouched.

## 8. Workstream E — Gallery 5, Solid Wood, Videos, and the four content pages

**Gallery 5 (`build_gallery5.py`) & Solid Wood (`build_solidwood.py`):** hero pairs → twin red; end-of-page CTA rows → twin red peers (today: red Call + outline Text, mixed with outline nav buttons which become neutral); project cards/pagination untouched. Both are short enough that no mid-page bands are needed (gallery 5 paces well already — audit).

**Videos page (`build_videos.py`):** the dozens of red `.vid-watch` buttons are restyled to plain dark ink buttons; `.vid-flag--short` red badge → neutral; hero pair → twin red; bottom pair → twin red; the `.btn-yt` channel buttons stay quiet/neutral; red is gone from this page except the twin contact pairs. Filter UI, modal player, featured section, JSON-LD: untouched. End-of-section neutral contact band added after the library grid (existing wording).

**About (`build_about_us.py`), Blog (`assemble_blog.py`), Deep-cleaning (`assemble_deep_cleaning.py`), Contact (`build_contact_us.py`), Assessments (`build_floor_assessments.py`):** every CTA row normalized to the twin red peer pair (Call first, Text second) — today these pages variously lead with Text or Call (audit S3; full mapping in §11). The assessments page's three-button card (Text / Call / Email-outline) keeps its third Email button as a quiet neutral outline. No body wording, section order, or content changes on these five pages. Contact page layout already validated as strongest — styling only.

**All pages:** hero `.kicker` "Est. 1990 • San Diego's Finest Hardwood Flooring Specialist" line stays verbatim; masthead tagline is the separate locked lockup tagline — both remain.

## 9. Flagged DOM/content-order change — SEO-risk review (owner acknowledgement required)

**The only DOM reorder in this plan:** on the homepage, the `<section class="block">` containing the 89-photo gallery (heading "Real San Diego Hardwood Floor Projects" + lede + grid) moves from position 6 to position 3, immediately after the dust-containment section. Additionally the hero video embed and its VideoObject block move from the hero into the dust-containment section.

- **What does not change:** every URL, the sitemap, all headings and their levels, all body wording, all image URLs/alt/captions, all schema content (the VideoObject block moves location in the DOM but its content is byte-identical; its `contentUrl`/`embedUrl`/thumbnail are unchanged), all internal-link destinations, all 89 photos and their numbering.
- **Risk assessment:** search engines render and index full pages; moving indexable content earlier in the DOM is generally neutral-to-positive for the moved content (image content sits closer to the top; the gallery's internal image links get earlier crawl priority). The textual sections that move *down* (deep cleaning, Bona, specialists) remain fully visible and crawlable in the same document. No content is hidden, collapsed, or deferred. Video structured data remains on the same URL.
- **Residual risks:** (a) relative prominence shifts among sections could nudge ranking signals for homepage queries in either direction; (b) if any section were accidentally dropped during the edit it would be a content loss — mitigated by the build check (89 figures counted) plus a full-text diff review of regenerated output limited to the intended move.
- **Mitigations:** regenerate → `git diff` review confirming only the intended blocks moved; verify all 89 figures, badge numbers, both VideoObject blocks, and section count in built output; re-run headless captures; monitor GSC after preview sign-off (production cutover is a separate later decision).

**Owner acknowledgement of this review is requested as part of plan approval.**

## 10. Functionality changes (non-visual)

- **Lightbox (`chrome/lightbox.html`):** per owner spec — opens larger (raise max dimensions; near-fullscreen on phones), adds a fullscreen-option button (Fullscreen API) alongside the existing close control, closes by clicking/tapping outside the image (already implemented — retained), keeps the caption and adds the photo's existing `#N` numbering (read from the figure's `.gallery-badge` when present, shown with the existing `n / total` counter). Keyboard behavior (Esc/arrows) retained. Touch/swipe gestures: deferred to the non-blocking tuning list.
- **Explore bar removed:** delete `scrollhint_and_toggle.html` and its injection/replace calls in `assemble_page.py` and `build_page.py` (owner-directed). Nothing else references it.
- **Dark mode removed:** see Workstream A. The `sdh-theme` localStorage key simply becomes unread; no migration needed.
- **Analytics (`chrome/analytics.html`) untouched:** its conversion events key off `tel:`/`sms:`/`mailto:` hrefs and assessment-link destinations, all of which survive unchanged. Post-build verification: click-test one tel:, one sms:, one mailto:, one assessment CTA in the preview and confirm events still fire.
- **Mini-header / drawer JS:** retained with small edits (twin-button markup, no theme toggle, no YouTube items). No new JS frameworks; vanilla JS consistent with the existing codebase.

## 11. CTA normalization map (audit S3 fix)

Red-primary assignment today vs. planned (every page → **twin solid red peers: Call → Text**):

| Page | Hero today | Planned (all CTA rows site-wide) |
|---|---|---|
| index | Text red / Call outline | Twin red: Call, Text |
| contact_us | Text red / Call outline | Twin red: Call, Text |
| about_us | Call red / Text outline (mixed mid-page) | Twin red: Call, Text |
| blog | Call red / Text outline | Twin red: Call, Text |
| deep-cleaning | Call red / Text outline | Twin red: Call, Text |
| floor-assessments | Text red / Call outline (+ Email outline) | Twin red: Call, Text (+ quiet Email) |
| galleries 1–4 | Call red / Text outline | Twin red: Call, Text |
| gallery 5 | Call red / Text outline | Twin red: Call, Text |
| solid_wood | Call red / Text outline | Twin red: Call, Text |
| videos | Text red / Call outline | Twin red: Call, Text |
| header (desktop) | Text red | Number text + twin red |
| header (mobile) / mini-header | Call red, Text hidden <900px | Number text + twin red, all widths |

## 12. Coverage matrix — all 13 URLs

| URL | Template | A: tokens/CSS | B: chrome (masthead/sticky/nav/footer) | C: hero/body changes | D/E: page-specific | F: lightbox | Removed items |
|---|---|---|---|---|---|---|---|
| `/` (index) | T1 | ✓ | ✓ | Billboard hero, video→dust section, gallery move, index strip, contact bands | — | ✓ | Dark mode, explore bar, hero video in viewport 1 |
| `contact_us.html` | T2 | ✓ | ✓ | CTA normalization only | — | (no gallery) | Dark mode, explore bar |
| `about_us.html` | T3 | ✓ | ✓ | CTA normalization only | — | (no gallery) | Dark mode, explore bar |
| `blog.html` | T4 | ✓ | ✓ | CTA normalization only | — | ✓ (.gallery nav widgets excluded today — preserved) | Dark mode, explore bar |
| `deep-cleaning-hardwood-floors-san-diego.html` | T4 | ✓ | ✓ | CTA normalization only | — | ✓ | Dark mode, explore bar |
| `floor-assessments-inspections.html` | T4 | ✓ | ✓ | CTA normalization (3rd Email button quieted) | End-of-section contact band | (no gallery) | Dark mode, explore bar |
| `recent_project_photo_gallery_1.html` | T5 | ✓ | ✓ | Hero pair → twin red | Mid-list + end contact bands, larger tiles | ✓ | Dark mode, explore bar |
| `recent_project_photo_gallery_2.html` | T5 | ✓ | ✓ | same as G1 | same as G1 | ✓ | Dark mode, explore bar |
| `recent_project_photo_gallery_3.html` | T5 | ✓ | ✓ | same + mid-page video CTA restyle | same as G1 | ✓ | Dark mode, explore bar |
| `recent_project_photo_gallery_4.html` | T5 | ✓ | ✓ | same + mid-page video CTA restyle | same as G1 | ✓ | Dark mode, explore bar |
| `recent_project_gallery_5.html` | T5 | ✓ | ✓ | Hero pair → twin red | End CTA row → twin red | ✓ | Dark mode, explore bar |
| `solid_wood_floor_photo_gallery.html` | T5 | ✓ | ✓ | Hero pair → twin red | End CTA row → twin red | ✓ | Dark mode, explore bar |
| `videos_of_refinishing_process.html` | T6 | ✓ | ✓ | Hero/bottom pairs → twin red | `.vid-watch` red→ink, badge neutral, post-library contact band | (modal player, not lightbox) | Dark mode, explore bar |

## 13. Execution sequence (each step ends in a verification gate)

1. **Tokens + dark-mode removal + overflow fix** (`site_css.html`, `darkmode_boot_scripts.html`, assembly scripts) → regenerate all 13 → 360/390/430/768/1440 captures, no clipping anywhere.
2. **Chrome rework** (`top.html`, `footer.html`) → regenerate → verify masthead/sticky/drawer/footer on all templates, both peer actions everywhere, lockup intact, no YouTube pill/items, explore bar gone (also step 1's scripts), analytics smoke test.
3. **Homepage rework** (`main_content.html`, `build_homepage.py`) → regenerate → diff review limited to intended moves; 89 figures + badges counted; both VideoObject blocks present; video plays in dust section.
4. **Gallery pages** (1–4, 5, solid wood) → regenerate → module counts unchanged, bands present, lightbox spec verified (larger view, fullscreen toggle, outside-tap close, numbering).
5. **Videos + remaining content pages** → regenerate → red reserved check (no red outside contact controls), filter/modal functional.
6. **Full-site QA sweep** → all 13 pages × 5 widths, link/CTA spot checks, legacy-CSS removal decision on evidence, then owner preview review on the `redesign` deployment. Owner's Samsung on-device check (360px overflow + sticky feel) before any production consideration.

Non-blocking tuning items deferred into implementation (per master plan): sticky-bar exact height, lightbox swipe gestures, drawer animation, tablet breakpoint values.

## 14. Out of scope for this phase

Production cutover configuration; reprocessing watermarked image files (owner decision: untouched); YouTube snapshot refresh; any wording/heading/URL/metadata changes; any new pages.

## 15. Approval requested

Approval of this plan authorizes: the chrome/CSS/JS and build-script edits described above, regeneration of all 13 pages, preview deployment to `redesign`, and the QA steps listed — with the §9 DOM-reorder risk review acknowledged. Commits will be proposed at implementation checkpoints; nothing is committed or deployed without owner confirmation at each gate.
