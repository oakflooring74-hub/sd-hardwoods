import sys
from pathlib import Path

# build/scripts/common/assemble_page.py -> build/chrome
CHROME = str(Path(__file__).resolve().parent.parent.parent / "chrome")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def assemble(head_meta_html, jsonld_html, ga_html, vcard_desc, scroll_topic, main_html, out_path):
    site_css = read(CHROME + r"\site_css.html")
    dm_scripts = read(CHROME + r"\darkmode_boot_scripts.html")
    top = read(CHROME + r"\top.html").replace("__VCARD_DESC__", vcard_desc)
    footer = read(CHROME + r"\footer.html")
    scrollhint = read(CHROME + r"\scrollhint_and_toggle.html").replace("__SCROLL_TOPIC__", scroll_topic)

    doc = f"""<!DOCTYPE html><html lang="en">
<head xmlns="">
<meta charset="utf-8"><base href="https://www.sdhardwoods.com/">
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
</body>
</html>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Wrote {out_path} ({len(doc)} chars)")
