# Milestone 2.4 — Technical SEO foundation (canonicals, sitemap, robots, contact links)

**Date:** 2026-07-18
**Branch:** `redesign` (production and `master` untouched)
**Scope:** generator-level technical cleanup only — no visual redesign, no content rewrites, no
image/alt/project changes, no CMS/framework/dependency additions, no redirects created.

## The approved canonical URL map (authoritative)

| # | Page (repo file) | Canonical URL |
|---|---|---|
| 1 | `index.html` | `https://www.sdhardwoods.com/` |
| 2 | `deep-cleaning-hardwood-floors-san-diego.html` | `https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html` |
| 3 | `recent_project_photo_gallery_1.html` | `https://www.sdhardwoods.com/recent_project_photo_gallery_1.html` |
| 4 | `recent_project_photo_gallery_2.html` | `https://www.sdhardwoods.com/recent_project_photo_gallery_2.html` |
| 5 | `recent_project_photo_gallery_3.html` | `https://www.sdhardwoods.com/recent_project_photo_gallery_3.html` |
| 6 | `recent_project_photo_gallery_4.html` | `https://www.sdhardwoods.com/recent_project_photo_gallery_4.html` |
| 7 | `recent_project_gallery_5.html` | `https://www.sdhardwoods.com/recent_project_gallery_5.html` |
| 8 | `solid_wood_floor_photo_gallery.html` | `https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html` |
| 9 | `videos_of_refinishing_process.html` | `https://www.sdhardwoods.com/videos_of_refinishing_process.html` |
| 10 | `about_us.html` | `https://www.sdhardwoods.com/about_us.html` |
| 11 | `blog.html` | `https://www.sdhardwoods.com/blog.html` |
| 12 | `contact_us.html` | `https://www.sdhardwoods.com/contact_us.html` |
| 13 | `floor-assessments-inspections.html` | `https://www.sdhardwoods.com/floor-assessments-inspections` *(intentionally extensionless — new page, Milestone 2.3)* |

This map is encoded in `build/scripts/common/build_sitemap.py` (`CANONICAL_URLS`). Internal
navigation (desktop nav, mobile drawer, mini-header, explore bar, footer, homepage gallery
tiles/service links, gallery prev/next, contact/assessment links, videos-page gallery
cross-links) now uses exactly these URLs. Before this milestone most nav links used
extensionless variants (`/about_us`, `/recent_project_photo_gallery_1`, …).

## Live URL behavior measured on 2026-07-18 (Turbify production site)

Tested with HEAD/GET requests, redirects not followed:

- `/`, all 12 `.html` canonical URLs → **200** directly.
- `/about_us`, `/blog` (extensionless) → **301** to the `.html` URL.
- `/contact_us`, `/videos_of_refinishing_process`, `/recent_project_photo_gallery_1`–`_4`,
  `/recent_project_gallery_5`, `/solid_wood_floor_photo_gallery` (extensionless) → **200**,
  but serving **byte-identical content** to the `.html` URL, whose own embedded canonical
  points at the `.html` version (verified for contact_us, gallery_1, videos by content-length
  + title + canonical comparison). **No conflicting independent pages exist**, so applying the
  `.html` canonical map is safe.
- `/recent_project_gallery_3.html` (the *wrong* URL that Gallery 3's old canonical pointed to)
  → **301** to `/recent_project_photo_gallery_3.html`. The defect was a self-inflicted
  canonical-to-redirect; corrected at the generator level (see below).
- `/floor-assessments-inspections` → **404 on Turbify production** (expected — the page is new
  in the redesign and only exists on the Cloudflare preview / future production deploy).

No redirects were created in this milestone (explicitly out of scope).

## What changed, per requirement

1. **Canonicals** — every one of the 13 pages now emits exactly one `<link rel="canonical">`
   matching the map. Six pages previously had none (about_us, contact_us, gallery_1,
   gallery_2, gallery_5, videos); Gallery 3's was wrong (`recent_project_gallery_3.html`,
   inherited from the live raw source — the raw snapshot itself carries the bad value).
   `build/scripts/common/build_page.py` now takes the canonical from its `CONFIGS` map instead
   of extracting it from raw source.
2. **Viewport** — `<meta name="viewport" content="width=device-width, initial-scale=1">` added
   exactly once per page: in `common/assemble_page.py` (10 pages), `common/build_page.py`
   (galleries 3–4), and the two standalone assemblers (`assemble_deep_cleaning.py`,
   `assemble_blog.py`). No page had any viewport tag before.
3. **Homepage title/description** — title replaced (was the videos-centric
   "…Dustless Sanding Videos…") with `Hardwood Floor Refinishing San Diego | San Diego
   Hardwoods` + the approved owner-operated meta description, set in `build_homepage.py`
   (no longer taken from raw source). Body/H1 untouched.
4. **Missing meta descriptions added** (approved copy, only where none existed): gallery_5,
   solid_wood, videos, about_us, contact_us. Pages that already had descriptions
   (galleries 1–4, blog, deep-cleaning, floor-assessments) were left untouched.
5. **Contact actions** — no `tel:` link anywhere carries texting language any more. Calls are
   `tel:+18586990072` labeled "Call …"; texting is a separate `sms:+18586990072` action
   labeled "Text Floor Photos"; email uses `mailto:sandiegohardwoods@gmail.com`. Applied in
   the masthead (which gained a Text Floor Photos link), mobile nav-band call button,
   mini-header, drawer, footer (now Call | Text | email), every page CTA row, contact cards,
   and gallery closing CTAs. All `tel:` URIs normalized from `tel:8586990072`/
   `tel:858-699-0072`; the sms prefilled `?&body=…` payloads (malformed URI form) were dropped
   in favor of the plain spec URI.
6. **Analytics** — the legacy Universal Analytics snippet (`UA-20793161-1`, `_gaq`, `ga.js`)
   is removed from every build script and no longer appears in any generated page.
   **GA4 remains blocked: do not add analytics until the owner supplies a real GA4
   Measurement ID.** No placeholder was invented.
7. **Sitemap** — `sitemap.xml` is now generated by `build/scripts/common/build_sitemap.py`
   (registered as the final `build_all.py` step). Exactly the 13 canonical URLs, one `<url>`
   each, no `lastmod` (no truthful per-page source for it exists — deliberately omitted rather
   than invented), no `changefreq`/`priority`. Previously it was a hand-maintained 3-URL file
   with invented dates.
8. **robots.txt** — did not exist; now generated by the same script at the repo root:
   allow-all + `Sitemap: https://www.sdhardwoods.com/sitemap.xml`. No crawl-delay, no blocks,
   no noindex. Verified no generated page contains any robots noindex directive.
9. **Videos-page gallery cross-links** — the curated `gallery_href` fields in
   `build/data/youtube_videos.json` updated to the `.html` canonical URLs (9 records were
   extensionless).

## Base-href decision: kept

`<base href="https://www.sdhardwoods.com/">` stays on every page. Dependency audit:

- **Project images** (`/LARK56.jpg`, gallery photos, `/images/thumbnails/…`) — root-relative
  `src`/`href` resolved against the base → still served live from Turbify hosting. Removing
  the base would 404 every photo on the Cloudflare preview.
- **Favicons/logo** — absolute URLs, unaffected.
- **`/floor-assessments-inspections` root-relative links** — resolve via base to the
  production URL (consistent with the absolute-URL nav convention).
- **Brand images** — deliberately bypass the base via the `data-brand-src` +
  `location.origin` resolver (see `top.html`).
- Safe removal would require migrating all images off Turbify first (the long-standing
  deferred item). Not attempted; explicitly out of scope of this milestone.

## Follow-ups / notes for the content-review milestone (not done here, by design)

- Deep-cleaning meta description contains a mojibake em-dash ("Countyâ€”") inherited from the
  raw-source extraction; it ships as-is because existing descriptions were off-limits this
  milestone. Fix during the content milestone (needs GSC data per the SEO audit doc).
- Existing descriptions on galleries 1–3 are long/keyword-heavy; recorded for the later
  content review, not rewritten.
- `verify_gallery5.py` (ad-hoc helper, not part of `build_all.py`) still *expects* `_gaq` to
  be present when comparing against raw source; harmless, but update it if it is ever used again.
- Repo-root `script.js`/`styles.css` are leftovers from the prior rebuild attempt on `master`;
  no generated page references them. Left untouched.

## GA4 blocker (unchanged)

GA4 installation is **blocked pending the owner's confirmed Measurement ID**. When supplied,
add the gtag snippet to the shared head generation (`assemble_page.py` + `build_page.py` +
the two standalone assemblers) so all 13 pages get it in one change.
