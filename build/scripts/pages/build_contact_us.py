import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble

HEAD_META = """<title>Contact San Diego Hardwoods | Hardwood Floor Refinishing, Repairs &amp; Installation</title>
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

with open(BUILD / "data" / "contact_us" / "jsonld.html", encoding="utf-8") as f:
    JSONLD = f.read()

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

VCARD = "SAN DIEGO LICENSED WOOD FLOOR RESTORATION/REFINISHING CONTRACTOR 858-699-0072 EXPERIENCE EXCEPTIONAL DUSTLESS HARDWOOD AND BAMBOO FLOOR REFINISHING IN SAN DIEGO. ALL WORK PERFORED BY A HIGHLY EXPERIENCED FLOORING EXPERT WITH OVER 30 YEARS EXPERIENCE RESTORING AND REPAIRING SOLID AND ENGINEERED HARDWOOD AND BAMBOO FLOORING. CALL TODAY TO SCHEDULE A CONSULTATION. TEXT PHOTOS OF YOUR PROJECT FOR AN IMMEDIATE ASSESSMENT."

MAIN = """
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Contact San Diego Hardwoods &mdash; Hardwood Floor Refinishing, Installation, Deep Cleaning, Repairs &amp; Restoration in San Diego</h1>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:8586990072">&#9742; Call or Text 858-699-0072 Today</a>
  </div>
</section>

<section class="block">
  <h2>Call or Text Today for a Free Hardwood Flooring Phone Assessment &mdash; Anywhere in San Diego County</h2>
  <p class="lede">Based in San Diego (92130), we restore and repair solid and engineered hardwood and bamboo flooring for homeowners throughout San Diego County, with select projects in Orange County. Texting photos of your floors is the fastest way to get an experienced specialist's assessment of your project &mdash; usually the same day.</p>
  <div class="info-grid">
    <div class="card">
      <h3>Call or Text</h3>
      <p style="font-size:22px;font-weight:700;"><a href="tel:858-699-0072" style="color:var(--cta-red);">858-699-0072</a></p>
      <p>Texting clear photos of your floors is the fastest way to get expert guidance.</p>
    </div>
    <div class="card">
      <h3>Email Project Photos or Questions</h3>
      <p style="font-size:18px;"><a href="mailto:sandiegohardwoods@gmail.com" style="color:var(--cta-red);font-weight:700;">sandiegohardwoods@gmail.com</a></p>
    </div>
    <div class="card">
      <h3>Response Time</h3>
      <p>We typically respond the same day to calls, texts, emails, and photo assessment requests throughout San Diego County.</p>
    </div>
  </div>

  <div class="card cta-card" style="margin-top:34px;">
    <div class="cta-copy">
      <h3>Not Every Hardwood Floor Needs Refinishing</h3>
      <p>Before investing in a complete refinishing project, let us evaluate your floors. Many hardwood, engineered hardwood, wire-brushed, hand-scraped and oil-finished floors can often be restored with our <strong>Bona Power Scrubber deep cleaning system</strong>, professional maintenance coat, or targeted repairs. We'll recommend the solution that gives you the best long-term value&mdash;not simply the most expensive option.</p>
      <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">Learn When Deep Cleaning Is a Better Option &rarr;</a></p>
    </div>
  </div>
</section>

<section class="block" id="consultation-services">
  <p class="eyebrow">Assessments, Inspections &amp; Consultation</p>
  <h2>Looking for Our Floor Assessment &amp; Inspection Services?</h2>
  <p class="lede">Our professional floor assessment, inspection, and consultation options &mdash; from the free phone and photo assessment to the in-home project assessment, pre-purchase floor inspections, and complex damage or insurance analysis &mdash; are now presented on our homepage.</p>
  <div style="text-align:center;">
    <a class="btn btn-outline" href="https://www.sdhardwoods.com/#professional-floor-assessments">View Floor Assessments &amp; Inspections &rarr;</a>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Ways to Reach Us", MAIN,
         str(BUILD.parent / "contact_us.html"))
