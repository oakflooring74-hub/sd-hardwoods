# -*- coding: utf-8 -*-
import sys, json
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble, gallery_progress_html

DATA = BUILD / "data" / "recent_project_gallery_5"

with open(DATA / "images.json", encoding="utf-8") as f:
    images = json.load(f)

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

figs = []
for im in images:
    href = im["href"] or im["src"]
    cls = im.get("class") or ""
    cls_attr = f' class="{esc(cls)}"' if cls.strip() else ""
    figs.append(f'<figure><a href="{href}"><img src="{im["src"]}" alt="{esc(im["alt"])}"{cls_attr} loading="lazy"></a></figure>')
gallery_html = "\n".join(figs)

MAIN = f"""
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>San Diego Hardwood Flooring Project Gallery</h1>
  <p>Expert restoration, repairs, custom installation, and specialty finishes &mdash; real before-and-after results from homes throughout San Diego County.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:8586990072">&#9742; Call or Text 858-699-0072</a>
  </div>
</section>

<section class="block">
  <div class="gallery-intro">
    <h2>Recent Project Photos</h2>
  </div>
  {gallery_progress_html(4)}
  <div class="gallery">
{gallery_html}
  </div>

  <div class="cta-row" style="justify-content:center;flex-wrap:wrap;gap:16px;margin-top:20px;">
    <a class="btn btn-outline" href="https://www.sdhardwoods.com/">Back to Home &rarr;</a>
    <a class="btn btn-call" href="tel:858-699-0072">Call or Text Now: 858-699-0072</a>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "More Real San Diego Hardwood Floor Projects", MAIN,
         str(BUILD.parent / "recent_project_gallery_5.html"))
