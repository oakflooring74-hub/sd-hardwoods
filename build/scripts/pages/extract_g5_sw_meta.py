import re
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
RAW = BUILD / "raw-source"
DATA = BUILD / "data"

for fname, label in [
    ("recent_project_gallery_5.html", "recent_project_gallery_5"),
    ("solid_wood_floor_photo_gallery.html", "solid_wood_floor_photo_gallery"),
]:
    with open(RAW / fname, encoding="utf-8", errors="replace") as f:
        html = f.read()
    tm = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    dm = re.search(r'name="DESCRIPTION"[^>]*content="([^"]*)"', html)
    cm = re.search(r'<link href="([^"]*)" rel="canonical">', html)
    vm = re.search(r'<span class="organization-name">(.*?)</span>', html, re.DOTALL)
    print("===", label, "===")
    print("title:", tm.group(1) if tm else None)
    print("desc:", dm.group(1) if dm else None)
    print("canonical:", cm.group(1) if cm else None)
    print("vcard:", vm.group(1)[:150] if vm else None)
    blocks = re.findall(r'<script type="application/ld\+json">.*?</script>', html, re.DOTALL)
    print("jsonld blocks:", len(blocks))
    with open(DATA / label / "jsonld.html", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(blocks))
    with open(DATA / label / "vcard.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(vm.group(1).strip() if vm else "")
