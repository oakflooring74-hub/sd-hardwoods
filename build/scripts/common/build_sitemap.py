# -*- coding: utf-8 -*-
"""Generates the repo-root sitemap.xml and robots.txt (Milestone 2.4).

sitemap.xml lists exactly the 13 approved canonical page URLs -- the 12 legacy
pages at their established .html filenames plus the new extensionless
/floor-assessments-inspections page. No lastmod is emitted: the repo has no
reliable per-page content-modification source (git history tracks regeneration,
not content change), and an invented date would be worse than none.
changefreq/priority are deliberately omitted (ignored by Google, noise otherwise).

robots.txt allows everything and points at the production sitemap. Both files
are deterministic so the CI regenerate-and-diff gate stays green.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # -> repo root

# The approved canonical URL map (Milestone 2.4). One entry per page, exactly 13.
CANONICAL_URLS = [
    "https://www.sdhardwoods.com/",
    "https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html",
    "https://www.sdhardwoods.com/recent_project_photo_gallery_1.html",
    "https://www.sdhardwoods.com/recent_project_photo_gallery_2.html",
    "https://www.sdhardwoods.com/recent_project_photo_gallery_3.html",
    "https://www.sdhardwoods.com/recent_project_photo_gallery_4.html",
    "https://www.sdhardwoods.com/recent_project_gallery_5.html",
    "https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html",
    "https://www.sdhardwoods.com/videos_of_refinishing_process.html",
    "https://www.sdhardwoods.com/about_us.html",
    "https://www.sdhardwoods.com/blog.html",
    "https://www.sdhardwoods.com/contact_us.html",
    "https://www.sdhardwoods.com/floor-assessments-inspections",
]

ROBOTS_TXT = """User-agent: *
Allow: /

Sitemap: https://www.sdhardwoods.com/sitemap.xml
"""


def main():
    assert len(CANONICAL_URLS) == 13, "canonical map must contain exactly 13 URLs"
    assert len(set(CANONICAL_URLS)) == 13, "canonical map contains a duplicate URL"
    for u in CANONICAL_URLS:
        assert u.startswith("https://www.sdhardwoods.com/"), f"non-canonical origin: {u}"

    entries = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n  </url>" for u in CANONICAL_URLS
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )

    sitemap_path = REPO_ROOT / "sitemap.xml"
    with open(sitemap_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(sitemap)
    print(f"Wrote {sitemap_path} ({len(CANONICAL_URLS)} URLs)")

    robots_path = REPO_ROOT / "robots.txt"
    with open(robots_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ROBOTS_TXT)
    print(f"Wrote {robots_path}")


if __name__ == "__main__":
    main()
