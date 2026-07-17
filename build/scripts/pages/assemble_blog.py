import re, json, html

from pathlib import Path
BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
RAW = str(BUILD / "raw-source" / "blog.html")
CHROME = str(BUILD / "chrome")
RECORDS = str(BUILD / "data" / "blog" / "case_studies.json")
OUT = str(BUILD.parent / "blog.html")
LOG = str(BUILD / "data" / "blog" / "assemble_log.txt")

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
meta_desc = re.search(r'content="([^"]*)" id="mDescription"', raw).group(1)
canonical = re.search(r'<link href="([^"]+)" rel="canonical"', raw).group(1)
gaq_block = re.search(r'<!--Google Analytics Tracking Code-->.*?</script>', raw, re.DOTALL).group(0)
vcard_desc = re.search(r'<span class="organization-name">(.*?)</span>', raw, re.DOTALL).group(1).strip()

# ---- gallery records ----
with open(RECORDS, encoding="utf-8") as f:
    data = json.load(f)
records = data["records"]
standalone_html = data["standalone_html"]

# merge case study #3 (title+prose sit in a standalone <h3 class="module caseStudy"> OUTSIDE
# the module_bd_container ul; its photos sit in an anonymous, title-less <li> INSIDE the ul --
# a broken/split pairing in the raw source that we reunite here, same approach as the
# malformed module on the deep-cleaning page).
link_m = re.search(r'<a[^>]*>(.*?)</a>', standalone_html, re.DOTALL)
link_text = clean_text(link_m.group(1)) if link_m else ""
prefix = clean_text(standalone_html[:link_m.start()]) if link_m else ""
remainder = clean_text(standalone_html[link_m.end():]) if link_m else clean_text(standalone_html)
cs3_title = f"{prefix} {link_text}".strip()
cs3_prose = remainder

for rec in records:
    if rec["id"] is None and rec["title"] is None and len(rec["images"]) == 4:
        rec["title"] = cs3_title
        rec["prose"] = [cs3_prose] if cs3_prose else []
        break

def render_figure(img, caption=None):
    href = img["href"] or img["src"]
    cls = (img["class"] or "").strip()
    cls_attr = f' class="{cls}"' if cls else ""
    fig = f'<figure><a href="{href}"><img src="{img["src"]}" alt="{img["alt"]}"{cls_attr} loading="lazy"></a>'
    if caption:
        fig += f'<figcaption>{caption}</figcaption>'
    fig += '</figure>'
    return fig

img_total = 0
case_study_cards = []
for rec in records:
    caption_map = {idx: txt for (txt, idx) in rec.get("captions", [])}
    parts = ['<div class="card">']
    if rec["title"]:
        parts.append(f'<h3>{rec["title"]}</h3>')
    for p in rec["prose"]:
        parts.append(f'<p>{p}</p>')
    if rec["images"]:
        cols = 2 if len(rec["images"]) > 1 else 1
        parts.append(f'<div class="gallery" style="grid-template-columns:repeat({min(cols,3)},1fr);margin-top:14px;">')
        for i, img in enumerate(rec["images"]):
            parts.append(render_figure(img, caption_map.get(i)))
            img_total += 1
        parts.append('</div>')
    parts.append('</div>')
    case_study_cards.append("\n".join(parts))

case_studies_html = "\n".join(case_study_cards)

# ---- vcard swap / scroll topic ----
body_top = top_html.replace("__VCARD_DESC__", vcard_desc)
scrollhint = scrollhint_html.replace("__SCROLL_TOPIC__", "Our Hardwood Flooring Case Studies")

# ---- reusable Deep Cleaning CTA card (appears twice in the raw source; rendered via the
# existing .card .cta-card component already used on the homepage) ----
deep_cleaning_cta = '''<div class="card cta-card">
  <div class="cta-copy">
    <h3>Could Deep Cleaning Save Your Hardwood Floors?</h3>
    <p>Not every hardwood floor needs refinishing. Many dull, dirty, lightly scratched, or worn floors can be dramatically improved with our Bona Power Scrubber deep cleaning system and a protective low-VOC maintenance coat. We also specialize in maintaining wire-brushed hardwood, matte finishes, satin finishes, natural oil finishes, engineered hardwood, and bamboo flooring throughout San Diego County.</p>
    <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">Learn When Deep Cleaning Is a Better Choice Than Refinishing &raquo;</a></p>
  </div>
  <div class="cta-media">
    <a href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">
      <img src="https://www.sdhardwoods.com/ultra%20clean%20button.png" alt="Professional hardwood floor deep cleaning in San Diego using the Bona Power Scrubber for hardwood, engineered hardwood, bamboo, wire-brushed, matte, satin, and oil-finished floors">
    </a>
  </div>
</div>'''

# ---- zB / zC nav-button widgets (Contact / About / Home / Next Page) ----
nav_buttons_html = '''<div class="gallery" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr));max-width:900px;margin:34px auto 0;">
<figure><a href="https://www.sdhardwoods.com/contact_us.html"><img src="/CONTACT US BETTER BUTTON 2025.png" alt="Contact San Diego Hardwoods for a free in-home estimate — hardwood floor refinishing, dust-free sanding, repairs, and installation services in La Jolla, Del Mar, Encinitas, Rancho Santa Fe, Carmel Valley, and North County San Diego" loading="lazy"></a></figure>
<figure><a href="https://www.sdhardwoods.com/about_us.html"><img src="/ABOUT US 2025 BUTTON.png" alt="About San Diego Hardwoods — meet your local hardwood floor refinishing and installation experts with 35+ years of experience serving La Jolla, Del Mar, Rancho Santa Fe, Encinitas, Carmel Valley, Solana Beach, and all coastal North County San Diego" loading="lazy"></a></figure>
<figure><a href="https://www.sdhardwoods.com/"><img src="/HOME BUTTON 2025.png" alt="san diego hardwood floor and bamboo floor deep cleaning refinishing installation and repairs. top rated flooring company in san diego county near me" loading="lazy"></a></figure>
<figure><a href="https://www.sdhardwoods.com/recent_project_photo_gallery_1.html"><img src="/NEXT PAGE BUTTON 2025.png" alt="SEE BEFORE AND AFTER PHOTOS OF SAN DIEGO HARDWOOD FLOOR REFINISHING DEEP CLEANING AND INSTALLATION FIX YOUR WOOD FLOOR TODAY NEAR ME FREE ESTIMATES SAN DIEGO HARDWOOD FLOOR INSTALLER" loading="lazy"></a></figure>
</div>'''
img_total += 4

img_total += 2  # the two Deep Cleaning CTA occurrences (1 img each)

main_html = f'''<main>

<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>San Diego Hardwood Flooring Blog &mdash; Expert Advice on Refinishing, Restoration, Deep Cleaning, Repairs, Installation &amp; Professional Floor Care</h1>
  <p>Licensed, Bonded &amp; Insured Hardwood Flooring Specialist with 35+ Years of Experience in Refinishing, Restoration, Repairs, Custom Installation, Dust Containment Sanding, Deep Cleaning, Custom Staining, Wire-Brushed &amp; Oil-Finished Floors. Call or Text <a href="tel:8586990072">858-699-0072</a> to Discuss Your Project with an Experienced Flooring Specialist.</p>
  <p>REFINISH RESTORE REPAIR WOOD HARDWOOD BAMBOO SOLID AND ENGINEERED WOOD FLOORING IN SAN DIEGO COUNTY. BONA CERTIFIED CRAFTSMAN</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:8586990072">&#9742; Call or Text 858-699-0072</a>
  </div>
</section>

<section class="block">
  <h2>{vcard_desc}</h2>
  <p class="lede">Hardwood floors are one of the most valuable features in a home, but years of foot traffic, pets, sunlight, moisture, and everyday wear can leave them scratched, dull, stained, or faded. Professional hardwood floor refinishing, restoration, repairs, deep cleaning, and maintenance can dramatically restore their beauty, durability, and value while extending the life of your investment.</p>
  <div class="info-grid">
    <div class="card">
      <h3>Why Homeowners Choose San Diego Hardwoods</h3>
      <p>For more than 35 years, San Diego Hardwoods has specialized exclusively in hardwood flooring. Every project is personally performed by an experienced flooring craftsman using premium equipment, proven techniques, and high-performance Bona finishing systems. We specialize in hardwood floor refinishing, restoration, repairs, custom installation, dust containment sanding, custom staining, deep cleaning, maintenance coats, wire-brushed hardwood floors, oil-finished floors, engineered hardwood, bamboo flooring, and premium floor care throughout San Diego County.</p>
    </div>
    <div class="card">
      <h3>Modern Hardwood Floor Refinishing</h3>
      <p>Today's hardwood floor restoration goes far beyond traditional drum sanding. Modern sanding equipment produces flatter, more consistent results while significantly reducing airborne dust through advanced dust containment systems. Combined with premium Bona sealers and finishes, your hardwood floors receive exceptional durability, outstanding appearance, and low-VOC protection for your home.</p>
    </div>
    <div class="card">
      <h3>Custom Stains &amp; Specialty Hardwood Finishes</h3>
      <p>Whether you're restoring traditional oak floors or updating your home with contemporary finishes, we create custom stain colors and specialize in today's most sought-after looks, including natural finishes, matte finishes, satin finishes, wire-brushed hardwood, and oil-finished flooring. Every floor is customized to complement your home's style while preserving the natural beauty of the wood.</p>
    </div>
    <div class="card">
      <h3>Not Every Hardwood Floor Needs Refinishing</h3>
      <p>Many hardwood floors can be dramatically improved without complete sanding. Professional deep cleaning with the Bona Power Scrubber, maintenance coats, and targeted repairs often restore clarity, improve appearance, and extend the life of your existing finish. We help homeowners determine whether deep cleaning, recoating, repairs, or complete refinishing is the most appropriate solution for their floors.</p>
    </div>
    <div class="card">
      <h3>Professional Hardwood Flooring Consultations</h3>
      <p>Every hardwood floor is unique. Whether you're considering refinishing, repairs, deep cleaning, custom installation, restoration after water damage, or maintaining specialty finishes, we'll help you understand your options and recommend the solution that best fits your floors, your home, and your long-term goals.</p>
    </div>
  </div>
  <div class="cta-row" style="justify-content:center;margin-top:34px;">
    <a class="btn btn-call" href="tel:8586990072">&#9742; Call or Text 858-699-0072 to Discuss Your Hardwood Flooring Project</a>
  </div>
</section>

<section class="block">
  <h2>Revitalize Your San Diego Hardwood Floors with Expert Refinishing &amp; Installation</h2>
  <p class="lede">Hardwood floors are one of the most valuable upgrades you can make to a San Diego home. Over time, even premium hardwood flooring can develop scratches, dents, fading, water damage, worn finishes, or outdated colors such as the heavy red tones found in many Brazilian Cherry floors. Professional hardwood floor refinishing, restoration, and installation can completely transform your home while preserving the beauty and character of real wood.</p>
  <p style="text-align:center;color:var(--ink-soft);max-width:820px;margin:0 auto 30px;">For more than 35 years, San Diego Hardwoods has specialized in hardwood floor refinishing, dustless sanding, repairs, custom staining, bleaching, deep cleaning, recoating, and complete hardwood floor installation throughout San Diego County. Whether you are searching for hardwood floor refinishing, a professional wood floor installer, or expert hardwood floor restoration, our goal is simple&mdash;deliver exceptional craftsmanship that lasts for decades.</p>

  <div class="info-grid">
    <div class="card">
      <h3>Why Homeowners Choose San Diego Hardwoods</h3>
      <ul>
        <li><strong>Advanced Dustless Sanding Equipment</strong> &ndash; Modern rotary sanding systems produce flatter, smoother floors while dramatically reducing airborne dust compared to traditional drum sanders.</li>
        <li><strong>Expert Color Matching &amp; Bleaching</strong> &ndash; We create custom colors ranging from natural finishes and modern white-washed hardwood to bleaching Brazilian Cherry and restoring historic hardwood floors.</li>
        <li><strong>Premium Bona Water-Based Finishes</strong> &ndash; Bona Traffic HD provides exceptional durability, beautiful clarity, low VOC emissions, and GreenGuard certification for healthier indoor air quality.</li>
        <li><strong>Over 35 Years of Experience</strong> &ndash; Every project is personally evaluated using decades of hardwood flooring knowledge to recommend the best long-term solution.</li>
      </ul>
    </div>
    <div class="card">
      <h3>Our Hardwood Floor Refinishing &amp; Installation Process</h3>
      <ul>
        <li><strong>Professional Evaluation</strong> &ndash; Every floor is inspected to determine the best restoration or installation approach.</li>
        <li><strong>Dust Containment &amp; Preparation</strong> &ndash; We carefully protect your home before any sanding begins.</li>
        <li><strong>Precision Sanding</strong> &ndash; Modern rotary sanding equipment creates an exceptionally flat surface ready for finishing.</li>
        <li><strong>Repairs &amp; Restoration</strong> &ndash; Damaged boards, gaps, stains, and worn areas are professionally repaired whenever possible.</li>
        <li><strong>Custom Staining or Bleaching</strong> &ndash; We match existing flooring or create completely new designer colors tailored to your home.</li>
        <li><strong>Professional Installation</strong> &ndash; We install solid hardwood, engineered hardwood, bamboo flooring, nail-down flooring, glue-down flooring, and wide plank hardwood flooring.</li>
        <li><strong>Premium Bona Protective Finish</strong> &ndash; Multiple coats provide exceptional durability and long-lasting beauty.</li>
      </ul>
    </div>
    <div class="card">
      <h3>Benefits of Professional Hardwood Floor Refinishing</h3>
      <ul>
        <li>Restore the natural beauty of existing hardwood floors.</li>
        <li>Increase the value and appeal of your home.</li>
        <li>Improve indoor air quality using low-VOC Bona finishes.</li>
        <li>Extend the life of your hardwood flooring for decades.</li>
        <li>Completely modernize outdated floor colors and worn finishes.</li>
      </ul>
    </div>
  </div>

  <h3 style="font-family:var(--font-serif);text-align:center;margin-top:40px;">Serving Homeowners Throughout San Diego County</h3>
  <p class="lede">San Diego Hardwoods proudly serves homeowners throughout La Jolla, Del Mar, Rancho Santa Fe, Encinitas, Carmel Valley, Solana Beach, Coronado, Pacific Beach, Mission Hills, Point Loma, Carlsbad, Oceanside, Vista, Escondido, Poway, Rancho Bernardo, and communities across San Diego County with expert hardwood floor refinishing, installation, restoration, deep cleaning, and repairs.</p>

  <h2>Request Your Free Hardwood Flooring Consultation</h2>
  <p class="lede">Whether you need hardwood floor refinishing, complete installation, repairs, restoration, dustless sanding, or professional deep cleaning, San Diego Hardwoods is ready to help. Call or text photos of your floors for a fast professional evaluation and honest recommendations backed by more than 35 years of experience.</p>
  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:8586990072">Call or Text: 858-699-0072</a>
  </div>
</section>

<section class="block">
  {deep_cleaning_cta}
</section>

<section class="block">
  <div class="gallery-intro">
    <h2>Hardwood Flooring Case Studies &amp; Project Stories</h2>
    <p class="lede">Twelve real San Diego hardwood flooring projects &mdash; refinishing, restoration, repairs, and installation &mdash; told in the words of the crew who did the work.</p>
  </div>
  <div class="info-grid" style="grid-template-columns:repeat(auto-fit,minmax(min(480px,100%),1fr));">
{case_studies_html}
  </div>
  {nav_buttons_html}
</section>

<section class="block">
  {deep_cleaning_cta}
</section>

</main>'''

head_extra = f'''<meta name="DESCRIPTION" id="mDescription" content="{meta_desc}">
	<link href="{canonical}" rel="canonical">
	<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
	<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">
	<link href="https://s.turbifycdn.com/ln/lib/smb/assets/hosting/yss/extensions/css/turbify_ss_extensions_1675321208.js" id="extensionsCSS" media="screen" rel="stylesheet" type="text/css">
	<title>{title}</title>
	<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
	<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
	<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
	<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180"><meta name="theme-color" content="#4b2e06"><meta name="msapplication-TileColor" content="#4b2e06"><meta name="msapplication-TileImage" content="https://www.sdhardwoods.com/LOGO-2025.png">
	<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
{gaq_block}
'''

full_html = f'''<!DOCTYPE html><html lang="en">
<head xmlns="">
  <meta charset="utf-8"><base href="https://www.sdhardwoods.com/">
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

with open(OUT, "w", encoding="utf-8") as f:
    f.write(full_html)

# ---- verification ----
log = []
def L(x): log.append(str(x))

new_img_count = len(re.findall(r"<img\b", full_html))
raw_img_count = len(re.findall(r"<img\b", raw))
L(f"NEW <img> count: {new_img_count}")
L(f"RAW <img> count: {raw_img_count}")
L(f"img_total tracked in script: {img_total}")
L(f"ld+json occurrences in NEW: {full_html.count('application/ld+json')}")
L(f"ld+json occurrences in RAW: {raw.count('application/ld+json')}")
L(f"triple-backtick occurrences in NEW: {full_html.count(chr(96)*3)}")
L(f"<footer count: {len(re.findall('<footer', full_html))}")
L(f"sdhMegaNav count: {len(re.findall('id=\"sdhMegaNav\"', full_html))}")
L(f"sdh-toggle count: {len(re.findall('id=\"sdh-toggle\"', full_html))}")
L(f"title extracted: {title!r}")
L(f"_gaq present in NEW: {'_gaq' in full_html}")
L(f"vcard_desc: {vcard_desc!r}")
L(f"cs3_title: {cs3_title!r}")

with open(LOG, "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("done")
