import re, json
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
path = BUILD / "raw-source" / "solid_wood_floor_photo_gallery.html"
with open(path, encoding="utf-8") as f:
    html = f.read()

start = html.index('<div id="bd"')
end = html.index('<div id="ft"')
region = html[start:end]

img_re = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
attr_re = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
a_href_re = re.compile(r'<a\s+[^>]*?href="([^"]+)"[^>]*>')

# figure out which zone (zA/zB/zC) each image is in, based on nearest preceding zone div id
zone_positions = []
for zid in ("zA", "zB", "zC"):
    m = re.search(r'<div id="%s"' % zid, region)
    if m:
        zone_positions.append((m.start(), zid))
zone_positions.sort()

def zone_for(pos):
    zone = None
    for zpos, zid in zone_positions:
        if zpos <= pos:
            zone = zid
        else:
            break
    return zone

results = []
for im in img_re.finditer(region):
    img_tag = im.group(0)
    attrs = dict(attr_re.findall(img_tag))
    preceding = region[max(0, im.start()-1000):im.start()]
    a_matches = list(a_href_re.finditer(preceding))
    href = None
    if a_matches:
        last_a = a_matches[-1]
        between = preceding[last_a.end():]
        if '</a>' not in between:
            href = last_a.group(1)
    results.append({
        "zone": zone_for(im.start()),
        "src": attrs.get("src", ""),
        "alt": attrs.get("alt", ""),
        "class": attrs.get("class"),
        "href": href,
    })

DATA = BUILD / "data" / "solid_wood_floor_photo_gallery"
with open(DATA / "images.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

raw_full = len(img_re.findall(html))
region_count = len(img_re.findall(region))
with open(DATA / "extraction_report.txt", "w", encoding="utf-8") as f:
    f.write(f"Extracted images (bd..ft region): {len(results)}\n")
    f.write(f"raw <img> count in bd..ft region: {region_count}\n")
    f.write(f"raw <img> count in ENTIRE raw-source/solid_wood_floor_photo_gallery.html (incl old nav/footer): {raw_full}\n")
    from collections import Counter
    c = Counter(r["zone"] for r in results)
    f.write(f"by zone: {dict(c)}\n")
