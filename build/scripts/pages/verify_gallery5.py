import re
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
raw_path = BUILD / "raw-source" / "recent_project_gallery_5.html"
new_path = BUILD.parent / "recent_project_gallery_5.html"

with open(raw_path, encoding="utf-8") as f:
    raw = f.read()
with open(new_path, encoding="utf-8") as f:
    new = f.read()

img_re = re.compile(r'<img\b', re.IGNORECASE)

raw_img = len(img_re.findall(raw))
new_img = len(img_re.findall(new))

ldjson_new = new.count('application/ld+json')
triple_backtick = new.count('```')
footer_count = len(re.findall(r'<footer\b', new))
mega_count = new.count('id="sdhMegaNav"')
toggle_count = new.count('id="sdh-toggle"')

title_raw = re.search(r'<title>(.*?)</title>', raw, re.DOTALL).group(1).strip()
title_new = re.search(r'<title>(.*?)</title>', new, re.DOTALL).group(1).strip()

gaq_new = new.count('_gaq')

out = BUILD / "data" / "recent_project_gallery_5" / "verify_report.txt"
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(f"raw <img> count: {raw_img}\n")
    f.write(f"new <img> count: {new_img}\n")
    f.write(f"MATCH: {raw_img == new_img}\n\n")
    f.write(f"new application/ld+json count: {ldjson_new}\n")
    f.write(f"triple backtick count in new: {triple_backtick}\n")
    f.write(f"<footer count in new: {footer_count}\n")
    f.write(f"sdhMegaNav id count in new: {mega_count}\n")
    f.write(f"sdh-toggle id count in new: {toggle_count}\n\n")
    f.write(f"title_raw: {title_raw!r}\n")
    f.write(f"title_new: {title_new!r}\n")
    f.write(f"title MATCH: {title_raw == title_new}\n\n")
    f.write(f"_gaq occurrences in new (should be >0, present in raw): {gaq_new}\n")
