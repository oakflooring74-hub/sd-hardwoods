# -*- coding: utf-8 -*-
import sys, json
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble

DATA = BUILD / "data" / "solid_wood_floor_photo_gallery"

with open(DATA / "images.json", encoding="utf-8") as f:
    images = json.load(f)

with open(DATA / "vcard.txt", encoding="utf-8") as f:
    VCARD = f.read().strip()

HEAD_META = """<title>San Diego Solid &amp; Engineered Wood Floor Installation, Refinishing, Repairs &amp; Dustless Sanding</title>
<link href="https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html" rel="canonical">
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

JSONLD = ""  # original solid_wood_floor_photo_gallery page has no JSON-LD block (confirmed)
GA = ""      # original page has no _gaq Google Analytics script either (confirmed) -- leave both out

def esc(s):
    return (s or "").replace('"', "&quot;")

figs = []
for im in images:
    href = im["href"] or im["src"]
    cls = im.get("class") or ""
    cls_attr = f' class="{esc(cls)}"' if cls.strip() else ""
    figs.append(f'<figure><a href="{href}"><img src="{im["src"]}" alt="{esc(im["alt"])}"{cls_attr} loading="lazy"></a></figure>')
gallery_html = "\n".join(figs)

MAIN = f"""
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Solid &amp; Engineered Wood Floor Installation, Refinishing, Repairs &amp; Dustless Sanding</h1>
  <p>Custom nail-down and glue-down hardwood installation throughout San Diego County, alongside our dustless refinishing, repair, and restoration services.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:8586990072">&#9742; Call or Text 858-699-0072</a>
  </div>
</section>

<section class="block">
  <div class="gallery-intro">
    <h2>Solid Wood Floor Installation Projects</h2>
  </div>
  <div class="gallery">
{gallery_html}
  </div>

  <div class="cta-row" style="justify-content:center;margin-top:20px;">
    <a class="btn btn-call" href="tel:858-699-0072">Call or Text Now: 858-699-0072</a>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Solid Wood Floor Installation Projects", MAIN,
         str(BUILD.parent / "solid_wood_floor_photo_gallery.html"))
