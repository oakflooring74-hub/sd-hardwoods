import re, json, sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
path = BUILD / "raw-source" / "recent_project_gallery_5.html"
with open(path, encoding="utf-8") as f:
    html = f.read()

# Content region: from <body to the old footer div id="ft" (exclusive), i.e. everything
# that is page-specific gallery/CTA content (excludes old header vcard block and old nav/footer).
start = html.index('<div id="bd"')
end = html.index('<div id="ft"')
region = html[start:end]

img_re = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
attr_re = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
a_href_re = re.compile(r'<a\s+[^>]*?href="([^"]+)"[^>]*>')

results = []
for im in img_re.finditer(region):
    img_tag = im.group(0)
    attrs = dict(attr_re.findall(img_tag))
    preceding = region[max(0, im.start()-800):im.start()]
    a_matches = list(a_href_re.finditer(preceding))
    href = None
    if a_matches:
        last_a = a_matches[-1]
        between = preceding[last_a.end():]
        if '</a>' not in between:
            href = last_a.group(1)
    # grab nearest preceding li class attr for before/after context
    li_matches = list(re.finditer(r'<li\s+class="([^"]*)"', preceding))
    li_class = li_matches[-1].group(1) if li_matches else None
    results.append({
        "src": attrs.get("src", ""),
        "alt": attrs.get("alt", ""),
        "class": attrs.get("class"),
        "href": href,
        "li_class": li_class,
    })

DATA = BUILD / "data" / "recent_project_gallery_5"
with open(DATA / "images.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

raw_full_count = len(img_re.findall(html))
region_count = len(img_re.findall(region))
with open(DATA / "extraction_report.txt", "w", encoding="utf-8") as f:
    f.write(f"Extracted images (bd..ft region): {len(results)}\n")
    f.write(f"raw <img> count in bd..ft region: {region_count}\n")
    f.write(f"raw <img> count in ENTIRE raw-source/recent_project_gallery_5.html (incl old nav/footer): {raw_full_count}\n")
