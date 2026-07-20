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
from alt_expand import append_sentences, strip_html_tags

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

# Aggressive alt-text expansion (2026-07-20): each image's own frozen-extraction alt
# (already rich) is preserved verbatim as the prefix. Appended: the project's own
# heading and note paragraph -- both already visible directly above these exact
# photos, describing species/construction, method, stain/finish, and location.
# No species/construction claim is changed; the known TRICIA WALNUT27/30/63/76
# filename-vs-white-oak conflict (flagged in docs/PROJECT_DECISIONS.md, deliberately
# unresolved) is left exactly as-is -- the appended text repeats only what the
# project heading/note already say (white oak), asserting nothing new either way.
for p in PROJECTS:
    heading_sentence = strip_html_tags(p["heading"])
    note_text = p["note"]
    for src in p["images"]:
        ALT[src] = append_sentences(ALT[src], heading_sentence, note_text)

with open(DATA / "vcard.txt", encoding="utf-8") as f:
    VCARD = f.read().strip()

HEAD_META = """<title>San Diego Solid &amp; Engineered Wood Floor Installation, Refinishing, Repairs &amp; Dustless Sanding</title>
<meta name="description" content="See solid and unfinished engineered hardwood installations in San Diego, including nail-down, glue-down, sanding and custom finishing.">
<link href="https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html" rel="canonical">
<link href="/favicon.ico" rel="icon" type="image/x-icon">
<link href="/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="/LOGO-2025.png" rel="logo" type="image/png">
<link href="/assets/legacy-css/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="/assets/legacy-css/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

# Schema milestone (2026-07-19): the original page had no JSON-LD block at
# all (confirmed) -- this adds one, built entirely from this page's own real
# content (INTRO/SOURCING/OUTRO above, project headings), not invented.
JSONLD = build_service_page_jsonld(
    page_url="https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html",
    page_id_slug="service",
    page_name="San Diego Solid & Engineered Wood Floor Installation, Refinishing, Repairs & Dustless Sanding",
    page_description="See solid and unfinished engineered hardwood installations in San Diego, including nail-down, glue-down, sanding and custom finishing.",
    service_name="Solid & Unfinished Engineered Wood Floor Installation",
    service_description="Installation of real solid and engineered wood flooring using nail-down, glue-down (over concrete), floating, and nail-assist methods -- unfinished flooring installed, sanded, and finished on site, or prefinished flooring installed ready-to-use. Includes cork and acoustic underlayment, sound-control assemblies, moisture and subfloor evaluation, custom colors, and true 100% dust-containment sanding. Premium mill-direct materials are sourced directly, with careful climate acclimation for San Diego's coastal and inland environments.",
    service_types=[
        "Solid hardwood floor installation", "Nail-down hardwood installation",
        "Glue-down hardwood installation over concrete", "Floating hardwood floor installation",
        "Nail-assist hardwood installation",
        "Unfinished engineered hardwood installation", "Prefinished hardwood installation",
        "Wide-plank engineered flooring installation", "Custom stain and finish application",
        "Cork and acoustic underlayment installation", "Subfloor and moisture evaluation",
        "True 100% dust-containment sanding", "Mill-direct hardwood flooring material sourcing",
    ],
    area_served=["San Diego County"] + PRIORITY_COASTAL_SD,
    offer_catalog_name="Solid & Engineered Wood Floor Installation Services",
    offer_items=[
        ("Solid Wood Strip & Plank Installation", "Installation of real solid wood strip and plank flooring, nailed down and finished on site."),
        ("Engineered Wood Floor Installation", "Engineered wood floors installed by glue-down over concrete, floating, or nail-assist depending on subfloor and product, including unfinished square-edge wide-plank flooring finished on site and ready-to-use prefinished flooring."),
        ("Custom Color & Finish Application", "Custom stain colors and Bona Traffic HD finishes applied on site after installation, with true 100% dust-containment sanding."),
        ("Cork, Underlayment & Subfloor Evaluation", "Cork and acoustic underlayment, sound-control assemblies, and moisture/subfloor evaluation before installation begins."),
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
  <p>Professional hardwood floor installation in San Diego &mdash; real solid and engineered wood flooring installed by nail-down, glue-down, floating, or nail-assist methods, acclimated, sanded, and finished on site (or installed prefinished and ready-to-use) throughout San Diego County, alongside our true 100% dust-containment refinishing, repair, and restoration services. Below: four complete installation projects, from staged raw lumber to the finished floor.</p>
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
  <h2>Installation Methods, Materials &amp; Feasibility</h2>
  <div class="info-grid">
    <div class="card">
      <h3>Nail-Down, Glue-Down, Floating &amp; Nail-Assist</h3>
      <p>We install real solid wood strip and plank using traditional nail-down methods, and engineered wood floors using glue-down installation over concrete, floating installation, or nail-assist &mdash; the right method depends on subfloor type, plank width, and the specific product.</p>
    </div>
    <div class="card">
      <h3>Unfinished &amp; Prefinished Flooring</h3>
      <p>Unfinished solid and engineered flooring is installed, sanded, and finished on site for a seamless custom look and true 100% dust-containment sanding; prefinished flooring is installed ready-to-use with no onsite sanding or finishing required.</p>
    </div>
    <div class="card">
      <h3>Cork, Underlayment &amp; Sound Control</h3>
      <p>Cork and acoustic underlayment, along with sound-control assemblies, are evaluated where relevant &mdash; particularly for condos, multi-story homes, and floating installations over concrete.</p>
    </div>
    <div class="card">
      <h3>Moisture, Subfloor &amp; Installation Feasibility</h3>
      <p>Before installation begins, we evaluate subfloor condition, moisture levels, transitions, and height limitations. For a full evaluation of installation feasibility on your subfloor, see our <a href="/floor-assessments-inspections" style="color:var(--brass-deep);font-weight:700;">Floor Assessments &amp; Inspections</a>.</p>
    </div>
  </div>
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
