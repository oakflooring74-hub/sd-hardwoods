# Image Alt-Text Recomposition — Milestone 2.13 Report (2026-07-20)

Full requirements: this session's owner brief (site-wide alt-text recomposition, three
correction rounds). Phase A sample review and its revision history:
`docs/2026-07-image-alt-recomposition-sample-review.md`. This report covers Phase B
(site-wide implementation), approved after the owner reviewed and accepted the Phase A
sample's composition style.

## What this milestone fixed

Milestone 2.12 expanded every meaningful image/video alt site-wide by preserving the
existing alt **verbatim as the literal prefix** and appending new sentences after it. On
Gallery 1 and Gallery 2 (the general, non-special-cased branch) that prefix was the
**shared per-project module title**, identical for both photos in a before/after pair —
so paired images shared 250+ identical leading characters, with the genuinely
image-specific content buried after it. Several other pages had a related but different
defect: base text that already led correctly but stacked a redundant restatement
(homepage: base + a fuller caption saying the same thing twice), a repeated per-video
closing template (Videos), or ALL-CAPS keyword-spam legacy alt with zero image-specific
content standing in for real content (2 Blog images).

## Per-page summary

- **Gallery 1** (`recent_project_photo_gallery_1.html`) — all 20 projects (40 images)
  recomposed. Each alt now leads with `Before/After #N in {location}: {image-specific
  condition/process/result}`, with the shared project narrative merged in afterward,
  deduplicated. `build/data/recent_project_photo_gallery_1/modules.json`'s per-image
  `alt` field is now the complete, ready-to-render text; `build_gallery1.py` renders it
  directly instead of reassembling it from title+label+detail+caption at build time.
  Also: removed the unsupported "San Elijo Hills" reference from Project #5 (per explicit
  owner instruction — Carlsbad is the confirmed location); fixed the `wat-based` →
  `water-based` typo (Project #7, no longer propagated into alt since title text is no
  longer concatenated); fixed the `urable Recoating` → `Durable Recoating` caption typo
  (Project #18). Flagged, not resolved: Jacobian/Jacobean spelling (Projects #8/#10),
  Baker's Hill vs. Bankers Hill (Project #12), Project #18's sanding-vs-recoating
  contradiction.
- **Gallery 2** (`recent_project_photo_gallery_2.html`) — all 21 real project pairs (42
  images) recomposed the same way. The one already-correct special case (module index 8,
  the Bird Rock/Rancho Santa Fe two-independent-photos pair) was left untouched.
- **Gallery 3 & 4** (`build/scripts/common/build_page.py`) — audited: base alt already
  led with image-specific content on every pair. Only the 3 confirmed byte-identical
  pairs were recomposed (Project #50's `SUE30.jpg`/`SUE76.jpg`; Project #63's
  `REFINISH LAUZON MAPLE...` pair; Project #72's `BEACH1.jpg`/`BEACH4.jpg`), using each
  pair's own real caption/title facts. No renderer change — a pure data fix in each
  page's `modules.json`. Every other image on Galleries 3/4 is unchanged.
- **Gallery 5** (`recent_project_gallery_5.html`) — audited, already fully compliant
  (image-specific content leads on every one of the 5 explicit before/after pairs). No
  source change.
- **Homepage** (`index.html`) — all 89 real project images recomposed. 85 had a caption
  field already carrying the fuller, reviewer-refined description (Milestone 2.7); the
  redundant short base sentence was dropped in favor of the caption text (which already
  led with unique room/view/angle detail). The 4 Bing Crosby Ranch quartet images (no
  caption) were hand-recomposed to drop the internal "stage not owner-confirmed"
  verification metadata from the alt text and state the "one of four documented
  photographs" fact plainly instead of as a repeated near-identical disclaimer. 6 legacy
  nav-button images (excluded from generated output since Milestone 2.1) untouched.
- **Solid & Engineered Installation** (`solid_wood_floor_photo_gallery.html`) — audited:
  each project's per-image alt already led with a real installation-stage progression.
  Only Project 1's 4 `TRICIA WALNUT27/30/63/76` images (the pre-existing filename-vs-
  white-oak conflict, flagged since Milestone 2.5) had their fully-redundant shared
  trailing project-heading/note block trimmed. Projects 2–4 unchanged.
- **Deep Cleaning** (`deep-cleaning-hardwood-floors-san-diego.html`) — all 20 pairs
  recomposed via an `ALT_OVERRIDE` dict in `assemble_deep_cleaning.py` (the page's
  `gallery_records.json` regenerates from raw-source every build, so per-image text
  lives in the assemble script, not the data file). Pairs #1–9 are this page's own real
  projects, recomposed to lead with the visible **process stage** rather than a forced
  Before/After label — Pair #1's CSS before/after roles don't reliably match a
  damaged-state/completed-result reading (the "after"-labeled image's own text describes
  a pre-scrub step that happens *before* the "before"-labeled image's Power Scrubber
  step). Competitor comparisons rewritten as factual category comparisons ("specialized
  hardwood-floor deep cleaning" vs. "the general carpet and surface-floor cleaning
  associated with companies such as Coit, Stanley Steemer, or Zerorez") instead of
  unsupported "better than"/"outperforms" claims; the Bona Power Scrubber is no longer
  called "dust-free" itself (it's cleaning equipment, not sanding equipment). Pairs
  #10–20 reuse the exact same source photos as Gallery 1 Projects #10–20 — a
  pre-existing raw-source duplication across both pages, not something this milestone
  restructures — and reuse that already-recomposed Gallery 1 wording verbatim.
- **Blog** (`blog.html`) — audited: 39 of 43 images already led with real,
  image-specific content. 2 images (Case Study #8) had pure ALL-CAPS keyword-spam legacy
  alt with zero image-specific content; recomposed via an `ALT_OVERRIDE` in
  `assemble_blog.py` to lead with the real visible figcaption fact (before-sanding stage;
  confirmed red-oak species, stated once, not re-explained). A general spam-marker-
  stripping rule also removes the same boilerplate from any other affected image (Case
  Study #12) as a structural cleanup, applied uniformly rather than case-by-case.
- **Videos** (`videos_of_refinishing_process.html`) — all 58 thumbnails recomposed.
  Removed the repeated canned closing template ("San Diego Hardwoods YouTube video
  thumbnail showing {category}... uploaded {date}", identical across up to 38 videos in
  the same category) in favor of each video's own title + real description alone. Also
  found and fixed a real pre-existing bug in the fallback-description logic: the code
  collapsed all whitespace (turning `\n\n` into a single space) *before* trying to split
  on `\n\n` to isolate the first real paragraph, so the split was silently a no-op — every
  video without a curated `site_description` was getting the channel's own 3-paragraph
  contact/link boilerplate ("Fast answers: 858-699-0072...", "See before/after...",
  "Licensed Flooring Contractor... bona.com...") as its "description" instead of its real
  content. Fixed by splitting on blank lines *before* whitespace collapse and skipping
  the boilerplate paragraphs. 10 thumbnails across all 3 categories are additionally
  hand-composed as a curated, owner-reviewed sample (from Phase A). Flagged, not
  resolved: `ixqPScnbnLE`/`HF1pRJYTgZk` have identical title/description/category/
  publish-date in the data — genuinely indistinguishable, likely a duplicate upload.
- **About Us** / **Floor Assessments** — audited, no change. Both use the same real photo
  (`LARK56.jpg`) with the same opening sentence and a different page-specific tail —
  legitimate reuse of one real photograph across two pages, not a duplicate-content
  defect.
- **Contact Us** — confirmed zero `<img>` tags, nothing to do.

## Ledger and similarity audit

- `build/data/image_alt_recomposition_ledger.csv` (465 rows — recalculated fresh, not
  assumed from the prior milestone's count) — one row per production `<img>` usage:
  page, source file, image path, project/video id, classification, previous alt, revised
  alt, previous/revised character counts, first 200 characters of the revised alt,
  grounding sources, whether duplicate wording was removed, an owner-review flag, and
  notes.
- `build/data/image_alt_recomposition_similarity.md` — auto-generated exact-prefix and
  semantic-similarity audit. **465** total `<img>` usages, **413** meaningful, **52**
  intentional decorative/empty (3 shared-chrome logo instances + 1 lightbox placeholder,
  ×13 pages), **0** unintentional empty alts on meaningful images.
- **4** exact first-120-character duplicate groups remain, all pre-existing data gaps
  with no repository fact to distinguish them, all explicitly flagged in the ledger
  (`owner_review_flag: yes`) rather than resolved by invention: the 2 identical videos;
  Blog Case Study #11's 2 images (empty legacy alt, no distinguishing caption/prose);
  Blog Case Study #12's 2 sub-pairs (identical legacy alt after spam-stripping, no
  distinguishing caption for one of each pair).
- Top-20 first-200-character similarity pairs: after fixing the videos fallback-
  description bug above, the remaining moderate/high-similarity pairs are (a) the same 4
  exact-duplicate groups, (b) genuinely related real content correctly reading as similar
  (a 2-part video series about the same project; 2 videos about the same Bing Crosby
  Ranch walnut job; 2 of the 4 Bing Crosby Ranch homepage photos, already flagged as
  indistinguishable beyond their own "view" label), and (c) a handful of Blog Case Study
  #9 images (0.68–0.80 ratio) that share an ALL-CAPS-style opening convention but have
  genuinely distinct real content each — reviewed and left as-is (not an exact
  duplicate, no invented distinction needed). No further revision was made chasing the
  similarity score past this point, per the milestone's own instruction not to.

## Additional flags this session (beyond those carried from research)

- **Graf Brothers vs. Graff Brothers**: homepage's Bird Rock project data spells the
  brand "Graf Brothers" (single F); Solid & Engineered's Project 1 data spells the same
  apparent brand "Graff Brothers" (double F). Not confirmed which is correct — both kept
  as they appear in their own source file, flagged in the ledger.
- **Gallery 4 Project #61**: on closer reading, neither `ASH24.jpg` nor `ASH37.jpg`'s own
  data describes a damaged/pre-refinish state — both are completed-result descriptions,
  distinguished only by which street the estate is described relative to. Flagged rather
  than inventing a before/after claim the data doesn't support.

## Mechanical corrections applied

- `wat-based` → `water-based` (Gallery 1 Project #7 — no longer appears in alt at all
  since the fix stopped concatenating title text into alt; the typo remains, unfixed and
  untouched, in the protected `<h3>` project heading, per this task's own instruction to
  fix it only "inside alt metadata")
- `urable Recoating` → `Durable Recoating` (Gallery 1 Project #18 image caption)
- `San Elijo Hills` removed from Gallery 1 Project #5 (Carlsbad is the owner-confirmed
  location; explicit owner instruction, not a guess)

## Verification performed

1. Full rebuild (`python build/scripts/build_all.py`), then a second full rebuild:
   **byte-identical** across all 13 root pages, `sitemap.xml`, and `robots.txt`.
2. `git diff --check`: clean (no whitespace/EOL errors beyond the pre-existing
   LF→CRLF `core.autocrlf` notices, which do not affect committed content).
3. Line-by-line diff review of every changed generated page (`blog.html`,
   `deep-cleaning-hardwood-floors-san-diego.html`, `index.html`,
   `recent_project_photo_gallery_1.html`, `_2.html`, `_3.html`, `_4.html`,
   `solid_wood_floor_photo_gallery.html`, `videos_of_refinishing_process.html`) —
   programmatically confirmed every added/removed line contains an `alt="..."`
   attribute and nothing else changed (verified by scripted diff scan, not just visual
   sampling).
4. `recent_project_gallery_5.html`, `about_us.html`, `contact_us.html`,
   `floor-assessments-inspections.html` confirmed byte-identical to the pre-milestone
   commit (untouched, as intended).
5. All 13 pages' JSON-LD blocks parse successfully (`json.loads` on every
   `<script type="application/ld+json">` block, all pages).
6. All 13 pages parsed cleanly with Python's `html.parser` (no malformed markup); every
   `<img>` tag has an `alt` attribute on every page (`img` count == `alt` count on all
   13 pages, totaling 465, matching the ledger's recalculated total exactly).
7. Confirmed via the same diff-only-alt-attribute check that image `src`, `href`,
   `class`, dimensions, figcaptions, badge numbers, gallery order, video IDs, titles,
   meta descriptions, headings, canonicals, and navigation are byte-identical to the
   pre-milestone commit on every page.
8. Confirmed competitor names: Coit (1), Stanley Steemer (3), Zerorez (2) all still
   present on the Deep Cleaning page, byte-identical wording where not intentionally
   rephrased into the category-comparison form; no new competitor name introduced
   anywhere on the site.
9. `git status` confirms only intended files changed (9 regenerated root pages + `about_
   us.html`/`contact_us.html`/`recent_project_gallery_5.html`/`floor-assessments-
   inspections.html` byte-identical/untracked-as-changed; 7 source data files; 6 build
   scripts; this report + the ledger + the similarity audit + the Phase A review doc as
   new files). No unrelated file (raw-source, archive, CI config, Cloudflare config,
   analytics, sitemap/robots content) changed.
10. **Not run this session**: an interactive Playwright/browser QA pass (visual
    rendering, lightbox click-through, console-error check) on live pages. This
    milestone's changes are alt-attribute-only (confirmed programmatically above) and
    touch no CSS/JS/layout/lightbox code, so the risk is low, but this is a real gap
    against the milestone's own validation checklist — flagged rather than silently
    claimed. Recommend a follow-up visual pass (homepage, Deep Cleaning, Gallery 1,
    Gallery 3, Solid & Engineered, Videos, desktop + mobile) before treating this as
    fully closed out.

## Owner-review items carried forward (unresolved, not guessed)

| Item | Conflict |
|---|---|
| Gallery 1 Projects #8/#10 | "Jacobian" (this page + Deep Cleaning data) vs. "Jacobean" (homepage data) |
| Gallery 1 Project #12 | "Baker's Hill" (this project's title) vs. "Bankers Hill" (Projects #8/#9, same file) |
| Gallery 1 Project #18 | Title claims "without a full sanding"; both image alts describe dust-free/dustless sanding |
| Videos `ixqPScnbnLE` / `HF1pRJYTgZk` | Identical title/description/category/publish-date in the data |
| Blog Case Study #11 (2 images) | Empty legacy alt, no distinguishing caption or prose |
| Blog Case Study #12 (2 sub-pairs + mapping) | Identical legacy alt within each sub-pair after spam-stripping; case study's `prose` list doesn't map cleanly 1:1 to its one figcaption |
| Solid & Engineered / Homepage | "Graff Brothers" (Solid & Engineered Project 1) vs. "Graf Brothers" (homepage Bird Rock) brand-spelling conflict |
| Solid & Engineered Project 1 | `TRICIA WALNUT27/30/63/76` filenames vs. published white-oak description (carried forward from Milestone 2.5, still unresolved) |
| Gallery 4 Project #61 | Neither photo's data describes a damaged/pre-refinish state; both are completed-result views distinguished only by geographic vantage |

## Files changed

**Source (generator) changes:**
`build/data/index/gallery.json`, `build/data/recent_project_photo_gallery_1/modules.json`,
`build/data/recent_project_photo_gallery_2/modules.json`,
`build/data/recent_project_photo_gallery_3/modules.json`,
`build/data/recent_project_photo_gallery_4/modules.json`,
`build/data/solid_wood_floor_photo_gallery/images.json`,
`build/scripts/pages/build_gallery1.py`, `build_gallery2.py`, `build_solidwood.py`,
`build_videos.py`, `assemble_deep_cleaning.py`, `assemble_blog.py`.

**New:** `build/scripts/generate_alt_recomposition_ledger.py`,
`build/data/image_alt_recomposition_ledger.csv`,
`build/data/image_alt_recomposition_similarity.md`,
`docs/2026-07-image-alt-recomposition-sample-review.md` (Phase A, all 3 revisions),
this report.

**Regenerated output (alt attributes only, verified byte-for-byte elsewhere):**
`index.html`, `recent_project_photo_gallery_1.html`, `recent_project_photo_gallery_2.html`,
`recent_project_photo_gallery_3.html`, `recent_project_photo_gallery_4.html`,
`solid_wood_floor_photo_gallery.html`, `deep-cleaning-hardwood-floors-san-diego.html`,
`blog.html`, `videos_of_refinishing_process.html`.

**Confirmed untouched:** `recent_project_gallery_5.html`, `about_us.html`,
`contact_us.html`, `floor-assessments-inspections.html`, `sitemap.xml`, `robots.txt`,
`CLAUDE.md`, `build/raw-source/`, `build/archive/`, `assets/ALL_IMAGES/`, all CI/Cloudflare
configuration, all navigation/footer/analytics chrome.
