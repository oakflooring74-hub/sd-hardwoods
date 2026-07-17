import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble

HEAD_META = """<title>Contact San Diego Hardwoods | Free Estimates for Hardwood Floor Refinishing, Repairs &amp; Installation</title>
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
    <div class="cta-media">
      <a href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">
        <img src="https://www.sdhardwoods.com/ultra%20clean%20button.png" alt="San Diego hardwood floor deep cleaning using the Bona Power Scrubber for hardwood, engineered hardwood, wire-brushed and oil-finished floors">
      </a>
    </div>
  </div>
</section>

<section class="block" id="consultation-services">
  <p class="eyebrow">More Than 35 Years of Specialized Expertise</p>
  <h2>Professional Consultation Services</h2>
  <p class="lede">When a floor needs more than a phone conversation, our in-home services put three decades of hands-on hardwood expertise to work for you &mdash; honest diagnosis, education, documentation, and planning. The free phone assessment is always the right first step, and it tells us which service, if any, actually fits your situation.</p>

  <div class="consult-grid">
    <div class="consult-card consult-free">
      <div class="consult-head">
        <h3>Free Phone Assessment</h3>
        <span class="consult-price">Free</span>
      </div>
      <p>Call or text clear photographs of your floor for an initial phone assessment at no charge. Emailed photographs are also welcome. This first step helps determine whether your floor appears to need cleaning, maintenance, repair, refinishing, damage evaluation &mdash; or an in-person consultation.</p>
      <div class="cta-row" style="justify-content:flex-start;margin-top:6px;">
        <a class="btn btn-call" href="tel:8586990072" style="padding:11px 22px;font-size:15.5px;">&#9742; Call or Text 858-699-0072</a>
        <a class="btn btn-outline" href="sms:+18586990072?&amp;body=Hi%20San%20Diego%20Hardwoods%2C%20I%20have%20photos%20of%20my%20floors%20to%20send%20for%20a%20free%20phone%20assessment." style="padding:11px 22px;font-size:15.5px;">Text Floor Photos</a>
      </div>
    </div>

    <div class="consult-card">
      <div class="consult-head">
        <h3>Initial In-Home Floor Assessment</h3>
        <span class="consult-price">$75</span>
      </div>
      <p>A focused appointment of up to one hour for straightforward concerns involving worn, faded, dirty, poorly maintained, water-affected, or tenant-damaged hardwood floors. Includes an initial visual assessment and practical recommendations for next steps.</p>
      <p class="consult-fine">Ideal when you simply want an experienced set of eyes on the floor and a clear direction.</p>
    </div>

    <div class="consult-card">
      <div class="consult-head">
        <h3>Extended Hardwood Floor Consultation &amp; Education</h3>
        <span class="consult-price">$150</span>
      </div>
      <p>A more detailed in-person consultation for owners who need deeper analysis, material or finish discussion, restoration options, maintenance planning, problem diagnosis, or one-on-one education about the condition and future care of their floor.</p>
      <p class="consult-fine">Choose this over the $75 assessment when you want time to go deep &mdash; not just a look, but a working session about your floor.</p>
    </div>

    <div class="consult-card">
      <div class="consult-head">
        <h3>Property Management &amp; Tenant Move-Out Floor Assessment</h3>
        <span class="consult-price">$350</span>
      </div>
      <p>Professional assessment and documentation of the visible hardwood-floor condition for property managers, landlords, owners, and tenant move-out situations. May address observed damage, maintenance condition, restoration needs, and the distinction between apparent damage and ordinary wear.</p>
      <p class="consult-fine">Documents visible floor condition from a flooring-trade perspective; it is not a binding legal determination regarding security deposits, liability, tenancy law, or damages.</p>
    </div>

    <div class="consult-card">
      <div class="consult-head">
        <h3>Insurance Damage Consultation &amp; Documentation Support</h3>
        <span class="consult-price">$750</span>
      </div>
      <p>An in-home hardwood-floor damage consultation focused on visible flooring conditions, damage analysis, restoration options, photographs, and organization of flooring-related information that may be useful to the owner, property manager, contractor, or insurer.</p>
      <p class="consult-fine">A flooring-expertise service &mdash; not a public-adjuster service, legal advice, insurance-policy interpretation, claim representation, or coverage advice, and no insurance payment or outcome is guaranteed.</p>
    </div>

    <div class="consult-card">
      <div class="consult-head">
        <h3>Formal Hardwood Floor Inspection Report &amp; Separate Project Estimate</h3>
        <span class="consult-price">$1,500</span>
      </div>
      <p>A detailed inspection service that may include site observations, photographic documentation, written findings, apparent damage or condition analysis, recommended remediation, and a separate estimate for proposed flooring work. The report may be provided by you to an insurer, property manager, attorney, or other relevant party.</p>
      <p><strong>Some or all of the inspection and report fee may be credited toward the approved flooring project under written agreement.</strong></p>
      <p class="consult-fine">Acceptance by any third party, and any specific outcome, cannot be guaranteed.</p>
    </div>
  </div>

  <p class="consult-note">These services reflect professional hardwood flooring expertise &mdash; diagnosis, education, and documentation &mdash; not a fee to estimate ordinary project work. Exact scope and deliverables are confirmed when scheduling. Call or text <a href="tel:8586990072" style="color:var(--cta-red);font-weight:700;">858-699-0072</a> to start with a free phone assessment.</p>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Ways to Reach Us", MAIN,
         str(BUILD.parent / "contact_us.html"))
