# Prelaunch Audit — 2026-07-19/20

Report-only audit of the 13-page generated site on `redesign` at baseline commit
`dde7ce4105631757a5f254ee059f96b5b5c27f50`. No site, asset, metadata, schema, build, branch,
DNS, or deployment files were modified. Working tree confirmed clean except the intentionally
untracked `assets/ALL_IMAGES/` archive.

Live comparisons were made against the current production Turbify site
(`https://www.sdhardwoods.com/...`), fetched directly (raw HTTP, not a markdown-converted
summary) during this session — see §6 for the one item that could not be checked this way.
Raw-source snapshots in `build/raw-source/` were used only as provenance evidence (to tell
whether a divergence predates this project or was introduced by it), per instructions not to
treat them as current.

---

## 1. Launch blockers

1. **All 13 pages still load two stylesheets live from Turbify's CDN**, with no local copy and
   no owner decision on record:
   `https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css` and
   `https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css`.
   Galleries 3 and 4 additionally load a third,
   `https://s.turbifycdn.com/lm/css/hosting/yss/v2/apps/beforenafter_1.css`. This is a real
   runtime dependency on the exact host this project exists to migrate away from — a single
   point of failure with no fallback if Turbify hosting is ever suspended or the account
   lapses. Unlike images/logo/favicons (fully localized in Milestone 2.10) or JS, this was
   never discussed in any milestone note or `PROJECT_DECISIONS.md` entry. Source:
   `s.turbifycdn.com` literal URLs hardcoded in each `build/scripts/pages/build_*.py` /
   `assemble_*.py` head-block template (11 separate copies).
2. **Galleries 3 and 4 leak a stale Turbify platform fingerprint** that the other 11 pages do
   not carry: `<meta http-equiv="X-UA-Compatible" content="IE=7">` and
   `<meta name="Generator" content="Site Solution - lunarlander">`, verbatim in
   `recent_project_photo_gallery_3.html` and `recent_project_photo_gallery_4.html`. Source:
   `build/scripts/common/build_page.py` (the shared script for these two pages) carries more of
   the raw legacy head block than the other 11 pages' scripts, which already strip these two
   tags. Low functional risk (not visible to visitors, browsers ignore both), but a real,
   easily-fixed inconsistency that announces "built on Yahoo/Turbify Site Solution" on 2 of 13
   public pages of a site whose entire purpose is leaving that platform.

Both are cheap, mechanical fixes confined to `build/scripts/` — no design, content, or schema
changes needed.

## 2. Owner decisions required

1. **Eight pages have title/meta description/H1 wording that differs from the current live
   site**, and several of those differences aren't recorded in any milestone or decision doc
   (see §3 for the full table). Specifically **not yet reconciled with any documented reason**:
   About Us meta description, Contact Us meta description, Gallery 2 H1, Gallery 5 meta
   description + H1, Solid Wood Gallery meta description + H1, Videos meta description. Need an
   owner call on each: intentional and worth documenting, or should be realigned to current live
   wording.
2. **The Videos page's live meta description has itself drifted since the original crawl** —
   `build/raw-source/videos_of_refinishing_process.html`'s snapshot description and the current
   live description are two different strings, and the generated page's description matches
   neither. This is independent evidence (not just this project's assumption) that the owner or
   someone else has edited live Turbify metadata since the rebuild started, exactly as flagged
   in this audit's instructions — worth a fresh look at what else on the live site may have
   moved before finalizing any further metadata work.
3. **Whether to localize or retire the two sitewide Turbify CSS files before go-live** (tied to
   Launch Blocker #1) — no prior decision recorded either way.
4. `docs/PROJECT_QUALITY_BAR.md`'s "Known gaps as of 2026-07-19" section says
   `recent_project_photo_gallery_1.html`, `solid_wood_floor_photo_gallery.html`, and
   `blog.html` have "no structured data of any kind." That's no longer accurate — automated
   JSON-LD parsing (this audit) confirms all three now carry valid, parseable `WebPage`/
   `Service`/`Blog` graphs tied to the shared `#local` business entity. The deeper Rich-Results
   gaps that same doc names (no `ImageObject`/`ItemList` schema for gallery photos; Videos
   page's 58 `VideoObject` entries not fully wired into a proper `ItemList`, beyond the one
   hero video linked in Milestone 2.9) still appear open. Recommend refreshing that doc's gap
   list rather than treating it as current.

## 3. Meaningful title/meta/H1/search-intent differences

**5 of 13 pages match the live site exactly** on title, meta description, and H1 (core text):
Gallery 1, Gallery 3, Gallery 4, Blog, and Floor Assessments (no legacy equivalent — checked
for internal consistency only, see §5). Gallery 2 matches on title and H1; its description
differs only by a trailing period (not meaningful).

**8 pages differ meaningfully.** Already-documented/approved divergences are marked; the rest
have no recorded reason found in `docs/`:

| Page | Title | Meta description | H1 | Status |
|---|---|---|---|---|
| Homepage | Differs | Differs | Differs | Documented (Milestone 2.4 title/desc rewrite, Milestone 2.1 owner-directed H1) |
| Deep Cleaning | Match | Differs | Match | Documented — Milestone 2.9 owner-locked verbatim; also removes a live "Dust-free" claims-policy violation still present in the current live description |
| Contact Us | Differs | Differs | Match | Title documented (Milestone 2.6, owner sign-off, drops live's "Free Estimates"); description **not documented** |
| About Us | Match | Differs | Match | **Not documented** — live/raw-source agree with each other; only ours diverges |
| Gallery 2 | Match | Match (trivial) | Differs | **Not documented** — live/raw-source H1 agree; ours diverges |
| Gallery 5 | Match | Differs | Differs | **Not documented** — live/raw-source agree; ours is shorter/generic on both |
| Solid Wood | Match | Differs | Differs | **Not documented** — live/raw-source agree (and still carry "100% dust containment"/"free estimate," both against current claims policy); ours is shorter and claims-compliant but loses several city/keyword mentions |
| Videos | Match | Differs | Match | **Not documented**, and live's own description no longer matches the raw-source snapshot either — see Owner Decision #2 above |

No recommendation to change any of the "not documented" items is made here — flagging for
owner review only, per instructions not to push proven live wording toward a "more optimized"
version without evidence.

**Structural note (all pages, informational):** the live Turbify pages wrap the brand name,
tagline, real heading, and on several pages a full paragraph of body copy inside one oversized
`<h1>`. The redesign uses one clean, correctly-scoped `<h1>` per page everywhere. This is a
genuine technical improvement, not a regression, even where the visible heading wording itself
also changed.

**Gallery 3 canonical bug:** live's own `<link rel="canonical">` self-references the wrong URL
(`recent_project_gallery_3.html`, missing `photo_`) — a pre-existing Turbify authoring bug. The
redesign's canonical is correct (`recent_project_photo_gallery_3.html`). Already fixed per
Milestone 2.4; confirmed still correct, no action needed.

**Floor Assessments page** (no legacy equivalent): title, meta description, single H1, and
self-referencing canonical (`https://www.sdhardwoods.com/floor-assessments-inspections`) are
all present and internally consistent; JSON-LD parses with 6 `Service`/`WebPage` nodes all tied
to the shared `#local` entity; linked from all 12 other pages (5–8 references each), not an
orphan.

## 4. Remaining Turbify or external dependencies

| Dependency | Where | Classification |
|---|---|---|
| `mc_global*.css` + `theme.css` (Turbify global/theme CSS) | All 13 pages, `<head>` | **Launch blocker** — see §1 |
| `beforenafter_1.css` (Turbify) | Galleries 3, 4 only | **Launch blocker** — see §1 (same fix) |
| `turbify_ss_extensions_*.js`, loaded via a malformed `<link rel="stylesheet">` pointing at a `.js` file | Galleries 3, 4 only | **Inert historical reference** — browsers can't execute JS via a stylesheet link; the request fires but does nothing functional. Safe to remove, not urgent. |
| Inline `YAHOO.util.Dom` / `.Event` / `.Anim` / etc. script block (references a `window.YAHOO` that nothing on the page defines) | Galleries 3, 4 only | **Inert historical reference** — the resulting "YAHOO is not defined" console error is pre-existing and already tracked (Milestone 2.5 QA notes); confirmed still present, not a new regression, doesn't break visible functionality per prior browser QA. |
| `X-UA-Compatible` / `Generator: Site Solution - lunarlander` meta tags | Galleries 3, 4 only | **Launch blocker** — see §1 |
| Turbify-hosted images, thumbnails, favicons, logo | — | **Resolved.** Zero remaining `sdhardwoods.com`-hosted image/favicon/logo/thumbnail URLs across all 13 pages (verified by regex scan); the one previously-flagged missing VideoObject thumbnail (About Us page) was fixed in the baseline commit `dde7ce4` itself. |
| `<base href>` Turbify bridge | — | **Resolved** (removed Milestone 2.10); one historical JS comment in `top.html` refers to it accurately as removed. |
| YouTube (`youtube.com`, `youtube-nocookie.com`, `i.ytimg.com`) | Videos page, nav/footer links | **Intentionally external** — owner's own channel, documented (Milestone 2.6). |
| Google Analytics (`googletagmanager.com`) | All 13 pages | **Intentionally external** — GA4, hostname-gated to production only, documented (Milestone 2.6). Verified directly in `build/chrome/analytics.html`: single shared loader, `PRODUCTION_HOSTS` gate on `www.sdhardwoods.com`/`sdhardwoods.com` only, exactly one loader per page confirmed across all 13. |
| Bona (`bona.com`) | Homepage | **Intentionally external** — manufacturer-partner verification link, documented (Milestone 2). |
| Google Maps short link (`maps.app.goo.gl`) | All 13 pages (footer/business info) | **Intentionally external** — outbound business-listing link, no action needed. |
| Web fonts | — | **None found** — system font stack only, no external font host of any kind. |
| Redirects / `_redirects` / `_headers` / `wrangler.toml` / `netlify.toml` | — | **None exist.** Consistent with the "no redirects without an approved milestone" rule; also means preview-vs-production header differentiation (see §5/§6) is entirely a Cloudflare Pages platform default, not repo-configured. |

## 5. Technical checks passed

- All 13 intended public URLs present as generated files; exactly 13 `.html` files at repo
  root, no unintended duplicates.
- `sitemap.xml`: exactly 13 `<loc>` entries, matching `CANONICAL_URLS` in
  `build/scripts/common/build_sitemap.py` exactly, including the assessments page's
  intentionally extensionless URL.
- `robots.txt`: `Allow: /` for all, correct `Sitemap:` pointer, consistent with sitemap.
- Every page's canonical self-references its own intended public URL correctly (spot-verified
  against the canonical map; Gallery 3's canonical is the corrected URL, not the live site's
  buggy one).
- No `<meta name="robots">` on any of the 13 generated pages — defaults to indexable
  (index, follow) on all of them, appropriate for production content.
- All local asset references (`src`/`href`/`content` attributes and JSON-LD `image`/
  `thumbnailUrl`/`logo`/`url` fields, all 13 pages) resolve to a file that exists on disk,
  checked **case-sensitively** against the actual on-disk filenames (930 files) — zero missing,
  zero case mismatches. This matters because Cloudflare Pages serves from a case-sensitive
  Linux filesystem; a case-only mismatch would work locally on Windows but 404 in production.
- All internal `<a href>` links across all 13 pages resolve to one of the 13 canonical URLs —
  zero broken internal links, zero links to a stray/unintended page.
- Floor Assessments page is linked from all 12 other pages (not orphaned).
- JSON-LD parses cleanly on every one of the 13 pages (all `<script type="application/ld+json">`
  blocks tested with a real JSON parser; zero parse failures).
- The shared business entity is declared with exactly one `@id`
  (`https://www.sdhardwoods.com/#local`) reused consistently across all 13 pages — no duplicate
  or conflicting business entities found.
- GA4: single shared implementation (`build/chrome/analytics.html`), hostname-gated to
  `www.sdhardwoods.com`/`sdhardwoods.com` only, exactly one loader injected per page across all
  13 — confirmed by direct source inspection, not just documentation.
- `redesign` deploys to preview only / `master` remains production: confirmed both from
  `.github/workflows/deploy-cloudflare-pages.yml` (deploy job only runs on `push`, passes
  `--branch=${{ github.ref_name }}`, Cloudflare's own production-branch setting does the
  Preview/Production classification) **and** empirically — live HTTP headers pulled this
  session show `x-robots-tag: noindex` on `redesign.sd-hardwoods.pages.dev` and no such header
  on the `master`-branch `sd-hardwoods.pages.dev` alias. `master`'s git history is fully
  disjoint from `redesign` (separate initial commit, confirmed via `git merge-base`) — the
  "prior owner's earlier rebuild attempt" is still what's there; production is untouched.
- The build-and-verify CI gate exists and does what it's supposed to: `build` job regenerates
  all pages via `build_all.py` and fails the workflow if that produces any diff against
  committed output, before `deploy` (which only runs on non-PR events) can run.

## 6. Items that could not be externally verified

- **Cloudflare Pages dashboard configuration** (production-branch setting, project-level
  domain/alias attachments, whether the preview environment could ever get a custom domain
  that would bypass the automatic `*.pages.dev` `noindex` header) — cannot be read from the
  repository. The `x-robots-tag: noindex` behavior on the preview URL was confirmed live this
  session, but it is a Cloudflare platform default, not something this repo configures or could
  enforce if the dashboard setup changes. There is no repo-level fallback (no `_headers` file,
  no hostname-conditional `<meta name="robots">`) the way GA4's hostname gate has one in code —
  worth considering as defense-in-depth, not because anything is currently wrong.
- **GitHub Actions repository secrets** (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`) —
  presence/validity can't be checked from the repo; prior sessions record them as configured
  and working (last confirmed green run referenced in `docs/NEXT_SESSION.md`), not re-verified
  here.
- **DNS / domain attachment for `www.sdhardwoods.com` on Cloudflare Pages** — out of scope for
  a repo-based audit and explicitly out of scope per instructions (no DNS changes/checks
  attempted).
- All 12 legacy live-page fetches in this audit succeeded (HTTP 200, direct raw HTML, not a
  markdown summary) — no page was unreachable, so no SEO comparison in §3 fell back to
  raw-source-only.

## 7. Smallest recommended implementation milestone

A tight, low-risk cleanup milestone that closes both launch blockers without touching design,
content, or schema:

1. Localize the two sitewide Turbify CSS files (`mc_global*.css`, `theme.css`) plus Gallery
   3/4's extra `beforenafter_1.css` — same pattern already used for images/logo/favicons in
   Milestone 2.10 (copy the file, point the existing `<link>` at the local path, verify
   rendering unchanged).
2. Strip the stale `X-UA-Compatible` and `Generator: Site Solution - lunarlander` meta tags
   from `build/scripts/common/build_page.py`'s head block (galleries 3/4 only) to match the
   other 11 pages.
3. Optional in the same pass since the script is already open: remove the dead
   `turbify_ss_extensions_*.js`-as-stylesheet `<link>` and the inline `YAHOO.util.*` script
   block from the same two pages (removes the long-standing console error).
4. Regenerate via `build_all.py`, confirm double-build byte-identical and zero remaining
   `turbifycdn.com` references, then bring the §2 owner-decision items (metadata wording,
   `PROJECT_QUALITY_BAR.md` refresh) to the owner as a separate, content-focused decision —
   don't bundle metadata wording changes into this technical cleanup.
