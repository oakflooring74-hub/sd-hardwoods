import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble

SCRATCH = str(BUILD / "data" / "about_us")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

HEAD_META = read(SCRATCH + r"\head_meta.html") + """
<meta name="description" content="Learn about San Diego Hardwoods, an owner-operated licensed flooring contractor providing refinishing, restoration, repairs and installation since 1990.">
<link href="https://www.sdhardwoods.com/about_us.html" rel="canonical">
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">
"""

JSONLD = read(SCRATCH + r"\jsonld.html")

# Milestone 2.4: obsolete Universal Analytics (UA-20793161-1 / _gaq / ga.js) removed
# site-wide. GA4 is blocked pending the owner's confirmed Measurement ID.
GA = ""

VCARD = read(SCRATCH + r"\vcard.txt").strip()

MAIN = """
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>About San Diego Hardwoods &mdash; Trusted Hardwood Floor Refinishing, Installation, Restoration &amp; Deep Cleaning Experts Serving San Diego Since 1990</h1>
  <p><strong>Text photos for a fast, expert assessment &mdash; most replies the same day.</strong></p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>

<section class="block">
  <div class="video-frame"><div id="heroVideoMount"></div></div>
  <div class="video-cta">
    <p><strong style="color:var(--cta-red);">Expert French Oak &amp; Wire-Brushed Refinishing.</strong> Text photos of your project to start your professional assessment.</p>
    <a class="btn btn-call" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>
<script type="text/javascript">
(function () {
    var YT_ID = "McBbfiMpqPg";
    var params = "rel=0&modestbranding=1&playsinline=1&autoplay=0&mute=1&controls=1&loop=1&playlist=" + YT_ID + "&enablejsapi=1";
    var src = "https://www.youtube-nocookie.com/embed/" + YT_ID + "?" + params;
    var mount = document.getElementById("heroVideoMount");
    var iframe = document.createElement("iframe");
    iframe.src = src;
    iframe.style.position = "absolute"; iframe.style.top = "0"; iframe.style.left = "0";
    iframe.style.width = "100%"; iframe.style.height = "100%";
    iframe.setAttribute("allowfullscreen", "allowfullscreen");
    mount.appendChild(iframe);
})();
</script>

<section class="block">
  <div class="card cta-card">
    <div class="cta-copy">
      <h3>Not Every Hardwood Floor Needs Refinishing</h3>
      <p>One of the biggest mistakes homeowners make is sanding a floor that could be restored another way. After more than 35 years refinishing hardwood floors throughout San Diego County, we can determine whether your floors would benefit most from a professional <strong>Bona Power Scrubber deep cleaning</strong>, a protective maintenance coat, targeted repairs, or complete refinishing. Deep cleaning is especially effective for <strong>wire-brushed hardwood, matte finishes, oil-finished floors, and floors with embedded dirt or residue</strong>, often restoring their natural beauty without the expense of sanding.</p>
      <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">Learn When Deep Cleaning Is the Better Option &rarr;</a></p>
    </div>
  </div>
</section>

<section class="block">
  <figure style="max-width:520px;margin:0 auto 30px;border-radius:10px;overflow:hidden;border:1px solid var(--line);">
    <a href="/LARK56.jpg"><img src="/LARK56.jpg" alt="Hardwood floor refinishing in Encinitas — deep cleaning and prep on wide-plank oak before a durable, dust-contained recoat for a coastal North County home." style="width:100%;display:block;"></a>
  </figure>

  <h2>About San Diego Hardwoods &ndash; 35+ Years of Dustless Refinishing &amp; Installation Expertise</h2>
  <p class="lede">Second-generation craftsmanship. Licensed, bonded and insured California flooring contractor. Bona Certified Craftsman specializing in hardwood floor refinishing, restoration, custom installation, repairs and deep cleaning throughout San Diego County.</p>

  <div class="info-grid">
    <div class="card">
      <h3>Our Story</h3>
      <p>The owner of San Diego Hardwoods is a second-generation hardwood floor craftsman who began learning the trade during the 1980s while working alongside family members. His early experience included traditional solid hardwood installations in Colorado's custom mountain homes, where every floor was nailed down, sanded, stained and finished by hand. Those traditional methods created a foundation of craftsmanship that continues today.</p>
      <p>While much of today's flooring industry has shifted toward floating floors, vinyl plank and prefabricated products, San Diego Hardwoods continues to install genuine solid hardwood flooring designed to last for generations.</p>
    </div>
    <div class="card">
      <h3>Bringing Traditional Craftsmanship to San Diego</h3>
      <p>Since establishing San Diego Hardwoods in 1990, we've specialized in refinishing, restoring, repairing and installing hardwood flooring throughout San Diego County. Our experience includes oak, maple, walnut, hickory, Brazilian cherry, engineered hardwood, bamboo flooring and many domestic and exotic species.</p>
      <p>Every installation begins with selecting the proper lumber, understanding grain orientation, stability and how each species performs within Southern California's coastal climate.</p>
    </div>
    <div class="card">
      <h3>Modern Equipment. Traditional Craftsmanship.</h3>
      <p><strong>Advanced Dust Containment</strong> &mdash; Our professional dust containment systems dramatically reduce airborne dust while protecting your home during refinishing.</p>
      <p><strong>Precision Rotary Sanding</strong> &mdash; Modern rotary sanding equipment produces flatter, smoother hardwood floors than traditional drum sanders while minimizing chatter marks and uneven sanding patterns.</p>
      <p><strong>Premium Bona Finishing Systems</strong> &mdash; We use Bona sealers and GREENGUARD Certified finishes that provide exceptional durability, beautiful appearance and low-VOC performance.</p>
    </div>
    <div class="card">
      <h3>Professional Credentials</h3>
      <p>Every project is personally supervised by an experienced flooring craftsman. San Diego Hardwoods is a CSLB-licensed, bonded and insured California flooring contractor &mdash; <strong>California contractor license #1017549</strong> &mdash; and a proud member of the Bona Certified Craftsman Program. All work is guaranteed and performed by a small crew of skilled, courteous craftsmen &mdash; and dust-containment sanding equipment is used on every phase of every project.</p>
    </div>
    <div class="card">
      <h3>Specialty Hardwood Flooring Services</h3>
      <p>Beyond traditional refinishing, we specialize in custom stain development, Scandinavian-inspired white finishes, wire-brushed hardwood floors, oil-finished flooring, historical floor restoration, hardwood floor repairs, engineered hardwood, bamboo flooring, professional deep cleaning using the Bona Power Scrubber, maintenance coats and complete hardwood floor restoration.</p>
    </div>
    <div class="card">
      <h3>Why Homeowners Choose San Diego Hardwoods</h3>
      <p><strong>35+ Years of Experience</strong> &mdash; Serving San Diego homeowners since 1990.</p>
      <p><strong>Owner-Operated Quality</strong> &mdash; The owner remains personally involved on every project.</p>
      <p><strong>Dust-Contained Sanding on Every Project</strong> &mdash; Cleaner, healthier hardwood floor refinishing with advanced dust collection systems.</p>
      <p><strong>Custom Color Expertise</strong> &mdash; Natural finishes, contemporary stains, whitewashed floors, matte finishes and specialty color matching.</p>
      <p><strong>Complete Hardwood Floor Services</strong> &mdash; Refinishing, restoration, repairs, installation, deep cleaning, maintenance coats and specialty hardwood flooring services.</p>
    </div>
  </div>

  <div class="card" style="max-width:820px;margin:34px auto 0;text-align:center;">
    <h3>Let's Discuss Your Hardwood Flooring Project</h3>
    <p>Whether your floors need refinishing, repairs, deep cleaning, custom installation or complete restoration, we're happy to discuss your options and recommend the solution that's right for your home.</p>
    <p style="font-size:20px;"><strong>Call <a href="tel:+18586990072" style="color:var(--cta-red);">858-699-0072</a> or <a href="sms:+18586990072" style="color:var(--cta-red);">text floor photos</a> today.</strong></p>
  </div>

  <div class="cta-row" style="justify-content:center;margin-top:30px;">
    <a class="btn btn-call" href="tel:+18586990072">Call 858-699-0072 for Your Free Phone Assessment</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Our Story &amp; Credentials", MAIN,
         str(BUILD.parent / "about_us.html"))
