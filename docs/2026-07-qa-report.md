# Visual & Responsive QA Report — redesign branch

**Date:** 2026-07-16
**Tested against:** https://redesign.sd-hardwoods.pages.dev (Cloudflare Pages preview of the `redesign` branch)
**Method:** Real headless Chromium (Playwright) across all 12 pages at 4 viewports (1920×1080 desktop, 1440×900 laptop, 768×1024 tablet, 390×844 mobile) — DOM measurements (horizontal overflow, touch-target sizes, computed font sizes, gallery image display-vs-natural dimensions) plus visual screenshots and a live click-through test. No code was changed while producing this report.

This is a point-in-time report. If the site changes before the fixes below are implemented, re-run the QA sweep rather than trusting these numbers blindly — see `build/README.md` for how the site is regenerated, and re-run the Playwright checks the same way (script pattern preserved in conversation history / can be rebuilt from this doc's methodology description).

## Status of each finding — owner's decisions (2026-07-16)

| # | Finding | Decision |
|---|---|---|
| 1 | Fixed nav button + toggle overlap content while scrolling | **Approved — fix** |
| 2 | SEO keyword paragraph dominates mobile above-the-fold | **Keep as-is, do not touch** |
| 3 | No real logo/masthead, just a text chip | **Approved — needs a real header/masthead treatment** |
| 4 | Gallery photos cropped 60–85% by fixed-height `object-fit:cover` | **Approved — fix globally via `chrome/site_css.html`** |
| 5 | No numbering on homepage gallery images | **Approved — homepage ONLY.** Other gallery pages already have text-numbered captions (e.g. "#41 Solid red oak…") and don't need this treatment. |
| 6 | Footer email text overflows horizontally on mobile, site-wide | **Approved — fix** |
| 7 | Before/after galleries stay 2-column and don't collapse on mobile (gallery_1–5); blog/deep-cleaning have worse overflow from a hardcoded `minmax(480px,…)` | **Two-column stays as-is, including on mobile — intentional "billboard CTA" feel.** The blog/deep-cleaning *overflow* (content literally wider than the viewport, not just cramped) still needs fixing — clarify with owner whether that specific overflow is in scope or also considered acceptable before touching it. |
| 8 | Clicking any gallery photo navigates away to a bare image file on a different domain, no lightbox | **Approved — add an in-page lightbox, on the condition that it introduces no new URLs/pages** (a JS overlay intercepting the click, not a route change) |
| 9 | Unoptimized images: avg ~354KB, one at 2.83MB, no responsive sizing | **Deferred.** Owner flagged legacy Turbify hosting as a likely blocker — see "Image optimization feasibility" below, this needs a feasibility answer before it's scheduled, not before it's dismissed. |
| 10 | One CTA graphic ("ultra clean button") is 941KB | Same as #9 — bundled with image optimization decision. |
| 11 | Nav button touch target is 43px tall (1px under the 44px guideline) | **Approved — fix, optimize touch targets generally while in that code** |
| 12 | Photo watermarks look slightly dated for a "premium" site | **No action — intentional, owner adds these in Photoshop, keep as-is** |

**New feature approved, not from the original QA list:** a persistent "jump to gallery / progress" indicator across the 5 before/after gallery pages, to keep visitors browsing instead of dropping off after one page.

## Full finding detail (for implementation reference)

### 1. Floating nav button/toggle overlap content while scrolling
`position:fixed` on `#sdhNavButton`/`#sdhMegaNav` wrapper and `#sdh-toggle` means they sit on top of whatever's beneath them at every scroll position — confirmed visually overlapping the deep-cleaning CTA card, the "Watch Videos" card, and the footer contact block on mobile. Global, `chrome/top.html` + `chrome/scrollhint_and_toggle.html`. Needs a real sticky header treatment (pushes content down) or scroll-aware show/hide, not a persistent floating chip.

### 3. Logo / masthead
Confirmed on every viewport: "SAN DIEGO HARDWOODS" is a small bordered text chip, floating disconnected from any real header bar. Owner confirmed the company name *is* the logo (no separate logo graphic to source) — this is about typography/treatment of a wordmark, not asset sourcing. Global, `chrome/top.html`.

### 4. Gallery image cropping
Sampled homepage photo: **1000×2110px native** (deliberate full-length vertical shot) displayed in a **269×320px** (desktop) / **340×240px** (mobile) box via `object-fit:cover`. The box is roughly square while the source is 2:1+ tall, so `cover` shows a thin horizontal slice of an image composed to be seen top-to-bottom. Applies to every tall photo across all 12 galleries. Global, one rule in `chrome/site_css.html` (`.gallery img { height:320px; object-fit:cover }`) — fix here applies everywhere at once. Options to evaluate: taller fixed height, aspect-ratio-based box, or `object-fit:contain` with a max-height.

### 5. Homepage numbering
No way currently to say "look at photo #14." Badge would come from each image's existing index in `build/data/index/gallery.json` (already-available ordered data, no new extraction needed) — CSS lives in `chrome/site_css.html` (shared class), but the index/data wiring is homepage-specific (`build/scripts/pages/build_homepage.py`), matching owner's instruction that only the homepage needs this.

### 6. Footer overflow
31px of horizontal scroll present on **all 12 pages** — confirmed both numerically and visually (`sandiegohardwoods@gmail.co…` cut off at the right edge on mobile). Root cause: the footer's contact line doesn't wrap. Global, `chrome/footer.html` — needs `flex-wrap` or responsive font-size on that line.

### 7. Before/after gallery columns
- Galleries 1–5: hardcode `grid-template-columns:repeat(2,1fr)` — shrinks instead of overflowing, but squeezes each photo to ~155px at 390px viewport width. **Owner: keep as-is, this is intentional.**
- Blog & deep-cleaning: hardcode `minmax(480px,1fr)` / `minmax(490px,1fr)` respectively — these **do** overflow (up to 520px of content on a 390px screen), the worst overflow found on the site. This is a different, more severe problem than the gallery pages' intentional 2-col squeeze — **needs explicit confirmation from owner whether this specific overflow is also "keep as-is" or should be fixed**, since it wasn't clearly distinguished from #7 in the approval. Page-specific: each page's own build script (`build_gallery1.py` etc., `assemble_blog.py`, `assemble_deep_cleaning.py`) sets these inline; no shared component yet for "before/after pair."

### 8. Lightbox / dead-end photo clicks
Tested directly: clicking a gallery photo navigates to `sdhardwoods.com/[filename].jpg` — a different domain, unstyled, no way back except browser back, no next/prev. Confirmed no lightbox JS is loaded at all (`document.querySelectorAll("script[src]")` returned empty on page load) — the legacy Turbify zoom classes on these images (`yssImg_allowZoomIn` etc.) reference a script that was never carried over, only its CSS. Global once built — every gallery image already shares the same `<a href="photo.jpg"><img></a>` wrapper structure, so one shared component in `chrome/` covers all 12 pages. **Constraint confirmed compatible with owner's requirement:** a JS overlay that intercepts the click and shows the image in an in-page modal (with next/prev through the current gallery) introduces no new URL or page — this is the standard lightbox pattern, not a routing change.

### 9–10. Image optimization feasibility (deferred, needs feasibility answer)
Sampled 12 homepage photos: average 354KB, one at 2.83MB, all displayed in boxes under 350px wide. No responsive `srcset`, no modern format (WebP/AVIF), no build-time resizing. `loading="lazy"` is present and working (that part is already good). Owner's instinct that this is hard because images are "legacy hosted at Turbify" is **partially right and worth unpacking before scheduling or dismissing this**:
- Images are currently served via the `<base href="https://www.sdhardwoods.com/">` shim, meaning yes — they're pulled live from Turbify's hosting, not from this repo or Cloudflare. Any resizing/compression pipeline run against files we don't control/host would need those files pulled down first.
- However: this only stays true as long as the site keeps depending on that `<base href>` shim. If/when images move to being repo-committed or hosted on Cloudflare (R2/Images), an automated resize+compress step becomes straightforward standard tooling (e.g. `sharp` in Node, or Cloudflare's own image resizing), not a hard problem — it becomes hard specifically *because* of the current Turbify dependency, not because image optimization itself is inherently difficult.
- **The 941KB CTA button (#10) is a different, easier case** regardless of the above — it's one file, already effectively "ours" to re-export (it's a designed graphic, not a customer photo), and doesn't require solving the Turbify-hosting question first.

### 11. Touch targets
Nav button measured 43px tall (guideline is ~44px minimum). Minor on its own; owner approved fixing while doing related work, and optimizing touch targets generally, not just this one measurement. Global, `chrome/top.html`.

## What's already working well (don't accidentally regress these)

- Homepage's main photo grid responds correctly: 4 columns → 2 (tablet) → 1 (mobile), no overflow. This is the reference pattern.
- `loading="lazy"` present and functioning on every gallery image.
- Hero heading responds correctly at the mobile breakpoint (44px → 32px).
- Dark-mode toggle and CSS variable system work consistently across all pages/viewports — no dark-mode-specific bugs found.
- JSON-LD, meta tags, and page titles render correctly at every viewport tested.

## Engagement / retention ideas (approved: progress indicator; others noted for later discussion)

1. Fix the lightbox first (#8) — highest leverage engagement fix, turns "click a photo, leave the site" into "click a photo, keep browsing."
2. **Approved:** a persistent "jump to gallery" / progress indicator across the 5 gallery pages (e.g. "Gallery 2 of 5 →"), so a visitor realizes there's more without needing to scroll all the way down.
3. Not yet decided, worth a future conversation: filtering/sorting galleries by wood type, neighborhood, or service type, and numbered-photo deep links (`#photo-14`) for referring a specific customer to a specific result — both build naturally on top of the lightbox once it exists.
