import re, json, sys
from pathlib import Path

# build/scripts/common/extract_gallery.py
BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
# IMPORTANT: read from the frozen raw-source snapshot, NOT the live repo-root index.html --
# the repo-root page is the *generated output* and no longer contains the original messy
# markup this script expects once the site has been rebuilt.
path = BUILD / "raw-source" / "index.html"
with open(path, encoding="utf-8") as f:
    html = f.read()

# Isolate the #zA and #zB gallery blocks
def block(html, div_id):
    start = html.index(f'<div id="{div_id}"')
    # find matching close by counting div depth from start of tag content
    idx = html.index(">", start) + 1
    depth = 1
    i = idx
    while depth > 0:
        nextopen = html.find("<div", i)
        nextclose = html.find("</div>", i)
        if nextclose == -1:
            raise Exception("no close found")
        if nextopen != -1 and nextopen < nextclose:
            depth += 1
            i = nextopen + 4
        else:
            depth -= 1
            i = nextclose + 6
    return html[idx:i-6]

zA = block(html, "zA")
zB = block(html, "zB")

img_re = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
attr_re = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
a_href_re = re.compile(r'<a\s+href="([^"]+)"[^>]*>')

def extract_images(section, label):
    results = []
    # walk through <p>...</p> blocks to associate an optional wrapping <a href>
    for pm in re.finditer(r'<p[^>]*>(.*?)</p>', section, re.DOTALL):
        p_content = pm.group(1)
        # find each img, and check if it's inside an <a href=...> that starts before it and ends after
        for im in img_re.finditer(p_content):
            img_tag = im.group(0)
            attrs = dict(attr_re.findall(img_tag))
            # find nearest preceding unmatched <a href> before this img within p_content
            preceding = p_content[:im.start()]
            a_matches = list(a_href_re.finditer(preceding))
            href = None
            if a_matches:
                # check no </a> between last <a and img start
                last_a = a_matches[-1]
                between = preceding[last_a.end():]
                if '</a>' not in between:
                    href = last_a.group(1)
            results.append({
                "section": label,
                "src": attrs.get("src", ""),
                "alt": attrs.get("alt", ""),
                "class": attrs.get("class", ""),
                "width": attrs.get("width"),
                "height": attrs.get("height"),
                "href": href,
            })
    return results

imgs = extract_images(zA, "zA") + extract_images(zB, "zB")
print(f"Total images extracted: {len(imgs)}", file=sys.stderr)
with open(BUILD / "data" / "index" / "gallery.json", "w", encoding="utf-8") as f:
    json.dump(imgs, f, indent=2, ensure_ascii=False)

# sanity check: no duplicated/missing alt text vs raw count of <img in section
raw_count = len(img_re.findall(zA)) + len(img_re.findall(zB))
print(f"raw <img> count in zA+zB: {raw_count}", file=sys.stderr)
