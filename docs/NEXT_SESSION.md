# Start here — project status as of 2026-07-16

Read this file first when picking this project back up. It links to everything else and tells you what's approved, what's blocked, and what to ask the owner before doing anything.

## The site, in one paragraph

sdhardwoods.com is a legacy Yahoo/Turbify "Site Solution" site for a San Diego hardwood-flooring contractor. All 12 pages have been rebuilt with a consistent modern design system (see `build/README.md` for the full generator/tooling architecture) and are live on a Cloudflare Pages preview at **https://redesign.sd-hardwoods.pages.dev** — this is NOT yet the production site; sdhardwoods.com itself is untouched. Everything lives in the GitHub repo **oakflooring74-hub/sd-hardwoods**, on the **`redesign` branch** (production/`master` still holds the prior owner's earlier, different rebuild attempt — do not merge without the owner's explicit go-ahead).

See also `docs/VISION.md` for the longer-term mission/goals this project is working toward.

## Decisions at a glance (2026-07-16)

**APPROVED — build next:**
- ✅ Sticky navigation (fix nav button/toggle overlapping content while scrolling)
- ✅ Logo redesign
- ✅ Gallery image height increase (fix the cropping)
- ✅ Homepage numbering (homepage only)
- ✅ Lightbox (no new URLs/pages)
- ✅ Footer fixes
- ✅ Touch target increase
- ✅ Gallery progress indicator

**DEFERRED — not now, not dismissed:**
- CMS (a way for the owner to add projects without a dev session)
- Desktop app (see prior discussion — feasible, but scoped out for now)
- Migration toolkit (turning this system into a general legacy-site-migration tool)
- Image optimization
- Cloudflare image migration (moving images off Turbify hosting)
- Google Search Console optimization (waiting on the data export)

**DO NOT CHANGE:**
- SEO paragraph (the keyword-heavy utility-bar text)
- Watermarks (owner adds these in Photoshop)
- Two-column before/after galleries (intentional "billboard CTA" feel, even on mobile)
- Legacy hosted images (still served live from Turbify via the `<base href>` shim)

## What's done

- All 12 pages rebuilt, verified (image counts, JSON-LD validity, structural checks), committed, and deployed to the Cloudflare preview.
- The full build pipeline (raw crawled source, extracted content data, shared design partials, generator scripts) is committed under `build/` — see `build/README.md` for how to regenerate any page and the list of known quirks.
- A full visual/responsive QA pass was done in a real browser at 4 viewport sizes across all 12 pages — see `docs/2026-07-qa-report.md` for the prioritized findings and the owner's decision on each one.
- An SEO discussion + a real H1/H2/H3 audit (legacy markup vs. redesign, not generic advice) was done — see `docs/2026-07-seo-heading-audit.md`.

## What's approved and ready to build (next time code changes are authorized)

From `docs/2026-07-qa-report.md`:
1. Fix the fixed-position nav button/toggle overlapping page content while scrolling (`chrome/top.html`, `chrome/scrollhint_and_toggle.html`)
2. Real logo/masthead treatment for "San Diego Hardwoods" (`chrome/top.html`)
3. Fix gallery image cropping — one CSS rule in `chrome/site_css.html`, applies to all 12 pages
4. Add numbered badges to homepage gallery photos **only** (other gallery pages already have text-numbered captions and don't need this)
5. Fix footer email text overflow, site-wide (`chrome/footer.html`)
6. Add an in-page lightbox for gallery photos (currently clicking a photo navigates away to a bare image file on a different domain — confirmed via live click-through test) — must introduce no new URL/page, a JS overlay only
7. Adjust/optimize touch targets generally while working in the header code
8. Build a persistent "jump to gallery" / progress indicator across the 5 before/after gallery pages

**Explicitly NOT to be touched:** the SEO keyword paragraph in the utility bar (owner wants it kept as-is), photo watermarks (owner adds these in Photoshop already).

## Open question to ask the owner before starting the build

The owner approved keeping the before/after galleries **2 columns wide even on mobile** as an intentional "billboard CTA" choice — but separately, the QA report found that **blog and deep-cleaning specifically have actual horizontal overflow** (content wider than the screen, not just a tight 2-column squeeze), caused by a different, hardcoded `minmax(480px,…)` grid rule on just those two pages. It's not clear from the owner's approval message whether this specific overflow was covered by "keep the 2-column layout" or whether it still needs fixing as its own bug. **Confirm which, before touching those two pages.**

## Blocked / waiting on the owner

- **Google Search Console export** (Query, Page, Clicks, Impressions, CTR, Position — full history, ideally per-page) — needed before any heading-level changes or meta-description rewrites on pages that already have one. See `docs/2026-07-seo-heading-audit.md` for exactly what this unlocks and why pulling it *before* the redesign goes live matters (it's the only way to get a clean pre-launch ranking baseline).
- **Image optimization** — deferred, but not dismissed. See the "Image optimization feasibility" section of `docs/2026-07-qa-report.md`: it's genuinely harder right now because images are still served live from Turbify hosting via a `<base href>` shim, not because image compression itself is hard. Worth revisiting if/when images move to being repo-hosted.

## Safe to do without waiting on GSC data

Adding meta descriptions to the 6 pages that currently have **none at all** (about_us, contact_us, videos_of_refinishing_process, blog, recent_project_photo_gallery_4, recent_project_gallery_5) — confirmed missing on the legacy site, not something the redesign removed, so there's no existing snippet performance to protect. Still needs the owner's go-ahead to actually write and add them (this was a discussion session, nothing was implemented), but doesn't need to wait on the GSC export the way changes to pages that already have a meta description do.

## Reference docs in this folder

- `docs/2026-07-qa-report.md` — full QA findings, owner decisions, chrome/ vs. page-specific breakdown
- `docs/2026-07-seo-heading-audit.md` — GSC strategy discussion, meta-description categorization, full legacy-vs-redesign heading data and analysis
- `build/README.md` — how the site is actually built/regenerated; read this before touching any `build/` script

## Key facts worth not re-deriving

- GitHub: `oakflooring74-hub/sd-hardwoods`, branch `redesign` (two commits ahead of where the tooling was organized: page rebuild, then build-pipeline commit)
- Cloudflare Pages project: `sd-hardwoods`, account tied to `sandiegohardwoods@gmail.com` — preview alias is `redesign.sd-hardwoods.pages.dev`; production (`sd-hardwoods.pages.dev`) is still the prior owner's build, untouched
- `gh` CLI has two logged-in accounts on this machine; make sure `oakflooring74-hub` is the active one before pushing (`gh auth switch --hostname github.com --user oakflooring74-hub`)
- The redesigned pages still depend on Turbify hosting for images/video/theme CSS via a `<base href="https://www.sdhardwoods.com/">` tag — this is a deliberate bridge, not an oversight, but it's the reason image optimization is currently hard and worth remembering when it comes up again
