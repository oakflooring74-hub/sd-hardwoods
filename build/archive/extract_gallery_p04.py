import re, json, sys
sys.path.insert(0, r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad")
from gallery_extract_common import (find_balanced_blocks, extract_imgs_with_href, img_re, parse_modules,
                                     render_all_projects, figure_html)

SRC = r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad\sdh-crawl\page04.html"
OUT_JSON = r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad\gallery_p04.json"
OUT_LOG = r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad\gallery_p04.log"

with open(SRC, encoding="utf-8") as f:
    html = f.read()

log = []

modules_raw = find_balanced_blocks(html, '<li class="module beforenafter', 'li')
log.append(f"module blocks found: {len(modules_raw)}")

projects, module_img_count = parse_modules(modules_raw)
log.append(f"module images captured: {module_img_count}")

# standalone images OUTSIDE the module list (header CTA pair, deep-clean CTA, zB CTA pair)
ul_blocks = find_balanced_blocks(html, '<ul class="module_bd_container"', 'ul')
assert len(ul_blocks) == 1, f"expected exactly 1 module_bd_container ul, got {len(ul_blocks)}"
list_block = ul_blocks[0]
list_start = html.index(list_block)
list_end = list_start + len(list_block)

region_start = html.index('<div id="hd"')
region_end = html.index('<div id="ft"')
region_before_list = html[region_start:list_start]
region_after_list = html[list_end:region_end]

standalone_imgs = []
for label, seg in [("before_list", region_before_list), ("after_list", region_after_list)]:
    for raw_tag, attrs, href in extract_imgs_with_href(seg):
        standalone_imgs.append({
            "zone": label,
            "src": attrs.get("src", ""),
            "alt": attrs.get("alt", ""),
            "class": re.sub(r'\s+', ' ', attrs.get("class", "")).strip(),
            "href": href,
        })
log.append(f"standalone images captured: {len(standalone_imgs)}")

total_extracted = module_img_count + len(standalone_imgs)
raw_img_count_region = len(img_re.findall(html[region_start:region_end]))
raw_img_count_fullfile = len(img_re.findall(html))
log.append(f"raw <img> count in region (hd..ft): {raw_img_count_region}")
log.append(f"raw <img> count in FULL file: {raw_img_count_fullfile}")
log.append(f"total extracted (module+standalone): {total_extracted}")
log.append(f"MATCH: {total_extracted == raw_img_count_fullfile}")

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"projects": projects, "standalone": standalone_imgs}, f, indent=2, ensure_ascii=False)

gallery_html = render_all_projects(projects)
fig_count_in_html = gallery_html.count("<figure>")
log.append(f"<figure> count in generated gallery html (module part): {fig_count_in_html}")
log.append(f"MATCH module figs vs module_img_count: {fig_count_in_html == module_img_count}")

with open(r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad\gallery_p04.html.txt", "w", encoding="utf-8") as f:
    f.write(gallery_html)

with open(OUT_LOG, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")

print("done", file=sys.stderr)
