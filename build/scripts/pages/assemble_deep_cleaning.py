import re, json, html
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
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
meta_desc = re.search(r'<meta name="DESCRIPTION" id="mDescription" content="([^"]*)"', raw).group(1)
canonical = re.search(r'<link href="([^"]+)" rel="canonical"', raw).group(1)
jsonld_block = re.search(r'<script type="application/ld\+json">.*?</script>', raw, re.DOTALL).group(0)
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

def esc(s):
    return s if s else ""

def render_figure(img, desc):
    if not img:
        return ""
    href = img["href"] or img["src"]
    cls = img["class"].strip()
    cls_attr = f' class="{cls}"' if cls else ""
    fig = f'<figure><a href="{href}"><img src="{img["src"]}" alt="{img["alt"]}"{cls_attr} loading="lazy"></a>'
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
    parts.append(render_figure(before["img"], before["desc"]))
    if before["img"]:
        img_count_in_gallery += 1
    parts.append(render_figure(after["img"], after["desc"]))
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
<a href="https://www.sdhardwoods.com/recent_project_photo_gallery_1.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">See Before &amp; After Project Galleries &rarr;</a>
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
  <h1>Hardwood Floor Deep Cleaning, Recoating &amp; Bona Traffic HD Finish Upgrades in San Diego</h1>
  <p>Restore dull, worn floors without the cost, dust, or disruption of full sanding. Our professional Bona PowerScrubber system deep cleans, removes wax and polish buildup, and prepares hardwood floors for a durable maintenance recoat or premium finish upgrade&mdash;often completed in just one day. Call <a href="tel:+18586990072">858-699-0072</a>, <a href="sms:+18586990072">text floor photos</a> or email <a href="mailto:sandiegohardwoods@gmail.com">sandiegohardwoods@gmail.com</a></p>
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
{jsonld_block}
'''

full_html = f'''<!DOCTYPE html><html lang="en">
<head xmlns="">
  <meta charset="utf-8"><base href="https://www.sdhardwoods.com/">
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
