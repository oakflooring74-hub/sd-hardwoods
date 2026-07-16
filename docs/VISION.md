# Vision

## Mission

Become the premier hardwood flooring website in San Diego.

## Goals

- Preserve decades of SEO
- Modern, responsive experience
- Luxury presentation
- Easy maintenance
- Built from one unified system

## Future

Eventually become the foundation of a legacy website modernization toolkit.

---

This is the north star for the San Diego Hardwoods rebuild, and the reason certain near-term decisions look the way they do:

- **"Preserve decades of SEO"** is why every heading/meta/content change on this project goes through the evidence-based process in `docs/2026-07-seo-heading-audit.md` rather than generic best-practice rewrites — the mission explicitly ranks preservation above theoretical optimization.
- **"Built from one unified system"** is why the `build/` pipeline (`chrome/` shared partials + per-page data + generator scripts, documented in `build/README.md`) exists instead of 12 independently hand-edited pages — it's not just a convenience for this rebuild, it's the intended long-term architecture.
- **"Foundation of a legacy website modernization toolkit"** is the reason the crawl → extract → template → verify methodology was built to be reasonably general (see `build/README.md`'s notes on what's already reusable vs. still San Diego Hardwoods-specific) even though generalizing it is explicitly deferred, not being built now. When that work does get picked up, this system — not a rewrite — is meant to be the starting point.

Two items on the deferred list (CMS, desktop app) are specifically about closing the gap between "a developer can regenerate this site" and "the business owner can add a new project photo without a dev session" — worth remembering that these aren't separate ideas, they're the same problem (a simple front end over the existing `build/data/*.json` + build-script pipeline) at different levels of polish.
