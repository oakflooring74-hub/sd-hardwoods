import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble
from public_business_rules import replace_area_served, FULL_SAN_DIEGO_AREAS, SOUTH_ORANGE_COUNTY

HEAD_META = """<title>Contact San Diego Hardwoods | Free Phone &amp; Photo Assessment</title>
<meta name="description" content="Call, text floor photos or email San Diego Hardwoods for a free preliminary phone and photo assessment of flooring service needs.">
<link href="https://www.sdhardwoods.com/contact_us.html" rel="canonical">
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
# Milestone 2.9: this page's #local declaration had no areaServed at all --
# add the complete, centralized San Diego + South Orange County list so the
# shared entity carries the full location footprint on every page it's
# declared on, not just the homepage.
JSONLD = replace_area_served(JSONLD, FULL_SAN_DIEGO_AREAS + SOUTH_ORANGE_COUNTY)

# Milestone 2.6: the shared GA4 implementation (build/chrome/analytics.html) is
# injected by assemble() -- leave this empty; never add a per-page loader.
GA = ""

VCARD = "SAN DIEGO LICENSED WOOD FLOOR RESTORATION/REFINISHING CONTRACTOR 858-699-0072 EXPERIENCE EXCEPTIONAL DUSTLESS HARDWOOD AND BAMBOO FLOOR REFINISHING IN SAN DIEGO. ALL WORK PERFORED BY A HIGHLY EXPERIENCED FLOORING EXPERT WITH OVER 30 YEARS EXPERIENCE RESTORING AND REPAIRING SOLID AND ENGINEERED HARDWOOD AND BAMBOO FLOORING. CALL TODAY TO SCHEDULE A CONSULTATION. TEXT PHOTOS OF YOUR PROJECT FOR AN IMMEDIATE ASSESSMENT."

MAIN = """
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Contact San Diego Hardwoods &mdash; Hardwood Floor Refinishing, Installation, Deep Cleaning, Repairs &amp; Restoration in San Diego</h1>
  <div class="cta-row">
    <a class="btn btn-call" href="sms:+18586990072">Text Photos for a Free Assessment</a>
    <a class="btn btn-outline" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
  </div>
</section>

<section class="block">
  <h2>Start With a Free Phone &amp; Photo Assessment &mdash; Anywhere in San Diego County</h2>
  <p class="lede">Based in Carmel Valley, San Diego 92130, we restore and repair solid and engineered hardwood and bamboo flooring for homeowners throughout San Diego County. Text clear overall and close-up photos of your floors for the fastest initial review &mdash; you are also welcome and encouraged to call, and photos may be emailed when texting is not practical.</p>
  <div class="info-grid">
    <div class="card">
      <h3>1. Text Photos for a Free Assessment</h3>
      <p style="font-size:18px;font-weight:700;"><a href="sms:+18586990072" style="color:var(--cta-red);">Text Floor Photos to 858-699-0072</a></p>
      <p>Texting clear overall and close-up photos of your floors is the fastest way to start your Free Phone &amp; Photo Assessment &mdash; usually with a same-day initial review.</p>
    </div>
    <div class="card">
      <h3>2. Call to Discuss Your Floor</h3>
      <p style="font-size:22px;font-weight:700;"><a href="tel:+18586990072" style="color:var(--cta-red);">Call 858-699-0072</a></p>
      <p>You are always welcome to simply call and talk through your floors with an experienced specialist.</p>
    </div>
    <div class="card">
      <h3>3. Email Photos</h3>
      <p style="font-size:18px;"><a href="mailto:sandiegohardwoods@gmail.com" style="color:var(--cta-red);font-weight:700;">sandiegohardwoods@gmail.com</a></p>
      <p>When texting is not practical, email your photos or questions instead.</p>
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

  <p class="lede" style="margin-top:30px;">Need an in-home project assessment, a pre-purchase floor inspection, or written floor-condition documentation? See our <a href="/floor-assessments-inspections" style="color:var(--brass-deep);font-weight:700;">Floor Assessments &amp; Inspections</a> services.</p>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Ways to Reach Us", MAIN,
         str(BUILD.parent / "contact_us.html"))
