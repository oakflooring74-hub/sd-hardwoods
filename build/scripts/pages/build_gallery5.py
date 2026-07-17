# -*- coding: utf-8 -*-
"""
Recent Project Gallery 5 builder (Milestone 2.1 rebuild).

The page now renders the raw source's five real project write-ups (#81-#85) as
explicit before/after pairs from data/recent_project_gallery_5/projects.json --
an explicit, deterministic pairing structure -- instead of the previous loose
photo grid built from images.json. images.json remains untouched as the frozen
record of the original extraction; the five legacy image-button records it
contains (ultra clean button x2, ultra clean button 2, NEXT PAGE BUTTON 2025,
CALL OR TEXT NOW BUTTON 2025) are deliberately excluded from generated output.
Desktop shows each pair side by side; on narrow screens the pair stacks but
stays together inside its project card.
"""
import sys, json
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble, gallery_progress_html

DATA = BUILD / "data" / "recent_project_gallery_5"

with open(DATA / "projects.json", encoding="utf-8") as f:
    PROJECTS = json.load(f)["projects"]

with open(DATA / "vcard.txt", encoding="utf-8") as f:
    VCARD = f.read().strip()

with open(DATA / "jsonld.html", encoding="utf-8") as f:
    JSONLD = f.read()

HEAD_META = """<title>San Diego Hardwood Flooring Project Gallery | Expert Restoration, Repairs, Custom Installation &amp; Specialty Finishes</title>
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

GA = """<script type="text/javascript">
                var _gaq = _gaq || [];
                _gaq.push(['_setAccount', "UA-20793161-1"]);
                _gaq.push(['_trackPageview']);
                (function() {
                  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
                  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
                  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
                })();
            </script>"""


def esc(s):
    return (s or "").replace('"', "&quot;")


def fig(img, label):
    return (f'<figure><a href="{esc(img["src"])}">'
            f'<img src="{esc(img["src"])}" alt="{esc(img["alt"])}" loading="lazy"></a>'
            f'<figcaption><strong>{label}</strong> &mdash; {img["caption"]}</figcaption></figure>')


def project_card(p):
    return f'''<div class="card" style="margin-bottom:28px;">
  <h3 style="text-align:left;">{p["title"]}</h3>
  <p style="color:var(--ink-soft);line-height:1.65;">{p["description"]}</p>
  <div class="gallery" style="grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));">
    {fig(p["before"], "Before")}
    {fig(p["after"], "After")}
  </div>
</div>'''


projects_html = "\n".join(project_card(p) for p in PROJECTS)

MAIN = f"""
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>San Diego Hardwood Flooring Project Gallery</h1>
  <p>Five recent projects, each shown before and after: solid white oak refinishing and a matching staircase in Mission Hills, sun-faded Brazilian cherry restored in El Cajon, engineered maple renewed in a Del Mar beachfront condo, and a failed DIY red oak refinish rescued with a modern gray stain in La Jolla &mdash; real restoration, repairs, and specialty finishes from homes across San Diego County.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:8586990072">&#9742; Call or Text 858-699-0072</a>
  </div>
</section>

<section class="block">
  <div class="gallery-intro">
    <h2>Recent Project Photos &mdash; Before &amp; After</h2>
  </div>
  {gallery_progress_html(4)}
{projects_html}

  <div class="card cta-card" style="margin-top:34px;">
    <div class="cta-copy">
      <h3>Not Every Hardwood Floor Needs Refinishing</h3>
      <p>Many hardwood floors can be dramatically improved without sanding. Our Bona Power Scrubber deep cleaning system removes years of embedded dirt, contaminants, polish buildup, and residue before applying a protective low-VOC recoat when appropriate. We also specialize in maintaining wire-brushed, matte, satin, and oil-finished hardwood floors using manufacturer-recommended cleaning methods.</p>
      <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">Learn When Deep Cleaning Is a Better Alternative Than Refinishing &rarr;</a></p>
    </div>
  </div>

  <div class="cta-row" style="justify-content:center;flex-wrap:wrap;gap:16px;margin-top:20px;">
    <a class="btn btn-outline" href="https://www.sdhardwoods.com/">Back to Home &rarr;</a>
    <a class="btn btn-call" href="tel:858-699-0072">Call or Text Now: 858-699-0072</a>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "More Real San Diego Hardwood Floor Projects", MAIN,
         str(BUILD.parent / "recent_project_gallery_5.html"))
