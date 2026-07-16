# SEO strategy discussion & H1/H2/H3 heading audit

**Date:** 2026-07-16
**Status:** Discussion only — no SEO/heading changes have been made. Waiting on a Google Search Console export before any heading-level or meta-description changes are implemented.

## Owner's standing instruction (do not deviate from this without saying so explicitly)

> Once we have Google Search Console exports, use the actual query, page, CTR, impression, and position data to identify opportunities to improve titles, meta descriptions, headings, internal linking, and content while protecting pages that already perform well. Do not recommend SEO changes based solely on generic best practices. Prioritize preserving existing rankings and only recommend changes supported by the current site architecture or future Google Search Console evidence.

This governs every SEO-adjacent decision on this project. Any future recommendation that isn't traceable to (a) something already true about the current site's structure/content, or (b) actual GSC query data, should be flagged as such rather than presented as a settled recommendation.

## Why a GSC export matters — and why now, specifically

The redesign (12 rebuilt pages, currently on the `redesign` branch / Cloudflare preview) has **not gone live** at sdhardwoods.com yet. This is the ideal moment to pull a baseline export, because:

- **Query + Page**, cross-referenced against the heading text on that page, is the only way to know which specific phrases are currently earning impressions — i.e. which headings are load-bearing vs. dead weight. This can't be inferred from the HTML alone.
- **Impressions + CTR + Position together** separates snippet problems from ranking problems: high impressions + low CTR + decent position (page 1) means the *title/meta* isn't competitive for where it already ranks — a CTR fix, not a content/ranking risk.
- **Position trends over time**, and specifically **a pre-launch snapshot**, are the only way to attribute any future ranking movement to this redesign specifically, versus an unrelated Google algorithm update or normal seasonality. Once the redesign ships, that baseline is gone — get the export before launch, not after.

**Recommended export:** Search Console → Performance report → Query, Page, Clicks, Impressions, CTR, Position — filtered per page if possible, full available history (GSC retains ~16 months).

## What a GSC export would let us do next

1. Cross-reference query data against the three pages flagged below (about_us, blog, solid_wood_floor_photo_gallery) to check whether any of the ~35 demoted-heading phrases are actually driving impressions/clicks. If none are, the demotion is very likely a non-issue. If a few are, the fix is narrow: promote those specific headings back to H2, not a wholesale reversal.
2. Identify high-impression/low-CTR pages as meta-description rewrite candidates (see below — this is separate from the "missing entirely" category, which doesn't need data to justify).
3. Identify any page with declining position trends pre-redesign, which would deserve extra caution/monitoring post-launch regardless of what we touch.

## Meta descriptions — two categories, only one is risk-free right now

**Category A — already has a written meta description** (confirmed present on the legacy site): home, gallery_1, gallery_2, gallery_3, deep-cleaning, solid_wood.
→ **Hold.** Don't touch until GSC data shows whether the existing snippet is underperforming (high impressions, low CTR) for a page that's otherwise ranking. Rewriting a snippet that's already working, without data, is exactly the generic-best-practice risk the owner ruled out.

**Category B — no meta description exists at all** (confirmed missing on the legacy source, not something the redesign removed): about_us, contact_us, videos_of_refinishing_process, blog, recent_project_photo_gallery_4, recent_project_gallery_5.
→ **Lower-risk regardless of GSC data**, since meta description isn't a ranking factor itself (only a CTR/snippet factor), and there's no existing snippet performance to protect on these six pages — Google is either auto-generating a snippet or showing nothing consistent. Still deferred pending owner's go-ahead per "discuss, don't code yet," but this category doesn't need to wait on the GSC export the way Category A does.

## Heading audit methodology

Extracted every `<h1>`, `<h2>`, `<h3>` — tag and full text content — from both:
- **Legacy source**: `build/raw-source/*.html` (frozen snapshot of the live Turbify site pre-redesign)
- **Redesign**: the 12 committed pages at the repo root

using a DOTALL-aware regex (not line-based `grep`, which produced a false "zero H1" reading on several pages during initial recon — corrected before this report; documenting the correction here so it isn't independently rediscovered as a "finding" next session).

## Per-page heading counts: legacy vs. redesign

| Page | Legacy H1/H2/H3 | New H1/H2/H3 | Note |
|---|---|---|---|
| index (home) | 1 / 4 / 7 | 1 / 5 / 10 | Stable |
| about_us | 1 / **11** / 9 | 1 / **1** / 8 | Large H2→H3 demotion — see detail below |
| contact_us | 1 / 1 / 2 | 1 / 1 / 4 | Stable |
| videos_of_refinishing_process | 1 / 3 / 14 | 1 / 2 / 14 | Stable |
| recent_project_photo_gallery_1 | 1 / 2 / 22 | 1 / 1 / 22 | Minor |
| recent_project_photo_gallery_2 | 1 / 2 / 23 | 1 / 1 / 22 | Minor |
| recent_project_photo_gallery_3 | 1 / 2 / 12 | 1 / 1 / 12 | Minor |
| recent_project_photo_gallery_4 | 1 / 1 / 21 | 1 / 1 / 22 | Stable |
| recent_project_gallery_5 | 1 / 1 / 6 | 1 / 1 / 6 | Stable |
| solid_wood_floor_photo_gallery | 1 / **8** / 6 | 1 / **3** / 4 | H2→H3 demotion — see detail below |
| deep-cleaning-hardwood-floors-san-diego | 1 / 1 / 20 | 1 / 2 / 20 | Stable |
| blog | 1 / **19** / 20 | 1 / **4** / 23 | Largest H2→H3 demotion — see detail below |

## H1 text: preserved everywhere

On 9 of 12 legacy pages, the H1 actually read `"SAN DIEGO HARDWOODS Est. 1990 • San Diego's Finest Hardwood Flooring Specialist [the real page-specific title]"` — brand name and tagline were concatenated into the H1 alongside the real heading (a markup habit, not a deliberate SEO choice — the same brand/tagline text already appears in the visible header on every page). The redesign strips that repeated prefix; **the page-specific portion is preserved word-for-word identical on every single page.** Example (about_us):

- Legacy: `SAN DIEGO HARDWOODS Est. 1990 • San Diego's Finest Hardwood Flooring Specialist About San Diego Hardwoods — Trusted Hardwood Floor Refinishing, Installation, Restoration & Deep Cleaning Experts Serving San Diego Since 1990`
- New: `About San Diego Hardwoods — Trusted Hardwood Floor Refinishing, Installation, Restoration & Deep Cleaning Experts Serving San Diego Since 1990`

This is the least risky of all the heading changes: the distinctive/topical text is unchanged; what's removed is sitewide brand-name repetition.

## The three pages with real structural change: what got demoted

### about_us: 11 legacy H2s → 1

Legacy H2s included: `CALL OR TEXT TODAY FOR HARDWOOD FLOOR ADVICE`, `858-699-0072` (the phone number itself was wrapped in its own H2 — a visual-styling artifact, not a content heading), `Our Story`, `Bringing Traditional Craftsmanship to San Diego`, `Modern Equipment. Traditional Craftsmanship.`, `Professional Credentials`, `Specialty Hardwood Flooring Services`, `Why Homeowners Choose San Diego Hardwoods`, `Let's Discuss Your Hardwood Flooring Project`, plus the page's real H2 title and the footer boilerplate.

In the redesign, all of these except the phone number and CTA text (dropped as non-content) became H3s nested under one real H2 (`About San Diego Hardwoods – 35+ Years of Dustless Refinishing & Installation Expertise`).

### blog: 19 legacy H2s → 4

Legacy H2s included several individual case-study titles as their own H2: `# 1 Coronado Hardwood Floor Restoration / Refinishing`, `# 2 Rancho Santa Fe San Diego Hickory Hardwood Floor Refinishing, Installation, and Butcher Block Restoration`, `# 4 San Diego Hardwood Floor Repair and Refinishing After Termite Damage`, `#6 Seasonal Shrinkage of Hardwood Floors in Coastal and Inland San Diego`, `#7 Restoring Factory Distressed and Hand Scraped Hardwood Floors in San Diego`, `# 8 Solid Oak Flooring Refinishing in San Diego`, plus section headings (`Why Homeowners Choose San Diego Hardwoods`, `Our Hardwood Floor Refinishing & Installation Process`, `Benefits of Professional Hardwood Floor Refinishing`, `Serving Homeowners Throughout San Diego County`, `Request Your Free Hardwood Flooring Consultation`).

In the redesign, all individual case studies became H3s grouped under one H2 (`Hardwood Flooring Case Studies & Project Stories`). This is the largest single structural change on the site.

### solid_wood_floor_photo_gallery: 8 legacy H2s → 3

Similar pattern at smaller scale — several per-project or per-section headings consolidated under fewer top-level H2s.

## Direct answers to the owner's six review questions

**Does every page have one clear H1?**
Yes — every one of the 12 pages had exactly one H1 on the legacy site, and has exactly one now. Never at risk, didn't change.

**Are H2s organized logically?**
Yes, in the redesign — H2 now consistently marks one real section boundary per page, a clean, human-readable outline. This is a genuine improvement over the legacy markup, which used H2 for nearly every visual block regardless of hierarchy (including, on about_us, wrapping a bare phone number in `<h2>` tags).

**Are H3s subordinate to H2s?**
Yes, structurally, consistently, in the redesign — no orphaned headings, no level-skipping (no H1 → H3 without an intervening H2). Not reliably true in the legacy markup.

**Are headings written for humans first?**
Mixed, and pre-existing rather than introduced by the redesign: section-level headings read naturally, but most of the heading *volume* on 8 of 12 pages is individual gallery-project titles, several of which are full run-on descriptive paragraphs mistagged as headings (example, gallery_3: *"#41 Solid red oak strip flooring in a grand Solana Beach estate on the edge of Rancho Santa Fe, carefully restored to its natural color. The first photo shows the floor sanded down to raw wood mid-process..."* as the entire H3). Preserved verbatim per the instruction not to rewrite marketing copy — flagged as a future content opportunity (split into a short heading + separate body text), not an urgent fix, and not to be touched without explicit sign-off since it's copy, not structure.

**Would changing them risk existing rankings?**
Text is unchanged everywhere (verified directly, not assumed) — minimal risk from a keyword-presence standpoint. The real open question is the H2→H3 demotions on the three pages above: heading level is a legitimate, if minor, Google relevance signal, and roughly 35 individual headings across those three pages moved from "major section" to "subsection" weight. This is the one place "probably fine" isn't the same as "verified fine."

**Which headings should remain untouched because they already rank?**
Cannot be answered from the HTML alone — this is the literal purpose of the GSC export described above. Next step once the export exists: check whether any of the ~35 demoted headings' phrasing shows up as a query this site already gets impressions or clicks for, on those three specific pages. Restore only the ones that do.
