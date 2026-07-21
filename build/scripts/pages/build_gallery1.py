# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble, gallery_progress_html
from public_business_rules import build_service_page_jsonld

SCRATCH = str(BUILD)  # unused after this point but kept for reference

with open(BUILD / "data" / "recent_project_photo_gallery_1" / "modules.json", encoding="utf-8") as f:
    data = json.load(f)

with open(BUILD / "data" / "recent_project_photo_gallery_1" / "vcard.txt", encoding="utf-8") as f:
    VCARD = f.read().strip()

HEAD_META = """<title>Hardwood Floor Refinishing Gallery | San Diego Before &amp; After Photos</title>
<meta name="description" content="View before and after hardwood floor refinishing projects completed throughout San Diego County. See dustless sanding, hardwood floor repairs, engineered hardwood refinishing, color changes, floor restoration, deep cleaning, and oiled floor upgrades completed in La Jolla, Del Mar, Mission Hills, Rancho Santa Fe, Encinitas, Carmel Valley, and nearby communities. Call or text 858-699-0072 for a professional phone consultation and expert floor evaluation.">
<link href="https://www.sdhardwoods.com/recent_project_photo_gallery_1.html" rel="canonical">
<link href="/favicon.ico" rel="icon" type="image/x-icon">
<link href="/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="/LOGO-2025.png" rel="logo" type="image/png">
<link href="/assets/legacy-css/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="/assets/legacy-css/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

# Schema milestone (2026-07-19): original page had no JSON-LD block at all
# (confirmed via inventory scan) -- built from this page's own real, already
# -approved meta description and project-heading locations, not invented.
JSONLD = build_service_page_jsonld(
    page_url="https://www.sdhardwoods.com/recent_project_photo_gallery_1.html",
    page_id_slug="service",
    page_name="Hardwood Floor Refinishing Gallery | San Diego Before & After Photos",
    page_description="View before and after hardwood floor refinishing projects completed throughout San Diego County. See dustless sanding, hardwood floor repairs, engineered hardwood refinishing, color changes, floor restoration, deep cleaning, and oiled floor upgrades completed in La Jolla, Del Mar, Mission Hills, Rancho Santa Fe, Encinitas, Carmel Valley, and nearby communities.",
    service_name="Hardwood Floor Refinishing, Sanding, Repair & Restoration Proof Gallery",
    service_description="Real before-and-after hardwood floor refinishing, dustless sanding, repair, restoration, and deep-cleaning projects completed throughout San Diego County.",
    service_types=[
        "Dustless hardwood floor sanding", "Hardwood floor refinishing",
        "Hardwood floor repairs", "Engineered hardwood refinishing",
        "Hardwood floor color changes", "Floor restoration",
        "Hardwood floor deep cleaning", "Oiled floor upgrades",
    ],
    area_served=[
        "San Diego County", "La Jolla", "Del Mar", "Mission Hills",
        "Rancho Santa Fe", "Encinitas", "Carmel Valley", "Solana Beach",
        "Golden Hill", "Hillcrest", "Bankers Hill", "South Park",
        "Mission Valley", "Point Loma", "Downtown San Diego",
    ],
    offer_catalog_name="Refinishing, Repair & Restoration Project Types Shown",
    offer_items=[
        ("Dustless Sanding & Refinishing", "Dust-contained sanding and refinishing shown in real before-and-after project pairs."),
        ("Hardwood Floor Repairs", "Board and finish repairs shown in real completed San Diego projects."),
        ("Engineered Hardwood Refinishing & Color Changes", "Refinishing and color-change transformations of engineered hardwood floors."),
        ("Floor Restoration & Deep Cleaning", "Restoration and deep-cleaning projects shown alongside full refinishing work."),
        ("Oiled Floor Upgrades", "Upgrades and conversions of oil-finished hardwood floors."),
    ],
)

# Milestone 2.4: obsolete Universal Analytics (UA-20793161-1 / _gaq / ga.js) removed
# site-wide. GA4 is blocked pending the owner's confirmed Measurement ID.
GA = ""

def esc(s):
    return (s or "").replace('"', "&quot;")

def module_html(m, idx):
    imgs = [i for i in m["images"] if "ultra%20clean" not in (i["src"] or "") and "BUTTON" not in (i["src"] or "").upper()]
    if len(imgs) < 2:
        return ""
    before, after = imgs[0], imgs[1]
    title = m["title"] or f"Project {idx+1}"
    def fig(img, label):
        src = img["src"]
        href = img["href"] or src
        cls = img["class"] or ""
        cls_attr = f' class="{esc(cls)}"' if cls.strip() else ""
        # Alt-text recomposition (Milestone 2.13): modules.json's per-image "alt" field
        # is now the complete, ready-to-render alt -- image-specific detail (Before/After
        # + project number + visible condition/process/result) leads, with the shared
        # project context merged in naturally and deduplicated by hand. It is used as-is,
        # not reassembled from title/label/caption at build time (see docs/2026-07-image-
        # alt-recomposition-report.md for the full rationale and per-project ledger).
        alt = (img.get("alt") or "").strip()
        return f'<figure><a href="{href}"><img src="{src}" alt="{esc(alt)}"{cls_attr} loading="lazy"></a><figcaption>{label}</figcaption></figure>'
    return f"""
<div class="card" style="margin-bottom:24px;">
  <h3>{title}</h3>
  <div class="gallery" style="grid-template-columns:repeat(2,1fr);">
    {fig(before, "Before")}
    {fig(after, "After")}
  </div>
</div>"""

modules_html = "\n".join(module_html(m, i) for i, m in enumerate(data["modules"]))

MAIN = f"""
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Hardwood Floor Refinishing Before &amp; After Gallery</h1>
  <p>Explore real San Diego hardwood floor refinishing projects featuring dust-contained floor sanding, hardwood floor repairs, deep cleaning, restoration, color changes, custom stain work, and dramatic before-and-after transformations completed by San Diego Hardwoods throughout San Diego County.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>

<section class="block">
  <div class="card cta-card">
    <div class="cta-copy">
      <h3>Not Every Hardwood Floor Needs Refinishing</h3>
      <p>Many hardwood floors can be dramatically improved without sanding. Our Bona Power Scrubber deep cleaning system removes years of embedded dirt, contaminants, and residue before applying a protective low-VOC maintenance recoat when appropriate.</p>
      <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">Learn When Deep Cleaning Is Better Than Refinishing &rarr;</a></p>
    </div>
  </div>
</section>

<section class="block">
  <div class="gallery-intro">
    <h2>Recent Before &amp; After Hardwood Floor Projects</h2>
  </div>
  {gallery_progress_html(0)}
  {modules_html}

  <div class="cta-row" style="justify-content:center;flex-wrap:wrap;gap:16px;margin-top:20px;">
    <a class="btn btn-outline" href="https://www.sdhardwoods.com/recent_project_photo_gallery_2.html">Next Page: Project Gallery 2 &rarr;</a>
    <a class="btn btn-call" href="tel:+18586990072">Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>

<section class="block">
  <div class="card cta-card">
    <div class="cta-copy">
      <h3>See Whether Deep Cleaning Could Save You From a Full Refinish</h3>
      <p>San Diego hardwood floor deep cleaning and polishing service — often the right call before committing to a full dust-contained sand and refinish.</p>
      <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">Professional Hardwood Floor Deep Cleaning &rarr;</a></p>
    </div>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Before &amp; After Project Photos", MAIN,
         str(BUILD.parent / "recent_project_photo_gallery_1.html"))
