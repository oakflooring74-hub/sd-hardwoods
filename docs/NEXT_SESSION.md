# Start here — project status as of 2026-07-20

Read this file first when picking this project back up — **together with `docs/PROJECT_OPERATING_MANUAL.md` (the permanent governing document, added 2026-07-18) and `docs/PROJECT_DECISIONS.md` (binding decisions + standing blockers)**. This file links to everything else and tells you what's done, what's approved next, and what to ask the owner before doing anything.

## Milestone 2.12 — Aggressive, Evidence-Grounded Image Alt-Text Expansion (2026-07-20)

Owner-directed, ranking-first milestone (deliberately unconventional-length alt
text by owner instruction). Full requirements:
`docs/SDH_Aggressive_Image_Alt_Expansion_Strategy_July_2026.md`. Full result and
verification record: `docs/2026-07-aggressive-image-alt-expansion-report.md`.

**What shipped:** every meaningful project image (homepage, Galleries 1–5, Solid
& Engineered Installation, Deep Cleaning, Blog, About, Floor Assessments) and
every video thumbnail on the Videos page (previously `alt=""` on all 58) now
carries dense, multi-sentence alt text built entirely from data already in the
repository — owner-approved captions, project titles/descriptions already visible
on the page, per-image alt fields that existed in `modules.json` but were never
actually rendered (Galleries 1–2), and curated video metadata already stored in
`youtube_videos.json`. No facts were invented.

- **413 of 465** total `<img>` usages expanded; **2** intentionally left empty
  (site logo mark, JS-only lightbox placeholder) and documented.
- **353** existing alt strings preserved **verbatim** as the literal prefix of
  their final alt — checked programmatically (`final_alt.startswith(current_alt)`),
  0 failures on the final build.
- New shared generator helper: `build/scripts/common/alt_expand.py` (verbatim-
  preserving sentence append, caption cleanup, HTML-entity/quote-attribute safety
  for the appended text only — never touches the preserved original bytes).
- New ledger: `build/data/image_alt_expansion_ledger.csv` (415 rows, full
  before/after record per placement).
- Two established Deep Cleaning competitor comparisons (Coit/Stanley
  Steemer/Zerorez) preserved byte-for-byte; **zero new competitor names added**
  anywhere on the site.
- **QA:** double build byte-identical; all 13 pages' JSON-LD still parses; exactly
  one `<h1>` per page; no `<img>` count / `alt=` count mismatch on any page (no
  malformed attributes); `git diff --check` clean; line-level diff review
  confirmed every changed line differs *only* in its `alt="..."` value (`src`,
  `href`, `class`, `data-caption`, dimensions, badge numbers all identical).
- **Two real defects caught during verification and fixed** (not present in the
  final build): (1) the first draft of the append helper stripped trailing
  whitespace from a few source alts before adding punctuation, which would have
  broken byte-exact verbatim preservation — fixed so the original text is never
  trimmed or altered; (2) appended prose/titles could contain a literal `"` or a
  bare `&` (inch-mark measurements, "Repairs & Installation" style headings),
  which would have produced invalid attribute values in the two overlay
  assemblers (Deep Cleaning, Blog) that don't otherwise escape — fixed with
  quote-escaping and entity-aware `&`-escaping applied only to newly appended text.

**Flagged, not fixed (out of this milestone's scope):**
- Solid Wood Gallery's pre-existing `TRICIA WALNUT27/30/63/76.jpg`
  filename-vs-white-oak conflict (flagged since Milestone 2.5) — still
  unresolved; this milestone's appended text repeats only the already-published
  white-oak wording, takes no new position.
- One Gallery 1 caption field (`ENCINITAS CHERRY18.jpg`) contains a leftover
  Yahoo Facebook-Like-button JS fragment instead of real caption text (raw-source
  extraction artifact) — excluded from appended alt text, not used as a source.
- `build/scripts/generate_media_inventory.py` is stale (last run 2026-07-18,
  predates Milestone 2.7's homepage image-30 removal). Regenerating it during
  this session surfaced one pre-existing orphaned placement
  (`HOME-IMG-034`) that the validator now flags as an error — unrelated to alt
  text, so the regeneration was **reverted** rather than absorbed into this
  milestone (no broad build-system refactor). Worth a few minutes of cleanup in
  a future media-facts session before the next `generate_media_inventory.py` run.

**Files changed:** `CLAUDE.md` (new durable protected-alt-text rule),
`build/scripts/common/alt_expand.py` (new), `build/scripts/common/build_page.py`,
`build/scripts/pages/{build_gallery1,build_gallery2,build_gallery5,build_solidwood,
build_videos,build_about_us,build_floor_assessments,assemble_deep_cleaning,
assemble_blog}.py`, `build/data/index/gallery.json`,
`build/data/index/main_content.html`, all 12 regenerated root pages except
`contact_us.html` (byte-identical, no images on that page), `build/data/
image_alt_expansion_ledger.csv` (new), `docs/2026-07-aggressive-image-alt-
expansion-report.md` (new).

**Git state:** committed to `redesign` as `f233a7d` ("Aggressive, evidence-grounded
image alt-text expansion (Milestone 2.12)"); owner instructions for this
milestone explicitly specified commit + push to `redesign` as in-scope.
`master`/production untouched throughout. See `docs/2026-07-aggressive-image-
alt-expansion-report.md` for push/preview-deploy confirmation.

## Milestone 2.11 — Google Search Footprint Preservation & final prelaunch alignment (2026-07-20)

Full requirements record: `docs/2026-07-google-search-footprint-preservation.md` (owner-approved
evidence from real Google searches + the query-to-page relationships this pass had to preserve).
One controlled pass across the existing 13-page site — no new pages, no schema restart, no
image/gallery reorganization.

**Protected page roles reconfirmed/strengthened:**
- **Homepage** — broad authority for refinishing/restoration/deep cleaning/recoating/
  installation/hardwood+bamboo/water damage/free assessment. Links out to Deep Cleaning,
  Installation, galleries/videos, and Assessments (all pre-existing, verified intact).
- **Deep Cleaning** — owner-locked title/meta/H1 reconfirmed unchanged (byte-match check against
  the exact owner text). Only a minor internal-link anchor-text tweak.
- **Solid & Engineered Installation** (`solid_wood_floor_photo_gallery.html`) — no longer reads
  as gallery-only: added a new "Installation Methods, Materials & Feasibility" section (nail-down/
  glue-down/floating/nail-assist, unfinished-vs-prefinished, cork/underlayment/sound control,
  moisture/subfloor evaluation linking to Assessments) + matching schema (`service_types`/
  `offer_items`). Title/meta/H1 unchanged (already matched the proven search intent).
- **Floor Assessments & Inspections** — the one page with a real new-visibility opportunity
  (`pre purchase floor inspection san diego` had zero prior SDH visibility). Title/meta/H1 now
  name "Bamboo" and "Pre-Purchase" explicitly; added a "Can This Floor Be Refinished?" diagnostic
  section (solid vs. engineered, wear layer, finish/oil-hard-wax-oil compatibility, textured
  surfaces, damage/repair matching) and the owner-required "not a substitute for a general home
  inspection" distinction inside the pre-purchase section. Existing Condition → Probable Cause →
  Feasibility/Limitations → Recommended Next Step report structure was already in place — left as
  is.
- **About / Videos** — dust-containment wording strengthened only (see below); titles/meta/H1
  otherwise untouched (no owner evidence to justify a rewrite there).
- **Galleries 1–5, Blog, Contact** — untouched. Their title/meta/description text is the
  established live/raw-source wording (prelaunch audit confirmed 5 of 13 pages match live
  exactly); this milestone's evidence didn't call for changes there, and rewriting established,
  ranking copy without owner evidence is exactly what this milestone's rules prohibit.

**True 100% dust containment restored as the precise claim** (owner-confirmed this session,
supersedes the prior "dust-contained" claims-policy guess — see `CLAUDE.md` and
`docs/PROJECT_DECISIONS.md` → "Claims policy enforcement" for the superseding note): homepage
(title/meta/H1/hero/dedicated dust section), About (two credential bullets), Videos (hero +
featured-section copy), Solid & Engineered Installation (hero + schema), and one Deep Cleaning
internal-link anchor. "Dustless hardwood-floor sanding and refinishing" kept everywhere as the
natural customer phrase alongside the precise claim. Legacy gallery/blog captions extracted
verbatim from frozen raw-source records still say "dust-free"/"dust-contained" in places —
deliberately left alone (pre-existing, out of this milestone's scope, same call as Milestone 2.9).

**QA:** double build byte-identical (7 pages changed both runs, same diff both times); all 13
pages' JSON-LD parses; exactly one full `#local` `LocalBusiness` declaration per page; unique
titles/meta descriptions across all 13; exactly one `<h1>` per page; zero visible "Orange County"
text on any page; all 58 YouTube IDs + the server-rendered hero intact on Videos; zero missing
local image references; zero broken internal links (script-verified against the canonical map);
`git diff --check` clean. Playwright browser QA (desktop 1440×900 + mobile 390×844) on homepage,
Deep Cleaning, Solid & Engineered Installation, Gallery 1, Videos, Floor Assessments: single H1,
zero horizontal overflow, zero console errors, no visible OC text — 12/12 checks passed.

**Files changed:** `CLAUDE.md`, `docs/PROJECT_DECISIONS.md`, `docs/2026-07-google-search-footprint-preservation.md`
(new), `build/data/index/main_content.html`, `build/scripts/pages/{build_homepage,build_about_us,
build_videos,build_solidwood,build_floor_assessments,assemble_deep_cleaning}.py`, and the 7
regenerated root pages (`index.html`, `about_us.html`, `videos_of_refinishing_process.html`,
`solid_wood_floor_photo_gallery.html`, `floor-assessments-inspections.html`,
`deep-cleaning-hardwood-floors-san-diego.html`) + `sitemap.xml`/`robots.txt` (regenerated,
unchanged content). Galleries 1–5, Blog, Contact: confirmed byte-identical, not touched.

## Milestone 2.10 — Turbify image localization & video-title typo fix (2026-07-19)

**All site-required images copied into the repo; `<base href>` Turbify bridge removed.**
Owner supplied a local archive of the highest-resolution recovered Turbify images
(`assets/ALL_IMAGES/`, untracked local source, left untouched) at
`C:\Users\oakfl\Desktop\SAN DIEGO HARDWOODS WEBSITE REMAKE JULY 2026\assets\ALL_IMAGES`.

- **351 unique images** matched by exact filename (350) plus one Python-level fixed
  string (the homepage's duplicate raw-source thumbnail) and copied byte-for-byte into
  tracked production paths, mirroring each image's existing site-relative path exactly
  (no renames): repo root (238 files — the legacy `/FILENAME.jpg` and bare-relative
  refs), `assets/images/` (108 files), `images/thumbnails/` (5 files, new folder
  mirroring the exact `images/thumbnails/...` path the schema already used).
- **`<base href="https://www.sdhardwoods.com/">` removed** from all 4 head templates
  (`assemble_page.py`, `build_page.py`, `assemble_blog.py`, `assemble_deep_cleaning.py`)
  — this was the actual mechanism sending every relative image request to Turbify
  regardless of path form; removing it (not just copying files) is what makes the
  local copies actually load. All 13 pages rebuild byte-identical on a second run
  (verified). `top.html`'s stale JS comment about the bridge updated to match.
- **Absolute Turbify URLs converted to local site-relative paths**, everywhere found:
  favicon.ico/-192/-512, `LOGO-2025.png`, `bonacc.jpeg` (13 build scripts, all had their
  own copy-pasted head block), the shared `CANONICAL_LOCAL_STUB` schema image/logo
  (`public_business_rules.py`), and 5 of 6 VideoObject `thumbnailUrl` schema fields
  (`about_us`/`gallery5`/`gallery2` frozen `jsonld.html` fragments, plus
  `build_homepage.py` and `common/build_page.py` for two raw-source-derived
  VideoObject blocks that a naive file-only sed pass would have missed).
- **One genuinely missing image, left unfixed on purpose:** the about_us page's
  VideoObject thumbnail `french_oak_and_wire_brushed_wood_floor_refinishing_san_diego.png`
  is not in the recovered archive (never successfully downloaded from Turbify) —
  `about_us/jsonld.html` still points at the live Turbify URL for this one field only.
  Flagged for owner review; not substituted, not upscaled, not invented.
- **"Sold Cherry" → "Solid Cherry" typo fixed** (video `AFiDErGMYdo`, Videos page) via
  the existing `site_display_title` curated-override field in
  `build/data/youtube_videos.json` — the raw `title` field (the actual live YouTube
  title) is intentionally left saying "Sold Cherry" per the site's existing policy of
  never silently editing the snapshot's source-of-truth field; fix the real YouTube
  title first if the owner wants that to change too, then re-run
  `update_youtube_videos.py`.
- **38 archive files intentionally not copied**: the legacy nav-button graphics already
  excluded from generated output since Milestone 2.1 (`HOME BUTTON 2025.png` etc.) plus
  a handful of alternate-resolution originals/unused crawl artifacts that no page
  currently references. `assets/ALL_IMAGES/` and its `image-manifest.csv` untouched,
  untracked, not part of this commit.
- **QA:** double build byte-identical; `git diff --check` clean; all 449 local image
  references across all 13 pages resolve to a file that exists on disk; zero remaining
  `sdhardwoods.com` image/favicon/logo/thumbnail URLs except the one flagged miss above;
  diff reviewed page-by-page — only head metadata/schema image URLs, the JS comment,
  and the one video title changed; gallery order, alt text, captions, and layout
  byte-identical everywhere else.

## Milestone 2.9 — prelaunch SEO & structured-data pass (2026-07-19)

Full record of the durable rules: `docs/PROJECT_DECISIONS.md` → "Service-area & metadata rules
(Milestone 2.9)". Headlines:

- **Fixed a real regression from 2.8:** the prior milestone's South Orange County expansion had
  landed visibly on 5 pages and inside multiple per-page `Service.areaServed` arrays, plus used
  an OC city list that didn't match the owner's latest exact 13-city list. Both fixed — OC now
  lives only on the shared `#local` entity's `areaServed`, never visible, never per-page.
- **New centralized service-area source**: `build/data/seo/service_areas.json` — the owner's
  detailed San Diego regional/enclave lists, merged with every San Diego area already in the
  site's data (owner instruction: never remove San Diego areas, only add — El Cajon/Chula
  Vista/National City/Imperial Beach/Bonita all deliberately kept), plus the exact South OC
  list. Shared `#local` entity now carries 174 areas (161 SD + 13 OC) identically on all 13
  pages (`replace_area_served()` in `public_business_rules.py`).
- **Deep-cleaning page**: title/meta description/H1 replaced with owner-exact text (also fixed
  a live "dust-free" claims-policy violation in the old meta description).
- **Videos page**: one server-rendered hero `<iframe>` added above the featured/library
  sections (reuses the existing featured-rank-1 video, `Jv1KsJndmww`) — present in initial HTML,
  not click-to-play. Linked into schema via `CollectionPage.video` → the hero's `ItemList`
  `@id`, no duplicate `VideoObject`. All 58 other videos, filters, and modal untouched.
- **Meta description casing** normalized (`DESCRIPTION`→`description`, dropped stray
  `id="mDescription"`) on blog/gallery1/gallery2/gallery3/deep-cleaning — content unchanged.
- **QA**: double build byte-identical; all 13 pages' JSON-LD parses, exactly one full `#local`
  declaration each, zero OC in any per-page `Service`, zero visible OC/wealth-language anywhere;
  all 58 video IDs still present; `git diff --check` clean.
- **Flagged, not fixed (out of this milestone's scope):** "dust-free" claims-policy wording
  still appears in real gallery captions/alt text on the deep-cleaning page (pre-existing,
  extracted from frozen raw-source records) and in a couple of other pages' video/image
  metadata (e.g. gallery4's video description, about_us's FAQ "What is dust-free sanding?").
  Worth a dedicated claims-language pass in a future session.
- **Not regenerated:** `build/data/media/assets.json` / `placements/*.json` were already stale
  before this session (per the 2.7 note below) and still are — regenerate before the next
  media-facts session; not touched here.

## Milestone 2.7 — COMPLETE, PUSHED to `origin/redesign` (2026-07-19)

**Homepage featured-image metadata (images 5–90).** Owner facts source:
`homepage_image_owner_facts_5-90.yaml` (repo root, untracked owner input).

- **Authoritative data:** `build/data/index/gallery.json` now carries owner-approved
  `alt` + new `caption` field for the 85 project images after the locked Tricia Walnut
  set (#1–#4 untouched, byte-identical output). Captions were refined per image after
  visually inspecting all 86 photos (view/room/angle wording only; no invented facts).
- **Separate visible caption:** `build_homepage.py` emits `data-caption` on each gallery
  link; shared `build/chrome/lightbox.html` shows `data-caption` and falls back to alt
  everywhere else (only lightbox change on the other 12 pages — behavior identical there).
- **Image #30 removed** (old numbering): visually confirmed near-duplicate of #17 — same
  Rancho Santa Fe wet-coat corridor shot 2 seconds apart (`20141113_181549` vs `_181551`).
  Generator renumbers badges automatically → homepage now #1–#89; gallery lede count
  updated "Ninety" → "Eighty-nine". No file deleted, no other page affected.
- **Image 71 location** published as owner-confirmed **San Elijo Hills**.
- **Bird Rock #10 and Bankers Hill #53–55 do NOT name Traffic HD** (unconfirmed, per YAML).
- **Factual note for owner:** YAML describes old #83 as an equipment/dust-containment view,
  but the photo shows a finished columned room with French doors (same Mission Hills
  project era; shot minutes after #72's photo). Caption written to match what is visible.
- **QA:** deterministic rebuild verified; 89 sequential badges; unique alts; Playwright
  desktop+mobile lightbox QA passed (captions on #5/#89, alt fallback on locked #4,
  counter "…/ 89", prev/next/Escape) — `qa-screenshots/m2-7-*.png`. Note: the
  `generate_media_inventory.py` snapshot (`build/data/media/placements/*.json`) predates
  this milestone; regenerate before the next media-facts session.

## Milestone 2.6 — COMPLETE, PUSHED to `origin/redesign` (2026-07-18)

**Public business rules, assessment conversion, YouTube metadata, GA4.** Full record:
`docs/2026-07-milestone-2.6-report.md`; durable owner decisions in
`docs/PROJECT_DECISIONS.md` → "Public-business rules". Headlines:

- **Service-area business:** no street address / `PostalAddress` / geo / hasMap in any
  generated output (build-time filter `build/scripts/common/public_business_rules.py`);
  approved wording "Based in Carmel Valley, San Diego 92130" in the shared footer.
- **License number removed** from public output & operational docs (generic
  CSLB-licensed wording stays).
- **Official YouTube channel** `@sandiegohardwoods` everywhere; `@SD-1974` retired.
- **"Free estimate(s)" banned** from output; entry service is the **Free Phone & Photo
  Assessment** with Text → Call → Email hierarchy site-wide; Contact retitled (owner
  sign-off) — the only metadata change.
- **Assessments page:** owner's clarified service-level descriptions ($95/$350/$750/
  Starting at $1,500; fee-credit sentence untouched) + new clearly-labeled illustrative
  "What a Professional Evaluation Can Clarify" section + consolidated no-automatic
  engineering/lab/appraisal/legal/testimony exclusion line.
- **YouTube titles:** live-channel refresh 2026-07-18 confirmed all 58 snapshot titles are
  the actual live titles (so "Sold Cherry"/"Title:" stay until fixed on YouTube); new
  curated `site_display_title` mechanism (refresh-preserved, used by `build_videos.py`)
  for any future blank/date-only titles.
- **GA4 `G-L9RDVK6H9W`** in one shared partial `build/chrome/analytics.html` (see
  `build/README.md` → "Analytics"): production hosts only (localhost/`*.pages.dev` make
  zero Analytics requests — browser-verified both ways); events `phone_call_click`,
  `text_message_click`, `email_click`, `assessment_cta_click`,
  `assessment_page_link_click`.
- **QA:** double build byte-identical; static gate green; media inventory 0 errors /
  4 known walnut warnings; browser QA 98/98. Committed locally on `redesign`
  (with the new root `CLAUDE.md`); **not pushed, not merged, no deploys, `master`
  untouched** — pushing to `redesign` (preview deploy) is the owner's call.

**Next step:** owner review of the preview once pushed; then the page-by-page owner
media-fact review (`docs/media-review/index.html`) and/or assessment practical-facts
completion (blockers 4–6 in `docs/PROJECT_DECISIONS.md`). Fixing the "Sold Cherry" /
"Title:" video titles happens on YouTube first, then `update_youtube_videos.py` + rebuild.

## Milestone 2.5 — COMPLETE & COMMITTED (see `git log` for the hash on `redesign`)

**Search Console content preservation, internal-link alignment, and the structured media-fact system.** Current branch: `redesign`. Everything below is generator-first; regenerating with `python build/scripts/build_all.py` reproduces the committed pages byte-for-byte.

- **SEO intent map:** `build/data/seo/page_intents.json` (13 records) + human-readable `docs/seo/search-console-content-preservation-map.md` — which GSC query themes each page owns, what must stay visible, cannibalization rules. Derived from the real GSC baseline in the operating manual §10.
- **Content alignment:** restrained visible-wording changes on 8 pages (homepage, deep-cleaning, gallery 1, gallery 5, solid wood, videos, about, assessments); galleries 2/3/4, blog, and contact byte-identical. **No titles/descriptions/H1s changed.** Full before/after log: `docs/seo/2026-07-content-alignment-changes.md`. Includes the §12-flagged claim removals on Solid Wood ("far exceeds"/"flawless"/"exact"/absolute dust) and About's license-number addition (reversed in Milestone 2.6 — the owner has since ruled the exact number is not published).
- **Confirmed Tricia walnut correction:** the four homepage `TRICIA WALNUT102/110/54/23.jpg` alts no longer claim bamboo/parquet/maple/RSF/La Jolla identities — restrained provisional wording (Bing Crosby Ranch walnut refinishing, stage unconfirmed), seeded as owner-confirmed facts in `build/data/media/owner_facts_confirmed.json`.
- **Structured media-fact system:** `build/scripts/generate_media_inventory.py` scans all 13 generated pages → `build/data/media/assets.json` (377 image + 58 video assets) and `build/data/media/placements/<page>.json` (516 placements, stable IDs like `HOME-IMG-005`, `VIDEOS-VID-014`). `build/scripts/validate_media_inventory.py` enforces completeness/uniqueness/no-auto-publish (currently 0 errors, 4 intentional warnings = the `TRICIA WALNUT27/30/63/76` filename-vs-white-oak conflict on Solid Wood, flagged for the owner, deliberately unchanged). Owner-facts merge preserves owner edits across regenerations; deterministic double-run verified.
- **Owner review surface:** `docs/media-review/README.md` (workflow) + 13 generated per-page `.md` files + static read-only `docs/media-review/index.html` (thumbnails, placement IDs, flags — local only, never deploy).
- **Assessment future-content inputs (empty by design):** `build/data/assessment/report_examples.json` + `practical_service_facts.json` — all values `awaiting_owner_input`; nothing publishes until owner-confirmed.
- **QA:** static gate green (canonicals/viewport/title/H1/no-UA/noindex/sitemap 13 URLs/robots/JSON+JSON-LD strict/internal links/tel-label check/walnut assertions/content-preservation counts vs HEAD); double build byte-identical; browser QA (Playwright/Chromium, local HTTP server, desktop+mobile, all 13 pages) 176/180 — the only 4 fails are the **pre-existing** "YAHOO is not defined" console error from the legacy inline Turbify script on galleries 3/4 (byte-identical to 2.4 output; cleanup candidate for the hardening milestone). Details appended to `docs/2026-07-qa-report.md`.
- **2.4 note resolved:** the suspected deep-cleaning meta-description mojibake ("Countyâ€”") is a display artifact — committed bytes are a correct UTF-8 em dash. No fix needed.

**Recommended next milestone (per the operating-manual roadmap §35):** Assessment-page content completion & consultation-card optimization — needs the owner blockers in `docs/PROJECT_DECISIONS.md` (report excerpts, visit/delivery facts). Alternatively, page-by-page owner media review can start immediately using `docs/media-review/index.html`.

## Milestone 2.4 — COMPLETE & COMMITTED (`1ecff4e`, pushed to origin/redesign)

Technical SEO foundation, completed 2026-07-18 — full record in `docs/2026-07-milestone-2.4-technical-seo.md`. Summary: one correct canonical on all 13 pages (Gallery 3's wrong canonical fixed; six missing canonicals added), one standard viewport everywhere, homepage title/description replaced (refinishing-led), five missing meta descriptions added, all `tel:`/`sms:`/`mailto:` actions separated (no "Call or Text" tel labels), obsolete Universal Analytics removed site-wide (GA4 blocked pending owner's Measurement ID), deterministic `sitemap.xml` (exactly 13 canonical URLs, no invented lastmod) + `robots.txt` generated by `build/scripts/common/build_sitemap.py`, internal nav aligned to canonical `.html` URLs, `<base href>` kept (images still served from Turbify). Live-URL behavior measured and documented; no redirects created; master/production untouched.

## Milestone 2.3 — COMPLETE & COMMITTED (`d008327`, pushed to origin/redesign)

The site now has a **13th page**: a dedicated Floor Assessments & Inspections page. *(Status update 2026-07-18: the "uncommitted, awaiting review" state described when this section was written was resolved — the milestone is committed as `d008327` "Complete Milestone 2.3: dedicated floor assessments and inspections page" and pushed.)* Screenshots: `qa-screenshots/m23-*.png`.

- **New page:** `floor-assessments-inspections.html`, generated by `build/scripts/pages/build_floor_assessments.py` (the one page with no raw-source snapshot — head metadata, JSON-LD, and body are authored in the script). Permanent public URL: `https://www.sdhardwoods.com/floor-assessments-inspections`; canonical matches. Registered in `build_all.py` (now 13 steps) and `sitemap.xml`.
- **Content:** the complete Milestone 2.2 paid-assessment presentation moved here from the homepage — free phone & photo assessment, $95 In-Home Project Assessment (with the exact fee-credit sentence, once), $350 verbal and $750 written pre-purchase inspections, Complex Damage, Dispute & Insurance Analysis from $1,500 — plus audiences/specialty-oak content, a service-area section, an appointments & payment section (Square invoice / Zelle wording), and a visible 8-question FAQ. JSON-LD: one `@graph` connecting `WebPage` + 5 `Service` entities (visible prices as Offers) to the homepage's established business entity via `@id https://www.sdhardwoods.com/#local` — no new business facts invented, no FAQ/Breadcrumb schema (site doesn't use them).
- **Internal links:** every reference now points root-relatively at `/floor-assessments-inspections` — desktop Services dropdown and mobile drawer (both with `data-nav` active-page marking), footer `f-links`, homepage CTA (**View Floor Assessment & Inspection Services**), homepage cards, and a neutral Contact Us line. Zero remaining links to `#professional-floor-assessments` or `contact_us#consultation-services`; those anchors/sections are gone (homepage now carries only a short intro in the same slot; Contact Us bridge section removed entirely).
- **Dark default (site-wide):** with no saved preference the site now opens **dark regardless of OS color scheme**; an explicit toggle choice (either direction) persists. Implemented in shared chrome only: `darkmode_boot_scripts.html` sets `html.sdh-dark` synchronously (no light flash; variables duplicated on `html.sdh-dark` in `site_css.html`) and the toggle keeps both classes in sync.
- **QA:** double build byte-identical across all 13 pages; static audit all green (titles/descriptions/canonicals of the original 12 unchanged, one H1 each, no duplicate IDs, every img has alt, all JSON-LD parses); 62/62 Playwright checks (dark default with OS-light + fresh storage on all 13 pages desktop+mobile, light/dark persistence, no horizontal overflow, nav/drawer/footer links, reduced motion).
- **Next step when the owner approves:** commit on `redesign` and push (Actions auto-deploys to the preview). The Cloudflare Pages clean-URL behavior serves `/floor-assessments-inspections` from the `.html` file, same as the existing extensionless URLs.

## Milestone 2.1 — COMPLETE, APPROVED & COMMITTED (2026-07-17)

The Milestone 2.1 refinement (owner's brief of 2026-07-16) is implemented, built, QA'd, **approved by the owner after visual review on 2026-07-17, and committed on `redesign`** ("Complete Milestone 2.1: owner-requested refinement, content restoration, video library, SEO cleanup & legacy-asset removal" — see `git log` for the hash). It is deliberately **not pushed, not merged to `master`, and not deployed** — pushing to `redesign` (which auto-deploys to the Cloudflare preview via Actions) and any production promotion are separate, owner-initiated next steps. Immediately before committing, the full verification suite was re-run: double build byte-identical, legacy-asset assertion zero matches, browser QA 330/330. `docs/2026-07-milestone-2.1-qa-report.md` is the authoritative record (build results, QA details, screenshots list, judgment calls). Highlights:

- Explore bar redesigned (translucent blue-glow surface; never over the initial hero; hides at footer; session-dismissable; reduced-motion aware).
- Top contact strip and tiny per-page SEO strip removed from the shared chrome; content responsibly relocated — full inventory in `docs/milestone-2.1-seo-content-map.md`. Footer now carries the ZIP + CSLB line.
- Homepage: new broader H1 (owner-directed), Bona DCS 2.0 dust-containment section, cleaning-only/recoat/oiled-conversion positioning. Only intentional metadata change site-wide is this H1.
- Theme control moved into the menu drawer (floating toggle gone); first visit now respects the system color scheme.
- All legacy image-button graphics (CONTACT US/NEXT PAGE/ABOUT US/CALL OR TEXT/HOME/ultra-clean ×2 variants) excluded from generated output on every page, replaced with text links where useful; assertion in the QA report proves zero occurrences remain.
- Gallery 5 rebuilt as five explicit before/after project pairs (raw-source write-ups #81–#85 restored) via `data/recent_project_gallery_5/projects.json`.
- Solid Wood Gallery restored to its original four-project structure via `data/solid_wood_floor_photo_gallery/projects.json`.
- Videos page rebuilt as the complete channel archive: 58 public videos (47 + 11 Shorts) from the checked-in snapshot `build/data/youtube_videos.json`; click-to-play nocookie modal (zero iframes on load); category filters; accurate VideoObject graph. Refresh utility: `build/scripts/update_youtube_videos.py` (see build/README.md).
- Build is deterministic (double-build byte-identical); regenerating after commit will keep CI's diff gate green.

Next session: when the owner says go, push `redesign` to origin — GitHub Actions will regenerate, verify the diff gate, and auto-deploy to the preview URL (`https://redesign.sd-hardwoods.pages.dev`). Do not merge to `master` or touch production without an explicit, separate owner instruction.

## The site, in one paragraph

sdhardwoods.com is a legacy Yahoo/Turbify "Site Solution" site for a San Diego hardwood-flooring contractor. All 12 legacy pages have been rebuilt with a consistent modern design system, plus a new 13th page (`/floor-assessments-inspections`, Milestone 2.3) — see `build/README.md` for the full generator/tooling architecture. Everything lives in the GitHub repo **oakflooring74-hub/sd-hardwoods**, on the **`redesign` branch** (production/`master` still holds the prior owner's earlier, different rebuild attempt — do not merge without the owner's explicit go-ahead). This is still NOT the production site; sdhardwoods.com itself is untouched.

See also `docs/VISION.md` for the longer-term mission/goals this project is working toward.

## Milestone 1 — COMPLETE (2026-07-16): first interactive site-improvement batch

All 8 items approved in the prior session's QA pass, plus the blog/deep-cleaning mobile overflow bug, are implemented, built, and locally tested. Committed on `redesign` as **"Complete first interactive site-improvement milestone"** (`5d911a6`), pushed to `origin/redesign`, and manually deployed to the Cloudflare preview via `wrangler pages deploy` — verified live at `redesign.sd-hardwoods.pages.dev`. Production (`master`) was not touched.

**What shipped:**
- ✅ Sticky header foundation — replaced the two independently `position:fixed` elements (brand chip + nav button) with a single in-flow, sticky `<header id="sdhHeader">`. This **fixes the overlap bug** (nav/toggle no longer float on top of arbitrary scrolled content), but **the header itself is only a functional foundation, not a finished redesign** — see Milestone 2 below.
- ✅ Gallery image crop fix — `.gallery img` changed from fixed `height:320px;object-fit:cover` to `height:420px;object-fit:contain`, so tall vertical before/after photos are no longer cropped 60–85%.
- ✅ Homepage numbered badges (`#1`–`#96`) on the homepage gallery only, per the owner's scoping.
- ✅ Site-wide in-page lightbox (`build/chrome/lightbox.html`) — clicking a gallery photo now opens a JS overlay with next/prev/close, instead of navigating to a bare image file on a different domain. No new URLs/pages. Correctly ignores the blog/deep-cleaning "Home/Contact/Next Page" button widgets (which also use the `.gallery` class but link to real pages, not images) via an image-extension check on the href.
- ✅ Persistent "jump to gallery" progress indicator ("Gallery N of 5" + numbered jump links + prev/next) on all 5 before/after gallery pages (`recent_project_photo_gallery_1–4`, `recent_project_gallery_5`).
- ✅ Footer email/phone overflow fix, site-wide.
- ✅ Touch targets increased to ≥44px (nav button, flyout links, dark-mode toggle).
- ✅ Dark-mode toggle no longer overlaps the footer — an `IntersectionObserver` fades it out while the footer is on screen.
- ✅ Blog and deep-cleaning mobile horizontal-overflow bug fixed — the hardcoded `minmax(480px,1fr)` / `minmax(520px,1fr)` inline grid rules changed to `minmax(min(Npx,100%),1fr)`, which was the open question from the prior session (resolved: this was a real bug, distinct from the intentional 2-column squeeze on galleries 1–5, and is now fixed independently of that decision).
- ✅ All 12 pages regenerated via `build/scripts/build_all.py` and locally tested with real Chromium (Playwright) at mobile/tablet/desktop widths: zero horizontal overflow anywhere, header/touch-target/footer/lightbox/badge/progress-indicator checks all passed.

**Environment changes made to get this done:**
- **Python 3.12 was installed on this laptop** via `winget install Python.Python.3.12` — the machine previously had no real Python, only a Windows Store stub alias, so the build pipeline (which is Python stdlib-only) could not run before this. See the updated Prerequisites section in `build/README.md`.
- **Playwright + Chromium were installed and used *outside* the repository** (in a scratch temp directory, not committed) to drive the pages in a real browser for testing — served locally via `python -m http.server`. Nothing was added to the project for this; if a future session wants repeatable browser testing, it would need its own `package.json`/`node_modules` decision.

**Preserved, verified via diff:** URLs, headings, SEO utility-bar paragraph, meta descriptions, image `src`/`alt` (byte-identical), watermarks (no changes to `raw-source/` or `data/`), and the 2-column before/after grid on galleries 1–4.

## Deployment Automation Milestone — COMPLETE (2026-07-16): GitHub Actions → Cloudflare Pages

A separate milestone, done between Milestone 1 and Milestone 2: manual `wrangler pages deploy` is no longer required for normal work. A GitHub Actions workflow now deploys automatically on every push.

**What shipped:**
- ✅ `.github/workflows/deploy-cloudflare-pages.yml` — two jobs, `build` (checkout exact pushed commit → install Python 3.12 → `python build/scripts/build_all.py` → **fail if regeneration produces any uncommitted diff**, so generated HTML can never silently drift from `build/` source templates) and `deploy` (needs `build`; deploys the **committed** repo root via `cloudflare/wrangler-action`, using the pushed branch name as `--branch`).
- ✅ Push to `redesign` → automatic **Preview** deploy. Push to `master` → automatic **Production** deploy. This is enforced by Cloudflare's own project config (production branch = `master`, already set before this milestone — confirmed via `wrangler pages deployment list`), not by anything this workflow does — the workflow just passes the pushed branch name through.
- ✅ Pull requests targeting `redesign` or `master` run the `build` job only (`if: github.event_name != 'pull_request'` gates the `deploy` job) — validation never deploys, to either environment.
- ✅ `workflow_dispatch` supported for a controlled manual rerun.
- ✅ Concurrency group per branch (`${{ github.workflow }}-${{ github.ref }}`, `cancel-in-progress: false`) so overlapping pushes to the same branch queue instead of racing or being interrupted mid-deploy.
- ✅ Least-privilege: top-level `permissions: contents: read`; commit message is passed to Wrangler via an `env:` var (not interpolated directly into the shell command) to avoid injection from special characters in commit messages; secrets are never echoed anywhere in the workflow.
- ✅ All third-party actions (`actions/checkout`, `actions/setup-python`, `cloudflare/wrangler-action`) pinned to exact commit SHA, with the version tag as a comment.
- ✅ `.wrangler/` (local Wrangler cache/metadata, not build output) added to `.gitignore`.
- ✅ `build/README.md` has a new "Deployment" section: normal workflow, required secrets, manual emergency-deploy command, production safety rule, how to find Actions logs, how to verify a deployment URL.

**Credential setup:**
- A dedicated Cloudflare API token was created — **not** the local Wrangler OAuth login credential — scoped to the minimum permission needed (Cloudflare Pages: Edit, this account only). Programmatic token creation was not possible from the existing authenticated session (Cloudflare's `wrangler login` OAuth grant deliberately excludes token-management permissions — creating a new token requires the dashboard), so this one step was done by the owner in the browser per the assistant's precise instructions, then entered directly via `gh secret set` — the token value itself was never written to disk, committed, or echoed anywhere.
- Repo secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set on `oakflooring74-hub/sd-hardwoods` (Settings → Secrets and variables → Actions). Only names are ever referenced in docs/workflow — never values.

**Actual first-run test results (2026-07-16):**
- Two real bugs surfaced and were fixed before the pipeline worked in CI — both were pre-existing latent issues in `build/scripts`, not something wrong with the workflow itself:
  1. **Path separators.** Every write/read in `build/scripts` joins paths with a hardcoded backslash (e.g. `CHROME + r"\site_css.html"`), which only resolves on Windows. The first CI run failed immediately with `FileNotFoundError` on `ubuntu-latest`. Fixed by running the `build` job on `windows-latest` instead of rewriting the existing generator scripts (see commit `a8abb91`).
  2. **Line endings.** All 22 write-mode `open(path, "w", encoding="utf-8")` calls across `build/scripts` used Python's default text-mode writing, which emits `\r\n` on Windows. The committed pages are LF (this repo normalizes to LF on commit). Regenerating on a Windows runner with `autocrlf` disabled therefore produced a full-file CRLF-vs-LF mismatch on every single line (8,460 insertions / 8,460 deletions across 19 files, despite zero real content change) — correctly caught and failed by the "fail if build changed committed output" gate, exactly as designed. Fixed by adding `newline="\n"` to all 22 calls, forcing deterministic LF output on any OS (commit `8f622b5`). Verified locally afterward: regenerating produces byte-for-byte identical output to HEAD (confirmed via `git diff --cached` / `cmp`, not plain `git status`, since this machine's own `core.autocrlf=true` gives a misleading "modified" signal on an unrelated axis when the file's on-disk EOL convention doesn't match what a fresh checkout would produce, even though the actual committed content is unchanged).
  3. **Cloudflare token rejected on the first deploy attempt** — `Authentication error [code: 10000]`, "Failed to automatically retrieve account IDs." The originally-created token was invalid/misconfigured; the owner created a replacement token and updated the `CLOUDFLARE_API_TOKEN` secret directly (bypassing this conversation entirely, the safest of the two options offered). No workflow change was needed — the second token authenticated successfully on the immediate rerun.
- **First fully green run:** GitHub Actions run [`29546738449`](https://github.com/oakflooring74-hub/sd-hardwoods/actions/runs/29546738449) (rerun after the token fix) — both `build` and `deploy` jobs succeeded.
- **Cloudflare deployment:** ID `47dc66ec-b62e-48cb-8078-d1e715357aac`, Environment `Preview`, Branch `redesign`, Source commit `8f622b5a00e3460670d6dff49e1dd6d32124535d` — **the exact same commit SHA the GitHub Actions run built from**, confirmed via both the workflow's own job summary and `wrangler pages deployment list`.
- **Live verification:** `https://redesign.sd-hardwoods.pages.dev` returns HTTP 200 and serves the new markup (`sdhLightbox`, `gallery-progress`, etc.) — confirmed pointing at this deployment. `https://sd-hardwoods.pages.dev` (production) returns HTTP 200 with none of that markup — confirmed untouched; `wrangler pages deployment list` shows Production deployments still pinned to `master` at `c3e8e0c`/`b6ac6a1`, unchanged throughout this entire milestone.
- **Conclusion:** the automation works end-to-end. Future pushes to `redesign` deploy automatically with no manual `wrangler` invocation needed.

## Milestone 2 — COMPLETE (2026-07-16): site-wide header, brand identity & navigation redesign

**Owner-approved, committed on `redesign` as "Complete Milestone 2: site-wide header, brand identity & navigation redesign" (`9117b84`), pushed, and auto-deployed to the Cloudflare preview** (Actions run `29555706718`, both jobs green — the CI regenerate-and-diff gate passed, confirming build determinism on `windows-latest` too). Verified live at `https://redesign.sd-hardwoods.pages.dev`: mini-header/consultation/gallery-nav markup all serving, brand WebP served directly from Cloudflare (normal caching), and production `https://sd-hardwoods.pages.dev` confirmed untouched (none of the new markup). The owner supplied the exact navigation grouping in the Milestone 2 brief, which resolved the "confirm grouping first" blocker from the previous session.

**What was built (all via shared `build/` sources, regenerated with `build_all.py`):**

1. **Brand identity & masthead** — the real San Diego Hardwoods medallion logo (from `assets/branding/LOGO 2025.png`, original preserved untouched) now anchors a proper masthead: logo + serif "San Diego Hardwoods" + tagline *"San Diego's Finest Hardwood Floor Specialist Since 1990"* + large clickable phone + email + "Free Phone Assessment" CTA. Optimized web derivatives live in `assets/branding/web/` (WebP + PNG, 12–15KB) — committed static files referenced via `data-brand-src` and resolved against `location.origin` at runtime (a literal root-relative URL would be rebased onto sdhardwoods.com by the `<base href>` bridge and 404 on the preview). The old generic square "SDH" chip is gone from primary use.
2. **Sticky mini-header** — the full masthead is in-flow and scrolls away; a compact (~56px) fixed mini-header slides in only after the masthead scrolls out (IntersectionObserver, reduced-motion aware, `aria-hidden` synced): compact brand, Menu, phone, "Text Floor Photos", "Call or Text — Free Assessment".
3. **Real navigation, centralized in `build/chrome/top.html`** — desktop band with 7 top-level items (Home, Services ▾, Project Galleries ▾, Videos ▾, About, Blog, Contact), accessible dropdowns (hover + click + keyboard + Escape + focus-out, `aria-expanded`), active-page marking derived from `location.pathname`, YouTube pill with the recognizable red play icon; mobile gets a right-side drawer (grouped `<details>` sections, all 12 pages, call/text CTAs, YouTube, email, scroll lock, Escape, focus restoration, focus trap). `<noscript>` fallback keeps every page reachable. Existing URLs only — same absolute-URL convention as before.
4. **SEO paragraph** — wording preserved byte-for-byte (still injected per-page via `__VCARD_DESC__`), now a visually subordinate strip below the nav; scrolls away with the masthead.
5. **Typography system** (`build/chrome/site_css.html`) — serif (Palatino-stack) headings/brand moments, Segoe UI-stack sans body/UI, `--brass-deep` accent for light-mode contrast, dark-mode nav/utility palettes, global reduced-motion kill switch.
6. **Hero rebalance (homepage)** — two-column hero: brand-led copy + CTAs left, video in a controlled ~45%-width frame right (stacks on mobile); caption + "Watch Our Work on YouTube" button under the video. Video no longer swallows the viewport.
7. **Bona Certified Craftsman band** (`#bona-certified`, homepage, near the existing Bona wording) — real Bona seal from `assets/branding` (original preserved; screenshot-sourced), accurate alt text, verify link to the canonical bona.com contractor page (`storeid=83667`, taken from the site's own raw source — not invented).
8. **Professional Consultation Services** — on the existing Contact page (`contact_us#consultation-services`, no new URL): 6 restrained premium cards — Free phone assessment (full-width, emphasized) / $75 / $150 / $350 / $750 / $1,500 — with the exact required credit wording, scope-confirmed-when-scheduling line, and all the required legal/insurance disclaimers phrased as positive scope statements. Homepage links to it from the "Start With a Free Phone Assessment" 3-step section and the evaluations card.
9. **CTA language** — outdated "free estimate / in-home estimate" CTAs refined to "free phone assessment" across build scripts and homepage/about/videos content. Protected SEO surfaces (meta titles/descriptions, image alt text, vcard paragraphs, JSON-LD) deliberately untouched.
10. **Homepage images #91–#96 removed at the generator level** (`build_homepage.py` excludes the six legacy nav-button records from `gallery.json`; the JSON and the hosted image files are untouched since other pages still use them). Badges stay sequential #1–#90. Replaced by a "Browse Our Detailed Project Galleries" tile section (galleries 1–5 + Solid Wood + text links to videos/deep-cleaning/about/contact).
11. **Explore bar** (`build/chrome/scrollhint_and_toggle.html`) — the old draggable scroll pill is now a refined bottom bar rotating through six *linked* destinations (galleries/videos/solid-wood, natural SEO language), pause on hover/focus, session-dismissable, hides on scroll, static under reduced motion.

**QA:** ~100 Playwright checks across all 12 pages at desktop/mobile + reduced-motion, all passing — details in `docs/2026-07-qa-report.md` ("MILESTONE 2 IMPLEMENTATION + QA"). Screenshots for review: `qa-screenshots/m2-*.png` (gitignored, local only). Regenerating via `build_all.py` reproduces the working tree exactly (deterministic).

**Judgment calls a reviewer may want to revisit:**
- At some desktop viewport heights the floating explore bar overlaps the hero's primary CTA button until the user scrolls or dismisses it (it hides past 320px scroll). Cosmetic; flagged, not fixed.
- Brand images load via a tiny JS resolver (`data-brand-src`) because of the `<base href>` Turbify bridge — with JS off, logos don't render (nav/noscript still works). Acceptable trade-off until images migrate off Turbify.
- The Bona seal derivative was made from the screenshot in `assets/branding` (`Screenshot 2026-07-16 193517.png`) — if the owner has an official higher-quality Bona asset, swap it into `assets/branding/web/` later.

**Status: approved by the owner on 2026-07-16 and deployed to the preview. `master` untouched — promoting to production remains a separate, owner-initiated decision.**

**Hard constraints honored (unchanged for future sessions):**
- URLs, canonical URLs, meta titles/descriptions, primary headings, image `src`/alt, watermarks, structured data, and the long SEO paragraph's wording/crawlable presence — all preserved.
- Two-column before/after layout on galleries 1–5 preserved (verified in QA).
- Milestone 1 features (lightbox, badges, gallery progress, footer/overflow fixes, dark/light modes) preserved (verified in QA).

## Decisions still standing from prior sessions

**DO NOT CHANGE:**
- SEO paragraph (the keyword-heavy utility-bar text) — content/presence protected; visual de-emphasis is the Milestone 2 goal, see above.
- Watermarks (owner adds these in Photoshop).
- Two-column before/after galleries (intentional "billboard CTA" feel, even on mobile).
- Legacy hosted images (still served live from Turbify via the `<base href>` shim).

**DEFERRED — not now, not dismissed:**
- CMS (a way for the owner to add projects without a dev session).
- Desktop app (see prior discussion — feasible, but scoped out for now).
- Migration toolkit (turning this system into a general legacy-site-migration tool).
- Image optimization.
- Cloudflare image migration (moving images off Turbify hosting).
- Google Search Console optimization (waiting on the data export).

## Blocked / waiting on the owner

- **Google Search Console export** (Query, Page, Clicks, Impressions, CTR, Position — full history, ideally per-page) — needed before any heading-level changes or meta-description rewrites on pages that already have one. See `docs/2026-07-seo-heading-audit.md` for exactly what this unlocks and why pulling it *before* the redesign goes live matters (it's the only way to get a clean pre-launch ranking baseline).
- **Image optimization** — deferred, but not dismissed. See the "Image optimization feasibility" section of `docs/2026-07-qa-report.md`: it's genuinely harder right now because images are still served live from Turbify hosting via a `<base href>` shim, not because image compression itself is hard. Worth revisiting if/when images move to being repo-hosted.
- ~~**Milestone 2 owner review**~~ — resolved: approved, committed (`9117b84`), pushed, and preview-deployed on 2026-07-16.

## Safe to do without waiting on GSC data

Adding meta descriptions to the 6 pages that currently have **none at all** (about_us, contact_us, videos_of_refinishing_process, blog, recent_project_photo_gallery_4, recent_project_gallery_5) — confirmed missing on the legacy site, not something the redesign removed, so there's no existing snippet performance to protect. Still needs the owner's go-ahead to actually write and add them (this was a discussion session, nothing was implemented), but doesn't need to wait on the GSC export the way changes to pages that already have a meta description do.

## Reference docs in this folder

- `docs/2026-07-qa-report.md` — full QA findings, owner decisions, **now updated with Milestone 1 completion status and current remaining issues**
- `docs/2026-07-seo-heading-audit.md` — GSC strategy discussion, meta-description categorization, full legacy-vs-redesign heading data and analysis (unchanged, still discussion-only)
- `build/README.md` — how the site is actually built/regenerated, including the Python prerequisite note; read this before touching any `build/` script

## Key facts worth not re-deriving

- GitHub: `oakflooring74-hub/sd-hardwoods`, branch `redesign`.
- `gh` CLI has two logged-in accounts on this machine; make sure `oakflooring74-hub` is the active one before pushing (`gh auth switch --hostname github.com --user oakflooring74-hub`).
- The redesigned pages still depend on Turbify hosting for images/video/theme CSS via a `<base href="https://www.sdhardwoods.com/">` tag — this is a deliberate bridge, not an oversight, but it's the reason image optimization is currently hard and worth remembering when it comes up again.
- Python 3.12 is now installed on this laptop (see Milestone 1 above) — the build pipeline can be run directly; no need to re-solve the missing-Python problem.
- Milestone 1 (`5d911a6`) and the deployment-automation milestone (`c759cf9`, `a8abb91`, `8f622b5`) are all **committed and pushed** to `origin/redesign` as of 2026-07-16, and the automation has been proven working end-to-end (first green run: Actions `29546738449`, Cloudflare deployment `47dc66ec`).
- **`build/scripts` write calls now force `newline="\n"`** (22 call sites, fixed in `8f622b5`) so generated output is deterministically LF on any OS — needed because this repo's commits normalize to LF but Python's default text-mode write emits CRLF on Windows. Don't remove this when touching those files; without it, the CI diff-check gate will spuriously fail on every regeneration.
- **The `build` job in `.github/workflows/deploy-cloudflare-pages.yml` runs on `windows-latest`, not `ubuntu-latest`** — because `build/scripts` still joins paths with hardcoded backslashes (e.g. `CHROME + r"\site_css.html"`). This works but is a latent portability debt: if a future session has time to spare, switching those to `pathlib`-style joins would let the job run on (cheaper, faster) `ubuntu-latest` instead. Not urgent — public repo, so Actions minutes are free either way.
- **Deployments are now automated** — see the "Deployment Automation Milestone" section above and the "Deployment" section in `build/README.md`. Don't reach for manual `wrangler pages deploy` for normal work; just push to `redesign` (preview) or `master` (production, owner-approved only) and let GitHub Actions handle it. Manual deploy is documented as the emergency-only fallback.
- Cloudflare Pages project `sd-hardwoods` has **no native Git integration** (`wrangler pages project list` shows "Git Provider: No") — the GitHub Actions workflow is a from-scratch deploy pipeline built specifically because that native integration isn't (and per this milestone's scope, still isn't) connected. Don't assume pushing alone triggers anything without checking the Actions tab if this workflow is ever removed/disabled.
