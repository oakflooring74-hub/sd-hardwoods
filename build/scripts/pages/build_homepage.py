# -*- coding: utf-8 -*-
import re, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from assemble_page import assemble
from public_business_rules import (
    sanitize_public_jsonld, augment_local_entity, replace_area_served,
    build_webpage_service_graph, PRIORITY_COASTAL_SD, FULL_SAN_DIEGO_AREAS,
    SOUTH_ORANGE_COUNTY,
)

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
RAW = BUILD / "raw-source" / "index.html"
DATA = BUILD / "data" / "index"

with open(RAW, encoding="utf-8") as f:
    raw = f.read()

canonical = re.search(r'<link href="([^"]+)" rel="canonical">', raw).group(1)
vcard_desc = re.search(r'<span class="organization-name">(.*?)</span>', raw, re.DOTALL).group(1).strip()
jsonld_blocks = re.findall(r'<script type="application/ld\+json">.*?</script>', raw, re.DOTALL)
# homepage carries no _gaq Google Analytics script in the live source (confirmed) -- leave GA empty

# Milestone 2.4: the homepage is the site's primary full-service flooring page, so its
# title/description no longer come from the raw source (whose title centered on videos).
title = "Hardwood Floor Refinishing San Diego | San Diego Hardwoods"
description = ("Owner-operated since 1990. Hardwood floor refinishing, restoration, repairs, "
               "installation, deep cleaning and dust-contained sanding throughout San Diego County.")

HEAD_META = f"""<title>{title}</title>
<meta name="description" content="{description}">
<link href="{canonical}" rel="canonical">
<link href="/favicon.ico" rel="icon" type="image/x-icon">
<link href="/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="/LOGO-2025.png" rel="logo" type="image/png">
<link href="/assets/legacy-css/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="/assets/legacy-css/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

# Schema milestone (2026-07-19): the homepage's #local entity already has a
# correct, single, richer declaration (areaServed, hours, description) -- it
# just needs the new owner-confirmed fields added, not consolidation. Runs
# assemble()'s own sanitize step here too (idempotent) because augment must
# see the YouTube handle already normalized before it dedupes sameAs.
JSONLD = sanitize_public_jsonld("\n".join(jsonld_blocks))
JSONLD = augment_local_entity(JSONLD)
# Milestone 2.9: the homepage's #local entity carried a legacy, since-superseded
# areaServed array (missing the owner's detailed coastal/estate enclaves and South
# Orange County, and using a different OC list than the rest of the site). Replace
# it wholesale with the centralized list -- augment_local_entity() above only
# appends list fields, which would leave the old array in place alongside the new
# one instead of correcting it.
JSONLD = replace_area_served(JSONLD, FULL_SAN_DIEGO_AREAS + SOUTH_ORANGE_COUNTY)

# Image-localization milestone (2026-07-19): the homepage's raw-source #org
# node (a second, still-linked Organization declaration that consolidate/
# augment leave alone -- see build/README.md quirk #1) carries its own
# "logo"/"image" pointing at the old absolute Turbify URL. The shared
# CANONICAL_LOCAL_STUB in public_business_rules.py already uses the local
# path; mirror that here since this one node is homepage-only raw content.
JSONLD = JSONLD.replace(
    "https://www.sdhardwoods.com/LOGO-2025.png", "/LOGO-2025.png")
# Same raw-source quirk: the homepage's own raw-extracted VideoObject block
# (separate from the hero VideoObject in main_content.html, which was already
# authored with a local path) still carries the old absolute thumbnail URL.
JSONLD = JSONLD.replace(
    "https://www.sdhardwoods.com/images/thumbnails/dust-free-hardwood-refinishing-san-diego.png",
    "/images/thumbnails/dust-free-hardwood-refinishing-san-diego.png")

# Schema milestone (2026-07-19): add a WebPage + Service (+ OfferCatalog)
# graph naming the site's real core service categories, built from the
# homepage's own real visible content (hero intro, "Not Every Hardwood
# Floor Needs Refinishing" section, Bona DCS 2.0 section) -- not invented.
# References the existing #local entity above by @id rather than
# re-declaring it (that entity already carries the full county-wide
# areaServed list; this Service's own areaServed is a shorter priority
# list so the two don't just repeat each other verbatim on the same page).
_homepage_graph = build_webpage_service_graph(
    page_url="https://www.sdhardwoods.com/",
    page_id_slug="service",
    page_name=title,
    page_description=description,
    service_name="Hardwood & Bamboo Floor Refinishing, Restoration, Repairs, Installation & Deep Cleaning",
    service_description="Since 1990, San Diego Hardwoods has restored solid, engineered, and bamboo floors through repair, dust-contained sanding and refinishing, intensive deep cleaning, maintenance recoating, and traditional nail-down and glue-down installation throughout San Diego County.",
    service_types=[
        "Hardwood floor refinishing", "Bamboo floor refinishing",
        "Dust-contained sanding", "Hardwood floor repairs",
        "Hardwood floor restoration", "Solid hardwood installation",
        "Engineered hardwood installation", "Hardwood floor deep cleaning",
        "Maintenance recoating",
    ],
    area_served=["San Diego County"] + PRIORITY_COASTAL_SD,
    offer_catalog_name="Complete Hardwood & Bamboo Flooring Services",
    offer_items=[
        ("Dust-Contained Refinishing & Sanding",
         "Bona DCS 2.0 portable dust-containment system with dual HEPA filtration and continuous bagging captures sanding and abrasion dust at the source, for virtually dust-free sanding in most normal project conditions."),
        ("Deep Cleaning & Maintenance Recoating",
         "Bona Power Scrubber deep cleaning removes years of embedded dirt, contaminants, and residue before an optional protective low-VOC maintenance recoat; cleaning-only service is offered as its own scope when a new coat of finish isn't needed."),
        ("Solid & Engineered Hardwood Installation",
         "Traditional nail-down and glue-down installation of solid and engineered hardwood floors."),
        ("Hardwood Floor Repairs & Restoration",
         "Board replacement, water or termite damage remediation, subfloor fixes, squeak elimination, and color-matched patches that blend with existing flooring."),
        ("Free Phone & Photo Assessment",
         "Initial floor evaluation by phone and photos to identify condition, finish compatibility, wear layer, and project scope before recommending the right service."),
    ],
)
_homepage_body = json.dumps({"@context": "https://schema.org", "@graph": _homepage_graph}, indent=1, ensure_ascii=False)
JSONLD = JSONLD + f'\n<script type="application/ld+json">\n{_homepage_body}\n</script>'
GA = ""

with open(DATA / "gallery.json", encoding="utf-8") as f:
    imgs = json.load(f)

# Obsolete navigation-button graphics from the pre-rebuild site (former homepage images
# #91-#96). Excluded here at the generator level -- not hidden with CSS -- so the numbered
# badges stay sequential (#1-#90). The image *files* stay hosted (other pages still use
# them); a dedicated gallery-navigation section in main_content.html replaces their job.
LEGACY_NAV_BUTTONS = {
    "/NEXT PAGE BUTTON 2025.png",
    "FLOOR DEEP CLEAN.png",
    "/PHOTO GALLERY 2025.png",
    "VIDEOS BUTTON 2025.png",
    "/CONTACT US BETTER BUTTON 2025.png",
    "/ABOUT US 2025 BUTTON.png",
}
imgs = [im for im in imgs if im["src"] not in LEGACY_NAV_BUTTONS]

def esc(s):
    return (s or "").replace('"', "&quot;")

figs = []
for idx, im in enumerate(imgs, start=1):
    src = im["src"]
    alt = esc(im["alt"])
    cls = im["class"]
    href = im["href"] or src
    cls_attr = f' class="{esc(cls)}"' if cls else ""
    # Milestone 2.7: owner-approved visible lightbox caption, distinct from the alt
    # text. The lightbox (chrome/lightbox.html) prefers data-caption over alt.
    cap_attr = f' data-caption="{esc(im["caption"])}"' if im.get("caption") else ""
    figs.append(f'<figure><span class="gallery-badge">#{idx}</span><a href="{href}"{cap_attr}><img src="{src}" alt="{alt}"{cls_attr} loading="lazy"></a></figure>')
gallery_html = "\n".join(figs)

with open(DATA / "main_content.html", encoding="utf-8") as f:
    main_template = f.read()

MAIN = main_template.replace("__GALLERY_GRID__", gallery_html)

assemble(HEAD_META, JSONLD, GA, vcard_desc, "Real Hardwood Floor Projects", MAIN,
         str(BUILD.parent / "index.html"))
