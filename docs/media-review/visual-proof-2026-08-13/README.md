# Visual Proof captures — Direction 1 "Workshop Billboard" (2026-08-13)

Headless-Chrome captures of the non-production Direction 1 visual-proof build (shared
visual system + homepage only; generator edits uncommitted; other 12 pages not yet
regenerated). Context: `docs/SITE-CONVERSION-REMAKE-MASTER-PLAN.md` decision log
(2026-08-13 entries) and `docs/2026-08-13-direction-1-implementation-plan.md`.

Revision numbering: files prefixed `r2-` are the current revision (revision 2).
Unprefixed files are revision 1 (kept for before/after comparison).

## Current (revision 2)

- `r2-desktop-fold-1440x900.png` — desktop first viewport: enlarged lockup, 46px Palatino
  serif number (tel: link), twin red Call/Text, natural-aspect hero photo top-aligned with H1
- `r2-mobile-fold-360x800.png` — mobile first viewport: lockup, serif number, twin
  full-width buttons, no email, no kicker repeat, nothing clipped
- `r2-gallery-junction-1440.png` — deep-cleaning section → single contact band → gallery
  (duplicate CTA row removed)
- `r2-mobile-herophoto-360.png` — mobile hero photo: cropped to 420px on mobile per owner
  correction (natural-length rendering is desktop-only; see master plan 2026-08-13 owner
  correction entry and the standing rule: desktop and mobile compositions are decided
  separately — never apply a desktop-directed change globally to mobile)
- `r2-homepage-full-clean.png` — full page, single-render method (no stitching artifact);
  order: hero → index strip → Free Assessment → dust containment + video → deep cleaning →
  contact band → 89-photo gallery → contact band → Bona band → gallery nav → specialists →
  assessments → recent projects → footer

## Revision 1 (superseded, kept for comparison)

- `1-desktop-fold-1440x900.png`, `3-mobile-fold-360x800.png` — folds before the
  branding/number enlargement and mobile declutter
- `2-desktop-sticky-1440x900.png`, `4-mobile-sticky-360x800.png` — sticky bars before the
  wide-centered-number rework (sticky bar markup changed only slightly in r2)
- `5-homepage-full-clean.png` — revision-1 full page (same section order as r2; r2's
  differences are the removed duplicate CTA row above the gallery and the uncropped,
  top-aligned hero photo)
- `5-homepage-full-1440.png` — Playwright fullPage capture with the known stitching
  duplication artifact (capture method flaw, not a page defect — see master plan 2026-08-13
  revision-1 entry)
- `5b-dust-video-1440.png` — relocated hero video inside the dust-containment section
- `6a-gallery-wall-1440.png`, `6b-lightbox-desktop-1440.png`, `6c-lightbox-mobile-360.png` —
  larger tiles + lightbox spec (larger view, fullscreen button, #N numbering, outside-click
  close); unchanged by r2

Capture tooling: scratch install outside the repo (`%TEMP%\sdh-proof`, playwright-core +
system Chrome); may be wiped by temp cleanup — recreate per build/README convention if
further captures are needed.
