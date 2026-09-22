# Session Handoff — Muirlands Oak Project Page Deployment

**Date:** 2026-09  
**Status:** Ready for commit + push to `redesign`  

---

## What's Done (Verified ✅)

1. **All 28 images copied** from source folder with SEO filenames
2. **Page generated:** `muirlands-oak-refinishing-la-jolla.html` (79,582 chars)
3. **Build system updated:**
   - `build/scripts/pages/build_muirlands_oak_refinishing_la_jolla.py` — build script
   - `build/scripts/common/build_sitemap.py` — 14 canonical URLs
   - `build/scripts/build_all.py` — STEPS entry added
   - `build/scripts/common/public_business_rules.py` — breadcrumb mapping
4. **Blog internal link added:** `build/data/blog/case_studies.json` now has project #13
5. **Visual QA passed:** All 28 images load correctly at localhost:8084

---

## Next Session Steps (Deployment)

```bash
# 1. Verify all files exist
ls muirlands-oak-refinishing-la-jolla.html
ls red-oak-*.jpg la-jolla-*.jpg | wc -l  # Should be ~28

# 2. Regenerate full build to ensure consistency
python build/scripts/build_all.py

# 3. Verify sitemap has exactly 14 URLs
grep -c "<url>" sitemap.xml  # Should be 14

# 4. Commit changes
git add muirlands-oak-refinishing-la-jolla.html
git add build/scripts/pages/build_muirlands_oak_refinishing_la_jolla.py
git add build/scripts/common/build_sitemap.py
git add build/scripts/build_all.py
git add build/scripts/common/public_business_rules.py
git add build/data/blog/case_studies.json
git add blog.html
git add *.jpg  # All new SEO-named images

git commit -m "Add Muirlands Oak individual project showcase page (SEO footprint expansion)"

# 5. Push to redesign branch (auto-deploys to Cloudflare preview)
git -c credential.helper= -c "credential.helper=!gh auth git-credential" push origin redesign

# 6. Verify GitHub Actions passed
# Check: https://github.com/oakflooring74-hub/sd-hardwoods/actions

# 7. Review Cloudflare preview
# URL: https://redesign.sd-hardwoods.pages.dev/muirlands-oak-refinishing-la-jolla.html
```

---

## Critical Constraints

- ⚠️ **Title/meta/H1 freeze active** — Do NOT modify existing 13 pages
- ✅ **New page only** — Safe to proceed (adding content, not modifying)
- 📍 **Use absolute URLs** — All internal links use `https://www.sdhardwoods.com/PAGE.html`
- 🔒 **Sitemap count = 14** — Verified in this session

---

## Git State Summary

**Modified files:**
- `build/scripts/common/build_sitemap.py`
- `build/scripts/build_all.py`
- `build/scripts/common/public_business_rules.py`
- `build/data/blog/case_studies.json`
- `blog.html` (regenerated with new internal link)

**New files:**
- `muirlands-oak-refinishing-la-jolla.html` (generated)
- `build/scripts/pages/build_muirlands_oak_refinishing_la_jolla.py`
- ~28 SEO-named image files (`red-oak-*.jpg`, `la-jolla-*.jpg`, etc.)

**Branch:** `redesign` — ready for commit + push

---

## Quick Start Phrase for Next Session

> **"Muirlands oak page: 28 images copied, build scripts updated to 14 URLs, blog link added (#13), visual QA passed. Ready to commit and push to redesign branch for Cloudflare preview deployment."**
