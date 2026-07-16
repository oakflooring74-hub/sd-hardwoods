import re
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
path = BUILD / "raw-source" / "recent_project_gallery_5.html"
with open(path, encoding="utf-8") as f:
    html = f.read()

# 1) head VideoObject ld+json
m1 = re.search(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "VideoObject".*?</script>', html, re.DOTALL)

# 2) the footer line containing FlooringContractor / Organization / Service array (single physical line)
lines = html.split('\n')
footer_line = None
for ln in lines:
    if 'FlooringContractor' in ln and 'application/ld+json' in ln:
        footer_line = ln
        break

# 3) the _gaq analytics script (single physical line region between markers)
idx_gaq_start = html.index('var _gaq = _gaq || [];')
# back up to the <script tag start
script_open = html.rfind('<script', 0, idx_gaq_start)
idx_gaq_end = html.index('</script>', idx_gaq_start) + len('</script>')
gaq_block = html[script_open:idx_gaq_end]

out = BUILD / "data" / "recent_project_gallery_5" / "jsonld_extracted_annotated.txt"
with open(out, "w", encoding="utf-8") as f:
    f.write("=== VIDEO_OBJECT ===\n")
    f.write(m1.group(0) if m1 else "NOT FOUND")
    f.write("\n\n=== FOOTER_LINE (contains 3 script tags) ===\n")
    f.write(footer_line if footer_line else "NOT FOUND")
    f.write("\n\n=== GAQ_BLOCK ===\n")
    f.write(gaq_block)
    f.write("\n\n=== COUNTS ===\n")
    f.write(f"total 'application/ld+json' occurrences in raw file: {html.count('application/ld+json')}\n")
    if footer_line:
        f.write(f"'application/ld+json' occurrences in footer line: {footer_line.count('application/ld+json')}\n")
