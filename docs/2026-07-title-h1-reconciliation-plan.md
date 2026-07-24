# Title / meta / H1 reconciliation plan + GSC findings (2026-07-24)

**Status: DRAFT — analysis complete, no page content changed yet.** This document
preserves the 2026-07-24 session's live-site pull, the owner's 16-month Google Search
Console export analysis, and the resulting keep-vs-revert recommendation table, so the
work can resume in a later session without re-pulling or re-deriving anything.

Context: the owner reported having "churned" live titles until ranking dropped, and asked
for a data-driven reconciliation between the live Turbify site and the redesign before
launch. The live pull below is the ground truth of what Google currently sees.

## 1. GSC findings (16-month export, ~2025-08-27 → 2026-07-22, Search type: Web)

Owner-supplied CSVs (Pages/Queries/Chart/Devices/Countries), analyzed 2026-07-24.

### 1a. The dominant finding: duplicate-URL split on the live site

Six pages serve identical content at two URLs (extensionless and `.html`), both HTTP 200
with no redirect (verified live 2026-07-24). Google splits them and ranks the
**non-canonical extensionless form far better**:

| Page | Extensionless: pos / impressions / clicks | .html: pos / impressions / clicks |
|---|---|---|
| Gallery 1 | **7.56** / 8,236 / 2 | 35.56 / 4,620 / 26 |
| Gallery 2 | **7.56** / 8,254 / 10 | 24.2 / 1,080 / 6 |
| Gallery 3 | **8.59** / 7,108 / **0 clicks** | 29.57 / 2,142 / 15 |
| Gallery 4 | **7.83** / 4,809 / 2 | 28.37 / 3,713 / 21 |
| Gallery 5 | **8.68** / 4,933 / 17 | 36.87 / 2,816 / 10 |
| Solid Wood | **7.54** / 3,706 / 3 | 44.16 / 4,735 / 24 |

This is what Milestone 3.0's Workers architecture fixes at launch: `.html` serves 200,
extensionless 301s to it, consolidating the split equity into the canonical form.

### 1b. Page-level click share (16 months) — sets reconciliation priority

Homepage **879 clicks (~82% of site)** → Deep-Cleaning 44 → Gallery 1 30 → Solid Wood 27
≈ Gallery 5 27 → Gallery 4 23 → Contact 21 → Gallery 2 16 → Gallery 3 15 → About 13 →
Videos 12 → Blog 8. Everything below the homepage is small; homepage decisions dominate.

### 1c. Query-level evidence

- **Brand**: "san diego hardwoods" — 88 clicks, position 1.74, 31% CTR. Safe.
- **Biggest-impression queries are barely ranking**: "hardwood floor refinishing"
  (3,342 impressions, position 34.5) and "hardwood floor refinishing near me"
  (2,463 impressions, position 56.8) — both homepage-intent per
  `build/data/seo/page_intents.json`, both effectively invisible.
- **Best wording signal**: the query "san diego hardwoods dustless hardwood and bamboo
  floor refinishing installation repairs and deep cleaning" ranks **#1 (pos 1.41, 17%
  CTR)** — nearly verbatim the REDESIGN's homepage H1, not the live one. Evidence favors
  the redesign's homepage direction.
- Several page-1 queries get zero clicks over 1,000+ impressions (e.g. "hardwood
  flooring san diego ca", pos 6.96, 1,223 impressions, 0 clicks) — snippet problem,
  consistent with the duplicate-URL split above.
- Core money queries currently around page 1–2: "hardwood floor refinishing san diego"
  pos 11.1 (29 clicks), "wood floor refinishing san diego" pos 10.0 (20 clicks).

## 2. Live-site pull (2026-07-24, all 12 live pages, via curl + html.parser)

Method: direct HTTP fetch of each live page, stdlib html.parser extraction of
title/meta-description/H1 (no JS, exact byte content). "≠" marks divergence from the
redesign's committed value.

| # | Page | Live title | Live meta description (abridged) | Live H1 |
|---|---|---|---|---|
| 1 | Homepage | ≠ "San Diego Hardwood Floor Refinishing, Installation & Deep Cleaning" | ≠ "San Diego Hardwoods restores, refinishes, deep cleans, recoats and installs hardwood and bamboo floors with 100% dust containment throughout San Diego County" | ≠ "Hardwood and Bamboo Floor Refinishing, Deep Cleaning and Installation in San Diego" |
| 2 | Deep-Cleaning | = (matches redesign) | ≠ "Clean dull or sticky floors fast across San Diego County—La Jolla, Del Mar, Encinitas & more. **Dust-free** deep cleaning restores wood, **vinyl** & bamboo floors. Call 858-699-0072." | ≠ "Hardwood, Engineered Wood and Bamboo Floor Deep Cleaning, Wax and Polish Removal, and Recoating in San Diego" |
| 3 | Gallery 1 | = | ≠ "View real before-and-after… including dustless sanding, repairs and restoration" | ≠ "San Diego Hardwood Floor Refinishing Before-and-After Gallery" |
| 4 | Gallery 2 | = | ≠ | ≠ masthead blob (brand + "Est. 1990…" tagline + heading all in one `<h1>`) |
| 5 | Gallery 3 | ≠ "San Diego Hardwood Floor Refinishing, Repairs & Installation" | = (same text) | ≠ masthead blob |
| 6 | Gallery 4 | ≠ "San Diego Hardwood Flooring Gallery \| Dustless Restoration \| Call 858-699-0072" (phone number in title) | = (same text) | ≠ masthead blob + intro paragraph inside the `<h1>` |
| 7 | Gallery 5 | ≠ "San Diego Hardwood & Bamboo Flooring Project Gallery" | ≠ | ≠ masthead blob |
| 8 | Solid Wood | = | ≠ long meta ending "…Call 858-699-0072 today for your **free estimate**." (banned phrase, Milestone 2.6) | ≠ masthead blob |
| 9 | Videos | = | ≠ "Watch real San Diego hardwood floor refinishing videos featuring 100% dust containment, repairs, restoration, engineered wood refinishing, and Bona finishes" | = |
| 10 | About | = | ≠ (close; live is longer) | text matches; live wraps masthead markup around it |
| 11 | Blog | = | = | ≠ (live: "San Diego Hardwood Flooring Blog, Project Guides and Expert Floor-Care Advice") |
| 12 | Contact | ≠ "Contact San Diego Hardwoods \| **Free assessments** for Hardwood Floor Refinishing, Repairs & Installation" (pre-2.6 wording) | ≠ | ≠ (close) |

Live-site technical defects observed (all already fixed in the redesign):
- Galleries 2–5 + About: entire masthead (brand + tagline + heading) inside ONE `<h1>`.
- Gallery 4 title contains a phone number.
- Deep-Cleaning meta says "Dust-free" and mentions vinyl; Solid Wood meta says "free
  estimate"; Contact title says "Free assessments" — all violate owner decisions
  (claims policy / Milestone 2.6) and appear to be un-reverted live churn.

## 3. Keep-vs-revert recommendation table (drafted 2026-07-24, NOT yet owner-ratified)

Key insight: nearly every "revert" already exists in the redesign — most rows require
**zero code changes**; launching the redesign as-committed IS the reconciliation.

| # | Page | Recommendation | Rationale |
|---|---|---|---|
| 1 | Homepage | **Ship the redesign's title/meta/H1** | 82% of clicks; live churn correlates with the ranking drop; the #1-ranking long query matches the redesign's H1 almost verbatim (§1c). |
| 2 | Deep-Cleaning | Ship redesign (title already =; meta fixes "Dust-free"/vinyl) | Claims-policy compliance + scope accuracy. |
| 3–7 | Galleries 1–5 | Ship redesign; the Milestone 3.0 redirects fix the real problem (§1a) | Low individual click volume; URL consolidation outweighs any wording tweak. |
| 8 | Solid Wood | Ship redesign (meta drops "free estimate") | Milestone 2.6 ban. |
| 9 | Videos | No change needed | Title/H1 already identical; meta difference immaterial. |
| 10 | About | Ship redesign (fixes masthead-H1 markup; same heading text) | Markup fix, not a wording decision. |
| 11 | Blog | No change needed | Title+meta already identical; H1 difference minor — redesign's is fine. |
| 12 | Contact | Ship redesign ("Free Phone & Photo Assessment" title) | Owner's own Milestone 2.6 retitle; live still has pre-2.6 wording. |
| 13 | Assessments (new page) | Ship as committed | No live counterpart, no GSC history. |

**Open owner decisions before this is final:** (a) ratify the homepage call — it is the
only high-stakes row; (b) confirm no attachment to Gallery 3/4/5's live title variants;
(c) after launch, do NOT touch titles for 4–6 weeks — the churn itself was part of the
problem; let Google re-settle, watch GSC weekly.

## 4. Remaining pre-launch sequence (as of 2026-07-24)

1. Owner ratifies §3 (mostly a yes/no on the homepage row).
2. Launch QA gate: Playwright browser pass (desktop+mobile), site-wide `BreadcrumbList`,
   `FlooringContractor` @type validation (Rich Results Test).
3. Production cutover (see `docs/NEXT_SESSION.md` → Milestone 3.0 "Next"): production
   Worker config replaces the CI guard job; owner attaches `www.sdhardwoods.com` and
   flips DNS from Turbify; then resubmit `sitemap.xml` in GSC + request indexing on the
   homepage and top pages. `build/scripts/verify_url_matrix.py` re-runs against
   production (noindex check must then be ABSENT — see the script docstring).
