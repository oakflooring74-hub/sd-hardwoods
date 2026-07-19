# Milestone 2.6 — Public business rules, assessment conversion, YouTube metadata, GA4

Date: 2026-07-18. Branch: `redesign`. Starting commit: `42e1d8f` (Milestone 2.5).
Durable decisions recorded in `docs/PROJECT_DECISIONS.md` ("Public-business rules").

## What was implemented

### 1. Service-area business — no published street address
- New build-time filter `build/scripts/common/public_business_rules.py`
  (`sanitize_public_jsonld`) runs on every page's JSON-LD in all four assembly paths
  (`assemble_page.py`, `build_page.py`, `assemble_deep_cleaning.py`, `assemble_blog.py`).
  It removes `address` (PostalAddress), `streetAddress`, `geo`, and `hasMap` (the legacy
  values embedded the street address / pinpointed it as coordinates), normalizes YouTube
  channel URLs, and hard-fails the build if any banned value survives.
- Before: homepage + deep-cleaning JSON-LD published `11772 Carmel Creek Rd` (+geo,
  +hasMap); seven other pages carried empty-street `PostalAddress` blocks. After: zero
  `PostalAddress`/`streetAddress` in generated output.
- Approved wording added: footer line on all 13 pages now reads
  **"Based in Carmel Valley, San Diego 92130 • CSLB-Licensed California Flooring
  Contractor"**; Contact lede updated from "Based in San Diego (92130)".
- Left intentionally unchanged (frozen/historical): `build/raw-source/*.html` snapshots
  (street address in index + deep-cleaning + contact vcard data) and 2.5-era data
  extractions not read by any build (`data/contact_us/tail_raw.html`,
  `data/videos_of_refinishing_process/head_meta.html`, `jsonld_as_broken_on_live_site.html`,
  `data/*/jsonld.html` — these last ARE read but are sanitized at build time).

### 2. No published contractor license number
- Removed from About's "Professional Credentials" card (`build_about_us.py`) — the only
  generated-output occurrence. Generic "CSLB-licensed, bonded and insured California
  flooring contractor" wording retained.
- Operational docs updated: `PROJECT_OPERATING_MANUAL.md` §1,
  `build/data/seo/page_intents.json` (About record),
  `docs/seo/search-console-content-preservation-map.md`, `PROJECT_DECISIONS.md`.
- Left intentionally unchanged (historical records only): the exact number remains in the
  dated Milestone 2.5 logs `docs/seo/2026-07-content-alignment-changes.md` and
  `docs/NEXT_SESSION.md`'s 2.5 history section — both describe what 2.5 did, not what to
  publish. The build-time filter also asserts the number never re-enters generated schema.

### 3. Official YouTube channel `@sandiegohardwoods`
- Normalized in: `chrome/top.html` (desktop nav, YouTube pill, drawer ×4), homepage
  `main_content.html`, `build_floor_assessments.py` schema `sameAs`,
  `update_youtube_videos.py` (docstring, `CHANNEL`, snapshot `_comment`),
  `youtube_videos.json` (`channel_url`), and via the build-time filter every legacy
  `@SD-1974` / `@SANDIEGOHARDWOODS` occurrence in raw-source-extracted JSON-LD
  (homepage ×2, contact, about, galleries 2–5, videos).
- Generated output now contains only `youtube.com/@sandiegohardwoods` (verified, 13 pages).

### 4. "Free estimates" replaced by the Free Phone & Photo Assessment
- Contact `<title>` retitled (owner-approved): "Contact San Diego Hardwoods | Free Phone &
  Photo Assessment" — the only title/H1/description change in this milestone (verified by
  a scripted parity check of all 13 pages vs HEAD).
- Homepage image #49 alt: minimal phrase swap "with free estimates" → "with a free phone
  and photo assessment" (no other alt text touched; media inventory regenerated).
- Contact hierarchy applied at the primary contact surfaces (chrome masthead CTA + drawer
  note, footer action row, homepage hero + "Start With a Free Phone & Photo Assessment"
  steps + closing CTA, Contact hero + numbered cards (Text → Call → Email → Response
  Time), About + Videos CTAs, assessments hero/free-card/get-started): texting photos
  first, calling clearly welcomed, email third, with the approved supporting language.
- Generated output contains zero case-insensitive "free estimate(s)" (verified).

### 5. Floor Assessments & Inspections page
- Each service card now leads with the owner's confirmed one-sentence service description
  ($95 / $350 / $750 / Complex "Starting at $1,500"); prices, boundaries, fine-print
  limitations, and the exact fee-credit sentence preserved byte-for-byte.
- Free assessment card leads with the confirmed description + "a paid visit is never a
  requirement for getting an initial answer".
- New section `#what-an-evaluation-clarifies` — "What a Professional Evaluation Can
  Clarify": clearly labeled illustrative report-style examples (Existing Condition /
  Probable Cause / Feasibility or Limitations / Recommended Next Step), with the explicit
  disclaimer that they are not excerpts from actual client reports and not a promise of
  testing/measurements/photos/written documentation.
- The concise pre-purchase example sentence added to the pre-purchase lede.
- Consolidated exclusion line: no automatic engineering, laboratory analysis, real-estate
  appraisal, legal opinions, insurance coverage decisions, destructive testing, testimony,
  or expert-witness services.

### 6. YouTube titles
- `update_youtube_videos.py` was run against the live channel (2026-07-18): all 58 records
  returned **byte-identical titles/dates/descriptions** — the snapshot already matches the
  live channel. Only the snapshot header changed (official handle, snapshot_date).
- Consequences: "Sold Cherry …" and the "Title:" prefix are the *actual live titles*, so
  per the owner's rule (correct only from the live channel) they are preserved; fix them
  on YouTube, then re-run the refresh. No live title is blank or date-only, so no
  `site_display_title` values were needed yet.
- Mechanism added for when they are: `site_display_title` is now a curated field preserved
  across refreshes and used by `build_videos.py` (cards, aria-labels, VideoObject names)
  with the restrained "Initial Hardwood Floor Sanding — Project Video" fallback pattern,
  disambiguated by upload date — no invented locations/species/finishes/stages.

### 7. GA4
- One shared implementation: `build/chrome/analytics.html` (ID `G-L9RDVK6H9W`), injected
  into the head of all 13 pages by the four assembly paths. Maintenance documented in
  `build/README.md` → "Analytics".
- Production-host gate: script returns before creating the gtag loader unless hostname is
  `www.sdhardwoods.com`/`sdhardwoods.com` → zero Analytics network requests from
  localhost/previews.
- Events (params: `link_url`, `link_text`, `page_slug` only): `phone_call_click`,
  `text_message_click`, `email_click`, `assessment_cta_click`,
  `assessment_page_link_click`. No Universal Analytics anywhere.

## QA evidence (all from actual tool runs, 2026-07-18)

- **Build:** `build_all.py` run twice → all 13 pages + sitemap.xml + robots.txt
  **byte-identical** (SHA-256 compared).
- **Static gate (scripted, all 13 pages):** no `1017549`; no `streetAddress` /
  `PostalAddress` / `11772` / `Carmel Creek`; no case-insensitive `free estimate(s)`; no
  `@SD-1974` / uppercase `@SANDIEGOHARDWOODS`; no `_gaq`/`ga.js`/`UA-20793161`; exactly one
  `G-L9RDVK6H9W` and one gtag loader per page; every JSON-LD block strict-parses; all
  internal links resolve; "Based in Carmel Valley, San Diego 92130" on all 13 pages;
  title/description/canonical/H1 parity vs HEAD — only the Contact title differs.
- **Media inventory:** regenerated; validator: **0 errors, 4 warnings** (the deliberate
  `TRICIA WALNUT27/30/63/76` conflict, unchanged and out of scope).
- **`git diff --check`:** clean.
- **Browser QA (Playwright/Chromium 149, real pages): 98/98 passed.** All 13 pages ×
  desktop (1280×900) + mobile (390×844): no horizontal overflow, no console errors (the
  pre-existing `YAHOO is not defined` on galleries 3/4 and Chromium's YouTube-iframe
  `compute-pressure` notice excluded as known/out-of-scope), **zero
  googletagmanager/google-analytics requests on a non-production host**. Production-host
  simulation (`www.sdhardwoods.com` routed to local files): gtag loader requested with the
  correct ID, config queued, and real clicks produced `phone_call_click`,
  `text_message_click`, `email_click`, `assessment_page_link_click`,
  `assessment_cta_click` with exactly the `link_url`/`link_text`/`page_slug` param shape.
- **Visual:** `qa-screenshots/m26-*.png` (assessments desktop+mobile, contact
  desktop+mobile, homepage desktop) — examples section, hierarchy, and footer wording
  inspected.

## Intentionally out of scope / unchanged
90 homepage image descriptions (beyond the single #49 phrase), page-by-page media-fact
review, walnut identity conflicts, `YAHOO is not defined` cleanup, canonical URLs,
redirects, unrelated titles/H1s/descriptions, `build/raw-source/`, `build/archive/`,
Git history.
