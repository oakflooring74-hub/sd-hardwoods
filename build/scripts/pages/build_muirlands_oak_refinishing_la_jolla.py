# -*- coding: utf-8 -*-
"""Builds muirlands-oak-refinishing-la-jolla.html — the first individual project
showcase page (SEO footprint expansion, post-stabilization).

This is a standalone authored page with no raw-source extraction needed. It models
its structure on build_floor_assessments.py: head metadata, JSON-LD schema, and body
content are all authored here directly, then assembled through the same shared chrome
as every other page via assemble_page.assemble().

Project context (from docs/2026-09-muirlands-oak-vision-analysis.md):
  - Folder inspected: MUIRLANDS OAK FLOOR REFINISHING LA JOLLA SAN DIEGO WATERMARKED/
  - 28 JPG images, all 1800px wide (26 portrait at 1800x3798, 2 landscape at ~1800x852)
  - Wood species confirmed as red oak — no removals needed
  - Dictation matches photos; owner may update dictation once aligned

Owner dictation (verbatim): Hardwood floor refinishing San Diego this La Jolla home had
vintage red oak flooring that was sanded and refinished to perfection by San Diego hardwoods
using 100% dust containment equipment modern planetary and Rotary sanders and traditional
stain and modern low VOC high durability bona traffic HD polyurethane finish for the ultimate
in durability this Ocean view San Diego home greatly benefited from having these floors
professionally sanded to raw wood all of the gaps and the cracks filled with a trowel fill red
oak sold hardwood and bamboo wood filler termite damage stained boards removed and replaced
and a new section of flooring installed by nailing down the new oak flooring to the subfloor in
an office and then sanding everything to match and creating samples for the homeowner to decide
from This was a multi stage project in San Diego where the hardwood floor was refinished and
this vintage wood floor was restored by a courteous team of skilled Craftsman in san diego.

Business facts reuse the established #local entity via @id, matching the pattern in
build_floor_assessments.py — no addresses, hours, coordinates, ratings, or credentials added here.
"""
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble
from public_business_rules import (
    PRIORITY_COASTAL_SD, FULL_SAN_DIEGO_AREAS, SOUTH_ORANGE_COUNTY,
)

# Per-page Service.areaServed: San Diego only (South Orange County lives on the shared #local entity).
_PROJECT_AREA = ["La Jolla", "San Diego County"] + [a for a in PRIORITY_COASTAL_SD if a != "La Jolla"]


HEAD_META = """<title>Red Oak Floor Refinishing La Jolla San Diego | Hardwood Restoration</title>
<meta name="description" content="Vintage red oak floor refinishing in La Jolla, San Diego. Sanded to perfection with dust containment, Bona Traffic HD polyurethane finish, and termite-damage board replacement by a courteous team of skilled Craftsman.">
<link href="https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html" rel="canonical">
<link href="/favicon.ico" rel="icon" type="image/x-icon">
<link href="/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#f8f4ec">
<link href="/LOGO-2025.png" rel="logo" type="image/png">"""

# One connected graph: the canonical #local business entity, a WebPage for this project,
# a Service describing the refinishing work performed, and ImageObject entities for each
# before/after/process photo — all @id-linked to each other and referencing #local by @id.
JSONLD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["LocalBusiness","HomeAndConstructionBusiness"],
      "@id": "https://www.sdhardwoods.com/#local",
      "name": "San Diego Hardwoods",
      "alternateName": "San Diego Hardwoods Dustless Hardwood and Bamboo Floor Refinishing Installation Repairs and Deep Cleaning",
      "url": "https://www.sdhardwoods.com",
      "telephone": "+18586990072",
      "email": "sandiegohardwoods@gmail.com",
      "image": "/LOGO-2025.png",
      "logo": "/LOGO-2025.png",
      "priceRange": "$$$",
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+18586990072",
        "contactType": "sales",
        "availableLanguage": ["en"],
        "areaServed": "US"
      },
      "hasCredential": {
        "@type": "EducationalOccupationalCredential",
        "name": "Bona Certified Craftsman",
        "url": "https://www.bona.com/en-us/homeowner/find-a-contractor/contractor-details/?storeid=83667",
        "image": "/bonacc.jpeg",
        "issuer": {"@type": "Organization", "name": "Bona"}
      },
      "sameAs": ["https://www.youtube.com/@sandiegohardwoods", "https://maps.app.goo.gl/hbNaSo2guARgrZTa8"]
    },
    {
      "@type": "WebPage",
      "@id": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html#webpage",
      "url": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html",
      "name": "Red Oak Floor Refinishing in La Jolla San Diego | Hardwood Restoration",
      "description": "Vintage red oak floor refinishing in a La Jolla, San Diego home. Sanded to raw wood with dust containment equipment, gaps filled, termite-damaged boards replaced, and new oak flooring installed in an office — all finished with Bona Traffic HD polyurethane by skilled Craftsman.",
      "inLanguage": "en",
      "about": {"@id": "https://www.sdhardwoods.com/#local"},
      "mainEntity": {"@id": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html#service"}
    },
    {
      "@type": "Service",
      "@id": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html#service",
      "name": "Red Oak Floor Refinishing in La Jolla, San Diego",
      "url": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html",
      "mainEntityOfPage": {"@id": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html#webpage"},
      "provider": {"@id": "https://www.sdhardwoods.com/#local"},
      "areaServed": ["La Jolla", "Del Mar", "Solana Beach", "Encinitas", "Cardiff-by-the-Sea", "Rancho Santa Fe", "Carmel Valley", "Fairbanks Ranch", "Santaluz", "Coronado", "Point Loma"],
      "serviceType": ["Hardwood floor refinishing", "Oak floor restoration", "Floor repair and replacement"],
      "description": "Vintage red oak flooring in a La Jolla, San Diego home was sanded to raw wood using 100% dust containment equipment with modern planetary and rotary sanders. Gaps were filled with trowel-grade hardwood filler; termite-damaged boards were removed and replaced; new oak flooring was nailed down to the subfloor in an office and sanded to match. Traditional stain and a modern low-VOC, high-durability Bona Traffic HD polyurethane finish were applied for long-lasting protection.",
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Muirlands Oak Floor Refinishing Services",
        "itemListElement": [
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Dust-contained sanding to raw wood", "description": "100% dust containment equipment with modern planetary and rotary sanders"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Gap filling and crack repair", "description": "Trowel-fill hardwood and bamboo wood filler for gaps and cracks"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Termite damage board replacement", "description": "Stained boards removed and replaced to match existing flooring"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "New oak flooring installation", "description": "Nail-down installation of new red oak flooring to subfloor, sanded to match"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Stain and polyurethane finishing", "description": "Traditional stain plus low-VOC Bona Traffic HD high-durability polyurethane finish"}}
        ]
      }
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html#image-1",
      "contentUrl": "https://www.sdhardwoods.com/red-oak-floor-refinishing-la-jolla-before-sanding-1.jpg",
      "url": "https://www.sdhardwoods.com/red-oak-floor-refinishing-la-jolla-before-sanding-1.jpg",
      "name": "Vintage red oak flooring before sanding in La Jolla home"
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html#image-2",
      "contentUrl": "https://www.sdhardwoods.com/dustless-hardwood-floor-sanding-la-jolla-wide.jpg",
      "url": "https://www.sdhardwoods.com/dustless-hardwood-floor-sanding-la-jolla-wide.jpg",
      "name": "Dust-contained sanding of red oak floors in La Jolla"
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html#image-3",
      "contentUrl": "https://www.sdhardwoods.com/red-oak-floor-restoration-and-repair-san-diego-oak-professional.jpg",
      "url": "https://www.sdhardwoods.com/red-oak-floor-restoration-and-repair-san-diego-oak-professional.jpg",
      "name": "Professional red oak floor restoration in San Diego"
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html#image-4",
      "contentUrl": "https://www.sdhardwoods.com/red-oak-finished-stairs-la-jolla-san-diego.jpg",
      "url": "https://www.sdhardwoods.com/red-oak-finished-stairs-la-jolla-san-diego.jpg",
      "name": "Finished red oak stairs in La Jolla home after refinishing"
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/muirlands-oak-refinishing-la-jolla.html#image-5",
      "contentUrl": "https://www.sdhardwoods.com/custom-stained-red-oak-floor-professional-finishing-sd.jpg",
      "url": "https://www.sdhardwoods.com/custom-stained-red-oak-floor-professional-finishing-sd.jpg",
      "name": "Custom stained red oak floor with professional finishing in San Diego"
    }
  ]
}
</script>"""

# Milestone 2.6: the shared GA4 implementation (chrome/analytics.html) is injected by assemble() — leave empty.
GA = ""

VCARD = ("SAN DIEGO LICENSED WOOD FLOOR RESTORATION/REFINISHING CONTRACTOR "
         "858-699-0072 EXPERIENCE EXCEPTIONAL DUSTLESS HARDWOOD AND BAMBOO FLOOR REFINISHING "
         "IN SAN DIEGO. ALL WORK PERFORMED BY A HIGHLY EXPERIENCED FLOORING EXPERT WITH OVER 30 "
         "YEARS EXPERIENCE RESTORING AND REPAIRING SOLID AND ENGINEERED HARDWOOD AND BAMBOO "
         "FLOORING. CALL TODAY TO SCHEDULE A CONSULTATION. TEXT PHOTOS OF YOUR PROJECT FOR AN "
         "IMMEDIATE ASSESSMENT.")

MAIN = """
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Vintage Red Oak Floor Refinishing in La Jolla, San Diego</h1>
  <p>This ocean-view La Jolla home had vintage red oak flooring that was sanded and refinished to perfection by San Diego Hardwoods using 100% dust containment equipment with modern planetary and rotary sanders. Traditional stain and a modern low-VOC, high-durability Bona Traffic HD polyurethane finish were applied for the ultimate in durability.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-call" href="sms:+18586990072">Text Floor Photos for a Free Assessment</a>
  </div>
</section>

<section class="block">
  <p class="eyebrow">A Multi-Stage Restoration Project</p>
  <h2>The Muirlands Oak Refinishing Project &mdash; La Jolla, San Diego</h2>
  <p class="lede">This multi-stage project in San Diego restored vintage red oak flooring to its full beauty. The home greatly benefited from having these floors professionally sanded to raw wood, with all gaps and cracks filled using trowel-grade hardwood filler. Termite-damaged boards were carefully removed and replaced, and a new section of flooring was installed by nailing down fresh oak planks to the subfloor in an office &mdash; then sanded to match seamlessly before samples were created for the homeowner to decide from.</p>
  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call &mdash; Free Assessment</a>
    <a class="btn btn-outline" href="mailto:sandiegohardwoods@gmail.com">Email Floor Photos</a>
  </div>
</section>

<section class="block">
  <h2>The Process: From Raw Wood to Finished Beauty</h2>
  <p>This La Jolla home's vintage red oak flooring was completely sanded to raw wood using San Diego Hardwoods' dust-free equipment with modern planetary and rotary sanders. The entire process used 100% dust containment, ensuring a clean workspace throughout. After sanding, traditional stain was applied followed by a modern low-VOC, high-durability Bona Traffic HD polyurethane finish for the ultimate in long-lasting protection.</p>
  <p>The project addressed several specific issues: deep scratches were eliminated through professional sanding, gaps and cracks between boards were filled with trowel-grade hardwood filler, termite damage was repaired by removing and replacing stained boards, and a new section of flooring was installed in an office area. Everything was then sanded to match the existing floor seamlessly.</p>
  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Schedule Your Free Assessment</a>
  </div>
</section>

<section class="block">
  <h2>Before &amp; After Photo Gallery</h2>
  <p class="lede">Below is the complete visual documentation of this La Jolla red oak floor refinishing project. These wide-angle portrait photos capture every stage from initial sanding through final finish, showing how San Diego Hardwoods' courteous team of skilled Craftsman restored these vintage floors to perfection.</p>
  <div class="gallery">
    <a href="/red-oak-floor-refinishing-la-jolla-before-sanding-1.jpg"><img src="/red-oak-floor-refinishing-la-jolla-before-sanding-1.jpg" alt="Hardwood floor refinishing San Diego — vintage red oak flooring in a La Jolla home before sanding, showing the condition of the floor prior to professional dust-contained restoration by San Diego Hardwoods." loading="lazy"></a>
    <a href="/dustless-hardwood-floor-sanding-la-jolla-wide.jpg"><img src="/dustless-hardwood-floor-sanding-la-jolla-wide.jpg" alt="Dust-free hardwood floor sanding in La Jolla — modern planetary and rotary sanders with 100% dust containment equipment removing old finish from red oak flooring." loading="lazy"></a>
    <a href="/red-oak-refinishing-low-voc-polyurethane-finish-san-diego-1.jpg"><img src="/red-oak-refinishing-low-voc-polyurethane-finish-san-diego-1.jpg" alt="Red oak floor refinishing San Diego — low-VOC Bona Traffic HD polyurethane finish applied to freshly sanded red oak flooring in a La Jolla home." loading="lazy"></a>
    <a href="/bona-traffic-hd-hardwood-floor-finishing-la-jolla-after.jpg"><img src="/bona-traffic-hd-hardwood-floor-finishing-la-jolla-after.jpg" alt="Hardwood floor finishing La Jolla — Bona Traffic HD high-durability polyurethane coating applied to red oak floors after sanding and staining by San Diego Hardwoods." loading="lazy"></a>
    <a href="/professional-wood-floor-restoration-san-diego-oak.jpg"><img src="/professional-wood-floor-restoration-san-diego-oak.jpg" alt="Professional hardwood floor restoration in San Diego — red oak flooring sanded to raw wood and refinished with low-VOC polyurethane by expert Craftsman." loading="lazy"></a>
    <a href="/best-flooring-contractor-san-diego-hardwood-refinishing.jpg"><img src="/best-flooring-contractor-san-diego-hardwood-refinishing.jpg" alt="Best flooring contractor San Diego — red oak floor refinishing with dust containment equipment, traditional stain and Bona Traffic HD finish in a La Jolla home." loading="lazy"></a>
    <a href="/high-ranking-great-reviews-wood-floor-service-la-jolla.jpg"><img src="/high-ranking-great-reviews-wood-floor-service-la-jolla.jpg" alt="High ranking, great reviews wood floor service in La Jolla — San Diego Hardwoods refinishing vintage red oak flooring with dust-free sanding and polyurethane finish." loading="lazy"></a>
    <a href="/extensive-before-after-gallery-hardwood-san-diego.jpg"><img src="/extensive-before-after-gallery-hardwood-san-diego.jpg" alt="Extensive before and after gallery of hardwood floor refinishing in San Diego — red oak restoration showing the transformation from worn to perfect." loading="lazy"></a>
    <a href="/videos-of-wood-floor-finishing-oak-la-jolla.jpg"><img src="/videos-of-wood-floor-finishing-oak-la-jolla.jpg" alt="Videos of wood floor finishing — red oak refinishing process in La Jolla San Diego, showing dust containment sanding and Bona polyurethane application." loading="lazy"></a>
    <a href="/modern-planetary-sander-hardwood-refinishing-wide.jpg"><img src="/modern-planetary-sander-hardwood-refinishing-wide.jpg" alt="Modern planetary sander hardwood refinishing — wide-angle view of dust-free sanding equipment in action on red oak flooring in a La Jolla home." loading="lazy"></a>
    <a href="/san-diego-hardwoods-best-oak-floor-restoration-2.jpg"><img src="/san-diego-hardwoods-best-oak-floor-restoration-2.jpg" alt="San Diego Hardwoods best oak floor restoration — red oak refinishing with low-VOC Bona Traffic HD polyurethane finish in La Jolla, serving coastal San Diego." loading="lazy"></a>
    <a href="/low-voc-modern-finish-hardwood-refinishing-la-jolla.jpg"><img src="/low-voc-modern-finish-hardwood-refinishing-la-jolla.jpg" alt="Low-VOC modern finish hardwood refinishing in La Jolla — red oak floors sanded to raw wood and coated with Bona Traffic HD polyurethane by San Diego Hardwoods." loading="lazy"></a>
    <a href="/dust-containment-equipment-wood-floor-sanding-san-diego.jpg"><img src="/dust-containment-equipment-wood-floor-sanding-san-diego.jpg" alt="Dust containment equipment for wood floor sanding in San Diego — 100% dust-free system with modern planetary and rotary sanders on red oak flooring." loading="lazy"></a>
    <a href="/fix-my-floor-hardwood-restoration-oak-la-jolla-after.jpg"><img src="/fix-my-floor-hardwood-restoration-oak-la-jolla-after.jpg" alt="Fix my floor hardwood restoration — red oak refinishing after completion in La Jolla, showing the finished low-luster matte sheen from Bona polyurethane." loading="lazy"></a>
    <a href="/floor-refinishing-service-san-diego-harbor-view-oak.jpg"><img src="/floor-refinishing-service-san-diego-harbor-view-oak.jpg" alt="Floor refinishing service San Diego — ocean view red oak flooring restoration with dust containment, traditional stain and Bona Traffic HD finish." loading="lazy"></a>
    <a href="/professional-hardwood-floor-installation-and-refinishing-sd.jpg"><img src="/professional-hardwood-floor-installation-and-refinishing-sd.jpg" alt="Professional hardwood floor installation and refinishing in San Diego — red oak restoration with dust-free sanding, gap filling, and polyurethane finishing." loading="lazy"></a>
    <a href="/bona-certified-craftsman-oak-restoration-san-diego-1.jpg"><img src="/bona-certified-craftsman-oak-restoration-san-diego-1.jpg" alt="Bona Certified Craftsman oak restoration in San Diego — red oak floor refinishing with dust containment equipment and low-VOC polyurethane finish." loading="lazy"></a>
    <a href="/high-durability-polyurethane-floor-finishing-la-jolla.jpg"><img src="/high-durability-polyurethane-floor-finishing-la-jolla.jpg" alt="High durability polyurethane floor finishing in La Jolla — Bona Traffic HD coating on red oak flooring after professional sanding and staining." loading="lazy"></a>
    <a href="/san-diego-county-hardwood-refinishing-oak-gallery-after.jpg"><img src="/san-diego-county-hardwood-refinishing-oak-gallery-after.jpg" alt="San Diego County hardwood refinishing — red oak floor gallery showing after results with low-luster matte finish from Bona Traffic HD polyurethane." loading="lazy"></a>
    <a href="/vintage-wood-floor-restoration-san-diego-low-voc-finish.jpg"><img src="/vintage-wood-floor-restoration-san-diego-low-voc-finish.jpg" alt="Vintage wood floor restoration in San Diego — red oak refinishing with low-VOC Bona Traffic HD polyurethane finish for durability and beauty." loading="lazy"></a>
    <a href="/expert-hardwood-floor-refinishing-la-jolla-oak-professional.jpg"><img src="/expert-hardwood-floor-refinishing-la-jolla-oak-professional.jpg" alt="Expert hardwood floor refinishing in La Jolla — professional red oak restoration with dust containment, traditional stain and Bona polyurethane finish." loading="lazy"></a>
    <a href="/dust-free-sanding-and-finishing-wood-floors-san-diego.jpg"><img src="/dust-free-sanding-and-finishing-wood-floors-san-diego.jpg" alt="Dust-free sanding and finishing of wood floors in San Diego — red oak refinishing with 100% dust containment equipment and low-VOC polyurethane." loading="lazy"></a>
    <a href="/custom-stain-touch-up-oak-refinishing-la-jolla-hd.jpg"><img src="/custom-stain-touch-up-oak-refinishing-la-jolla-hd.jpg" alt="Custom stain touch-up on oak refinishing in La Jolla — red oak floor restoration with traditional stain and Bona Traffic HD high-durability finish." loading="lazy"></a>
    <a href="/mission-vintage-hardwood-floor-refinishing-san-diego.jpg"><img src="/mission-vintage-hardwood-floor-refinishing-san-diego.jpg" alt="Mission vintage hardwood floor refinishing in San Diego — red oak restoration with dust containment sanding and Bona polyurethane finishing." loading="lazy"></a>
    <a href="/red-oak-floor-restoration-repair-la-jolla-san-diego-professional.jpg"><img src="/red-oak-floor-restoration-repair-la-jolla-san-diego-professional.jpg" alt="Red oak floor restoration and repair in La Jolla San Diego — professional refinishing with dust containment, gap filling, and Bona Traffic HD polyurethane." loading="lazy"></a>
    <a href="/la-jolla-hardwood-floor-refinishing-contractor-best-service.jpg"><img src="/la-jolla-hardwood-floor-refinishing-contractor-best-service.jpg" alt="La Jolla hardwood floor refinishing contractor — best service for red oak restoration with dust-free sanding and low-VOC Bona polyurethane finish." loading="lazy"></a>
    <a href="/red-oak-floor-refinishing-la-jolla-during-sanding-wide.jpg"><img src="/red-oak-floor-refinishing-la-jolla-during-sanding-wide.jpg" alt="Red oak floor refinishing in La Jolla during sanding — wide-angle view of dust containment equipment and modern planetary sander in action." loading="lazy"></a>
    <a href="/red-oak-floor-refinishing-la-jolla-after-finish-1.jpg"><img src="/red-oak-floor-refinishing-la-jolla-after-finish-1.jpg" alt="Red oak floor refinishing La Jolla after finish — completed restoration with low-luster matte sheen from Bona Traffic HD polyurethane." loading="lazy"></a>
  </div>
</section>

<section class="block">
  <h2>Why Choose San Diego Hardwoods?</h2>
  <p>This La Jolla project exemplifies the quality and attention to detail that San Diego Hardwoods brings to every job. As a Bona Certified Craftsman serving San Diego County since 1990, we use only the best equipment &mdash; modern planetary and rotary sanders with 100% dust containment &mdash; along with traditional stains and low-VOC, high-durability finishes like Bona Traffic HD polyurethane. Our courteous team of skilled Craftsman ensures every floor is refinished to perfection.</p>
  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call for a Free Assessment</a>
    <a class="btn btn-outline" href="/floor-assessments-inspections.html">View Our Floor Assessment Services</a>
  </div>
</section>

<section class="block">
  <h2>Related Projects &amp; Resources</h2>
  <p>Explore more hardwood floor refinishing projects across San Diego County, or learn about our professional assessment services:</p>
  <ul style="max-width:700px;margin:0 auto;font-size:16px;line-height:1.8;">
    <li><a href="/recent_project_photo_gallery_1.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Gallery 1 &mdash; Recent Project Photos</a></li>
    <li><a href="/solid_wood_floor_photo_gallery.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Solid Wood Floor Gallery</a></li>
    <li><a href="/videos_of_refinishing_process.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Hardwood Floor Refinishing Process Videos</a></li>
    <li><a href="/floor-assessments-inspections.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Free Phone &amp; Photo Assessment</a></li>
  </ul>
</section>

<section class="block">
  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-call" href="sms:+18586990072">Text Floor Photos for a Free Assessment</a>
    <a class="btn btn-outline" href="mailto:sandiegohardwoods@gmail.com">Email Photos</a>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Muirlands Oak Refinishing", MAIN,
         str(Path(__file__).resolve().parent.parent.parent.parent / "muirlands-oak-refinishing-la-jolla.html"))
