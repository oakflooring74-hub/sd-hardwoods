# Project Quality Bar — the goal this remake must hit, and the rule that protects it

Added 2026-07-19 per explicit owner instruction, after a schema-consolidation pass silently
excluded three pages (`recent_project_photo_gallery_1.html`, `solid_wood_floor_photo_gallery.html`,
`blog.html`) instead of flagging that they had no structured data and asking whether that was
acceptable. It wasn't. This file exists so that kind of silent gap does not happen again.

## The final goal, in the owner's words

This project is not a lift-and-shift of the legacy sdhardwoods.com site. It is a remake and an
**enhanced** version of it. Enhanced means the finished site must:

- Clearly present San Diego Hardwoods' full current offerings, including newer ones (e.g. the
  paid floor assessment/inspection services) — not just what the legacy site happened to show.
- Be easier to find than the legacy site: preserve and build on its established organic
  rankings, never regress them, and close real gaps (structured data, technical SEO, local
  signals) the legacy site never had.
- Be easier to navigate than the legacy site.
- Pass Google's Rich Results Test on every page where a rich result is achievable — with
  particular emphasis on the videos page, which has real, substantial content (58 real videos)
  and should be a flagship rich-result page, not an afterthought.
- Have the best achievable `<title>` and meta description on every individual page — each one
  specific to that page's actual content, not generic boilerplate, while still reading as part
  of one coherent site that represents San Diego Hardwoods' full range of offerings.

Every piece of work on this project should be judged against this bar, not against "did I do the
specific thing that was literally asked."

## The standing rule: question anything that doesn't unify or progress toward that goal

From 2026-07-19 onward, work on this project must proactively raise a question — before
proceeding silently — whenever a piece of work:

- **Leaves out pages it should logically cover.** Any task framed as "do X across the site" or
  "do X for the gallery pages" must explicitly account for every one of the 13 pages (see the
  canonical URL map in `docs/PROJECT_DECISIONS.md`) — either in scope, or explicitly named and
  deferred with a stated reason. Silently skipping a page because it "didn't have anything to
  consolidate" or "wasn't in the original list" is exactly the failure this rule exists to stop.
- **Doesn't clearly serve the goal above.** If a change is technically correct but doesn't move
  the site toward being easier to find, easier to navigate, richer in valid structured data, or
  better titled/described, stop and ask whether it's actually worth doing rather than doing it
  just because it was mentioned in passing.
- **Creates inconsistency between pages** that are supposed to represent the same business, the
  same offerings, or the same navigational system.
- **Is ambiguous about scope** — "the gallery pages" could mean 2 pages or 6; confirm which
  before starting.

Asking a clarifying question, or naming an explicit gap and proposing how to close it, is always
the right move — never quietly do the narrow interpretation and let the rest fall through a
crack.

## Known gaps as of 2026-07-19 (opened by this instruction, not yet closed)

Recorded here so a future session doesn't have to rediscover them from scratch — status moves to
`docs/NEXT_SESSION.md` as each is actually closed out:

- `recent_project_photo_gallery_1.html` — no structured data of any kind.
- `solid_wood_floor_photo_gallery.html` — no structured data of any kind.
- `blog.html` — no structured data of any kind.
- No gallery page (1–5, or solid wood) has `ImageObject`/`ItemList`/`CollectionPage` schema for
  its actual photos, despite photo galleries being one of the site's largest content assets.
- `videos_of_refinishing_process.html`'s 58 `VideoObject` entries are flat siblings, not a proper
  `ItemList`, and its `CollectionPage` node isn't linked to them — needs to reach full Rich
  Results eligibility per the goal above, as the priority page for this.
- Titles and meta descriptions across all 13 pages have not yet been audited page-by-page against
  "is this the best achievable title/description for exactly this page's content" — see
  `docs/2026-07-seo-heading-audit.md` for the evidence-based method already established for that
  kind of change, and the GSC baseline in `docs/PROJECT_OPERATING_MANUAL.md` §10 before touching
  any page that already ranks.
