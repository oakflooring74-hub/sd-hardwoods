# Individual Project Showcase Pages — SEO Footprint Expansion Workflow

**Purpose:** Create individual HTML pages for specific flooring projects, each with its own keyword-rich URL, proper schema markup, and meta tags. These pages connect to the live blog page (not orphaned) so Google sees them as an expanding, interconnected content footprint while preserving all existing ranking signals on the 13-page core site.

**Last Updated:** [Current Date]  
**Status:** Active workflow for post-stabilization SEO expansion

---

## Strategic Context & Constraints

### Why We're Doing This
- **Migration timeline:** Site moved from legacy Yahoo/Turbify → Cloudflare Workers in mid-July 2026 (~2.5 months ago)
- **Current state:** Site has stabilized on Google, but lost ranking on specific natural language terms that previously ranked at #1
- **Goal:** Regain ranking by expanding content footprint with individual project pages that target long-tail keywords (e.g., "walnut floor refinishing La Jolla Bing Crosby Ranch", "oak installation Del Mar hardwood")
- **Primary audience for these pages:** Google (footprint expansion), not necessarily direct traffic — but they must still look gorgeous and professional

### CRITICAL CONSTRAINTS — What We CANNOT Touch
These elements on the existing 13-page site are protected. Do NOT modify them:

| Element | Why Protected | How to Preserve |
|---------|---------------|-----------------|
| **Canonical URLs** (all 13 pages) | Google has indexed these for 2.5 months; changing = ranking churn | New pages get their own canonicals; existing pages unchanged |
| **JSON-LD schema on core pages** (`#local` LocalBusiness, Service, BreadcrumbList) | These generate rich results; breaking them loses visibility | New pages have their own fresh schema; core page schema untouched |
| **Meta titles/descriptions (all 13 pages)** | Post-launch freeze still in effect; these are ranking signals | New pages get unique metas; existing pages byte-identical |
| **H1 headings (all 13 pages)** | Protected per title/meta/H1 freeze policy | Never edit core page H1s |
| **Image alt text on existing galleries** | Already optimized; changing = risk | New pages have their own alt text; existing galleries untouched |
| **Internal link structure on core pages** | Established crawl paths | Only minimal edits to blog page to add links to new pages |

**Bottom line:** We're adding NEW content, not modifying EXISTING content. The 13-page core site remains byte-identical except for the blog page's internal link additions.

---

## Technical Architecture

### Page Structure
Each individual project page is a standalone HTML file with:
- **SEO-heavy URL:** `sdhardwoods.com/[keyword-rich-project-name].html` (e.g., `walnut-floor-refinishing-la-jolla-bing-crosby-ranch.html`)
- **Unique meta title + description** targeting specific keywords
- **Canonical URL tag** pointing to itself
- **JSON-LD schema markup** (LocalBusiness + Service/Article + ImageObject for project photos)
- **Keyword-rich paragraphs** in natural language describing the project, location, wood species, services performed
- **Before/after image grid** with proper alt text

### Connection Strategy — NOT Orphaned Pages
New pages connect to Google via:
1. **Sitemap inclusion:** Each new canonical URL added to `sitemap.xml` (auto-discovery by Google)
2. **Internal link from blog page:** Minimal edit to `build/data/blog/case_studies.json` to add a "Featured Projects" section linking to the new page
3. **No navigation wiring required:** We do NOT update the 13-page main nav — this would require editing all pages and risks ranking churn

**Google sees:** New URL → in sitemap → has internal link from established blog page → indexed as part of expanding footprint

---

## Image Handling Workflow (Wide-Angle Portrait Photos)

### Understanding Your Source Images
- **All photos taken with wide-angle lens** — long/skinny aspect ratio
- **Display vertically on website** — portrait orientation despite being landscape capture
- **No manual resizing needed** — CSS grid handles responsive behavior automatically

### Grid Layout Specifications (CSS, No Manual Resizing)
| Device | Columns | Behavior |
|--------|---------|----------|
| Desktop (≥1024px) | 3–4 wide | Test and finalize per project; default to 4 if images allow |
| Tablet (768–1023px) | ~3 wide | Auto-adjust via media query |
| Mobile (<768px) | Max 2 wide, drops to 1 if needed | Stacked vertically for readability |

**CSS Implementation:** Use `display: grid` with `grid-template-columns` and `@media` queries. No hardcoded image dimensions — images scale naturally within their grid cells.

### Image Preparation Checklist
Before adding a new project page:

| Step | Command / Action | Purpose |
|------|------------------|---------|
| 1. Copy images to repo root | From Downloads folder → `C:\Users\Andrew\Documents\GitHub\sd-hardwoods\` | Images must be in tracked location |
| 2. Get exact pixel dimensions | `/c/WINDOWS/py -c "from PIL import Image; img = Image.open('IMAGE.jpg'); print(f'{img.width}x{img.height}')"` | Write down output for HTML `width`/`height` attributes |
| 3. Verify aspect ratios match | Compare width÷height across all project images — should be similar (±10%) | Prevents one image looking stretched or having whitespace gaps |
| 4. SEO-heavy filenames | Use descriptive names like `walnut-floor-refinishing-la-jolla-before.jpg` instead of `IMG_1234.jpg` | Helps Google understand image content |

**If images have different dimensions:** Resize the smaller one to match the larger using Photoshop or similar. Keep aspect ratio locked to prevent distortion.

### SEO Alt Text Guidelines
Write natural sentences that include your main keyword once (no stuffing):

> ✅ Good: *"Hardwood floor refinishing in La Jolla — dust-contained sanding and professional refinish of walnut floors by Bona Certified Craftsman at Bing Crosby Ranch"*

> ❌ Bad: Keyword stuffing like "walnut floor La Jolla refinishing hardwood San Diego" or generic text like "floor image"

---

## SEO Keyword Requirements — Restore Lost Ranking (2026-09 Crawl Findings)

**Live site crawl analysis revealed:** You lost ranking on simple, high-intent search terms that people actually type. New project pages MUST include these missing terms naturally to restore ranking:

| Missing Term | Why It Matters | How to Include in New Pages |
|--------------|----------------|------------------------------|
| "wood floor refinisher" | High-intent short search | "As a professional wood floor refinisher serving [neighborhood]..." |
| "hardwood floor finishing" | Core service term | "We specialize in hardwood floor finishing — from sanding to final coat..." |
| "floor finishing service" | Service query | "This [location] project demonstrates our floor finishing service quality..." |
| "sanding hardwood floors" | Process-specific search | "Our dust-contained sanding hardwood floors process ensures clean workspace..." |
| "refinish wood floor" | Short, common search | "When you need to refinish wood floor in [area], this project shows the results..." |
| "[neighborhood] hardwood floor finishing" | Local + core service | "[Neighborhood] homeowners choose us for hardwood floor finishing because..." |
| "refinish wood floor [city]" | High-intent local | "To refinish wood floor San Diego, call San Diego Hardwoods — this La Jolla project proves the quality..." |

**Strategy:** Each new project page should naturally weave 3-5 of these terms into owner dictation-based paragraphs. Don't stuff — make them flow naturally within real project descriptions.

---

## Build Script Creation (One-Time Per Project)

### §3a. Owner-Dictated Project Content Workflow
1. **Owner provides verbal/written dictation** describing the project: location, wood species, room(s), damage/issues observed, services performed (specific products/processes used), and final outcome.
2. **Vision-capable session inspects ALL photos in the assigned folder** — however many exist (3–25+). Compares each frame against owner dictation to verify accuracy and selects only those that clearly show: confirmed wood species, documented damage/repair stages, and consistent lighting/color outcomes with described results. Suggests removing duplicates, blurry frames, or images contradicting dictation.
3. **All selected photos display in portrait orientation** for page consistency — landscape-ratio images (if any) are cropped to portrait via CSS grid handling per §5 specs; never displayed sideways.

### File 1: Create `build/scripts/pages/build_[project_name].py`
This Python script generates the page HTML using the existing build system. It reuses shared CSS classes to match exact site style/layout.

**Script must include:**
- SEO-heavy title + meta description (author constants, not extracted)
- Canonical URL tag pointing to own page
- **JSON-LD schema markup for Google rich results:**
  - `WebPage` entity with name/description
  - `Service` entity for the flooring work performed  
  - **5+ `ImageObject` entities** for key before/after/process photos (Google requires multiple images for rich results)
  - Connect to shared `#local` LocalBusiness via `@id` only (no duplicate business declarations)
  - All entities linked together with `@id` references
- **Keyword-rich paragraphs in natural language:** Combine owner dictation + SEO keyword requirements above — weave missing terms naturally into project descriptions
- Before/after image grid using existing CSS classes: `.hero`, `.block`, `.gallery`

**Template pattern:** Copy the structure from `build_muirlands_oak_refinishing_la_jolla.py` — this is now the proven template for all future project pages.

**Schema requirements for Google rich results:**
- At least 5 ImageObject entities with real contentUrl, url, and name fields
- WebPage entity connected to Service via `mainEntity`
- All `@id`s unique and properly linked
- No duplicate LocalBusiness declarations (reuse shared `#local` via `@id`)

### File 2: Edit `build/scripts/common/build_sitemap.py`
Add the new canonical URL to the `CANONICAL_URLS` set:
```python
"https://www.sdhardwoods.com/[seo-heavy-url].html",  # ADD THIS LINE
```

### File 3: Add to `build/scripts/build_all.py` CONFIGS list
```python
("[project_name]", "[Page Title]"),  # ADD THIS LINE
```

---

## Localhost Testing Protocol (Critical Rules)

| Rule | What It Means | Why It Matters |
|------|---------------|----------------|
| **Use HTTP server, not file://** | Always start `/c/WINDOWS/py -m http.server 8084` before opening in browser | Images won't load via file:// protocol |
| **No screenshots unless asked** | Judge layout directly in browser — don't take/read screenshots on your own | Faster workflow; you can see the real result |
| **Open localhost automatically** | Always run `start http://localhost:8084/[page].html` after making changes | User shouldn't have to manually open browser |
| **Verify images load correctly** | Check each image displays at proper dimensions with no stretching | Get actual pixel dimensions via Python/Pillow first |

---

## Deployment Workflow (Preview → Production)

### Phase 1: Local Development & Testing
| Step | Command / Action | Purpose |
|------|------------------|---------|
| 1. Make changes | Create build script, edit sitemap.py, edit build_all.py | Add new page to build system |
| 2. Regenerate page | `/c/WINDOWS/py build/scripts/pages/build_[project_name].py` | Generate the HTML file |
| 3. Start HTTP server | `/c/WINDOWS/py -m http.server 8084` | Serve files so images load correctly |
| 4. Open in browser | `start http://localhost:8084/[page].html` | Visual QA — judge directly, no screenshots unless asked |

### Phase 2: Cloudflare Preview Deployment (For Review)
| Step | Command | Purpose |
|------|---------|---------|
| 5. Commit changes | `git add -A && git commit -m "Add [project] showcase page"` | Save changes locally |
| 6. Push to redesign branch | `git checkout redesign && git merge master && git push origin redesign` | Trigger GitHub Actions preview deployment |
| 7. Wait for Actions | Check: `https://github.com/oakflooring74-hub/sd-hardwoods/actions` | Should complete in ~2 minutes with ✅ green checkmark |
| 8. View preview URL | `https://sd-hardwoods-preview.sandiegohardwoods.workers.dev/[page].html` | Client review / visual testing |

### Phase 3: Production Deployment (Go Live on sdhardwoods.com)
| Step | Command | Purpose |
|------|---------|---------|
| 9. Merge preview to master | `git checkout master && git merge redesign && git push origin master` | Trigger production deployment |
| 10. Wait for Actions | Check: `https://github.com/oakflooring74-hub/sd-hardwoods/actions` | Should complete in ~2 minutes with ✅ green checkmark |
| 11. Verify live site | `https://www.sdhardwoods.com/[page].html` (hard refresh: Ctrl+Shift+R) | Confirm changes are visible to all users |

**Important:** Production deployment assumes custom domain is already attached to Cloudflare Worker (confirmed as done on September 5, 2026).

---

## Internal Linking Strategy (SEO Boost Without Navigation Complexity)

### Option A: Link from Blog Page (Recommended — Minimal Edits)
Add a "Featured Projects" section at the top of `build/data/blog/case_studies.json`:
```json
{
  "featured_projects": [
    {
      "title": "[Project Title]",
      "url": "/[seo-heavy-url].html",
      "excerpt": "[Brief SEO-rich description]"
    }
  ]
}
```

**Why this works:** Blog page is already established in Google's crawl graph. New pages get discovered via internal link + sitemap inclusion. No nav wiring needed.

### Option B: Create Dedicated "Project Showcase" Nav Item (More Work — Skip Unless 5+ Pages)
Add to `build/chrome/top.html` navigation — but this requires updating all 13+ pages. Not recommended unless you have 5+ project pages already created.

---

## SEO Impact Summary

| Approach | Indexed URLs | Internal Links | Crawl Priority | Effort |
|----------|--------------|----------------|----------------|--------|
| Individual Pages (this workflow) | ✅ Each page = own URL | ⚠️ Connected via blog + sitemap | Medium | Moderate (one-time setup, then easy per page) |
| Blog Section Only (old approach) | ❌ One shared URL | ✅ In nav | High | Low |

**For SEO footprint expansion:** Individual pages win. Google indexes each page separately, you get 10+ indexed URLs instead of 1, and content is discoverable via sitemap even without full navigation wiring.

---

## CRITICAL: Redirect Rules for Every New Page

**Every new project page MUST have redirect rules added to `_redirects` file.** This ensures clean URLs work without `.html`:

```
/[project-name] /[project-name].html 301
/[project-name]/ /[project-name].html 301
```

**Example (Muirlands Oak):**
```
/muirlands-oak-refinishing-la-jolla /muirlands-oak-refinishing-la-jolla.html 301
/muirlands-oak-refinishing-la-jolla/ /muirlands-oak-refinishing-la-jolla.html 301
```

**Why this matters:** Without these rules, visitors typing the clean URL (without `.html`) might get a 404 error. The redirect automatically sends them to the correct `.html` version.

**When to add:** Before committing — add both lines to `_redirects` file at the end of the list.

---

## Files That Change (Only These)

| File | Purpose | When to Edit |
|------|---------|--------------|
| Repo root (`C:\Users\Andrew\Documents\GitHub\sd-hardwoods`) | New image files + generated page HTML | Always copy images here first; page auto-generated by script |
| `build/scripts/pages/build_[project_name].py` | Page generation script | One-time creation per project (I do this) |
| `build/data/blog/case_studies.json` | Blog JSON with featured projects links | Add internal link to new page here |
| `build/scripts/common/build_sitemap.py` | Sitemap URL list | Add canonical URL for each new page |
| `build/scripts/build_all.py` | Master build config list | Add project name + title per new page |
| `_redirects` | Clean URL redirect rules | **ADD 2 LINES PER NEW PAGE** (with and without trailing slash) |

**Important:** Never edit generated `.html` files directly — always use the build script to regenerate.

---

## Verification Checklist (Before Declaring Complete)

Run through this checklist after completing a new project page. All items must be ✅ green before considering the task done.

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | Images copied to repo root | `ls` in repo folder shows all image files |
| 2 | Image dimensions recorded | You wrote down width×height from Python/Pillow output |
| 3 | Build script created | File exists at `build/scripts/pages/build_[project_name].py` |
| 4 | Sitemap URL added | Search for new URL in `build_sitemap.py` CANONICAL_URLS set (count should increase by 1) |
| 5 | CONFIGS entry added | Search for project name in `build_all.py` CONFIGS list |
| 6 | Page regenerated | Generated `.html` file exists at repo root with correct filename |
| 7 | Redirect rules added | Check `_redirects` file — 2 new lines for clean URL support (with/without trailing slash) |
| 8 | Localhost test successful | Open `http://localhost:PORT/[page].html`; images load; layout matches site style |
| 9 | Grid responsive behavior verified | Resize browser window; confirm 4-wide desktop → 3-wide tablet → 1–2 wide mobile |
| 10 | Changes committed to Git | `git status` shows "nothing to commit, working tree clean" |
| 11 | Pushed to `redesign` branch | `git push origin redesign` completed without errors |
| 12 | GitHub Actions passed | Actions tab shows ✅ green checkmark for latest commit |
| 13 | Cloudflare preview updated | Visit preview URL; see new page with correct content + layout (wait ~60 seconds after Actions succeeds) |
| 14 | Internal link added to blog | Search `case_studies.json` for new page URL in featured_projects section |

**If all 13 checks pass:** Task complete. The individual project showcase page has been successfully created, deployed to production, and is indexed by Google via sitemap for SEO footprint expansion.

---

## Common Mistakes to Avoid

| Mistake | What Happens | How to Prevent |
|---------|--------------|----------------|
| **Editing generated `.html` files directly** | Changes lost on next rebuild | Always edit `build/scripts/pages/build_[project_name].py` source |
| **Using `file://` protocol locally** | Images don't load; you see alt text instead | Always run `/c/WINDOWS/py -m http.server PORT` first, then open `http://localhost:PORT` |
| **Hardcoding wrong dimensions in `<img>` tags** | Image looks stretched or squashed | Get actual pixel dimensions using Python/Pillow before editing HTML |
| **Modifying core page schema/meta/canonicals** | Loses existing ranking signals on 13-page site | New pages get their own fresh markup; existing pages byte-identical |
| **Keyword stuffing alt text or paragraphs** | Google flags as spam | Natural sentences with one keyword mention per image/paragraph |
| **Creating orphaned pages (no internal link)** | Slower discovery by Google | Always add featured_projects link to blog page + include in sitemap |
| **Pushing to wrong branch** | Cloudflare preview doesn't update | Push to `redesign` branch only — not `master`, not random test branches |

---

## Difficulty Assessment & Timeline

| Task | Difficulty | Time Estimate | Notes |
|------|------------|---------------|-------|
| First project page | ⚠️ Moderate | 30–45 minutes | Requires creating new build script template (I do this) |
| Subsequent pages | ✅ Easy | 15–20 minutes each | Copy/paste first script, swap content |
| Matching exact style/layout | ✅ Easy | Included above | Reuse existing CSS classes (.hero, .block, .before-after-grid) |
| Navigation wiring | ❌ Hard (skip it) | N/A | Requires updating 13+ pages — NOT needed for SEO discovery |

---

## What Succeeds When This Workflow Is Followed

✅ Each project gets its own indexed URL with keyword-rich content  
✅ Google sees expanding footprint via sitemap + blog internal links  
✅ Existing 13-page site ranking signals remain untouched  
✅ New pages look gorgeous with proper responsive grid layout  
✅ Wide-angle portrait photos display correctly without manual resizing  
✅ Schema markup helps Google recognize quality immediately  
✅ Long-tail keywords targeted per project (location + wood species + service)  

---

## Session Protocol — What to Do When Starting a New Project Page Session

1. **Read this document first** — `docs/INDIVIDUAL_PROJECT_PAGES_WORKFLOW.md`
2. **Ask the owner:** "What project are we adding today?" (folder location, target keywords, wood species, neighborhood)
3. **Confirm image preparation complete** — images in Downloads folder, SEO-heavy filenames chosen
4. **Follow the workflow above** — create build script → regenerate → test locally → deploy preview → merge to master
5. **Use localhost for testing** — never `file://` protocol
6. **No screenshots unless explicitly asked** — judge directly in browser
7. **Deploy to preview first** — get owner approval before production merge
8. **Document any new patterns discovered** during the session (update this doc if needed)

---

## Quick Start Phrase for Future Sessions

When starting a new project page deployment session, use this phrase to give the AI immediate context:

> **"Add [project name] individual showcase page from folder [folder path]. All images ready with SEO filenames. Follow established workflow: build script → sitemap (14+ URLs) → redirect rules → blog link (#XX) → commit → push to redesign for preview deployment."**

**Example:**
> *"Add Muirlands Oak individual showcase page from folder MUIRLANDS OAK FLOOR REFINISHING LA JOLLA SAN DIEGO WATERMARKED. All 28 images ready with SEO filenames. Follow established workflow: build script → sitemap (14 URLs) → redirect rules → blog link (#13) → commit → push to redesign for preview deployment."*

This phrase tells the AI exactly what to do without re-reading all documentation.

---

## Future Work Types & How They Relate

| Work Type | Relationship to This Workflow | Files Involved |
|-----------|-------------------------------|----------------|
| **Simple image swap on existing pages** | Separate workflow — doesn't create new URLs | `build/data/[page]/main_content.html`, `site_css.html` |
| **Adding photos to existing galleries** | Separate workflow — adds to current gallery JSON files | `build/data/gallery_X/modules.json` or `projects.json` |
| **New blog case studies (old approach)** | Superseded by this workflow for SEO footprint goals | `build/data/blog/case_studies.json` only |
| **Individual project pages (this doc)** | Primary workflow for SEO expansion going forward | Build script + sitemap.py + build_all.py + case_studies.json |

---

**Last verified:** [Current Date] — Full deployment workflow documented and ready for immediate use. All tools, credentials, and workflows recorded for future sessions.
