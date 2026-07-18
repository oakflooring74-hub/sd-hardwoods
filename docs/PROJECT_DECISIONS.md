# PROJECT DECISIONS — binding record

Created 2026-07-18 (Milestone 2.5) per `docs/PROJECT_OPERATING_MANUAL.md` §29/§42.
Record binding decisions here; do not rewrite the operating manual itself.

## Canonical URL map (Milestone 2.4, verified 2.5)

The 13-page map in `docs/2026-07-milestone-2.4-technical-seo.md` and
`build/scripts/common/build_sitemap.py` (`CANONICAL_URLS`) is binding. Highlights:
12 legacy pages keep `.html` canonicals; the new assessments page is intentionally
extensionless (`https://www.sdhardwoods.com/floor-assessments-inspections`); Gallery 5 keeps
its unusual `recent_project_gallery_5.html` filename; Gallery 3's canonical is the corrected
`recent_project_photo_gallery_3.html`. Milestone 2.4 final commit: `1ecff4e63e0c5395c4f0382e22f72fbb6addf743`.

## Business positioning & assessment architecture (Milestones 2.2–2.3)

- Free Phone & Photo Assessment → $95 In-Home Project Assessment → $350 Pre-Purchase Verbal
  Inspection → $750 Pre-Purchase Inspection with Written Documentation → Complex Damage,
  Dispute & Insurance Analysis from $1,500.
- Exact fee-credit sentence (do not alter): "Some or all of the inspection and report fee may
  be credited toward the approved flooring project under written agreement."
- Contact page stays low-friction lead intake; never carries the full pricing table.
  Its legacy "Free Estimates" SEO title is deliberately preserved (Milestone 2.2 decision);
  retitling requires owner sign-off.
- No automatic litigation/testimony/engineering/lab/legal/appraisal implications anywhere.

## Design lock (Milestones 2–2.3)

Masthead/nav/drawer/mini-header, dark-default theme system, typography, service cards,
gallery structure, lightbox, and assessment-page architecture are approved. No open-ended
visual redesign without an owner-authorized milestone.

## Media-fact policy (Milestone 2.5)

- Structured inventory is permanent: `build/data/media/assets.json` +
  `build/data/media/placements/*.json`; owner facts enter ONLY via
  `build/data/media/owner_facts_confirmed.json` or reviewed placement-file edits.
- Stable IDs (`HOME-IMG-001`, `G1-…`, `VIDEOS-VID-…`) are the owner's reference vocabulary.
- Nothing is auto-published from the inventory; approval workflow in
  `docs/media-review/README.md`. Never invent species/location/stage/finish/damage facts.
- Confirmed 2026-07-18: `TRICIA WALNUT102/110/54/23.jpg` = one walnut refinishing project at
  Bing Crosby Ranch, San Diego (stage/angle per photo still unconfirmed). False homepage
  identities removed.
- Flagged, unresolved: `TRICIA WALNUT27/30/63/76.jpg` filename vs. white-oak installation
  description on the Solid Wood Gallery.

## Claims policy enforcement (Milestone 2.5)

"Dust-contained" (never "100%"/"dust-free"), no "flawless"/"perfect"/"far exceeds"/"exact
match", qualified response-time claims. License number 1017549 is published on About.

## Standing blockers (owner input required)

1. GA4 Measurement ID (no analytics until supplied; never invent one).
2. Public street-address / NAP decision.
3. Official YouTube channel URL (`@SANDIEGOHARDWOODS` visible vs. `@SD-1974` in
   assessments-page schema `sameAs`).
4. Image/video owner facts (media-review workflow).
5. Assessment visit durations, report-delivery ranges, preparation/access expectations
   (`build/data/assessment/practical_service_facts.json`).
6. Anonymized report excerpts (`build/data/assessment/report_examples.json`).
7. YouTube title cleanups ("Title:" prefix, "Sold Cherry", duplicate titles) — fix on
   YouTube, then rerun `update_youtube_videos.py`.

## Deployment / launch

Push to `redesign` auto-deploys the Cloudflare **preview** only. `master` = production; never
merge or push without explicit owner instruction. Production Turbify site untouched until the
owner-controlled launch milestone.
