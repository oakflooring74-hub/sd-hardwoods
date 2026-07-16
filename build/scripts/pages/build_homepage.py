# -*- coding: utf-8 -*-
import re, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from assemble_page import assemble

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
RAW = BUILD / "raw-source" / "index.html"
DATA = BUILD / "data" / "index"

with open(RAW, encoding="utf-8") as f:
    raw = f.read()

title = re.search(r"<title>(.*?)</title>", raw, re.DOTALL).group(1)
canonical = re.search(r'<link href="([^"]+)" rel="canonical">', raw).group(1)
vcard_desc = re.search(r'<span class="organization-name">(.*?)</span>', raw, re.DOTALL).group(1).strip()
jsonld_blocks = re.findall(r'<script type="application/ld\+json">.*?</script>', raw, re.DOTALL)
# homepage carries no _gaq Google Analytics script in the live source (confirmed) -- leave GA empty

HEAD_META = f"""<title>{title}</title>
<link href="{canonical}" rel="canonical">
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

JSONLD = "\n".join(jsonld_blocks)
GA = ""

with open(DATA / "gallery.json", encoding="utf-8") as f:
    imgs = json.load(f)

def esc(s):
    return (s or "").replace('"', "&quot;")

figs = []
for im in imgs:
    src = im["src"]
    alt = esc(im["alt"])
    cls = im["class"]
    href = im["href"] or src
    cls_attr = f' class="{esc(cls)}"' if cls else ""
    figs.append(f'<figure><a href="{href}"><img src="{src}" alt="{alt}"{cls_attr} loading="lazy"></a></figure>')
gallery_html = "\n".join(figs)

with open(DATA / "main_content.html", encoding="utf-8") as f:
    main_template = f.read()

MAIN = main_template.replace("__GALLERY_GRID__", gallery_html)

assemble(HEAD_META, JSONLD, GA, vcard_desc, "Real Hardwood Floor Projects", MAIN,
         str(BUILD.parent / "index.html"))
