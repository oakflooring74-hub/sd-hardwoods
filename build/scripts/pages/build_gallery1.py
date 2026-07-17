# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble, gallery_progress_html

SCRATCH = str(BUILD)  # unused after this point but kept for reference

with open(BUILD / "data" / "recent_project_photo_gallery_1" / "modules.json", encoding="utf-8") as f:
    data = json.load(f)

with open(BUILD / "data" / "recent_project_photo_gallery_1" / "vcard.txt", encoding="utf-8") as f:
    VCARD = f.read().strip()

HEAD_META = """<title>Hardwood Floor Refinishing Gallery | San Diego Before &amp; After Photos</title>
<meta name="DESCRIPTION" content="View before and after hardwood floor refinishing projects completed throughout San Diego County. See dustless sanding, hardwood floor repairs, engineered hardwood refinishing, color changes, floor restoration, deep cleaning, and oiled floor upgrades completed in La Jolla, Del Mar, Mission Hills, Rancho Santa Fe, Encinitas, Carmel Valley, and nearby communities. Call or text 858-699-0072 for a professional phone consultation and expert floor evaluation.">
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

JSONLD = ""  # original page04 has no JSON-LD schema block (confirmed via inventory scan)

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
        alt = f"{title} — {label}"
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
  <p>Explore real San Diego hardwood floor refinishing projects featuring dustless sanding, hardwood floor repairs, restoration, color changes, custom stain work, and dramatic before-and-after transformations completed by San Diego Hardwoods throughout San Diego County.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:8586990072">&#9742; Call or Text 858-699-0072</a>
  </div>
</section>

<section class="block">
  <div class="card cta-card">
    <div class="cta-copy">
      <h3>Not Every Hardwood Floor Needs Refinishing</h3>
      <p>Many hardwood floors can be dramatically improved without sanding. Our Bona Power Scrubber deep cleaning system removes years of embedded dirt, contaminants, and residue before applying a protective low-VOC maintenance recoat when appropriate.</p>
      <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">Learn When Deep Cleaning Is Better Than Refinishing &rarr;</a></p>
    </div>
    <div class="cta-media">
      <a href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">
        <img src="https://www.sdhardwoods.com/ultra%20clean%20button.png" alt="hardwood floor deep cleaning in San Diego with professional Bona Power Scrubber maintenance">
      </a>
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
    <a class="btn btn-call" href="tel:858-699-0072">Call or Text Now: 858-699-0072</a>
  </div>
</section>

<section class="block">
  <div class="card cta-card">
    <div class="cta-copy">
      <h3>See Whether Deep Cleaning Could Save You From a Full Refinish</h3>
      <p>San Diego hardwood floor deep cleaning and polishing service — often the right call before committing to a full dust-contained sand and refinish.</p>
      <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">Learn More &rarr;</a></p>
    </div>
    <div class="cta-media">
      <a href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">
        <img src="https://www.sdhardwoods.com/ultra%20clean%20button%202.png" alt="San Diego hardwood floor deep cleaning and polishing service">
      </a>
    </div>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Before &amp; After Project Photos", MAIN,
         str(BUILD.parent / "recent_project_photo_gallery_1.html"))
