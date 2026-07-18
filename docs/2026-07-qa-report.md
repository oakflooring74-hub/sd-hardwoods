# Visual & Responsive QA Report — redesign branch

**Date:** 2026-07-16
**Tested against:** https://redesign.sd-hardwoods.pages.dev (Cloudflare Pages preview of the `redesign` branch)
**Method:** Real headless Chromium (Playwright) across all 12 pages at 4 viewports (1920×1080 desktop, 1440×900 laptop, 768×1024 tablet, 390×844 mobile) — DOM measurements (horizontal overflow, touch-target sizes, computed font sizes, gallery image display-vs-natural dimensions) plus visual screenshots and a live click-through test. No code was changed while producing this report.

This is a point-in-time report. If the site changes before the fixes below are implemented, re-run the QA sweep rather than trusting these numbers blindly — see `build/README.md` for how the site is regenerated, and re-run the Playwright checks the same way (script pattern preserved in conversation history / can be rebuilt from this doc's methodology description).

## IMPLEMENTATION STATUS UPDATE (2026-07-16, later same day)

**Findings #1, #3 (partial), #4, #5, #6, #7 (blog/deep-cleaning overflow), #8, #11, and the progress-indicator idea are now implemented, built, and locally tested** (real Chromium via Playwright, mobile/tablet/desktop, all 12 pages — zero horizontal overflow found anywhere). Committed on `redesign` as "Complete first interactive site-improvement milestone." Not yet pushed. See `docs/NEXT_SESSION.md` for the full Milestone 1 summary and the Milestone 2 (header/nav redesign) scope that comes next — **finding #3 (logo/masthead) is only partially resolved: the overlap bug is fixed and a basic monogram+wordmark treatment was added, but a follow-up screenshot review found the brand still reads as too small and the header still needs a dedicated redesign (Milestone 2).**

Findings #2, #9, #10, #12 remain exactly as documented below — no action taken, per owner decision (unchanged).

## MILESTONE 2 IMPLEMENTATION + QA (2026-07-16, evening — approved & preview-deployed)

The full header/brand/navigation redesign scoped below in "Remaining issues after Milestone 1" **is now implemented and locally QA'd**, along with the rest of the owner's Milestone 2 spec (consultation-services pricing, hero rebalance, homepage images #91–#96 removed at the generator level, gallery-navigation replacement, explore-bar redesign, CTA language shift to "free phone assessment"). **Owner approved on 2026-07-16; committed as `9117b84`, pushed, and auto-deployed to the Cloudflare preview (verified live; production untouched).** Full change list in `docs/NEXT_SESSION.md`.

**QA method:** all 12 regenerated pages served over local HTTP (`python -m http.server`), driven with real headless Chromium (Playwright) at 1440×900 desktop and 390×844 mobile, plus a `prefers-reduced-motion: reduce` context. ~100 scripted checks, all passing:

- **Masthead/brand:** real medallion logo renders from `assets/branding/web/` (committed static files, browser-cacheable); brand name + "Since 1990" tagline; phone `tel:` + email `mailto:` links; "Free Phone Assessment" CTA. SEO paragraph preserved verbatim (still fed from each page's vcard text) but visually subordinate (10.5px, reduced opacity) and no longer sticky.
- **Mini-header:** hidden at top, slides in only after the full masthead scrolls out (IntersectionObserver), ~56px vs ~250px masthead, `position:fixed` so it never displaces content; disappears again at top. Works on mobile (≤76px) and under reduced motion.
- **Navigation:** 7 top-level items (Home / Services / Project Galleries / Videos / About / Blog / Contact); dropdowns open on hover *and* click, close on Escape and focus-out, `aria-expanded` synced; keyboard Enter opens; active page marked (`aria-current` + group highlight verified on gallery 3); YouTube pill with brand icon, `target="_blank" rel="noopener"`. `<noscript>` fallback exposes all grouped links inline.
- **Mobile drawer:** opens from both the nav-band Menu button and the mini-header Menu button; 3 grouped `<details>` sections + all 12 pages + YouTube + email; call/text CTAs; scroll lock (`html.sdh-lock`); Escape closes; focus returns to the opener; focus trapped while open.
- **Homepage gallery:** exactly 90 figures, badges sequential #1–#90, zero legacy button graphics in the grid; replacement gallery-navigation tiles (galleries 1–5 + solid wood) with correct hrefs.
- **Consultation section (`contact_us#consultation-services`):** 6 tiers priced Free/$75/$150/$350/$750/$1,500, exact required credit wording present, scope-confirmed-at-scheduling wording present, anchor lands below the header (`scroll-margin-top`), cards stack cleanly on mobile.
- **Milestone 1 regressions checked:** lightbox opens/closes on homepage and gallery 1; gallery progress control present on gallery 1; two-column before/after grid still exactly 2 columns on gallery 1 desktop; dark/light toggle works; light mode visually verified.
- **Overflow:** zero horizontal overflow on any of the 12 pages, desktop and mobile.
- **Reduced motion:** mini-header still appears; explore bar stops rotating (static single message).

**Screenshots for owner review:** `qa-screenshots/m2-*.png` (5 shots: desktop top, desktop scrolled mini-header, mobile menu open, consultation section, bottom gallery navigation). The `qa-screenshots/` folder is gitignored — local only, never deployed.

**QA caveat discovered while testing:** Turbify (which still hosts all project images + legacy theme CSS via the `<base href>` bridge) began hanging/throttling requests mid-run, which blocks `DOMContentLoaded` in automated tests. Later test passes aborted non-localhost requests (all design CSS is inline in each page, so layout is unaffected). Worth remembering for future QA sweeps — and it's one more data point for the deferred "move images off Turbify" item.

## Status of each finding — owner's decisions (2026-07-16)

| # | Finding | Decision | Status |
|---|---|---|---|
| 1 | Fixed nav button + toggle overlap content while scrolling | **Approved — fix** | ✅ **Fixed** — sticky in-flow header; toggle fades near footer |
| 2 | SEO keyword paragraph dominates mobile above-the-fold | **Keep as-is, do not touch** | Untouched (content/presence protected). Visual de-emphasis is now the Milestone 2 goal — see `docs/NEXT_SESSION.md` |
| 3 | No real logo/masthead, just a text chip | **Approved — needs a real header/masthead treatment** | ⚠️ **Partially fixed** — overlap bug gone, monogram+wordmark added, but a screenshot review after shipping found the brand still reads too small; full masthead redesign is Milestone 2 |
| 4 | Gallery photos cropped 60–85% by fixed-height `object-fit:cover` | **Approved — fix globally via `chrome/site_css.html`** | ✅ **Fixed** — `object-fit:contain`, height 320→420px, no cropping |
| 5 | No numbering on homepage gallery images | **Approved — homepage ONLY.** Other gallery pages already have text-numbered captions (e.g. "#41 Solid red oak…") and don't need this treatment. | ✅ **Fixed** — badges #1–#96 on homepage gallery. *(Milestone 2 note: now #1–#90 — the six obsolete legacy nav-button graphics that occupied #91–#96 were removed at the generator level, replaced by a real gallery-navigation section.)* |
| 6 | Footer email text overflows horizontally on mobile, site-wide | **Approved — fix** | ✅ **Fixed** — `.f-call` now flex-wraps, no overflow |
| 7 | Before/after galleries stay 2-column and don't collapse on mobile (gallery_1–5); blog/deep-cleaning have worse overflow from a hardcoded `minmax(480px,…)` | **Two-column stays as-is, including on mobile — intentional "billboard CTA" feel.** The blog/deep-cleaning *overflow* (content literally wider than the viewport, not just cramped) still needs fixing — clarify with owner whether that specific overflow is in scope or also considered acceptable before touching it. | ✅ **Both resolved** — 2-col layout on galleries 1–5 preserved untouched; blog/deep-cleaning overflow fixed (`minmax(min(Npx,100%),1fr)`), confirmed as a real, separate bug and fixed independently of the 2-col decision |
| 8 | Clicking any gallery photo navigates away to a bare image file on a different domain, no lightbox | **Approved — add an in-page lightbox, on the condition that it introduces no new URLs/pages** (a JS overlay intercepting the click, not a route change) | ✅ **Fixed** — `build/chrome/lightbox.html`, JS overlay only, no new URLs |
| 9 | Unoptimized images: avg ~354KB, one at 2.83MB, no responsive sizing | **Deferred.** Owner flagged legacy Turbify hosting as a likely blocker — see "Image optimization feasibility" below, this needs a feasibility answer before it's scheduled, not before it's dismissed. | Still deferred, untouched |
| 10 | One CTA graphic ("ultra clean button") is 941KB | Same as #9 — bundled with image optimization decision. | Still deferred, untouched |
| 11 | Nav button touch target is 43px tall (1px under the 44px guideline) | **Approved — fix, optimize touch targets generally while in that code** | ✅ **Fixed** — nav button, flyout links, dark-mode toggle all ≥44px |
| 12 | Photo watermarks look slightly dated for a "premium" site | **No action — intentional, owner adds these in Photoshop, keep as-is** | Untouched, as decided |

**New feature approved, not from the original QA list:** a persistent "jump to gallery / progress" indicator across the 5 before/after gallery pages, to keep visitors browsing instead of dropping off after one page. **✅ Fixed** — "Gallery N of 5" + numbered jump links + prev/next on all 5 gallery pages.

## Remaining issues after Milestone 1 (screenshot review, 2026-07-16)

A post-implementation screenshot review of the shipped header found three things that Milestone 1 did not (and wasn't scoped to) fix — these define Milestone 2, detailed in `docs/NEXT_SESSION.md`:

- **Brand is too small.** The monogram+wordmark lockup added in Milestone 1 fixed the "disconnected floating chip" problem but didn't fix the underlying visual-hierarchy problem: the brand still doesn't read as the dominant element of the header.
- **The SEO utility-bar strip visually dominates** the top of the page, more prominent than brand+nav combined. Its *content* is still protected (finding #2, unchanged) — this is specifically about visual weight/hierarchy, not the text itself.
- **Navigation is inadequate.** A single "☰ Explore Our Services" button hiding all 12 pages in one flat, undifferentiated flyout list doesn't scale as real information architecture. Milestone 2 needs to group the 12 pages into clear categories, and give the YouTube channel link a prominent, recognizable YouTube-style treatment instead of burying it as plain text in the flyout.

**Update (2026-07-16, evening):** all three findings in this section are now addressed by the Milestone 2 implementation — see "MILESTONE 2 IMPLEMENTATION + QA" above. Kept here for the historical record of what motivated the milestone.

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

### 7. Before/after gallery columns — RESOLVED 2026-07-16
- Galleries 1–5: hardcode `grid-template-columns:repeat(2,1fr)` — shrinks instead of overflowing, but squeezes each photo to ~155px at 390px viewport width. **Owner: keep as-is, this is intentional.** Left untouched, confirmed via diff (image src/alt and the inline `1fr 1fr` / `repeat(2,1fr)` rules are unchanged).
- Blog & deep-cleaning: hardcoded `minmax(480px,1fr)` / `minmax(520px,1fr)` respectively — these **did** overflow (up to 520px of content on a 390px screen), the worst overflow found on the site. **Resolved as its own bug, independent of the galleries' 2-col decision**: changed to `minmax(min(Npx,100%),1fr)` in `assemble_blog.py` / `assemble_deep_cleaning.py`. Verified zero horizontal overflow on both pages at all 3 tested viewports post-fix.

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

---

# MILESTONE 2.5 QA — 2026-07-18 (content alignment + media-fact system)

**Branch:** `redesign` · **Method:** static gate + double-build determinism + real headless Chromium (Playwright) via local HTTP server (`http://127.0.0.1`, never file://), all 13 pages at desktop 1280×900 and mobile 390×844, with remote hosts stubbed for hermetic runs.

## Commands run

```
python build/scripts/build_all.py                       # twice → byte-identical (md5 across 13 pages + sitemap + robots)
python build/scripts/generate_media_inventory.py        # twice → deterministic (diff-clean)
python build/scripts/validate_media_inventory.py        # 0 errors, 4 intentional owner-review warnings
<scratchpad>/qa_static_m25.py                           # static gate
<scratchpad>/qa_browser_m25.py                          # browser gate
```

## Static gate — PASSED (all 13 pages)

- Exactly one canonical per page, matching the Milestone 2.4 approved map; sitemap.xml has exactly the 13 canonical URLs; robots.txt allow-all + sitemap pointer, no forbidden directives.
- Exactly one viewport, one `<title>`, one `<h1>` per page; no `noindex`; no `_gaq`/`UA-20793161`/`ga.js` anywhere.
- No `tel:` link labeled as a text action; every JSON-LD block strict-parses; every JSON file under `build/data/` strict-parses; all internal page links resolve to local files.
- Content preservation vs `HEAD` (Milestone 2.4 commit `1ecff4e`): image count, video count, and heading count did not drop on any page — no project, section, image placement, or video disappeared.
- The four corrected Bing Crosby Ranch walnut alts present; all four false alt fragments (bamboo / parquet / La Jolla maple / "museum grade") absent.

## Media inventory — PASSED

377 image assets + 58 video assets; 516 placements across 13 pages; every scanned image/video placement has a record; asset and placement IDs unique site-wide; no conflicting approved project identities; nothing auto-published. The 4 warnings are the deliberate `TRICIA WALNUT27/30/63/76` filename-vs-white-oak-description conflict flags (Solid Wood Gallery), awaiting the owner.

## Browser gate — 176 / 180 checks passed

Per page × viewport: no JS pageerrors, one H1, header + single footer present, no horizontal overflow, dark default. Interactive: mobile drawer open/Escape-close, desktop Services dropdown, mini-header on scroll, theme toggle to light + persistence across reload, gallery lightbox open/Escape-close, videos modal open + on-demand nocookie iframe + Escape-close, category filters, and the new Milestone 2.5 internal links (deep-cleaning → Gallery 4 / refinishing-home).

**The 4 failing checks are one pre-existing issue, not a 2.5 regression:** galleries 3 and 4 (byte-identical to Milestone 2.4 output) carry the legacy inline Turbify `var $D…` script extracted from the raw source, which throws a console-only `YAHOO is not defined` pageerror because the Yahoo library it expects no longer loads. Page rendering and all functionality are unaffected. Recorded as a cleanup candidate for the performance/hardening milestone (remove or guard the legacy script at the generator level).

## Preview verification

Performed after the Milestone 2.5 push — see the milestone final report / NEXT_SESSION for the deployed commit confirmation. Production (`master`, Turbify live site) untouched.
