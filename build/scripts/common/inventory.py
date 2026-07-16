import re, os
from pathlib import Path

# build/scripts/common/inventory.py -> build/raw-source
RAW = Path(__file__).resolve().parent.parent.parent / "raw-source"

SLUGS = [
    "index",
    "about_us",
    "contact_us",
    "videos_of_refinishing_process",
    "recent_project_photo_gallery_1",
    "recent_project_photo_gallery_2",
    "recent_project_photo_gallery_3",
    "recent_project_photo_gallery_4",
    "recent_project_gallery_5",
    "solid_wood_floor_photo_gallery",
    "deep-cleaning-hardwood-floors-san-diego",
    "blog",
]

for slug in SLUGS:
    path = RAW / (slug + ".html")
    with open(path, encoding="utf-8", errors="replace") as f:
        html = f.read()
    title_m = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    desc_m = re.search(r'name="DESCRIPTION"[^>]*content="([^"]*)"', html)
    canon_m = re.search(r'<link href="([^"]*)" rel="canonical">', html)
    img_count = len(re.findall(r"<img\b", html))
    form_count = len(re.findall(r"<form\b", html, re.IGNORECASE))
    ldjson_count = len(re.findall(r"application/ld\+json", html))
    has_meganav = "sdhMegaNav" in html
    has_darkmode = "sdh-darkmode-boot" in html
    has_scrollhint = "sdhScrollHint" in html
    backticks = html.count("```")
    size_kb = round(len(html)/1024, 1)
    print(f"=== {slug} ({path.name}) [{size_kb}KB] ===")
    print(f"  title: {title_m.group(1).strip() if title_m else 'MISSING'}")
    print(f"  desc: {(desc_m.group(1)[:100] + '...') if desc_m else 'MISSING'}")
    print(f"  canonical: {canon_m.group(1) if canon_m else 'MISSING'}")
    print(f"  imgs={img_count} forms={form_count} ld+json={ldjson_count} meganav={has_meganav} darkmode={has_darkmode} scrollhint={has_scrollhint} backticks={backticks}")
    print()
