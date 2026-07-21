import re, json, html, sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from public_business_rules import (
    sanitize_public_jsonld, build_service_page_jsonld, PRIORITY_COASTAL_SD,
)
from alt_expand import append_sentences, strip_html_tags
RAW = str(BUILD / "raw-source" / "deep-cleaning-hardwood-floors-san-diego.html")
CHROME = str(BUILD / "chrome")
RECORDS = str(BUILD / "data" / "deep-cleaning-hardwood-floors-san-diego" / "gallery_records.json")
OUT = str(BUILD.parent / "deep-cleaning-hardwood-floors-san-diego.html")
LOG = str(BUILD / "data" / "deep-cleaning-hardwood-floors-san-diego" / "assemble_log.txt")

with open(RAW, encoding="utf-8") as f:
    raw = f.read()

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

site_css = read(CHROME + r"\site_css.html")
darkmode_boot = read(CHROME + r"\darkmode_boot_scripts.html")
top_html = read(CHROME + r"\top.html")
footer_html = read(CHROME + r"\footer.html")
scrollhint_html = read(CHROME + r"\scrollhint_and_toggle.html")
lightbox_html = read(CHROME + r"\lightbox.html")

script_strip_re = re.compile(r"<script\b.*?</script>", re.DOTALL)
tag_strip_re = re.compile(r"<[^>]+>")
def clean_text(s):
    s = script_strip_re.sub("", s)
    s = tag_strip_re.sub("", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# ---- head bits ----
title = re.search(r"<title>(.*?)</title>", raw, re.DOTALL).group(1).strip()
canonical = re.search(r'<link href="([^"]+)" rel="canonical"', raw).group(1)
# Milestone 2.9 (owner-specified, verbatim): the raw legacy meta description
# ("Dust-free deep cleaning...") violated the project's own claims policy
# (never "dust-free", only "dust-contained" -- docs/PROJECT_DECISIONS.md) and
# mentioned no maintenance recoating. Replaced with the owner's exact text.
meta_desc = ("Professional hardwood, engineered wood and bamboo floor deep cleaning, wax "
             "and polish removal, and maintenance recoating throughout San Diego County.")
# Schema milestone (2026-07-19): the raw source's thin, generic schema
# (single "Hardwood Floor Deep Cleaning and Re-Coating" Service, ~7-city
# areaServed) is replaced with a WebPage + Service + OfferCatalog graph
# built from this page's own real, already-approved visible content --
# the three actual service distinctions from the info-grid cards below
# (cleaning-only / intensive-cleaning-before-recoating / wire-brushed &
# oil-finished), not invented copy. Milestone 2.9: description mirrors the
# real meta description above; South Orange County stays out of every
# per-page Service (shared #local entity only, per owner direction).
jsonld_block = build_service_page_jsonld(
    page_url="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html",
    page_id_slug="service",
    page_name="Hardwood Floor Deep Cleaning & Maintenance Recoating | San Diego",
    page_description=meta_desc,
    service_name="Hardwood, Engineered Wood, Vinyl, Laminate, Bamboo & Cork Floor Deep Cleaning and Maintenance Recoating",
    service_description="Professional deep cleaning and restoration for hardwood, engineered wood, vinyl, laminate, bamboo, and cork floors using commercial Bona PowerScrubber equipment and specialty cleaning solutions that remove embedded dirt, wax buildup, cloudy residue, cleaning-product films, and contaminants that ordinary mopping cannot eliminate -- reaching smooth, wire-brushed, hand-scraped, and textured surfaces without sanding or creating dust. When appropriate, the process is completed with a professional low-VOC maintenance recoat, or older oil-finished floors are evaluated for conversion to a durable, low-sheen Bona Traffic HD waterborne finish.",
    service_types=[
        "Hardwood floor deep cleaning",
        "Engineered wood floor deep cleaning",
        "Bamboo floor deep cleaning",
        "Vinyl and laminate floor deep cleaning",
        "Cork floor deep cleaning",
        "Wire-brushed and textured floor cleaning",
        "Oiled-floor cleaning and finish-conversion evaluation",
        "Maintenance recoating preparation and application",
    ],
    area_served=(
        ["San Diego County"] + PRIORITY_COASTAL_SD + ["Poway", "Escondido"]
    ),
    offer_catalog_name="Deep Cleaning & Maintenance Recoating Services",
    offer_items=[
        ("Cleaning-Only Service",
         "Removing embedded dirt, old cleaner residue, and polish buildup so an existing finish looks and performs its best again -- a stand-alone service when a new coat of finish is not the appropriate scope."),
        ("Intensive Cleaning Before Recoating",
         "Deep cleaning and preparation of the floor, confirmation of finish compatibility, then a protective low-VOC maintenance coat -- extending the life of the floor without full sanding."),
        ("Wire-Brushed, Textured & Oil-Finished Floor Cleaning",
         "Reaches dirt trapped deep in wire-brushed and textured grain that mops can't reach; oil-finished floors receive manufacturer-approved care, with conversion to a durable, easy-to-clean, low-sheen waterborne finish such as Bona Traffic HD discussed when a floor has become a maintenance burden."),
    ],
)
# Milestone 2.6: every page's schema passes through the shared
# public-business-rules filter (no PostalAddress/street address, official
# YouTube channel) -- harmless here since nothing above introduces that
# data, but keeps the same safety net every page's schema goes through.
jsonld_block = sanitize_public_jsonld(jsonld_block)
analytics_html = read(CHROME + r"\analytics.html")
vcard_desc = re.search(r'<span class="organization-name">(.*?)</span>', raw, re.DOTALL).group(1).strip()

# ---- prose paragraphs (extracted, not retyped) ----
def para_containing(marker):
    idx = raw.index(marker)
    p_start = raw.rindex("<p", 0, idx)
    p_end = raw.index("</p>", idx) + len("</p>")
    return raw[p_start:p_end]

def heading_containing(marker, tag):
    idx = raw.index(marker)
    h_start = raw.rindex(f"<{tag}", 0, idx)
    h_end = raw.index(f"</{tag}>", idx) + len(f"</{tag}>")
    return raw[h_start:h_end]

p_professionally = clean_text(para_containing("We professionally deep clean and restore hardwood"))
# Milestone 2.9: the South Orange County sentence added in 2.8 is removed --
# per owner direction, OC appears only in the shared #local schema entity,
# never in visible copy. Original approved sentence preserved verbatim.
p_proudly = clean_text(para_containing("We proudly serve homeowners throughout San Diego County"))
h2_sub = clean_text(heading_containing("Professional Deep Cleaning, Recoating", "h2"))
h3_gallery_intro = clean_text(heading_containing("See Our Hardwood Floor Deep Cleaning System in Action", "h3"))

# ---- gallery records ----
with open(RECORDS, encoding="utf-8") as f:
    records = json.load(f)

# Manual fix for malformed module #5 (raw source has broken li nesting: no <h3> title,
# and the "#5 ..." heading text sits as bare text before each <a><img></a>, which the
# extraction script (correctly) does not fold into alt/src/class/href. Recovered here
# from direct inspection of page06.html lines 414-433.)
for rec in records:
    if rec["index"] == 5:
        rec["title"] = "#5 Wire-Brushed Hardwood Floor Deep Cleaning – San Diego Home Prepping for Recoat"
        shared_desc = "Wire-brushed oak floors trap dirt deep in the grain. Our San Diego hardwood deep-cleaning service reaches where steam mops and store cleaners can’t—removing buildup safely before applying a fresh coat."
        rec["before"]["desc"] = shared_desc
        rec["after"]["desc"] = None
        rec["note_text"] = None

# Alt-text recomposition (Milestone 2.13): gallery_records.json is regenerated from
# raw-source on every build (build_deep_cleaning.py), so per-image alt overrides live
# here rather than in that regenerated JSON. Pairs #1-9 are this page's own real
# deep-cleaning projects, recomposed to lead with the visible process stage (not a
# forced Before/After label -- see docs/2026-07-image-alt-recomposition-report.md for
# why: at least one pair's "before"/"after" CSS roles don't reliably match a
# damaged-state/completed-result reading). Pairs #10-20 use the exact same source
# photos as Gallery 1 Projects #10-20 (a pre-existing raw-source duplication across
# both pages, not something this milestone restructures) -- their alt text reuses the
# already-recomposed Gallery 1 wording verbatim for the same real facts.
ALT_OVERRIDE = {
    "DEEP CLEAN HARDWOOD FLOORS SAN DIEGO WIRE BRUSH CLEANING.jpg": "Deep cleaning #1, dual-brush stage: a Bona Power Scrubber performing specialized hardwood-floor deep cleaning on wire-brushed floors in a San Diego home, its dual white brushes scrubbing and extracting years of dirt, polish residue, and buildup without sanding — the same process San Diego Hardwoods uses in La Jolla, Del Mar, Encinitas, and Rancho Santa Fe homes, safe for wire-brushed, textured, and smooth wood floors, and distinct from the general carpet and surface-floor cleaning associated with companies such as Coit or Stanley Steemer.",
    "DEEP CLEAN WIRE BRUSHED FLOORING SAN DIEGO.jpg": "Deep cleaning #1, rotary pre-scrub stage: a rotary buffer loosening old polish, residue, and grime on this same wire-brushed hardwood floor ahead of the Bona Power Scrubber step, part of San Diego Hardwoods' specialized hardwood-floor deep-cleaning process for wire-brushed, textured, and smooth wood floors across San Diego, La Jolla, Del Mar, and Encinitas.",
    "DEEP CLEANING OF WOOD FLOORING SAN DIEGO POLISH REMOVAL AND MAINTENANCE.jpg": "Deep cleaning #2, in-progress: a technician performing precision Bona Power Scrubber deep cleaning and re-coating preparation on hardwood floors in a San Diego living room, part of San Diego Hardwoods' Bona-approved, specialized hardwood-floor process that safely revives hardwood in this North County home, leaving it clean, even, and ready for a protective finish.",
    "ENCINITAS DEEP CLEANING OF WOOD FLOORING POLISH REMOVAL SAN DIEGO.jpg": "Deep cleaning #2, completed result: the same San Diego living room's hardwood floor after Bona Power Scrubber deep cleaning and re-coating, its satin finish and natural wood clarity and warmth fully restored by San Diego Hardwoods — restored without sanding and without sanding dust.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 81.png": "Deep cleaning #3, in-progress: a rotary scrubber and neutral Bona cleaner removing years of buildup from hardwood flooring in a San Diego kitchen, part of San Diego Hardwoods' specialized hardwood-floor deep-cleaning service that safely revives dull or sticky wood, bamboo, or engineered floors without sanding, mess, or damage.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 79.png": "Deep cleaning #3, completed result: the same San Diego kitchen floor after Bona PowerScrubber deep cleaning removed dirt and residue and restored its natural satin finish using water-based cleaners, without sanding — a safe, fast, eco-friendly refresh that revives dark hardwood floors in just hours.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 129.png": "Deep cleaning & recoating prep #4, wet-scrub stage: a distressed engineered wood floor in a San Diego home wet-scrubbed with a rotary scrubber to dissolve old polish and wax buildup, part of San Diego Hardwoods' deep-cleaning and recoating-prep process that reveals clean wood ahead of a smooth new protective coating.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 131.png": "Deep cleaning & recoating prep #4, prepped result: the same engineered floor deep-scrubbed clear of polish and wax residue by San Diego Hardwoods, its natural color restored and surface ready for a durable new recoat finish.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 43.png": "Deep cleaning #5, in-progress: a Bona PowerScrubber performing specialized hardwood-floor deep cleaning on the deep grain of a wire-brushed oak floor in a San Diego home ahead of re-coating, reaching embedded dirt through a hardwood-specific process distinct from the general carpet and surface-floor cleaning associated with companies such as Stanley Steemer or Zerorez, without sanding.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 41.png": "Deep cleaning #5, completed result: the same wire-brushed oak floor after specialized Bona PowerScrubber hardwood-floor deep cleaning lifted dirt from its textured wood grain, ready for protective recoating — San Diego Hardwoods' hardwood-specific alternative to the general carpet and surface-floor cleaning offered by companies such as Stanley Steemer or Zerorez.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 10.png": "Deep cleaning #6, before: this heavily grimy engineered white oak restaurant floor in Del Mar, packed with dirt and traffic residue from daily use, shown ahead of San Diego Hardwoods' Bona-based deep-cleaning process that dissolves buildup without sanding or disruption.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 142.png": "Deep cleaning #6, after: the same Del Mar restaurant's engineered white oak floor after one Bona PowerScrubber session lifted the embedded grime, its natural color and cleanliness restored and ready for recoating.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 154.png": "Deep cleaning & recoating prep #7: this Del Mar restaurant's engineered white oak floor prepared with Bona PowerScrubber equipment to remove grease, dirt, and polish buildup ahead of recoating.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 141.png": "Deep cleaning & recoating prep #7, completed: the same Del Mar restaurant floor after professional deep cleaning and recoating, its clarity, sheen, and protection restored with Bona commercial-grade finishes overnight.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 100.png": "Deep cleaning, re-staining & recoating #8: an engineered distressed floor in this Carlsbad home after wax buildup was scrubbed and abraded away, re-stained in a modern, even tone by San Diego Hardwoods to restore rich color and grain without full replacement.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 105.png": "Deep cleaning, re-staining & recoating #8, completed: the same Carlsbad kitchen's engineered floor freshly re-coated over its new dark stain, its sheen and protection restored with a satin finish once cured.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 84.png": "Deep cleaning, wax removal & re-staining #9: this completely worn engineered hardwood floor in a Carlsbad home, covered in old polish buildup, shown as San Diego Hardwoods' Bona PowerScrubber deep cleans and abrades the surface to remove wax and residue ahead of re-staining.",
    "DEEP CLEAN WOOD FLOORS BAMBOO CLEANING POLISH 104.png": "Deep cleaning, wax removal & re-staining #9, completed: the same Carlsbad floor fully restored after deep cleaning, re-staining, and recoating, its rich color and satin sheen renewed with a fresh protective coat.",
    "/DOUGLAS FIR REFINISHING1.jpg": "Before #10 in Golden Hill: another late-1800s historic apartment's vintage Douglas Fir flooring shown mid-process, being stripped of paint and years of wear with an industrial belt sander connected to a Bona portable dust-containment system.",
    "/DOUGLAS FIR REFINISHING16.jpg": "After #10 in Golden Hill near South Park and Bankers Hill: the same Douglas Fir floor fully restored, stained in a rich Jacobian color and sealed with a satin commercial-grade finish, leaving a spotless, durable restoration that proves the effectiveness of true dust-free sanding.",
    "/BENG CHERRY.jpg": "Before #11 in 4S Ranch: engineered Brazilian cherry flooring in this North County San Diego home near Rancho Santa Fe and Carmel Mountain Ranch, sun-faded and worn with its aluminum-oxide factory finish still intact, shown ahead of dust-contained sanding to remove that coating.",
    "/BENG CHERRY 2.jpg": "After #11 in 4S Ranch: the same engineered Brazilian cherry floor with its aluminum-oxide coating removed through dust-contained sanding, sealed with a traditional oil-based sealer to deepen the rich cherry color and finished with a matte-sheen residential water-based coat, restoring decades of worn wood and highlighting the floor's custom cherry corner round detail.",
    "/FRENCH OAK INSTALL21.jpg": "Before #12 in this Baker's Hill commercial space near South Park and Mission Valley: wide-plank, seven-inch random-length engineered French oak shown raw, installed but not yet sanded, ahead of professional dust-free sanding and site finishing.",
    "/FRENCH OAK INSTALL60.jpg": "After #12 in this Baker's Hill commercial space near South Park and Mission Valley: the same wide-plank engineered French oak floor sanded flat and finished on site with the same durable commercial finish and natural tone used in the first phase, creating a smooth, modern wide-plank floor built to withstand heavy restaurant use.",
    "assets/images/hickory.356121752_sq_thumb_m.jpg": "Before #13 in Rancho Santa Fe: engineered hickory flooring in this North County estate, originally distressed and badly sun-faded, shown ahead of dust-contained sanding to remove the wear and texture.",
    "assets/images/hickory_1.356121807_sq_thumb_m.jpg": "After #13 in Rancho Santa Fe: the same engineered hickory floor sanded flat with dust containment, custom-mixed to the perfect stain tone and sealed with Bona Traffic HD for a satin, durable finish, restoring the floor's elegance in this North County estate.",
    "/HICKORY SANDING17.jpg": "Before #14 in Carmel Valley near Del Mar: wide-plank solid hickory flooring in this home, extremely sun-faded and worn with its natural color lost after years of exposure, shown ahead of professional dust-free sanding and restoration.",
    "/HICKORY SANDING78.jpg": "After #14 in Carmel Valley near Del Mar: the same solid hickory floor dust-contained sanded to raw wood and sealed with a natural color sealer that highlights the rich grain and beauty of the wide planks, bringing the floor back to life with a timeless, durable finish.",
    "assets/images/rsf_1.356121907_sq_thumb_m.jpg": "Before #15 near Solana Beach and Del Mar, Rancho Santa Fe: hardwood floors in this North County home coated in layers of old wax that left the surface dull and uneven, shown ahead of professional deep cleaning and wax removal.",
    "assets/images/rsf_5.356121924_sq_thumb_m.jpg": "After #15 near Solana Beach and Del Mar, Rancho Santa Fe: the same floors after a full professional cleaning and wax removal and a fresh commercial-grade recoat, restoring the floors' natural beauty and durability without a full sanding.",
    "assets/images/01-12-10_0210.313133752_sq_thumb_m.jpg": "Before #16 in the Gaslamp District, downtown San Diego: solid pine flooring inside this Hooters restaurant location, worn and damaged from years of heavy foot traffic, shown ahead of professional dust-contained sanding and repair.",
    "assets/images/hooters-after.39225501_sq_thumb_m.jpg": "After #16 in the Gaslamp District, downtown San Diego: the same solid pine floor sanded clean and finished with Bona Traffic HD, a two-part commercial polyurethane system in satin sheen, delivering maximum durability and bringing back the pine's warm natural character for this busy commercial space.",
    "assets/images/20200525_135341.15483527_sq_thumb_m.jpg": "Before #17 in Point Loma: solid plank Brazilian cherry flooring in this coastal San Diego home, worn, sun-faded, and discolored from years of use, shown ahead of dust-free sanding and deep cleaning.",
    "assets/images/20200531_104412.15483832_sq_thumb_m.jpg": "After #17 in Point Loma: the same solid cherry floor restored with dust-free sanding, sealed clear to highlight the deep, rich red tones, and finished with Bona Traffic HD, a two-part commercial polyurethane system, demonstrating how Brazilian cherry can be refinished rather than replaced.",
    "/RECOAT OAK6.jpg": "Before #18 in Scripps Ranch: engineered white oak flooring in this home, dulled and worn from years of use, shown prepared for professional repair, deep cleaning, and dust-free sanding to ensure proper adhesion before a new protective finish.",
    "/RECOAT OAK8.jpg": "After #18 in Scripps Ranch: the same engineered white oak floor restored with professional preparation, dustless sanding, and a commercial-grade Bona polyurethane finish in an extra-matte sheen, durable recoating that extends the life of quality hardwood floors without a full sanding.",
    "/RECOAT OAK10.jpg": "Before #19 in Carmel Valley: solid walnut flooring in this home, sun-faded and surface-worn from years of daily use, shown ahead of professional dust-free sanding, color restoration, and protective recoating.",
    "/RECOAT OAK19.jpg": "After #19 in Carmel Valley: the same solid walnut floor restored with dustless sanding, a fresh custom color application to even out tone, and a durable commercial-grade Bona Traffic HD polyurethane finish, restoring the deep natural walnut look with protection designed to handle years of use, refreshed without a full sanding.",
    "assets/images/walnutafter.356114726_sq_thumb_m.jpg": "Before #20 in the Gaslamp District at this Omni Hotel condo: engineered walnut flooring worn and faded from heavy use, shown ahead of professional dust-free sanding equipment being applied to restore the floor.",
    "assets/images/walnutafter2.356114805_sq_thumb_m.jpg": "After #20 in the Gaslamp District at this Omni Hotel condo overlooking the Coronado Bay Bridge: the same engineered walnut floor sanded back to raw wood with dust containment and finished with Bona Traffic HD for a durable, modern, flawless restoration in this high-rise setting.",
}


def esc(s):
    return s if s else ""

def render_figure(img, desc, title=None):
    if not img:
        return ""
    href = img["href"] or img["src"]
    cls = img["class"].strip()
    cls_attr = f' class="{cls}"' if cls else ""
    override = ALT_OVERRIDE.get(img["src"])
    alt = override if override is not None else append_sentences(
        img["alt"], strip_html_tags(title) if title else None, desc)
    alt = alt.replace('"', "&quot;")  # this file doesn't otherwise escape attribute values
    fig = f'<figure><a href="{href}"><img src="{img["src"]}" alt="{alt}"{cls_attr} loading="lazy"></a>'
    if desc:
        fig += f'<figcaption>{desc}</figcaption>'
    fig += '</figure>'
    return fig

gallery_cards = []
img_count_in_gallery = 0
for rec in records:
    card_title = rec["title"]
    before = rec["before"]
    after = rec["after"]
    parts = [f'<div class="card">', f'<h3>{card_title}</h3>', '<div class="gallery" style="grid-template-columns:repeat(2,1fr);">']
    parts.append(render_figure(before["img"], before["desc"], card_title))
    if before["img"]:
        img_count_in_gallery += 1
    parts.append(render_figure(after["img"], after["desc"], card_title))
    if after["img"]:
        img_count_in_gallery += 1
    parts.append('</div>')
    if rec["note_text"]:
        parts.append(f'<p style="margin-top:14px;color:var(--ink-soft);">{rec["note_text"]}</p>')
    parts.append('</div>')
    gallery_cards.append("\n".join(parts))

# Milestone 2.1: the trailing legacy image-buttons from item #20's note_imgs (NEXT PAGE /
# CALL OR TEXT NOW graphics) are no longer rendered -- replaced with real text links.
cta_buttons_html = '''
<p style="text-align:center;margin:34px auto 0;font-size:15.5px;">
<a href="https://www.sdhardwoods.com/recent_project_photo_gallery_1.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Real Hardwood Floor Refinishing Projects &rarr;</a>
&nbsp;&bull;&nbsp; <a href="https://www.sdhardwoods.com/recent_project_photo_gallery_4.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Restoration &amp; Deep-Cleaning Projects &rarr;</a>
&nbsp;&bull;&nbsp; <a href="https://www.sdhardwoods.com/contact_us.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Contact San Diego Hardwoods</a>
&nbsp;&bull;&nbsp; <a href="tel:+18586990072" style="color:var(--cta-red);font-weight:700;text-decoration:underline;">Call 858-699-0072</a>
&nbsp;&bull;&nbsp; <a href="sms:+18586990072" style="color:var(--cta-red);font-weight:700;text-decoration:underline;">Text Floor Photos</a>
</p>'''

gallery_html = "\n".join(gallery_cards)

# ---- vcard swap ----
body_top = top_html.replace("__VCARD_DESC__", vcard_desc)
scrollhint = scrollhint_html.replace("__SCROLL_TOPIC__", "Our Deep Cleaning Process")

# ---- video embed script (page's own YouTube Shorts ID) ----
video_script = '''<script type="text/javascript">
(function () {
    var YT_ID = "ixqPScnbnLE";
    var params = "rel=0&modestbranding=1&playsinline=1&autoplay=0&mute=1&controls=1&loop=1&playlist=" + YT_ID + "&enablejsapi=1";
    var src = "https://www.youtube-nocookie.com/embed/" + YT_ID + "?" + params;

    var mount = document.getElementById("heroVideoMount");
    var iframe = document.createElement("iframe");
    iframe.setAttribute("title", "Bona Power Scrubber – Deep Cleaning in San Diego");
    iframe.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
    iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    iframe.src = src;
    iframe.style.position = "absolute";
    iframe.style.top = "0";
    iframe.style.left = "0";
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.setAttribute("allowfullscreen", "allowfullscreen");

    mount.appendChild(iframe);
})();
</script>'''

main_html = f'''<main>

<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Hardwood Floor Deep Cleaning, Wax &amp; Polish Removal and Maintenance Recoating in San Diego</h1>
  <p>Professional hardwood floor cleaning without the cost, dust, or disruption of full sanding. Our Bona PowerScrubber wood floor deep cleaning system removes embedded dirt, wax and polish buildup, and prepares hardwood floors for a durable maintenance recoat or premium finish upgrade&mdash;often completed in just one day. Call <a href="tel:+18586990072">858-699-0072</a>, <a href="sms:+18586990072">text floor photos</a> or email <a href="mailto:sandiegohardwoods@gmail.com">sandiegohardwoods@gmail.com</a></p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>

<section class="block">
  <div class="video-frame">
    <div id="heroVideoMount" style="position:relative;padding-top:56.25%;height:0;overflow:hidden;"></div>
  </div>
</section>
{video_script}

<section class="block">
  <h2>{h2_sub}</h2>
  <div class="card">
    <p>{p_professionally}</p>
    <p>{p_proudly}</p>
  </div>

  <div class="info-grid" style="margin-top:26px;">
    <div class="card">
      <h3>Cleaning-Only Service</h3>
      <p>Not every floor needs a new coat of finish. When intensive cleaning is the appropriate scope, we provide deep cleaning as a stand-alone service &mdash; removing embedded dirt, old cleaner residue, and polish buildup so your existing finish looks and performs its best again.</p>
    </div>
    <div class="card">
      <h3>Intensive Cleaning Before Recoating</h3>
      <p>A maintenance recoat only bonds well over a genuinely clean, compatible finish. We deep clean and prepare the floor first, confirm finish compatibility, and then apply a protective low-VOC maintenance coat &mdash; extending the life of the floor without full sanding.</p>
    </div>
    <div class="card">
      <h3>Wire-Brushed, Textured &amp; Oil-Finished Floors</h3>
      <p>Wire-brushed and textured floors trap dirt deep in the grain where mops can't reach, and oil-finished floors need manufacturer-approved care. We deep clean both safely &mdash; and where an oiled floor has become a maintenance burden, we can discuss converting suitable floors to a durable, easy-to-clean, low-sheen waterborne finish such as Bona Traffic HD.</p>
    </div>
    <div class="card">
      <h3>When Cleaning Isn't Enough</h3>
      <p>Deep cleaning cannot repair a finish that is worn through, deep scratches into raw wood, or gray, water-damaged boards. When a floor has reached that point, it needs full sanding and refinishing &mdash; see our <a href="https://www.sdhardwoods.com/" style="color:var(--brass-deep);font-weight:700;">true 100% dust-containment hardwood floor refinishing in San Diego</a>. We'll tell you honestly which service your floor actually needs.</p>
    </div>
  </div>

  <div class="cta-row" style="justify-content:center;margin-top:34px;">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>

<section class="block">
  <div class="gallery-intro">
    <h2>{h3_gallery_intro}</h2>
    <p class="lede">Twenty real San Diego deep-cleaning and recoating projects, each shown before and after &mdash; from wire-brushed oak to commercial restaurant floors.</p>
  </div>
  <div class="info-grid" style="grid-template-columns:repeat(auto-fit,minmax(min(520px,100%),1fr));">
{gallery_html}
  </div>
{cta_buttons_html}
</section>

</main>'''

head_extra = f'''<meta name="description" content="{meta_desc}">
	<link href="{canonical}" rel="canonical">
	<link href="/assets/legacy-css/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
	<link href="/assets/legacy-css/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">
	<title>{title}</title>
	<link href="/favicon.ico" rel="icon" type="image/x-icon">
	<link href="/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
	<link href="/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
	<link href="/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180"><meta name="theme-color" content="#4b2e06"><meta name="msapplication-TileColor" content="#4b2e06"><meta name="msapplication-TileImage" content="/LOGO-2025.png">
	<link href="/LOGO-2025.png" rel="logo" type="image/png">
{jsonld_block}
{analytics_html}
'''

full_html = f'''<!DOCTYPE html><html lang="en">
<head xmlns="">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{head_extra}
{site_css}
{darkmode_boot}
</head>
<body class="lo_layout2wt" dir="ltr" spellcheck="false">
{body_top}
{main_html}
{footer_html}
{scrollhint}
{lightbox_html}
</body>
</html>
'''

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(full_html)

# ---- verification ----
log = []
def L(x): log.append(str(x))

new_img_count = len(re.findall(r"<img\b", full_html))
raw_img_count = len(re.findall(r"<img\b", raw))
L(f"NEW <img> count: {new_img_count}")
L(f"RAW <img> count: {raw_img_count}")
L(f"gallery img count tracked: {img_count_in_gallery}")
L(f"ld+json occurrences in NEW: {full_html.count('application/ld+json')}")
L(f"triple-backtick occurrences in NEW: {full_html.count(chr(96)*3)}")
L(f"<footer count: {len(re.findall('<footer', full_html))}")
L(f"sdhMegaNav count: {len(re.findall('id=\"sdhMegaNav\"', full_html))}")
L(f"sdh-toggle count: {len(re.findall('id=\"sdh-toggle\"', full_html))}")
L(f"title extracted: {title!r}")
L(f"_gaq present in NEW (should be False since Milestone 2.4): {'_gaq' in full_html}")

with open(LOG, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(log))
print("done")
