# San Diego Hardwoods — site rebuild tooling

This directory holds everything used to rebuild all 12 pages of sdhardwoods.com from the
original Yahoo/Turbify "Site Solution" site into the current design. The generated output
(the actual `.html` files people visit) lives at the **repo root**, one level up from here.
This folder is the *generator* — raw crawled source, extracted content data, shared design
partials, and the scripts that combine them. Keeping the two separate means you can change
the design system in one place (`chrome/`) and regenerate every page consistently, instead of
hand-editing 12 pages that have each drifted independently (which is the exact problem the
original site had).

Read this file before touching anything in here. It explains what exists, why it's shaped
the way it is, and where the rough edges are.

## Prerequisites

- Python 3.10+, standard library only — nothing to `pip install`.
- On Windows, if you only have Git Bash / WSL available, note that `python3` may not be on
  its `PATH` even when a Windows Python install exists. Run scripts via a native PowerShell
  or `cmd` session (`python script.py`) if Bash gives you `command not found`.
- **2026-07-16 note:** on this laptop, `python`/`python3` previously resolved only to the
  Windows Store's stub alias (which errors instead of running anything) — there was no real
  Python interpreter installed at all, not just a `PATH` issue. Real Python 3.12 was installed
  via `winget install Python.Python.3.12` to unblock the build; this is now resolved and the
  pipeline runs normally. If `python --version` ever reports the Store-redirect error again on
  a fresh machine, that's this same issue, not a `PATH` misconfiguration.
- Browser-based QA/testing (Playwright + Chromium) is **not** part of this build pipeline and
  is not installed in this repo — a prior session installed both in a scratch temp directory
  outside the project to drive the regenerated pages in a real browser for cross-viewport
  testing, then discarded them. Reach for the same approach (or a project-local install, if a
  future session wants repeatable browser testing) rather than assuming either is available.

## Directory map

```
build/
  README.md              <- this file
  chrome/                <- shared header/nav/footer/dark-mode partials, reused by every page
  raw-source/             <- frozen snapshot of each live page's original HTML, as crawled
  data/                   <- extracted content per page (JSON + companion fragments)
  scripts/
    common/               <- reusable extraction + assembly tools
    pages/                <- one (or two) build scripts per page
    build_all.py           <- regenerates all 12 pages in one run
  archive/                <- superseded/abandoned exploratory scripts, kept for history only
```

## Quick start: regenerate everything

```
python build/scripts/build_all.py
```

This overwrites the repo-root `.html` files directly (the live pages). **Always run `git
diff` afterward and review before committing** — see "Known quirks" below for the two pages
where a fresh regeneration will *not* be byte-identical to what's currently committed, and
why that's expected.

## Quick start: regenerate one page

Run its script(s) directly, e.g.:

```
python build/scripts/pages/build_about_us.py
```

See the reference table below for which script(s) each page needs and in what order.

## How a page gets built

Every page follows the same shape:

1. **Raw source** (`raw-source/<slug>.html`) — an unmodified snapshot of what was live on
   Turbify when this rebuild was done. Never edit these; they're the ground truth for
   "what did the original page actually contain."
2. **Extraction** — a script reads the raw source and pulls out the reusable pieces: page
   title, meta description, canonical URL, JSON-LD schema blocks, the Google Analytics
   snippet (if present), the vcard business-description text, and every image (`src`/`alt`/
   `class`/wrapping link). This gets saved as JSON (and a few plain-text/HTML fragments) into
   `data/<slug>/`.
3. **Assembly** — a script combines that extracted data with the shared `chrome/` partials
   (site-wide CSS, dark-mode toggle, sticky header/nav, footer, scroll hint) and page-specific
   prose/layout (hand-written once, when the page was first rebuilt) into the final HTML,
   written to the repo root.

Most pages do steps 2 and 3 in one script (`build_X.py`, using `scripts/common/assemble_page.py`
as the shared final-HTML template). A few do it in two scripts (`build_X.py` then
`assemble_X.py`) because they were built before that shared helper existed. Both patterns
work the same way conceptually; the table below says which is which.

### Why `chrome/` matters

`chrome/` holds the one shared copy of:
- `site_css.html` — every CSS custom property (colors, type) and component class (`.btn`,
  `.card`, `.gallery`, `.hero`, etc.) used across all 12 pages.
- `darkmode_boot_scripts.html` — the dark-mode-by-default boot logic + toggle click handler.
- `top.html` — the utility bar, brand bar, and mega-nav flyout (with a `__VCARD_DESC__`
  placeholder each page's build script fills in with its own business-description text).
- `footer.html` — the single unified footer (the original site had this duplicated, with
  drifted content, on almost every page).
- `scrollhint_and_toggle.html` — the "scroll to explore" pill + the light/dark toggle button
  (with a `__SCROLL_TOPIC__` placeholder for page-specific wording).

**Change something in `chrome/`, then re-run `build_all.py`, and it applies to all 12 pages
at once.** That's the entire point of this refactor versus the original site.

## Per-page reference

| Slug | Raw source | Data | Script(s) | Notes |
|---|---|---|---|---|
| `index` (home) | `raw-source/index.html` | `data/index/` (`gallery.json`, `main_content.html`) | `pages/build_homepage.py` | See quirk #1 below |
| `about_us` | `raw-source/about_us.html` | `data/about_us/` | `pages/build_about_us.py` | |
| `contact_us` | `raw-source/contact_us.html` | `data/contact_us/` | `pages/build_contact_us.py` | No contact form on this site — call/text/email only |
| `videos_of_refinishing_process` | `raw-source/videos_of_refinishing_process.html` | `data/videos_of_refinishing_process/` | `pages/build_videos.py` | See quirk #2 (broken JSON-LD, fixed) |
| `recent_project_photo_gallery_1` | `raw-source/recent_project_photo_gallery_1.html` | `data/recent_project_photo_gallery_1/` (`modules.json`) | `pages/build_gallery1.py` | Before/after module pairs |
| `recent_project_photo_gallery_2` | `raw-source/recent_project_photo_gallery_2.html` | `data/recent_project_photo_gallery_2/` | `pages/build_gallery2.py` | See quirk #3 (split project fragment, fixed) |
| `recent_project_photo_gallery_3` | `raw-source/recent_project_photo_gallery_3.html` | `data/recent_project_photo_gallery_3/` (`modules.json`) | `common/build_page.py` | Also builds gallery_4 in the same run (shared `CONFIGS` list) |
| `recent_project_photo_gallery_4` | `raw-source/recent_project_photo_gallery_4.html` | `data/recent_project_photo_gallery_4/` (`modules.json`) | `common/build_page.py` | Same script as gallery_3 |
| `recent_project_gallery_5` | `raw-source/recent_project_gallery_5.html` | `data/recent_project_gallery_5/` (`images.json`) | `pages/build_gallery5.py` | See quirk #4 |
| `solid_wood_floor_photo_gallery` | `raw-source/solid_wood_floor_photo_gallery.html` | `data/solid_wood_floor_photo_gallery/` (`images.json`) | `pages/build_solidwood.py` | See quirk #4. No GA on this page (matches original) |
| `deep-cleaning-hardwood-floors-san-diego` | `raw-source/deep-cleaning-hardwood-floors-san-diego.html` | `data/deep-cleaning-hardwood-floors-san-diego/` | `pages/build_deep_cleaning.py` **then** `pages/assemble_deep_cleaning.py` | Two-step |
| `blog` | `raw-source/blog.html` | `data/blog/` (`case_studies.json`) | `pages/build_blog.py` **then** `pages/assemble_blog.py` | Two-step. 12 case-study entries |

Extraction-only helper scripts that (re)produce a page's `data/` files from `raw-source/`,
kept separate from the main build script:
- `pages/extract_gallery5.py`, `pages/extract_jsonld5.py` → `data/recent_project_gallery_5/`
- `pages/extract_gallery_solidwood.py` → `data/solid_wood_floor_photo_gallery/`
- `pages/extract_g5_sw_meta.py` → title/description/canonical/vcard/JSON-LD for both of the above
- `pages/verify_gallery5.py` — compares a rebuilt gallery_5 page against its raw source
  (image count, JSON-LD validity, footer/nav/toggle uniqueness, title match)
- `common/extract_gallery.py` → `data/index/gallery.json` (homepage's 96-photo grid)
- `common/extract_ba.py` — generic before/after-module extractor, used for galleries 1–4
  (run as `python extract_ba.py <raw_html_path> <out_json_path>`)
- `common/inventory.py` — quick structural scan across all 12 raw-source pages (title, meta
  description, canonical, image count, and whether old-site markers like the mega-nav or
  dark-mode boot script are present) — useful as a sanity check, not part of the build itself

## To re-crawl the live site

If the owner has since edited the live Turbify site and you want a fresh baseline:

```
python build/scripts/common/crawl_live_site.py
```

This overwrites `raw-source/*.html`. Re-run the relevant extraction + build scripts
afterward to pick up whatever changed. (The *original* crawl for this rebuild was done with
ad hoc `curl` commands that were never saved as a script — this one is a clean equivalent
written afterward so the step isn't lost. It hasn't been run against the live site itself,
only checked for correctness against the already-saved raw-source files it's meant to
reproduce.)

## Known quirks

1. **Homepage predates the `chrome/` consolidation.** `build_homepage.py` was the very first
   page built, before the shared partials in `chrome/` existed as their current, most-complete
   version — the homepage originally shipped with its own embedded copy of the CSS/dark-mode
   scripts, snapshotted at that earlier point. This has since been rewritten to use `chrome/`
   like every other page (so future `chrome/` edits *do* apply to the homepage too), but that
   means running it now produces output that's very slightly different from what's currently
   committed at the repo root — mainly a few CSS values that were refined afterward (hero
   heading size, added `.blog-list`/`figcaption` styles) and the simplified dark-mode toggle
   script instead of the original, functionally-equivalent-but-more-verbose Turbify one. Not a
   bug — just confirms the tooling wasn't re-applied to the homepage after the fact. Review
   the diff before deciding whether to accept it.

2. **A JSON-LD bug in the live source, fixed.** On `videos_of_refinishing_process`, two
   schema blocks (`CollectionPage` and a `VideoObject` `@graph` array) were fused into one
   invalid JSON blob by a missing `</script>` tag on the live site. `data/videos_of_refinishing_process/jsonld_fixed.html`
   is the corrected version (same content, restored closing tag); `jsonld_as_broken_on_live_site.html`
   is kept alongside it for reference so the original bug isn't lost to history.

3. **A split project write-up, reunited.** On `recent_project_photo_gallery_2`, project
   "#27" (Rancho Santa Fe & Bird Rock) had its title text and its two photos split across
   broken, duplicate `<li>` fragments in the live source (visible in
   `data/recent_project_photo_gallery_2/broken-fragments/`). `build_gallery2.py` manually
   reunites them (see the "Patch" comment in that script) rather than silently dropping the
   project. The same style of bug (title separated from its images by broken markup) also
   showed up in the blog page's case study #3 — `assemble_blog.py` handles that one the same
   way.

4. **`recent_project_gallery_5` and `solid_wood_floor_photo_gallery`'s original generator
   code wasn't saved.** Both pages were originally assembled by an agent running ad hoc
   Python directly in its shell, not as a saved script — so when this tooling was organized,
   there was extracted data (`images.json`, etc.) and a *working, already-verified* final
   page, but no script that reproduced it. `build_gallery5.py` and `build_solidwood.py` were
   written afterward to close that gap, using the same pattern as every other page and the
   already-extracted data. Running them reproduces a page with all the same images, alt text,
   and JSON-LD — verified byte-for-byte against the extracted data — but laid out as a plain
   responsive photo grid rather than whatever specific arrangement the original inline code
   happened to produce (which is no longer known). Not a content loss, just a specific-layout
   difference worth knowing about.

5. **Google Analytics is inconsistently present on the live site, not just in this rebuild.**
   10 of 12 pages carry the legacy `_gaq`/`ga.js` tracking snippet (account `UA-20793161-1`);
   the homepage and `solid_wood_floor_photo_gallery` do not, on the *original* live site. This
   tooling preserves that inconsistency faithfully rather than guessing whether it was
   intentional — if you decide it should be everywhere, the snippet is in every other page's
   `<head>` extraction and can be copied into those two build scripts.

6. **`archive/` is not maintained.** It holds abandoned exploratory scripts from early in this
   rebuild (a first attempt at extracting galleries 1/2 that was superseded by
   `common/extract_ba.py`, and two early draft assemblers). Kept for provenance only — don't
   expect these to run against the current directory layout, and don't build on them.

7. **`data/*/*.json` files may contain a `"source"` field with an old absolute path** from
   the machine/session where the extraction was originally run. That's inert historical
   metadata, not something the build scripts read back — safe to ignore.
