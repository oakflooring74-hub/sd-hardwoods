import sys
from pathlib import Path

# build/scripts/common/assemble_page.py -> build/chrome
CHROME = str(Path(__file__).resolve().parent.parent.parent / "chrome")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

# The 5 before/after project-gallery pages, in browsing order, for the shared
# "jump to gallery" progress indicator (recent_project_gallery_5's filename is the
# one page in this set that doesn't follow the "..._photo_gallery_N" naming pattern).
GALLERY_PAGES = [
    ("https://www.sdhardwoods.com/recent_project_photo_gallery_1.html", "Gallery 1"),
    ("https://www.sdhardwoods.com/recent_project_photo_gallery_2.html", "Gallery 2"),
    ("https://www.sdhardwoods.com/recent_project_photo_gallery_3.html", "Gallery 3"),
    ("https://www.sdhardwoods.com/recent_project_photo_gallery_4.html", "Gallery 4"),
    ("https://www.sdhardwoods.com/recent_project_gallery_5.html", "Gallery 5"),
]

def gallery_progress_html(current_index):
    """Persistent 'jump to gallery' + 'Gallery N of 5' progress bar, shared across
    the 5 before/after gallery pages so a visitor always knows there's more to browse."""
    total = len(GALLERY_PAGES)
    dots = []
    for i, (href, label) in enumerate(GALLERY_PAGES):
        cls = ' class="active"' if i == current_index else ""
        aria = ' aria-current="page"' if i == current_index else ""
        dots.append(f'<a href="{href}"{cls}{aria} aria-label="{label}">{i + 1}</a>')

    if current_index > 0:
        prev_href = GALLERY_PAGES[current_index - 1][0]
        prev_html = f'<a class="gp-prev" href="{prev_href}">&larr; Prev</a>'
    else:
        prev_html = '<span class="gp-disabled">&larr; Prev</span>'

    if current_index < total - 1:
        next_href = GALLERY_PAGES[current_index + 1][0]
        next_html = f'<a class="gp-next" href="{next_href}">Next &rarr;</a>'
    else:
        next_html = '<span class="gp-disabled">Next &rarr;</span>'

    return f'''<nav class="gallery-progress" aria-label="Gallery pages">
  {prev_html}
  <div class="gp-dots">
    {"".join(dots)}
  </div>
  <span class="gp-label">Gallery {current_index + 1} of {total}</span>
  {next_html}
</nav>'''

def assemble(head_meta_html, jsonld_html, ga_html, vcard_desc, scroll_topic, main_html, out_path):
    site_css = read(CHROME + r"\site_css.html")
    dm_scripts = read(CHROME + r"\darkmode_boot_scripts.html")
    top = read(CHROME + r"\top.html").replace("__VCARD_DESC__", vcard_desc)
    footer = read(CHROME + r"\footer.html")
    scrollhint = read(CHROME + r"\scrollhint_and_toggle.html").replace("__SCROLL_TOPIC__", scroll_topic)
    lightbox = read(CHROME + r"\lightbox.html")

    doc = f"""<!DOCTYPE html><html lang="en">
<head xmlns="">
<meta charset="utf-8"><base href="https://www.sdhardwoods.com/">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_meta_html}
{jsonld_html}
{ga_html}
{site_css}
{dm_scripts}
</head>
<body class="lo_layout2wt" dir="ltr" spellcheck="false">
{top}
<main>
{main_html}
</main>
{footer}
{scrollhint}
{lightbox}
</body>
</html>
"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)
    print(f"Wrote {out_path} ({len(doc)} chars)")
