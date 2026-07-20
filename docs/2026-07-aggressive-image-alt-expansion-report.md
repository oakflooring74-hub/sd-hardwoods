# Aggressive, Evidence-Grounded Image Alt-Text Expansion — Implementation Report

2026-07-20. Owner-directed, ranking-first milestone. Full requirements record:
`docs/SDH_Aggressive_Image_Alt_Expansion_Strategy_July_2026.md`. This report is the
completed-implementation record; read alongside `CLAUDE.md` and `docs/NEXT_SESSION.md`.

## Summary

- **465** total `<img>` usages audited across all 13 pages.
- **413** meaningful image/thumbnail usages expanded with dense, grounded alt text.
- **58** meaningful video thumbnails expanded (previously `alt=""` on every one).
- **2** intentional decorative empty alts documented (the site logo mark and the
  JS-only lightbox placeholder — see "Decorative images" below).
- **353** existing alt strings preserved **verbatim** as the literal prefix of their
  final alt (byte-for-byte checked, see "Verification" below).
- **0** unverified facts added. Every appended sentence is drawn from data already
  in the repository (owner-approved captions, project titles/descriptions already
  visible on the page, per-image alt fields already present but previously unused,
  or curated video metadata already stored in `youtube_videos.json`).

## Page-by-page coverage

| Page | Total placements | Expanded | Decorative empty |
|---|---|---|---|
| Homepage (`/`) | 90 (89 gallery images + 1 Bona badge) | 90 | 0 |
| Gallery 1 | 40 | 40 | 0 |
| Gallery 2 | 42 | 42 | 0 |
| Gallery 3 | 20 | 20 | 0 |
| Gallery 4 | 40 | 40 | 0 |
| Gallery 5 | 10 | 10 | 0 |
| Solid & Engineered Installation | 28 | 28 | 0 |
| Deep Cleaning | 40 | 40 | 0 |
| About | 1 | 1 | 0 |
| Floor Assessments & Inspections | 1 | 1 | 0 |
| Blog | 43 | 43 | 0 |
| Videos | 58 (thumbnails) | 58 | 0 |
| Contact | 0 (no `<img>` on this page — confirmed, not skipped) | — | — |
| Shared chrome (all 13 pages) | logo ×3 placements/page + lightbox placeholder | 0 | 2 (documented once, applies site-wide) |

Every page in the canonical 13-page map is accounted for; Contact carries no
`<img>` elements at all (verified by parse, not assumed) and required no changes.

## Length statistics (final alt, meaningful placements only, n=413)

- Minimum: **197** characters
- Median: **703** characters
- Average: **734.4** characters
- Maximum: **2,380** characters (`RECOAT WOOD FLOORING DEEP CLEAN CARMEL VALLEY SAN DIEGO.jpg`, Blog case study #6 — a photo whose case study has three prose paragraphs, all genuinely about that image)

These lengths were driven entirely by how much verified detail existed for each
image, not by a target — no alt was padded or artificially shortened.

## Existing alt strings preserved verbatim

**353 of 415** ledger rows retained an existing alt string as the literal, unedited
prefix of the final alt. Verified programmatically: for every such row,
`final_alt.startswith(current_alt)` — **0 failures** on the final build. (An
earlier draft of the shared expansion helper trimmed trailing whitespace from a
handful of source alts before appending punctuation; this was caught during
verification and fixed so the original bytes are never altered — see "Verification
performed" below.)

The remaining 60 non-verbatim rows are exactly the cases where there was no
existing alt to preserve: all 58 video thumbnails (previously `alt=""` on every
one) and 2 blog case-study images whose original alt was empty.

## Duplicate final alts

**4 duplicate groups**, all pre-existing duplication in the source data, faithfully
carried through rather than artificially differentiated:

1. Gallery 3, `/SUE30.jpg` + `/SUE76.jpg` — identical alt text already existed in
   `modules.json` before this milestone (same module, same project).
2. Blog, two images in case study #11 — both had an **empty** original alt and
   share the same case-study title/prose (no other distinguishing text existed
   for either photo).
3. Blog, two images in case study — both already carried identical alt text in
   `case_studies.json` before this milestone.
4. Videos, `ixqPScnbnLE` and `HF1pRJYTgZk` — two distinct YouTube videos that
   already share the same title in `youtube_videos.json` and both have no
   `site_description` (so both fall back to the same truncated raw description).

Per the milestone's explicit instruction, none of these were shortened or
rewritten to force artificial difference — duplication here reflects duplication
already present in the site's own data.

## Competitor names — retained / added

- **Retained (2 placements)**: the Deep Cleaning page's two pre-existing
  competitor comparisons ("...better than Coit or Stanley Steemer" on
  `DEEP CLEAN HARDWOOD FLOORS SAN DIEGO WIRE BRUSH CLEANING.jpg"`, and
  "...better than steam cleaning or standard mopping used by companies like
  Stanley Steemer or Zerorez" on `DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 43.png`).
  Both were extracted verbatim from `build/raw-source/deep-cleaning-hardwood-floors-san-diego.html`
  before this milestone and remain **byte-for-byte unchanged** as part of the
  preserved prefix.
- **Added (0)**: no new competitor-name references were introduced anywhere on
  the site. New mentions were only permitted when genuinely supported and
  coherent; none of the appended text needed one.

## Protected ranking images and metadata

- All homepage image numbers (#1–#89), order, `href`, `data-caption`, and
  lightbox behavior are byte-identical except the `alt` attribute.
- All gallery pairs (Galleries 1–5, Solid Wood) keep their original order,
  before/after pairing, filenames, and visible captions/figcaptions untouched.
- All 58 YouTube video IDs, upload dates, durations, embeds, titles (raw and
  curated `site_display_title`), and the `ItemList`/`VideoObject`/`CollectionPage`
  schema graph are untouched — confirmed by diffing `build/data/youtube_videos.json`
  (no diff) and re-parsing every page's JSON-LD (see "Verification performed").
- No page URL, canonical, `<title>`, meta description, or `<h1>` changed on any
  of the 13 pages (confirmed — see below).
- The Deep Cleaning page's owner-locked title/meta/H1 (Milestone 2.9/2.11) are
  unchanged.
- The known, previously-flagged `TRICIA WALNUT27/30/63/76.jpg` filename-vs-white-oak
  conflict on the Solid & Engineered Installation page (`docs/PROJECT_DECISIONS.md`)
  was **not** resolved by this milestone — the appended text repeats only the
  already-published "white oak" wording from the project heading/note, asserting
  nothing new about species identity either way. Flagged again below for owner
  review.

## Source files changed

Generator sources (permanent, drive regenerated output):

- `build/scripts/common/alt_expand.py` — **new** shared helper (verbatim-preserving
  sentence-append, caption cleanup, HTML-entity/quote-attribute safety).
- `build/scripts/pages/build_gallery1.py`, `build_gallery2.py`, `build_gallery5.py`,
  `build_solidwood.py`, `build_videos.py`, `build_about_us.py`,
  `build_floor_assessments.py`
- `build/scripts/pages/assemble_deep_cleaning.py`, `assemble_blog.py`
- `build/scripts/common/build_page.py` (shared Gallery 3/4 renderer)

Data:

- `build/data/index/gallery.json` — homepage per-image `alt` fields expanded in place.
- `build/data/index/main_content.html` — Bona Certified Craftsman badge alt expanded.

Regenerated output (all 13 root pages regenerate deterministically from the above;
only `alt="..."` attribute values differ from the pre-milestone commit):

`index.html`, `about_us.html`, `blog.html`, `deep-cleaning-hardwood-floors-san-diego.html`,
`floor-assessments-inspections.html`, `recent_project_gallery_5.html`,
`recent_project_photo_gallery_1.html` through `_4.html`, `solid_wood_floor_photo_gallery.html`,
`videos_of_refinishing_process.html`. `contact_us.html`, `sitemap.xml`, `robots.txt`
regenerate byte-identical (no diff).

New:

- `build/data/image_alt_expansion_ledger.csv` — full before/after ledger, 415 rows.
- This report.

Deliberately **not** modified: `assets/ALL_IMAGES/` (untouched, as required);
`build/data/media/` and `docs/media-review/` (regenerating these surfaced an
unrelated, pre-existing data-hygiene issue — see "Unresolved / flagged for owner
review" below — reverted rather than absorbed into this milestone's scope).

## Unresolved or conflicting facts requiring owner review

1. **Solid Wood Gallery — `TRICIA WALNUT27/30/63/76.jpg`.** Filenames say
   "walnut"; the project heading/alt/note all describe a Graff Brothers
   **white oak** installation. Flagged since Milestone 2.5, still unresolved.
   This milestone's appended text repeats only the already-published white-oak
   wording — it does not take a position on the conflict. (4 ledger rows,
   `confidence: medium`.)
2. **Gallery 1 caption contamination.** One legacy caption field
   (`ENCINITAS CHERRY18.jpg`) contains a leftover Yahoo Facebook-Like-button JS
   fragment instead of real caption text (a raw-source extraction artifact).
   Excluded from the appended alt text entirely; not used as a source. (1 ledger
   row flagged `owner_review_required`.)
3. **Media-inventory drift (not part of this milestone, noted for awareness).**
   Regenerating `build/scripts/generate_media_inventory.py` (last run
   2026-07-18, i.e. stale since before Milestone 2.7) surfaced one pre-existing
   orphaned placement (`HOME-IMG-034`, referencing an image removed from the
   homepage in Milestone 2.7's near-duplicate cleanup) that the validator flags
   as an error once the inventory catches up. This is unrelated to image alt
   text and was **not** fixed here — the regeneration was reverted to avoid
   scope creep, per this milestone's "no broad build-system refactor" and "stop
   and report unrelated changes" rules. Worth a few minutes in a future
   media-facts session.

## Verification performed

1. **Rebuilt all 13 pages** via `python build/scripts/build_all.py` — succeeded.
2. **Confirmed a second rebuild is byte-identical** — SHA-256 over all 13 root
   pages + `sitemap.xml` + `robots.txt` matched exactly across two consecutive runs.
3. **Every meaningful project image and video thumbnail has nonempty alt text** —
   parsed all 13 pages with `html.parser`; 465 total `<img>` elements; 0 meaningful
   placements with empty `alt` (only the 3-per-page logo instances and the JS
   lightbox placeholder are intentionally empty).
4. **Every preserved alt appears verbatim at the start of its final alt** —
   programmatically checked `final_alt.startswith(current_alt)` for all 353
   applicable ledger rows: 0 failures on the final build. (A bug in the first
   draft of the shared append helper — stripping trailing whitespace from the
   original alt before adding punctuation — was caught by this exact check,
   fixed in `alt_expand.py` so the base text is never trimmed or altered, and
   the entire pipeline was rebuilt and re-verified.)
5. **No existing phrase was silently removed** — confirmed by the same
   verbatim-prefix check plus manual diff review (see step 9).
6. **All HTML attributes/entities valid, no truncation** — confirmed `<img>` count
   equals `alt="` count on every page (no malformed attributes); confirmed the
   longest alt (2,380 chars) renders in full in the actual HTML, not truncated;
   found and fixed two real defects during verification: (a) appended prose
   containing a literal `"` (inch-mark) character would have broken the
   unescaped `alt="..."` attribute in the Deep Cleaning and Blog assemblers —
   fixed by escaping quotes in those two files; (b) appended title/heading text
   containing a bare `&` (e.g. "Repairs & Installation") would have been
   invalid inside an attribute value — fixed by adding entity-aware `&`-escaping
   to the shared helper (`escape_bare_amp`, applied to every appended sentence,
   never to the preserved original text). Re-verified 0 raw-ampersand and 0
   unescaped-quote issues across all 13 pages after the fix.
7. **No image path, filename, capitalization, order, number, caption, dimensions,
   or source changed** — confirmed by line-level diff review: every changed line
   differs *only* in its `alt="..."` value; `src`, `href`, `class`,
   `data-caption`, `width`/`height`, and gallery badge numbers are identical
   before/after on every changed line (spot-checked across all 13 pages).
8. **No page URL, canonical, title, meta, H1, navigation, CTA, or visible layout
   changed** — confirmed exactly one `<h1>` per page; confirmed via diff that no
   `<title>`, `<meta name="description">`, `rel="canonical"`, nav, or footer line
   changed on any page.
9. **All JSON-LD blocks still parse** — every `<script type="application/ld+json">`
   block on all 13 pages parses as valid JSON after rebuild.
10. **Duplicate final alts reported, not auto-shortened** — see "Duplicate final
    alts" above; all 4 groups are pre-existing duplication in source data,
    left intact.
11. **`git diff --check`** — clean (only benign `core.autocrlf` LF/CRLF advisory
    warnings on this Windows checkout, zero actual whitespace errors).
12. **Full diff reviewed** for unrelated changes — confirmed the only content
    diffs are `alt="..."` attribute values (see step 7); confirmed
    `build/data/media/` and `docs/media-review/` regeneration was reverted after
    it surfaced the unrelated pre-existing issue noted above.
13. Browser/visual QA of representative pages (homepage, a gallery, Deep
    Cleaning, Solid & Engineered, Videos) was not additionally performed in
    this session beyond HTML-level verification, since alt text is not visually
    rendered and no visible markup, layout, or interaction code was touched —
    consistent with the milestone's own instruction that alt-text work "must
    not require altering unrelated markup or architecture."

## Commit and deployment status

- Committed to `redesign` as `f233a7d` (implementation) and `50ecdbc` (commit-hash
  record in `docs/NEXT_SESSION.md`).
- Pushed to `origin/redesign`. GitHub Actions run
  [`29764815648`](https://github.com/oakflooring74-hub/sd-hardwoods/actions/runs/29764815648):
  both jobs green — `Build and verify generated output` (the CI regenerate-and-diff
  gate: regenerating from the committed generator sources produces zero drift
  from the committed root pages) and `Deploy to Cloudflare Pages`.
- Cloudflare Pages preview deployed successfully at commit `50ecdbc5eabb05416e6a4546c4b6e68df773ab52`:
  deployment URL `https://7b7d82b9.sd-hardwoods.pages.dev`, alias
  `https://redesign.sd-hardwoods.pages.dev`.
- `master` and production were not touched at any point in this session.
