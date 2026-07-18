# Search Console content-preservation map (Milestone 2.5)

**Date:** 2026-07-18 · **Branch:** `redesign` · **Structured companion:** `build/data/seo/page_intents.json`

This document translates the owner's actual Google Search Console evidence (domain property,
~2025-08-27 through 2026-07-16: ~1,049 clicks / ~143,234 impressions; homepage variants alone
~862 clicks / ~132,190 impressions) into a binding **search-intent ownership map**: which search
themes belong on which page, which wording already earns clicks and must stay visible, which
pages must not compete with each other, and what was (and deliberately was not) changed in
Milestone 2.5. The query themes are an intent map — **not** a paste list; no phrase was
inserted verbatim more than naturally warranted, and no private GSC credentials or account
data are stored anywhere in the repository.

## Search-theme ownership (who owns what)

| Search theme | Owning page | Supporting pages |
|---|---|---|
| San Diego Hardwoods (brand) | Homepage | About |
| hardwood/wood floor refinishing San Diego, floor refinishing near me | **Homepage** | Galleries 1–5, Videos |
| hardwood floor repair San Diego | Homepage | Galleries 1–5 |
| hardwood/wood floor installation San Diego, nail-down/glue-down, unfinished engineered | **Solid Wood Gallery** | Gallery 2, Homepage |
| professional hardwood floor cleaning, wood floor deep cleaning, recoating, maintenance | **Deep-Cleaning page** | Gallery 4, Homepage |
| floor sanding / wood floor sanding San Diego | Homepage + galleries | Videos |
| bamboo/hardwood floor restoration | Gallery 4 | Homepage, Gallery 1 |
| refinishing/sanding **videos** | **Videos page** | — |
| refinishing company / contractors / refinishers (trust) | **About** | Homepage |
| floor assessment / inspection / pre-purchase / written report | **Assessments page** (new, no history) | Contact |
| contact / lead intake | **Contact** | — |

Anti-cannibalization rules enforced this milestone:

- The assessments page keeps assessment/inspection language only; it must never become the
  destination for generic refinishing searches (homepage keeps a short intro + link only).
- The deep-cleaning page does not absorb refinishing intent — instead it now states plainly
  when cleaning is *not* enough and links to the homepage's refinishing service.
- The Milestone 2.4 homepage title (refinishing-led) and the Videos page (video-led) remain
  deliberately split; neither was touched.
- Irrelevant impressions (e.g. a terrazzo query on the cleaning page) were **not** chased.

## Wording that already earns clicks and was preserved untouched

- All 13 titles and meta descriptions (Milestone 2.4 set; zero metadata changes in 2.5).
- All H1s on all 13 pages.
- Every project write-up, gallery module, case study, video, and technical explanation —
  no project, image placement, or long-form section was removed anywhere.
- Gallery 5's unusual filename/canonical; Gallery 3's corrected canonical; the full
  canonical map (re-verified byte-level this milestone).
- Contact's legacy "Free Estimates…" title (Milestone 2.2 decision; retitling would need
  owner sign-off since it has snippet history — body copy carries the accurate
  free-*phone*-assessment framing).
- The deep-cleaning meta description: 2.4 flagged a suspected "Countyâ€”" mojibake; byte
  inspection this milestone shows the committed file contains a **correct UTF-8 em dash** —
  the mojibake was a display artifact in the earlier tooling. Nothing to fix.

## What changed (visible wording), and the search/visitor reason

Full before/after texts: `docs/seo/2026-07-content-alignment-changes.md`. Summary:

1. **Homepage** — four false walnut alt texts corrected from confirmed owner facts
   (Bing Crosby Ranch; see §17 of the operating manual); gallery intro now names
   refinishing/sanding/repair/deep-cleaning/restoration naturally; hero video iframe title
   drops the unsupported "100% dust-free" absolute.
2. **Deep-Cleaning** — hero states "professional hardwood floor cleaning" / "wood floor deep
   cleaning" naturally (its two strongest GSC themes); new "When Cleaning Isn't Enough" card
   links to homepage refinishing; closing links now include Gallery 4 proof and Contact.
3. **Gallery 1** — intro adds deep cleaning + dust-contained floor sanding to the service
   breadth; generic "Learn More →" anchor replaced with a descriptive cleaning anchor.
4. **Gallery 5** — closing navigation now uses descriptive anchors (refinishing home,
   solid/engineered installation gallery).
5. **Solid Wood** — hero leads with "Professional hardwood floor installation in San Diego"
   (its dominant GSC theme) + acclimation/on-site finishing; removed the §12-flagged
   unsupported claims ("far exceeds", "flawless", "exact", "perfectly flat", "100% dust
   containment", "dust-free"); added closing links to homepage refinishing, Gallery 2,
   and Contact.
6. **Videos** — intro adds custom staining + installation to the breadth list; closing links
   to Gallery 1, Deep-Cleaning, and Contact.
7. **About** — adds the owner-confirmed **California contractor license #1017549**;
   "100% Dust Containment Sanding" → "Dust-Contained Sanding on Every Project";
   "same-day replies" → "most replies the same day" (claims policy).
8. **Assessments** — closing section links to the Contact page and to project/video proof.
9. **Galleries 2, 3, 4, Blog, Contact** — no content changes (already aligned; byte-identical
   to Milestone 2.4 output).

## Items still blocked on owner facts

- Stage/angle of each of the four confirmed `TRICIA WALNUT` homepage photos (identity is
  confirmed; stage wording stays provisional).
- The `TRICIA WALNUT27/30/63/76.jpg` filename-vs-white-oak-description conflict on the Solid
  Wood Gallery (flagged in the media inventory; unchanged pending the owner).
- Project facts for ~370 other image placements (media-review workflow,
  `docs/media-review/`).
- Assessment-page report excerpts and practical visit/delivery facts
  (`build/data/assessment/*.json`, all fields `awaiting_owner_input`).
- Official YouTube channel URL (visible `@SANDIEGOHARDWOODS` vs. schema `sameAs` `@SD-1974`
  on the assessments page), GA4 Measurement ID, public street-address decision.
- YouTube title cleanups flagged in the video inventory ("Title:" prefix, "Sold Cherry",
  four duplicate-title pairs) — fixable only on YouTube, then re-snapshot.
