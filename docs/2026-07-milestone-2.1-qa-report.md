# Milestone 2.1 — Implementation & QA report

Date: 2026-07-17. Branch: `redesign`. **Approved by the owner after visual review on 2026-07-17** and committed on `redesign` as a single Milestone 2.1 commit (hash recorded in `docs/NEXT_SESSION.md` and `git log`). Not pushed, not merged to `master`, not deployed — those remain separate, owner-initiated steps. Production untouched throughout.

Final pre-commit verification (2026-07-17): `build_all.py` ×2 → exit 0 both runs, byte-identical output; legacy-asset assertion re-run in Python (14 strings × 12 pages) → zero matches; full browser QA suite re-run → **330 passed, 0 failed**.

## Scope delivered

1. **Explore bar redesigned** (`build/chrome/scrollhint_and_toggle.html`): translucent charcoal/navy surface with backdrop blur, fine blue outline, soft border-glow pulse (~7s) and ≤4px vertical float; hidden over the initial hero on every page — appears only after `scrollY > 250` **and** the hero (CTA area included) is fully above the bar's strip of the viewport; hides again while the footer is on screen; dismissable with session persistence; hover/focus pauses all animation; `prefers-reduced-motion` disables pulse, float, and message rotation entirely. Copy: eyebrow **EXPLORE REAL PROJECTS**, primary line **See Before-and-After Hardwood Floor Transformations**, rotating linked destinations (dust-contained refinishing videos, repairs & restoration, deep cleaning & recoating, solid hardwood installation, project galleries, refinishing videos). Every message is a real link; visible focus states; accessible dismiss label.
2. **Top contact strip removed** from all pages; NAP preserved in masthead/footer/Contact/JSON-LD, with `San Diego, CA 92130 • CSLB-Licensed California Flooring Contractor` added to the footer.
3. **Tiny SEO strip removed and relocated** — full inventory and disposition in `docs/milestone-2.1-seo-content-map.md`.
4. **Homepage repositioned**: new H1 (*Dust-Contained Hardwood & Bamboo Floor Refinishing, Restoration, Deep Cleaning & Installation in San Diego*), broadened hero copy (solid/engineered/bamboo; repair; dust-contained sanding; deep cleaning; recoating; nail-down & glue-down installation), new **Bona DCS 2.0** section (dual HEPA filtration, continuous bagging, capture at the source, "virtually dust-free in most normal project conditions" — no absolute zero-dust claim), deep-cleaning section now covers cleaning-only scope, wire-brushed floors, and oiled-floor conversion to low-sheen low-VOC waterborne systems; service list gains glue-down installation and oiled-floor conversion.
5. **Theme control moved into the menu**: floating "Toggle Light Mode" button removed site-wide; an accessible toggle (icon + visible text "Use Light Appearance"/"Use Dark Appearance", `aria-pressed`) sits at the bottom of the drawer, reachable from the mobile Menu button and the mini-header Menu button (same shared drawer). Selection persists (`localStorage`); first visit respects `prefers-color-scheme` (falling back to the site's dark default); keyboard operable with visible focus; nothing floats over content.
6. **Legacy image-buttons removed globally at the generator/data level** (see table below) — not hidden with CSS; none render as gallery photos, enter the lightbox, or leave broken links. Useful destinations replaced with real text links.
7. **Gallery 5 rebuilt as before/after pairs** from a new explicit data structure (`build/data/recent_project_gallery_5/projects.json`): the raw source's five project write-ups #81–#85 restored, each with heading, original description, Before/After labeled pair, original captions and byte-identical alt text. Desktop side-by-side; mobile stacks the pair inside the same card. Lightbox order preserves pair order.
8. **Solid Wood Floor Gallery restored to four distinct projects** (`build/data/solid_wood_floor_photo_gallery/projects.json`): original intro ("Craftsman-Level Hardwood Floors…"), material-sourcing section, four project sections with the raw source's own headings (3"×¾" rift & quartered white oak / 2¼" white oak Mission Hills kitchen / 2¼" white oak cottage natural / 2¼" red oak plainsawn North County), each with only its own images (4/7/8/9 = 28 photos), plus the original "Since 1990…" outro. Alt text byte-identical to the frozen extraction.
9. **Videos page expanded to the full public channel archive**: checked-in deterministic snapshot `build/data/youtube_videos.json` (**58 public videos: 47 standard + 11 Shorts**, harvested 2026-07-16 from the public channel pages — no API key involved anywhere); manual refresh utility `build/scripts/update_youtube_videos.py` (documented in `build/README.md`; preserves curated fields, reports removed videos loudly, never runs during normal builds). Page: intro, 6 featured cards, complete library grid, category filters, click-to-activate `youtube-nocookie` modal player (no autoplay, Escape closes, focus returns to the activating card), lazy thumbnails, per-card "Watch on YouTube" links, "View All Videos on YouTube" channel CTA, and accurate `VideoObject` structured data for all 58 (real dates/durations; empty fields omitted, nothing invented).

### Featured videos (6) & categories

Featured: Bona DCS 2.0 edge sanding (Jv1KsJndmww) · White Oak Restoration & Flattening flagship (DsGl1rajDys) · Complete Deep Cleaning with results, wire-brushed oak (IbGVK9cFs8w) · 100-Year-Old Douglas Fir restoration (ARfEQTQFbBo) · White Oak plug repairs, North Park (rMtQ0TfEkwc) · Teak specialty refinish, Solana Beach (McBbfiMpqPg).

Categories (baked into the snapshot for deterministic rendering): Dust-Contained Sanding & Refinishing (38) · Repairs & Restoration (16) · Deep Cleaning & Recoating (4) · Shorts filter (11) · All Videos (58). The channel has **no installation-specific or finish-upgrade-specific videos**, so those filters are (correctly) not fabricated; the 14 curated project descriptions and gallery cross-links from the previous hand-built page are preserved on their matching cards via `site_description`/`gallery_href`.

## Legacy image-button removals by page

| Page | Removed |
|---|---|
| Videos | CONTACT US BETTER BUTTON 2025.png, NEXT PAGE BUTTON 2025.png, ABOUT US 2025 BUTTON.png |
| Gallery 3 | NEXT PAGE BUTTON 2025.png, CALL OR TEXT NOW BUTTON 2025.png, ultra clean button.png ×2 |
| Gallery 4 | NEXT PAGE BUTTON 2025.png, CALL OR TEXT NOW BUTTON 2025.png, ultra clean button.png ×2 |
| Gallery 5 | ultra clean button.png ×2, ultra clean button 2.png, NEXT PAGE BUTTON 2025.png, CALL OR TEXT NOW BUTTON 2025.png |
| Solid Wood Gallery | NEXT PAGE BUTTON 2025.png, CONTACT US BETTER BUTTON 2025.png, ABOUT US 2025 BUTTON.png, HOME BUTTON 2025.png |
| Blog | CONTACT US BETTER BUTTON 2025.png, ABOUT US 2025 BUTTON.png, HOME BUTTON 2025.png, NEXT PAGE BUTTON 2025.png, ultra clean button.png ×2 |
| Deep Cleaning | NEXT PAGE BUTTON 2025.png, CALL OR TEXT NOW BUTTON 2025.png |
| Homepage / About / Contact / Galleries 1–2 | ultra clean button.png (and ultra clean button 2.png on Gallery 1) removed from the deep-cleaning CTA cards (cards kept as text + button link) |

The archived image files themselves (hosted on Turbify, referenced in frozen `data/*/images.json` extractions) were **not** deleted — only excluded from generated output, as the brief allows.

**Legacy-asset assertion (required by the brief) — PASS.** A case-insensitive search of all 12 generated HTML files for every listed string (`CONTACT US BETTER BUTTON 2025.png`, `NEXT PAGE BUTTON 2025.png`, `ABOUT US 2025 BUTTON.png`, `CALL OR TEXT NOW BUTTON 2025.png`, `ultra clean button.png`, each in space and `%20` form, plus `ultra clean button 2.png` and `HOME BUTTON 2025.png` discovered during the audit) returns **zero matches**.

## Build results

- `python build/scripts/build_all.py` → exit 0, all 12 pages regenerated.
- Second run → exit 0, **byte-identical output for all 12 pages** (cmp), re-verified after the final chrome tweak. CI's regenerate-and-diff gate will pass once the working tree is committed as-is (the gate compares regeneration against the committed tree).
- Working tree contains only intentional Milestone 2.1 changes (file list below).

## Browser QA

Playwright + Chromium 149 (installed outside the repo, per project convention), served over local HTTP (node http-server), not `file://`.

- **Matrix**: all 12 pages × desktop 1440×900 × mobile 390×844 — no horizontal overflow, header logo resolves, strips absent, no floating toggle, theme control present in drawer, exactly one H1, explore bar hidden over hero / appears after scroll / hides at footer, mini-header appears after masthead scrolls out, no console errors caused by the changes.
- **Interactions**: drawer open/close/Escape/focus-restore/scroll-lock; desktop dropdown click + Escape with `aria-expanded` sync; theme toggle (label + `aria-pressed` + icon sync, persistence across reload, dark default under a dark system scheme, light honored for first-visit light-scheme users); explore-bar dismissal + session persistence + no interactive element under the bar when shown.
- **Videos**: 0 iframes on initial load; 58 unique cards; filters show 4 (deep cleaning), 11 (Shorts) with featured section auto-hiding when empty; modal opens on activation with a `youtube-nocookie` embed, **no autoplay**, Escape closes, iframe destroyed on close (playback stops), focus returns to the activating button; mobile player works; no horizontal overflow.
- **Gallery 5**: desktop pairs side-by-side; mobile pairs stacked and kept together; lightbox order = pair order; labels present.
- **Solid Wood**: four project sections render with their headings and grouped images.
- **Deep Cleaning**: relocated scope content (cleaning-only / recoat prep / wire-brushed & oiled) renders readably.
- **Reduced motion** (`prefers-reduced-motion: reduce`): explore bar still appears but with `animation: none` (no pulse/float) and message rotation disabled; global reduced-motion kill switch still active.
- **Light mode**: stored light preference honored; about page light render clean; first visit with a light system scheme gets the light theme (new behavior — system preference respected before any stored choice).

**Final: 330 checks, 0 failures.**

Screenshots (gitignored `qa-screenshots/`): `m2-1-home-desktop-top.png`, `m2-1-home-desktop-explore-visible.png`, `m2-1-home-desktop-light.png`, `m2-1-home-mobile-menu-theme-control.png`, `m2-1-videos-desktop-library.png`, `m2-1-videos-desktop-modal.png`, `m2-1-videos-mobile-player.png`, `m2-1-gallery5-before-after.png`, `m2-1-solid-gallery-four-projects.png`, `m2-1-deep-cleaning-readable-seo-content.png`.

## SEO content QA

- Old strip text fully inventoried; useful concepts retained naturally; no repeated boilerplate block, micro-text, or hidden keyword content added (see `docs/milestone-2.1-seo-content-map.md`).
- Titles, meta descriptions, canonicals, and H1s verified unchanged against the previous build on all pages **except** the homepage H1 (the owner-directed change). Structured data preserved everywhere; the videos page's VideoObject graph replaced with an accurate, complete one (documented improvement).

## Known notes / judgment calls for the reviewer

1. **`#82` project title (Gallery 5)** — the raw source's #82 write-up has no heading of its own (the text runs straight into the description). The heading "*#82 Mission Hills Staircase Refinishing — Solid Oak Treads & Tile Risers*" was derived from that description; nothing was invented beyond it. The #83 after-photo caption in the raw source was a copy of the before-caption (source typo); the after-image's own alt text was used instead. Both choices are recorded in `projects.json`.
2. **Solid Wood project notes** — each project section's short intro line is composited from the raw source's sourcing lines and the images' own alt-text facts (species, sizes, stains, finishes, locations); the four headings are byte-faithful to the source.
3. **Explore bar over body text** — while scrolling mid-page, the fixed bar necessarily sits over whatever content passes beneath it (currently ~64px tall, centered, dismissible, hides at the footer and over the hero). This is inherent to any fixed bottom bar; the CTA-overlap defect from Milestone 2 is fixed.
4. **`YAHOO is not defined` console error on galleries 3–4** — pre-existing on the committed Milestone 2 pages (verified by loading the HEAD version side by side): a legacy inline Turbify script extracted from the raw source references a library the rebuilt pages never load. Out of scope here; worth cleaning up in a future pass.
5. **Videos-page vcard string** — still passed to `assemble()` (now unused by the chrome). Left in place so the frozen extraction record remains obvious; can be dropped whenever the `__VCARD_DESC__` plumbing is retired.
6. **YouTube snapshot date** — 2026-07-16. New uploads after that date won't appear until someone runs the refresh utility and rebuilds (by design; normal builds are offline/deterministic).

## Files changed (working tree, uncommitted)

**Chrome/shared**: `build/chrome/top.html`, `build/chrome/site_css.html`, `build/chrome/scrollhint_and_toggle.html`, `build/chrome/darkmode_boot_scripts.html`, `build/chrome/footer.html`
**Generators**: `build/scripts/common/build_page.py`, `build/scripts/pages/build_videos.py` (rewritten), `build/scripts/pages/build_gallery5.py` (rewritten), `build/scripts/pages/build_solidwood.py` (rewritten), `build/scripts/pages/build_gallery1.py`, `build/scripts/pages/build_gallery2.py`, `build/scripts/pages/build_about_us.py`, `build/scripts/pages/build_contact_us.py`, `build/scripts/pages/assemble_blog.py`, `build/scripts/pages/assemble_deep_cleaning.py`
**New data**: `build/data/youtube_videos.json`, `build/data/recent_project_gallery_5/projects.json`, `build/data/solid_wood_floor_photo_gallery/projects.json`
**New tooling**: `build/scripts/update_youtube_videos.py`
**Content data**: `build/data/index/main_content.html`
**Regenerated output**: all 12 root `.html` pages (+ `build/data/build_page_results.json`, `build/data/*/assemble_log.txt`, `build/data/blog/case_studies.json`, `build/data/deep-cleaning-hardwood-floors-san-diego/gallery_records.json` — regenerated build byproducts)
**Docs**: `docs/milestone-2.1-seo-content-map.md` (new), this report (new), `build/README.md`, `docs/NEXT_SESSION.md`
