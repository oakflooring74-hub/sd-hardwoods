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
  ~~Its legacy "Free Estimates" SEO title is deliberately preserved~~ — superseded 2026-07-18
  (Milestone 2.6): the owner signed off on retitling to
  "Contact San Diego Hardwoods | Free Phone & Photo Assessment" (see below).
- No automatic litigation/testimony/engineering/lab/legal/appraisal implications anywhere.

## Public-business rules (Milestone 2.6, 2026-07-18) — DURABLE OWNER DECISIONS

1. **Service-area business — no published street address.** San Diego Hardwoods does not
   publish a street or mailing address anywhere in public output: no `streetAddress`, no
   public `PostalAddress` schema, no wording implying customers visit a storefront. (The
   legacy schema's `geo` coordinates and street-address `hasMap` link are removed under the
   same rule.) Approved public wording: **"Based in Carmel Valley, San Diego 92130"**
   (consistent with the Google Business Profile). Accurate San Diego County service-area
   wording stays. Never invent a street address. Frozen `build/raw-source/` snapshots and
   dated historical reports keep their legacy address data; the build-time filter
   `build/scripts/common/public_business_rules.py` strips it from every generated page.
2. **No published contractor license number.** The exact CSLB license number must not appear
   in generated pages, structured data, active metadata, active generator content, or
   current operational documentation. Generic truthful wording is approved: "Licensed
   California flooring contractor", "Licensed, bonded and insured", "CSLB-licensed".
   (Occurrences in frozen raw-source and dated 2.5-era historical records remain as
   history only.)
3. **Official YouTube channel:** `https://www.youtube.com/@sandiegohardwoods` — used in
   navigation, footer/drawer, structured data (`sameAs`), video data, outbound links, and
   docs. The `@SD-1974` handle and uppercase `@SANDIEGOHARDWOODS` variant are retired;
   the build-time filter normalizes any legacy schema occurrence.
4. **"Free estimate(s)" is banned from public output** (any capitalization). The approved
   entry service is the **Free Phone & Photo Assessment**, presented with the contact
   hierarchy: 1) Text Photos for a Free Assessment, 2) Call to Discuss Your Floor,
   3) Email Photos. Texting photos is preferred; visitors must clearly feel welcome to
   call; never imply every inquiry requires a paid visit.
5. **GA4:** Measurement ID `G-L9RDVK6H9W`, implemented once in
   `build/chrome/analytics.html` (see build/README.md "Analytics"). Transmits ONLY on
   `www.sdhardwoods.com` / `sdhardwoods.com`; localhost and `*.pages.dev` previews make no
   Analytics network requests. Conversion events: `phone_call_click`,
   `text_message_click`, `email_click`, `assessment_cta_click`,
   `assessment_page_link_click`. No message/photo/visitor-entered contents are collected.
6. **YouTube titles:** live-channel titles are authoritative and preserved. Where a live
   title is blank or date-only, curated `site_display_title` (preserved across snapshot
   refreshes) supplies a restrained display title ("Initial Hardwood Floor Sanding —
   Project Video", disambiguated by upload date); the owner confirms date-only videos show
   the initial sanding stage. As of the 2026-07-18 live verification no blank/date-only
   titles exist; "Sold Cherry" and the "Title:" prefix are still the actual live titles —
   correct them on YouTube, then re-run `update_youtube_videos.py`.

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
match", qualified response-time claims. ~~License number is published on About~~ —
superseded by Milestone 2.6 rule 2 above: the exact number is NOT published anywhere.

## Standing blockers (owner input required)

1. ~~GA4 Measurement ID~~ — resolved Milestone 2.6 (`G-L9RDVK6H9W`, shared implementation).
2. ~~Public street-address / NAP decision~~ — resolved Milestone 2.6 (service-area
   business; "Based in Carmel Valley, San Diego 92130").
3. ~~Official YouTube channel URL~~ — resolved Milestone 2.6
   (`https://www.youtube.com/@sandiegohardwoods`).
4. Image/video owner facts (media-review workflow) — including the unresolved
   `TRICIA WALNUT27/30/63/76` filename-vs-white-oak conflict (deliberately unchanged).
5. Assessment visit durations, report-delivery ranges, preparation/access expectations
   (`build/data/assessment/practical_service_facts.json`).
6. Anonymized report excerpts (`build/data/assessment/report_examples.json`) — the
   Milestone 2.6 "What a Professional Evaluation Can Clarify" section uses clearly labeled
   illustrative examples in the meantime.
7. YouTube title cleanups ("Title:" prefix, "Sold Cherry", duplicate titles) — verified
   still live 2026-07-18; fix on YouTube, then rerun `update_youtube_videos.py`.

## Deployment / launch

Push to `redesign` auto-deploys the Cloudflare **preview** only. `master` = production; never
merge or push without explicit owner instruction. Production Turbify site untouched until the
owner-controlled launch milestone.
