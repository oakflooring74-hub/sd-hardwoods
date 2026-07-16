import re, json, sys
sys.path.insert(0, r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad")
from gallery_extract_common import (find_balanced_blocks, extract_imgs_with_href, img_re, parse_modules,
                                     render_all_projects, figure_html)

SRC = r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad\sdh-crawl\page09.html"
OUT_JSON = r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad\gallery_p09.json"
OUT_LOG = r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad\gallery_p09.log"

with open(SRC, encoding="utf-8") as f:
    html = f.read()

log = []

# The module list here is a top-level <li class="module beforenafter ...> sequence directly
# inside <ul class="module_bd_container" id="mbdcontainer_zA.1"> (no <div id="zA"> wrapper).
# The final entry is a stray <li class="modfieldgrp after"> (CALL button) that is a sibling of
# the module li's, not nested inside one -- find_balanced_blocks on '<li class="module
# beforenafter' won't grab it, so we handle it via the fallback scan of the whole outer <ul>.
ul_blocks = find_balanced_blocks(html, '<ul class="module_bd_container"', 'ul')
assert len(ul_blocks) == 1, f"expected exactly 1 module_bd_container ul, got {len(ul_blocks)}"
list_block = ul_blocks[0]
list_start = html.index(list_block)
list_end = list_start + len(list_block)

modules_raw = find_balanced_blocks(list_block, '<li class="module beforenafter', 'li')
log.append(f"module blocks found: {len(modules_raw)}")

projects, module_img_count = parse_modules(modules_raw)
log.append(f"module images captured: {module_img_count}")

# catch the stray trailing <li class="modfieldgrp after"> (CALL button) that sits directly in
# the outer ul, not inside any module li -- do this by diffing: scan the WHOLE list_block for
# images, subtract ones already captured via module parsing (by raw tag text).
captured_in_modules = set()
for p in projects:
    for coll in (p["before"], p["after"], p["extra_imgs"]):
        for item in coll:
            captured_in_modules.add((item["src"], item["alt"], item["href"]))

stray_imgs = []
for raw_tag, attrs, href in extract_imgs_with_href(list_block):
    key = (attrs.get("src", ""), attrs.get("alt", ""), href)
    if key in captured_in_modules:
        captured_in_modules.discard(key)  # only skip once per match
        continue
    stray_imgs.append({
        "zone": "stray_in_list",
        "src": attrs.get("src", ""),
        "alt": attrs.get("alt", ""),
        "class": attrs.get("class", ""),
        "href": href,
    })
log.append(f"stray images directly in outer <ul> (not in any module li): {len(stray_imgs)}")

# standalone images OUTSIDE the module list (header CTA pair, deep-clean CTA, zB NEXT PAGE
# button). Note: page09 also has a SECOND real-content CTA block ("deepclean-cta-bottom") that
# sits AFTER the <div id="ft"> footer-zone markup but BEFORE the legacy scroll-hint junk -- it's
# genuine page content (own h3/p copy + image), not chrome, so it must be captured too.
region_start = html.index('<div id="hd"')
region_end = html.index('<div id="ft"')
trailing_content_end = html.index('#sdhScrollHint')
trailing_style_start = html.rindex('<style>', region_end, trailing_content_end)

region_before_list = html[region_start:list_start]
region_after_list = html[list_end:region_end]
trailing_region = html[region_end:trailing_style_start]

standalone_imgs = []
for label, seg in [("before_list", region_before_list), ("after_list", region_after_list),
                    ("trailing_after_ft", trailing_region)]:
    for raw_tag, attrs, href in extract_imgs_with_href(seg):
        standalone_imgs.append({
            "zone": label,
            "src": attrs.get("src", ""),
            "alt": attrs.get("alt", ""),
            "class": re.sub(r'\s+', ' ', attrs.get("class", "")).strip(),
            "href": href,
        })
log.append(f"standalone images captured: {len(standalone_imgs)}")

total_extracted = module_img_count + len(stray_imgs) + len(standalone_imgs)
raw_img_count_region = len(img_re.findall(html[region_start:region_end]))
raw_img_count_fullfile = len(img_re.findall(html))
log.append(f"raw <img> count in region (hd..ft): {raw_img_count_region}")
log.append(f"raw <img> count in FULL file: {raw_img_count_fullfile}")
log.append(f"total extracted (module+stray+standalone): {total_extracted}")
log.append(f"MATCH: {total_extracted == raw_img_count_fullfile}")

# also verify JSON-LD block count in footer + head
ldjson_count = len(re.findall(r'<script[^>]*type="application/ld\+json"', html))
log.append(f"application/ld+json script tags in raw source: {ldjson_count}")

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"projects": projects, "stray": stray_imgs, "standalone": standalone_imgs}, f, indent=2, ensure_ascii=False)

gallery_html = render_all_projects(projects)
for s in stray_imgs:
    gallery_html += "\n" + figure_html(s, None)
fig_count_in_html = gallery_html.count("<figure>")
log.append(f"<figure> count in generated gallery html (module+stray part): {fig_count_in_html}")
log.append(f"MATCH module+stray figs: {fig_count_in_html == module_img_count + len(stray_imgs)}")

with open(r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad\gallery_p09.html.txt", "w", encoding="utf-8") as f:
    f.write(gallery_html)

with open(OUT_LOG, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")

print("done", file=sys.stderr)
