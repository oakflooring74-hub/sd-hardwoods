# San Diego Hardwoods Website — Project Entry Point

**Read this first in every session.** Then read `docs/NEXT_SESSION.md` for current status.

---

## Current Status (as of 2026-09)

Muirlands Oak showcase page committed (`e156113`), ready to push to `redesign` branch for preview deployment at `sd-hardwoods-preview.sandiegohardwoods.workers.dev`.

Owner has many folders with watermarked photos → each becomes one SEO-rich individual project page. Goal: expand Google footprint, regain ranking lost during legacy-to-modern site cutover.

---

## Two Workflows — Know Which One You're In

### Workflow A: Add New Project Showcase Pages (Safe, Automatic)
**When you say:** *"Add [folder name] as new showcase page"* or *"Resume Muirlands deployment"*

**AI does this automatically:**
1. Read `docs/INDIVIDUAL_PROJECT_PAGES_WORKFLOW.md` — full checklist
2. Copy images from folder to repo root with SEO filenames
3. Create build script (`build/scripts/pages/build_[project_name].py`)
4. Update sitemap (add URL, increment count)
5. Add redirect rules to `_redirects` (2 lines: with/without trailing slash)
6. Add blog internal link (`build/data/blog/case_studies.json` featured_projects)
7. Add breadcrumb mapping (`public_business_rules.py`)
8. Commit locally → working tree clean
9. **STOP** — wait for owner to say "push to redesign"

**Files AI touches:** `_redirects`, `build_sitemap.py`, `build_all.py`, `public_business_rules.py`, `case_studies.json`, new build script, repo root images

---

### Workflow B: Edit Existing 13 Pages (Protected by Default)
**When you say:** *"I want to change [specific thing on [page name]]"* — explicit request required

**AI does NOT touch these unless you explicitly ask:**
- All 13 generated `.html` pages (index.html, blog.html, gallery_*.html, etc.)
- `build/chrome/top.html` (main navigation)
- `build/chrome/site_css.html` (site-wide CSS)

**These have byte-for-byte ranking signals from Google.** Only edit when you say exactly what to change on which page.

---

## Deployment Protocol — Individual Project Pages Workflow

**Repeatable cycle for each new project page:**

1. **Development on `redesign` branch:** Work locally, generate HTML, commit to `redesign` (local only)
2. **Owner review/approval:** When satisfied with the page, say "push [page name] to production" or "live push"
3. **Merge to master:** That specific page gets merged/pushed to `master` → deploys live to sdhardwoods.com
4. **Return to `redesign`:** Next project page starts fresh on `redesign` branch

This cycle repeats many times as you build out your SEO footprint. Each completed page:
- Gets its own indexed URL with keyword-rich content
- Links from the blog page's featured_projects section (stacking up over time)
- Expands Google's discovery of San Diego Hardwoods' individual project work

| Branch | Where It Deploys | When to Use |
|--------|------------------|-------------|
| `redesign` | Preview only (`sd-hardwoods-preview.sandiegohardwoods.workers.dev`) | Development, testing, local commits for new pages |
| `master` | Production live site (`www.sdhardwoods.com`) | **Only when owner explicitly says "push to production" or "live push"** |

### CRITICAL BRANCH RULE (Effective Immediately)

- **All development commits default to `redesign` branch only** — never touch master during page creation
- **NEVER push to `master` unless the owner explicitly says "push to production," "go live," or "merge to master"**
- When a page is approved for production: merge that commit to `master`, then immediately return to `redesign` for next page

---

## Quick Start Phrases for New Sessions

- *"Resume Muirlands deployment"* → Push committed page to preview
- *"Add [folder] as new showcase page"* → Follow Workflow A automatically
- *"I want to change [specific thing on [page name]]"* → Edit existing 13 pages (Workflow B)

---

## Reference Documents

| Document | When to Read |
|----------|--------------|
| `docs/NEXT_SESSION.md` | **Every session — first read** |
| `docs/INDIVIDUAL_PROJECT_PAGES_WORKFLOW.md` | Workflow A (new project pages) |
| `docs/PROJECT_DECISIONS.md` | Standing rules, protection policy |

---

## Session Protocol — Auto-Documentation Rule

**At the end of EVERY session:**
1. Update `docs/NEXT_SESSION.md` with what you did and what's ready for next session (overwrite the "Current State" section at top)
2. Ask owner: *"Do you want to commit these changes?"*

**Why:** One living document, no bloat from 50 separate reports. Next session reads `NEXT_SESSION.md` → knows exactly what was done and what's next. Continuity flows naturally without re-learning.

---

## Goal for San Diego Hardwoods

Expand SEO footprint with individual project showcase pages → regain ranking lost during legacy-to-modern site cutover. Keep existing 13-page core protected unless owner explicitly requests changes.
