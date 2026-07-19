# -*- coding: utf-8 -*-
"""
Solid Wood Floor Photo Gallery builder (Milestone 2.1 rebuild).

Restores the raw source's original four-project structure -- each installation
project with its own heading, description, and only its own images -- from
data/solid_wood_floor_photo_gallery/projects.json, instead of the previous
single undifferentiated photo grid. Image alt text is joined in from
images.json (the frozen extraction, kept byte-identical). The four legacy
image-button records (NEXT PAGE / CONTACT US / ABOUT US / HOME) are
deliberately excluded from generated output.
"""
import sys, json
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble
from public_business_rules import build_service_page_jsonld, PRIORITY_COASTAL_SD

DATA = BUILD / "data" / "solid_wood_floor_photo_gallery"

with open(DATA / "images.json", encoding="utf-8") as f:
    images = json.load(f)
ALT = {im["src"]: im["alt"] for im in images}

with open(DATA / "projects.json", encoding="utf-8") as f:
    pdata = json.load(f)
PROJECTS = pdata["projects"]
INTRO = pdata["intro"]
SOURCING = pdata["sourcing"]
# Milestone 2.9: the South Orange County sentence added in 2.8 is removed --
# per owner direction, OC appears only in the shared #local schema entity,
# never in visible copy. OUTRO is the original, frozen-extraction text.
OUTRO = pdata["outro"]

# every image referenced by a project must exist in the frozen extraction
for p in PROJECTS:
    for src in p["images"]:
        assert src in ALT, f"projects.json references unknown image {src}"

with open(DATA / "vcard.txt", encoding="utf-8") as f:
    VCARD = f.read().strip()

HEAD_META = """<title>San Diego Solid &amp; Engineered Wood Floor Installation, Refinishing, Repairs &amp; Dustless Sanding</title>
<meta name="description" content="See solid and unfinished engineered hardwood installations in San Diego, including nail-down, glue-down, sanding and custom finishing.">
<link href="https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html" rel="canonical">
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

# Schema milestone (2026-07-19): the original page had no JSON-LD block at
# all (confirmed) -- this adds one, built entirely from this page's own real
# content (INTRO/SOURCING/OUTRO above, project headings), not invented.
JSONLD = build_service_page_jsonld(
    page_url="https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html",
    page_id_slug="service",
    page_name="San Diego Solid & Engineered Wood Floor Installation, Refinishing, Repairs & Dustless Sanding",
    page_description="See solid and unfinished engineered hardwood installations in San Diego, including nail-down, glue-down, sanding and custom finishing.",
    service_name="Solid & Unfinished Engineered Wood Floor Installation",
    service_description="Installation, sanding, and finishing of real solid wood strip and plank flooring, along with unfinished engineered wood floors glued to concrete, with custom colors, square-edge unfinished engineered wide plank flooring, and dust-contained sanding. Premium mill-direct materials are sourced directly, with careful climate acclimation for San Diego's coastal and inland environments.",
    service_types=[
        "Solid hardwood floor installation", "Nail-down hardwood installation",
        "Unfinished engineered hardwood installation", "Glue-down installation over concrete",
        "Wide-plank engineered flooring installation", "Custom stain and finish application",
        "Dust-contained sanding", "Mill-direct hardwood flooring material sourcing",
    ],
    area_served=["San Diego County"] + PRIORITY_COASTAL_SD,
    offer_catalog_name="Solid & Engineered Wood Floor Installation Services",
    offer_items=[
        ("Solid Wood Strip & Plank Installation", "Installation of real solid wood strip and plank flooring, nailed down and finished on site."),
        ("Unfinished Engineered Wood Floor Installation", "Unfinished engineered wood floors glued to concrete, including square-edge wide-plank flooring for exceptionally flat surfaces."),
        ("Custom Color & Finish Application", "Custom stain colors and Bona Traffic HD finishes applied on site after installation."),
        ("Mill-Direct Material Sourcing", "Premium solid and engineered hardwood flooring sourced directly from trusted mills, with climate acclimation for San Diego's coastal and inland environments."),
    ],
)
GA = ""      # original page has no _gaq Google Analytics script either (confirmed) -- leave out


def esc(s):
    return (s or "").replace('"', "&quot;")


def fig(src):
    return (f'<figure><a href="{esc(src)}">'
            f'<img src="{esc(src)}" alt="{esc(ALT[src])}" loading="lazy"></a></figure>')


def project_section(p, idx):
    figs = "\n".join(fig(src) for src in p["images"])
    return f'''<div class="card" style="margin-bottom:34px;">
  <h3 style="text-align:left;line-height:1.4;">{p["heading"]}</h3>
  <p style="color:var(--ink-soft);line-height:1.65;">{p["note"]}</p>
  <div class="gallery" style="grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));">
{figs}
  </div>
</div>'''


projects_html = "\n".join(project_section(p, i) for i, p in enumerate(PROJECTS))

MAIN = f"""
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Solid &amp; Engineered Wood Floor Installation, Refinishing, Repairs &amp; Dustless Sanding</h1>
  <p>Professional hardwood floor installation in San Diego &mdash; custom nail-down and glue-down installation of solid and unfinished engineered wood floors, acclimated, sanded, and finished on site throughout San Diego County, alongside our dust-contained refinishing, repair, and restoration services. Below: four complete installation projects, from staged raw lumber to the finished floor.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>

<section class="block">
  <h2>{INTRO["heading"]}</h2>
  <p class="lede">{INTRO["body"]}</p>
</section>

<section class="block">
  <div class="card">
    <h3>{SOURCING["heading"]}</h3>
    <p style="color:var(--ink-soft);line-height:1.65;">{SOURCING["body"]}</p>
    <p style="color:var(--ink-soft);line-height:1.65;"><em>{SOURCING["note"]}</em></p>
  </div>
</section>

<section class="block">
  <div class="gallery-intro">
    <h2>Four Solid Wood Floor Installation Projects</h2>
  </div>
{projects_html}

  <p class="lede" style="margin-top:10px;">{OUTRO}</p>

  <div class="cta-row" style="justify-content:center;margin-top:20px;">
    <a class="btn btn-call" href="tel:+18586990072">Call 858-699-0072 &mdash; Discuss Your Installation Project</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>

  <p style="text-align:center;margin:26px auto 0;font-size:15.5px;">
  <a href="https://www.sdhardwoods.com/" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Hardwood Floor Refinishing in San Diego &rarr;</a>
  &nbsp;&bull;&nbsp; <a href="https://www.sdhardwoods.com/recent_project_photo_gallery_2.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">More Installation &amp; Refinishing Projects &rarr;</a>
  &nbsp;&bull;&nbsp; <a href="https://www.sdhardwoods.com/contact_us.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Contact San Diego Hardwoods</a>
  </p>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Solid Wood Floor Installation Projects", MAIN,
         str(BUILD.parent / "solid_wood_floor_photo_gallery.html"))
