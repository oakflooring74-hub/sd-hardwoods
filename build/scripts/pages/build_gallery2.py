# -*- coding: utf-8 -*-
import sys, json
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble, gallery_progress_html

DATA = BUILD / "data" / "recent_project_photo_gallery_2"

with open(DATA / "modules.json", encoding="utf-8") as f:
    data = json.load(f)

with open(DATA / "vcard.txt", encoding="utf-8") as f:
    VCARD = f.read().strip()

with open(DATA / "jsonld.html", encoding="utf-8") as f:
    JSONLD = f.read()

HEAD_META = """<title>Recent Hardwood Flooring Projects | Refinishing, Installation &amp; Repair | San Diego</title>
<meta name="DESCRIPTION" content="Browse recent San Diego hardwood floor refinishing, installation, repair, and restoration projects featuring dust containment sanding, deep cleaning, wire-brushed and oil-finished floors, custom stains, bamboo, and engineered hardwood. Explore our craftsmanship and discuss your project with an expert">
<link href="https://www.sdhardwoods.com/recent_project_photo_gallery_2.html" rel="canonical">
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

# Milestone 2.4: obsolete Universal Analytics (UA-20793161-1 / _gaq / ga.js) removed
# site-wide. GA4 is blocked pending the owner's confirmed Measurement ID.
GA = ""

def esc(s):
    return (s or "").replace('"', "&quot;")

# Patch: module 8 (index 8) is a broken source fragment -- its real descriptive title (#27,
# Rancho Santa Fe & Bird Rock) landed on the separate, image-less module at index 7 due to a
# malformed <li> in the live source (title and images split across duplicate/empty <li> fragments).
# Borrow that title here rather than dropping the project or its 2 real images.
modules = list(data["modules"])
modules[8] = dict(modules[8])
modules[8]["title"] = modules[7]["title"]

CTA_FILTER_STRINGS = ["BUTTON", "ultra clean button"]

def is_cta(img):
    s = (img["src"] or "")
    return "BUTTON" in s.upper() or "ultra clean button" in s.lower()

def module_html(m, idx):
    imgs = [i for i in m["images"] if not is_cta(i)]
    if len(imgs) < 2:
        return ""
    a, b = imgs[0], imgs[1]
    title = m["title"] or f"Project {idx+1}"

    # Modules 7/8 are a special case: two independent project photos (not a before/after pair
    # of the same floor) -- label with their own alt text instead of generic "Before"/"After".
    special = (idx == 8)

    def fig(img, label):
        src = img["src"]
        href = img["href"] or src
        cls = img["class"] or ""
        cls_attr = f' class="{esc(cls)}"' if cls.strip() else ""
        alt = img["alt"] if (special and img["alt"]) else f"{strip_html(title)} — {label}"
        return f'<figure><a href="{href}"><img src="{src}" alt="{esc(alt)}"{cls_attr} loading="lazy"></a><figcaption>{label}</figcaption></figure>'

    if special:
        return f"""
<div class="card" style="margin-bottom:24px;">
  <h3>{title}</h3>
  <div class="gallery" style="grid-template-columns:repeat(2,1fr);">
    {fig(a, "Bird Rock")}
    {fig(b, "Rancho Santa Fe")}
  </div>
</div>"""
    return f"""
<div class="card" style="margin-bottom:24px;">
  <h3>{title}</h3>
  <div class="gallery" style="grid-template-columns:repeat(2,1fr);">
    {fig(a, "Before")}
    {fig(b, "After")}
  </div>
</div>"""

import re as _re
def strip_html(s):
    return _re.sub(r"<[^>]+>", "", s or "")

SKIP_INDICES = {7, 9, 10}  # empty/duplicate fragments from the broken source region
modules_html = "\n".join(
    module_html(m, i) for i, m in enumerate(modules) if i not in SKIP_INDICES
)

MAIN = f"""
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Recent Hardwood Flooring Projects Throughout San Diego County</h1>
  <p>Browse recent San Diego hardwood floor refinishing, installation, repair, and restoration projects featuring dust containment sanding, deep cleaning, wire-brushed and oil-finished floors, custom stains, bamboo, and engineered hardwood.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>

<section class="block">
  <div class="card cta-card">
    <div class="cta-copy">
      <h3>Not Every Hardwood Floor Needs Refinishing</h3>
      <p>Many hardwood floors can be dramatically improved without sanding. Our Bona Power Scrubber deep cleaning system removes years of embedded dirt and residue before applying a protective low-VOC maintenance recoat when appropriate.</p>
      <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">San Diego Floor Deep Cleaning Service &rarr;</a></p>
    </div>
  </div>
</section>

<section class="block">
  <div class="gallery-intro">
    <h2>Recent Before &amp; After Hardwood Floor Projects</h2>
  </div>
  {gallery_progress_html(1)}
  {modules_html}

  <div class="cta-row" style="justify-content:center;flex-wrap:wrap;gap:16px;margin-top:20px;">
    <a class="btn btn-outline" href="https://www.sdhardwoods.com/recent_project_photo_gallery_3.html">Next Page: Project Gallery 3 &rarr;</a>
    <a class="btn btn-call" href="tel:+18586990072">Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Recent Hardwood Flooring Projects", MAIN,
         str(BUILD.parent / "recent_project_photo_gallery_2.html"))
