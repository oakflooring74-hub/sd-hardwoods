# -*- coding: utf-8 -*-
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble

HEAD_META = """<title>Hardwood Floor Refinishing &amp; Dustless Sanding Videos | San Diego</title>
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

SCRATCH = str(BUILD / "data" / "videos_of_refinishing_process")
with open(BUILD / "data" / "videos_of_refinishing_process" / "jsonld_fixed.html", encoding="utf-8") as f:
    JSONLD = f.read()
# Note: the live source has 2 of these 5 script blocks fused together (a missing </script> merges
# the CollectionPage schema into the following VideoObject @graph schema, making both invalid JSON
# as served). Split back into 5 valid, separately-closed <script> blocks above -- content unchanged,
# only the missing closing tag was restored.

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

VCARD = "THE BEST HARDWOOD FLOOR REFINISHING IN SAN DIEGO CALL TODAY 858-699-0072 LICENSED CONTRACTOR WITH OVER 30 YEARS EXPERIENCE WITH ALL TYPES OF SOLID AND ENGINEERED WOOD FLOORS. ALL WORK IS GUARANTEED AND PERFORMED BY A SMALL CREW OF SKILLED AND COURTEOUS CRAFTSMEN. TEXT PHOTOS FOR QUICK ASSESSMENT OF YOUR FLOORING PROJECT. CSLB LICENSED FLOORING CONTRACTOR IN SAN DIEGO. DUST CONTAINMENT SANDING EQUIPMENT USED FOR ALL PHASES OF EACH PROJECT."

VIDEOS = [
    dict(title="Engineered Maple Hardwood Floor Refinishing – Encinitas Oceanfront Home",
         desc="Watch the first stage of refinishing an engineered maple hardwood floor with a sun-faded aluminum oxide factory finish. Our specialist carefully removes the original finish without sanding through the engineered wear layer, creating a flat foundation for later planetary sanding and a premium Bona water-based finish. This process is especially important for coastal homes exposed to UV sunlight, salt air, and heavy daily wear.",
         yt="7mhqGYozb1o", extra="&start=10",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_1.html", "See results in Project Gallery 1")),
    dict(title="Carmel Valley Richard Marshall walnut. Old tung‑oil wear and sun fade required a full restoration. Initial SUPERHUMMEL pass takes the field flat; later (not shown) we planetary‑sand dead‑flat, re‑scrape the V‑grooves, restore the French bleed, apply a custom walnut stain, and finish with an extra‑matte commercial water‑based system.",
         desc=None, yt="JJtaFORkXKw", extra="",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_2.html", "See results in Project Gallery 2")),
    dict(title="Richard Marshall solid Walnut Hardwood Floor Restoration and deep cleaning – Carmel Valley",
         desc="Watch the restoration of a premium Richard Marshall walnut hardwood floor in Carmel Valley. Years of wear, sun fading, and an aging tung oil finish required complete restoration. This video shows the initial SUPERHUMMEL belt sanding process that prepares the floor for precision planetary sanding, restoration of the original French bleed and V-grooves, custom walnut staining, and a durable extra-matte Bona commercial-grade water-based finish.",
         yt="og_K3Gi2i8o", extra="&start=14", gallery=None),
    dict(title="Engineered Maple Hardwood Floor Refinishing – Encinitas Oceanfront Home",
         desc="This video shows the professional refinishing of an engineered maple hardwood floor in an Encinitas oceanfront home. We carefully remove the factory aluminum oxide finish and years of sun and salt-air damage while protecting the thin engineered wear layer. After the initial HUMMEL sanding shown here, the floor is precision-flattened with the Bona Power Drive system before being finished with a premium Bona Traffic HD water-based finish in the homeowner's preferred sheen for exceptional durability and easy maintenance.",
         yt="aP4VimeOu2Q", extra="&start=4", gallery=None),
    dict(title="Professional Hardwood Floor Sanding &amp; Refinishing – San Diego",
         desc="Watch the first stage of a professional hardwood floor refinishing project in San Diego. This video demonstrates precision belt sanding to remove worn finishes, flatten uneven floors, and prepare the surface for rotary and Bona Power Drive planetary sanding. The completed floor is finished with a durable commercial-grade Bona water-based finish that provides long-lasting beauty, exceptional durability, and easy maintenance.",
         yt="4Cr1w962mvI", extra="",
         gallery=("https://www.sdhardwoods.com/recent_project_gallery_5.html", "See results in Project Gallery 5")),
    dict(title="Vintage Red Oak Hardwood Floor Refinishing – Bird Rock, La Jolla",
         desc="Watch the professional restoration of a vintage red oak hardwood floor in Bird Rock, La Jolla. This video demonstrates the initial SUPERHUMMEL belt sanding process used to remove worn finishes, surface contamination, and previous sanding imperfections while creating a flat foundation for precision Bona Power Drive planetary sanding. The completed floor receives a durable commercial-grade Bona water-based finish that restores the natural beauty of the original red oak while providing exceptional long-term protection.",
         yt="ix6RoN95uV0", extra="&start=10",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_1", "See results in Project Gallery 1")),
    dict(title="White Oak Hardwood Floor Restoration &amp; Cupping Repair – Rolando / SDSU",
         desc="Watch the restoration of a mid-century white oak hardwood floor near San Diego State University. This video demonstrates professional angle sanding to safely reduce floor cupping before straight-with-the-grain sanding creates a flat foundation for Bona Power Drive planetary sanding. The restored floor is completed with a durable Bona water-based finish that preserves the character of vintage hardwood while providing exceptional long-term protection and easy maintenance.",
         yt="Yn0LaA26Emc", extra="&start=10",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_2", "See results in Project Gallery 2")),
    dict(title="Engineered Brazilian Cherry (Jatoba) Hardwood Floor Refinishing – Solana Beach",
         desc="Watch the professional refinishing of an engineered Brazilian Cherry (Jatoba) hardwood floor in Solana Beach. This video demonstrates the careful removal of a factory aluminum oxide finish and years of sun fading while protecting the engineered wear layer. After the initial sanding shown here, the floor is precision-flattened with the Bona Power Drive system before receiving a durable Bona Traffic HD water-based finish. We also offer professional bleaching and lightening services for homeowners looking to modernize dark Brazilian Cherry floors.",
         yt="jMVl659t-8g", extra="&start=10",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_3", "See results in Project Gallery 3")),
    dict(title="100-Year-Old Douglas Fir Floor Restoration – Little Italy, San Diego",
         desc="Watch the restoration of a 100-year-old Douglas Fir hardwood floor in Little Italy, San Diego. This video demonstrates the initial sanding process used to remove paint, glue, mastic, and decades of wear while carefully preserving the character of this historic softwood floor. After precision flattening and final preparation, the floor is completed with a premium Bona water-based finish that protects the wood while maintaining its original beauty. We specialize in restoring historic Douglas Fir floors throughout San Diego's older homes and historic neighborhoods.",
         yt="0q3G7s7NAkg", extra="&start=10",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_4", "See results in Project Gallery 4")),
    dict(title="White Oak Hardwood Floor Refinishing &amp; Repair – North Park, San Diego",
         desc="Watch the refinishing of a white oak hardwood floor in North Park, San Diego. This video shows the initial sanding process used to remove a dark, outdated finish while flattening the floor and blending professional wood repairs for a seamless appearance. After precision Bona Power Drive sanding, the floor is finished with a premium Bona Traffic HD water-based finish that highlights the natural beauty of the white oak while providing exceptional durability and easy maintenance.",
         yt="EHHRst9MvXU", extra="&start=10",
         gallery=("https://www.sdhardwoods.com/recent_project_gallery_5", "See results in Project Gallery 5")),
    dict(title="White Oak Hardwood Floor Repair &amp; Refinishing – North Park, San Diego",
         desc="Watch the first stage of repairing and refinishing a white oak hardwood floor in North Park, San Diego. This video demonstrates professional belt sanding that levels the floor while blending recessed fasteners and precision white oak plug repairs into the surrounding wood. The project is completed with Bona Power Drive planetary sanding and a premium Bona Traffic HD water-based finish for exceptional durability, easy maintenance, and a natural appearance.",
         yt="rMtQ0TfEkwc", extra="&start=10",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_1", "See results in Project Gallery 1")),
    dict(title="White Oak Hardwood Floor Color Change &amp; Refinishing – North Park, San Diego",
         desc="Watch the transformation of a white oak hardwood floor in North Park, San Diego, as a dark stained finish and worn polyurethane coating are professionally removed to reveal the natural beauty of the wood. This video shows the initial sanding process that levels the floor and prepares it for Bona Power Drive planetary sanding and a premium Bona Traffic HD water-based finish. Whether you want to restore natural white oak or completely change your floor color, we provide expert hardwood floor refinishing throughout San Diego.",
         yt="wh0dV0th238", extra="&start=10",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_2", "See results in Project Gallery 2")),
    dict(title="Hardwood Floor Refinishing &amp; Dustless Sanding – San Diego",
         desc="Watch professional hardwood floor refinishing performed in San Diego using advanced dustless sanding equipment and the Bona hardwood floor finishing system. This video demonstrates the initial sanding process that removes worn finishes, scratches, discoloration, and surface damage while preparing the floor for precision Bona Power Drive sanding and a premium Bona Traffic HD water-based finish. We specialize in hardwood floor refinishing, engineered wood refinishing, repairs, restoration, and complete floor color transformations throughout San Diego County.",
         yt="_kxWUWkSkUA", extra="",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_3", "See results in Project Gallery 3")),
    dict(title="Historic Douglas Fir Floor Restoration – Golden Hill, San Diego",
         desc="Watch the restoration of a historic Douglas Fir floor in a Golden Hill apartment. This project demonstrates the professional removal of heavy paint, old finishes, and surface damage while preserving the character of this century-old softwood flooring. After precision sanding and restoration, the floor is protected with a premium Bona Traffic HD water-based finish that provides exceptional durability while maintaining the authentic appearance of historic Douglas Fir. We specialize in restoring original hardwood floors throughout San Diego's historic homes and neighborhoods.",
         yt="KfMyOOqha6o", extra="",
         gallery=("https://www.sdhardwoods.com/recent_project_photo_gallery_4", "See results in Project Gallery 4")),
]

def video_block(v):
    gallery_html = ""
    if v["gallery"]:
        url, label = v["gallery"]
        gallery_html = f'<p><a href="{url}" class="btn btn-outline" style="padding:8px 18px;font-size:15px;">{label} &rarr;</a></p>'
    desc_html = f'<p>{v["desc"]}</p>' if v["desc"] else ""
    src = f'https://www.youtube-nocookie.com/embed/{v["yt"]}?rel=0&modestbranding=1&playsinline=1&autoplay=0&controls=1&loop=1&playlist={v["yt"]}&enablejsapi=1{v["extra"]}'
    return f"""
<div class="card" style="margin-bottom:28px;">
  <h3>{v["title"]}</h3>
  {desc_html}
  <div class="video-frame" style="margin:18px 0;"><iframe src="{src}" title="{v["title"]}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="aspect-ratio:16/9;"></iframe></div>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:8586990072" style="padding:8px 18px;font-size:15px;">Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:18586990072" style="padding:8px 18px;font-size:15px;">Text Photos for a Free Assessment</a>
  </div>
  {gallery_html}
</div>"""

video_entries = "\n".join(video_block(v) for v in VIDEOS)

MAIN = f"""
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Real Hardwood Floor Refinishing, Dustless Sanding &amp; Restoration Videos</h1>
  <div class="video-frame" style="margin:20px auto;max-width:800px;">
    <iframe width="800" height="450" src="https://www.youtube.com/embed/7mhqGYozb1o" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>
  <p><strong>Watch real hardwood floor refinishing projects</strong> completed throughout <strong>San Diego</strong>. These videos demonstrate our <strong>100% dustless sanding process</strong>, hardwood floor repairs, engineered hardwood refinishing, restoration techniques, and <strong>Bona finishing systems</strong> on actual customer homes. See the craftsmanship, attention to detail, and professional methods that have earned the trust of San Diego homeowners for over 35 years.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:8586990072">&#9742; Call or Text 858-699-0072 for a Free Phone Assessment</a>
  </div>
</section>

<section class="block">
  <h2>Hardwood Floor Refinishing Videos by Project</h2>
  {video_entries}
</section>

<section class="block">
  <div class="cta-row" style="justify-content:center;flex-wrap:wrap;gap:20px;margin-bottom:30px;">
    <a href="https://www.sdhardwoods.com/contact_us.html"><img src="/CONTACT US BETTER BUTTON 2025.png" alt="Contact San Diego Hardwoods for a free in-home estimate — hardwood floor refinishing, dust-free sanding, repairs, and installation services in La Jolla, Del Mar, Encinitas, Rancho Santa Fe, Carmel Valley, and North County San Diego" style="height:180px;width:180px;border-radius:10px;"></a>
    <a href="https://www.sdhardwoods.com/recent_project_photo_gallery_1.html"><img src="/NEXT PAGE BUTTON 2025.png" alt="SEE BEFORE AND AFTER PHOTOS OF SAN DIEGO HARDWOOD FLOOR REFINISHING DEEP CLEANING AND INSTALLATION FIX YOUR WOOD FLOOR TODAY NEAR ME FREE ESTIMATES SAN DIEGO HARDWOOD FLOOR INSTALLER" style="height:180px;width:180px;border-radius:10px;"></a>
    <a href="https://www.sdhardwoods.com/about_us.html"><img src="/ABOUT US 2025 BUTTON.png" alt="About San Diego Hardwoods — meet your local hardwood floor refinishing and installation experts with 35+ years of experience serving La Jolla, Del Mar, Rancho Santa Fe, Encinitas, Carmel Valley, Solana Beach, and all coastal North County San Diego" style="height:180px;width:180px;border-radius:10px;"></a>
  </div>

  <h2>Why Homeowners Throughout San Diego Watch Our Videos Before Hiring a Hardwood Floor Contractor</h2>
  <p class="lede">For more than <strong>35 years</strong>, San Diego Hardwoods has helped homeowners restore <strong>hardwood, engineered hardwood, bamboo, cork, and historic wood floors</strong> throughout San Diego County. These videos feature actual customer projects&mdash;not stock footage or demonstrations&mdash;so you can see our <strong>100% dustless sanding equipment</strong>, hardwood floor repair techniques, professional restoration process, and premium Bona finishing systems being used in real homes.</p>
  <p class="lede">Whether your floors need <strong>hardwood floor refinishing</strong>, repairs, deep cleaning, recoating, color changes, engineered hardwood restoration, or complete hardwood floor installation, we provide free phone assessments throughout <strong>La Jolla, Del Mar, Rancho Santa Fe, Encinitas, Carmel Valley, Solana Beach, Point Loma, Mission Hills, Coronado, Poway, Escondido</strong>, and communities across San Diego County.</p>

  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:8586990072">Call or Text 858-699-0072</a>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Our Refinishing Process Videos", MAIN,
         str(BUILD.parent / "videos_of_refinishing_process.html"))
