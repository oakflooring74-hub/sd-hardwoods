# -*- coding: utf-8 -*-
"""Builds maple-floor-refinishing-kensington.html — individual project showcase page
for 100-year-old solid maple floor restoration + red oak kitchen refinishing.

Images: 19 PNG files in repo root, SEO filenames derived from dictation topics.
Alt text approved per session review (no repeats across batch).
"""
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble
from public_business_rules import PRIORITY_COASTAL_SD, FULL_SAN_DIEGO_AREAS, SOUTH_ORANGE_COUNTY

# Service area: Kensington + San Diego County
_PROJECT_AREA = ["Kensington", "San Diego"] + [a for a in FULL_SAN_DIEGO_AREAS if a != "San Diego"]


HEAD_META = """<title>Hardwood Floor Refinishing San Diego — Maple Floor Restored Kensington</title>
<meta name="description" content="100-year-old maple floor refinishing Kensington San Diego — wood floor refinisher restores historical hardwood, termite repair, Bona Traffic HD finish.">
<link href="https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html" rel="canonical">
<link href="/favicon.ico" rel="icon" type="image/x-icon">
<link href="/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#f8f4ec">
<link href="/LOGO-2025.png" rel="logo" type="image/png">"""

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
      "sameAs": ["https://www.youtube.com/@sandiegohardwoods", "https://maps.app.goo.gl/hbNaSo2guARgrZTa8"],
      "areaServed": ["San Diego", "Kensington", "North Park", "Hillcrest", "Mission Hills", "University Heights", "Normal Heights", "Adams-Normandy", "City Heights", "Oak Park", "East Village", "Little Italy", "Gaslamp Quarter", "Bankers Hill", "Liberty Station", "Point Loma", "Ocean Beach", "Mission Beach", "Pacific Beach", "La Jolla", "Del Mar", "Solana Beach", "Encinitas", "Cardiff-by-the-Sea", "Leucadia", "Olympia Mesa", "Rancho Santa Fe", "Carmel Valley", "Torrey Pines", "La Jolla Village", "Sorrento Valley", "Mira Mesa", "Scripps Ranch", "Riviera Del Mar", "Fairbanks Ranch", "Del Sur", "San Dieguito", "Four Mile Canyon", "Black Mountain Ranch", "Town and Country", "College Area", "San Carlos", "Allied Gardens", "Grantville", "Kearny Mesa", "Tierrasanta", "Jamul", "Dulzura", "Alpine", "Spring Valley", "Lemon Grove", "La Presa", "Flintstone", "Bonita", "Chula Vista", "National City", "Imperial Beach", "Coronado", "South Orange County", "Irvine", "Newport Beach", "Huntington Beach", "Costa Mesa", "Westminster", "Garden Grove", "Santa Ana", "Anaheim", "Fullerton", "Buena Park", "La Palma", "Cypress", "Seal Beach", "Los Alamitos", "Foothill Ranch", "Lake Forest", "Ladera Ranch", "Mission Viejo", "Rancho Santa Margarita", "San Juan Capistrano", "San Clemente", "Laguna Niguel", "Aliso Viejo", "Laguna Hills", "Laguna Beach", "Dana Point", "San Diego County"]
    },
    {
      "@type": "WebPage",
      "@id": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html#webpage",
      "url": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html",
      "name": "Maple Floor Refinishing Kensington San Diego — Century-Old Hardwood Restoration",
      "description": "A 100-year-old solid maple hardwood floor in Kensington, San Diego was sanded and restored by San Diego Hardwoods. Termite-damaged boards were replaced, the floor was sealed with Bona low-VOC water-based sealer, then finished with multiple coats of Bona Traffic HD polyurethane for fast drying and quick cure time.",
      "inLanguage": "en",
      "about": {"@id": "https://www.sdhardwoods.com/#local"},
      "mainEntity": {"@id": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html#service"}
    },
    {
      "@type": "Service",
      "@id": "https://www.sdhardoods.com/maple-floor-refinishing-kensington.html#service",
      "name": "Maple Floor Refinishing and Historical Hardwood Restoration Kensington San Diego",
      "url": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html",
      "mainEntityOfPage": {"@id": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html#webpage"},
      "provider": {"@id": "https://www.sdhardwoods.com/#local"},
      "areaServed": ["Kensington", "San Diego County"],
      "serviceType": ["Maple floor refinishing", "Hardwood floor sanding", "Historical home floor restoration", "Termite damage repair", "Red oak kitchen floor refinishing"],
      "description": "Century-old solid maple hardwood flooring in a Kensington, San Diego historical building was sanded to raw wood with modern planetary equipment. Termite-damaged and missing boards were replaced with new maple for seamless repair. Bona low-VOC water-based sealer blended new wood with original patina, then multiple coats of water-based polyurethane provided fast drying and quick cure time.",
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Kensington Maple Floor Refinishing Services",
        "itemListElement": [
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Century-old maple floor sanding to raw wood", "description": "Modern planetary equipment flattens vintage hardwood before Bona low-VOC water-based sealer application"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Termite damage board replacement", "description": "Missing and damaged maple boards replaced with new solid hardwood for seamless historical restoration"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Bona water-based sealer application", "description": "Low-VOC sealer gives subtle amber tone to blend new wood with original patina on century-old flooring"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Water-based polyurethane finishing", "description": "Multiple layers dry quickly and cure fast so homeowners return sooner after hardwood refinishing"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Random-width red oak kitchen floor restoration", "description": "Hand-scraped grooves between boards, decorative plug installation for unique vintage character on solid hardwood"}}
        ]
      }
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html#image-1",
      "contentUrl": "https://www.sdhardwoods.com/maple-floor-before-kensington.png",
      "url": "https://www.sdhardwoods.com/maple-floor-before-kensington.png",
      "name": "Century-old solid maple hardwood before refinishing Kensington San Diego"
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html#image-2",
      "contentUrl": "https://www.sdhardwoods.com/hardwood-sanding-san-diego.png",
      "url": "https://www.sdhardwoods.com/hardwood-sanding-san-diego.png",
      "name": "Maple floor sanding removes old finish San Diego"
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html#image-3",
      "contentUrl": "https://www.sdhardwoods.com/termite-repair-maple-floors.png",
      "url": "https://www.sdhardwoods.com/termite-repair-maple-floors.png",
      "name": "Termite damage repair on 100-year-old maple floor Kensington"
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html#image-4",
      "contentUrl": "https://www.sdhardwoods.com/planetary-floor-sanding-equipment.png",
      "url": "https://www.sdhardwoods.com/planetary-floor-sanding-equipment.png",
      "name": "Planetary sanding equipment flattens vintage hardwood San Diego"
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.sdhardwoods.com/maple-floor-refinishing-kensington.html#image-5",
      "contentUrl": "https://www.sdhardwoods.com/dust-contained-refinishing-kensington.png",
      "url": "https://www.sdhardwoods.com/dust-contained-refinishing-kensington.png",
      "name": "Floor sanding company Kensington — dust-contained work area"
    }
  ]
}
</script>"""

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
  <h1>Maple Floor Refinishing Kensington — Restore Wood Floors San Diego Historical Building</h1>
  <p>A 100-year-old solid maple hardwood floor in a historical Kensington building was severely yellowed and amber from decades of UV exposure and old oil polyurethane. San Diego Hardwoods sanded the floor to raw wood, replaced termite-damaged boards with new maple, then sealed it with Bona low-VOC water-based sealer that gave subtle amber tone to blend with the historical patina.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-call" href="sms:+18586990072">Text Floor Photos for a Free Assessment</a>
  </div>
</section>

<section class="block">
  <p class="eyebrow">Historical Maple Restoration + Red Oak Kitchen Refinishing</p>
  <h2>Century-Old Maple Hardwood Refinished Kensington San Diego</h2>
  <p class="lede">This historical building in the Kensington area of San Diego had a traditional maple hardwood floor that was white with small pink lines and closed grain — severely yellowed from decades of excessive ultraviolet light and the normal life cycle of old-school oil polyurethane on maple. A wood floor refinisher who specializes in vintage restoration, San Diego Hardwoods sanded this solid maple hardwood floor down to raw wood with modern planetary equipment to ensure the floor was as flat as possible.</p>
  <p>We replaced several termite-damaged and missing boards with brand new maple flooring to match, then laced in the new boards making a seamless repair. We then proceeded to use modern planetary equipment to ensure this floor was as flat as possible, then sealed the floor with Bona brand low-VOC water-based sealer that gave it a subtle amber tone to blend in with the age and patina of this historical building in San Diego.</p>
  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call &mdash; Free Assessment</a>
    <a class="btn btn-outline" href="mailto:sandiegohardwoods@gmail.com">Email Floor Photos</a>
  </div>
</section>

<section class="block">
  <h2>Water-Based Polyurethane — Fast Drying, Quick Cure Time</h2>
  <p>We then applied multiple layers of modern water-based polyurethane which allowed the finish to dry quickly and cure quickly as well, allowing the homeowner to only be out of the house for the least amount of time possible. We gave them a satin sheen and this floor came out absolutely amazing.</p>
  <p>A floor sanding company that understands historical homes, we contained all of the dust with our Bona portable dust containment unit — this is a true restoration of a San Diego landmark. The finish protects century-old maple from future wear while maintaining its original character and patina.</p>
</section>

<section class="block">
  <h2>Random-Width Red Oak Kitchen Floors Hand-Scraped + Restored</h2>
  <p>We also restored their random-width solid red oak floors in the kitchen. You can see in the picture that they were completely blackened from decades of overuse and lack of maintenance. We sanded them down to raw wood, hand-scraped the grooves between the boards, replaced some red oak plugs that are decorative to give the floor a unique look.</p>
  <p>We applied clear sealer to lighten up the red oak and keep tone of the reds and pinks down — reducing those bright colors is what is popular now and desirable. That's what we get a lot of calls for. These types of floors are all over San Diego County from the border with Mexico up to Oceanside and into south Orange County.</p>
</section>

<section class="block">
  <h2>Hardwood Floor Sanding Service — Extensive Repairs + Termite Damage Restoration</h2>
  <p>We restore these types of solid oak floors on a regular basis and we perform extensive repairs, termite damage repair, and we do consultations for people that don't understand what they have or what is possible to achieve with it. Anybody looking to purchase a home in San Diego County that has a wood floor can contact us to schedule a consultation — we even do pre-purchase inspection reports for a fee.</p>
  <p>The oak flooring in the kitchen came out perfect and matches the dining room. We restored the thresholds and also contained all of the dust as we always do. This project received Bona brand Traffic HD — Bona Certified Craftsman finish. We prefer this product for durability, low VOC, beauty, and ease of maintenance.</p>
</section>

<section class="block">
  <h2>Before &amp; After Photo Gallery — Maple Floor Refinishing Kensington + Red Oak Kitchen Restoration</h2>
  <p class="lede">Every stage of this historical hardwood restoration is documented below: century-old maple before refinishing, sanding to raw wood with dust containment equipment, termite repair, Bona sealer application, water-based polyurethane finishing, red oak kitchen restoration, and final results showing seamless threshold transitions.</p>
  <div class="gallery">
    <a href="/maple-floor-before-kensington.png"><img src="/maple-floor-before-kensington.png" alt="Hardwood floor refinishing San Diego — century-old maple before restoration Kensington, yellowed from decades of old finish" loading="lazy"></a>
    <a href="/hardwood-sanding-san-diego.png"><img src="/hardwood-sanding-san-diego.png" alt="Wood floor refinish San Diego — sanding removes years of buildup to reveal raw maple with natural pink grain lines" loading="lazy"></a>
    <a href="/termite-repair-maple-floors.png"><img src="/termite-repair-maple-floors.png" alt="Floor sanding service San Diego — termite damage repair on 100-year-old hardwood, seamless board replacement for historical home" loading="lazy"></a>
    <a href="/planetary-floor-sanding-equipment.png"><img src="/planetary-floor-sanding-equipment.png" alt="San Diego Hardwood floor refinishing — planetary equipment flattens vintage floor before Bona low-VOC water-based sealer" loading="lazy"></a>
    <a href="/dust-contained-refinishing-kensington.png"><img src="/dust-contained-refinishing-kensington.png" alt="Floor sanding company San Diego — dust-contained work area protects Kensington historical building during maple restoration" loading="lazy"></a>
    <a href="/bona-sealer-amber-tone-maple.png"><img src="/bona-sealer-amber-tone-maple.png" alt="Restore wood floors San Diego — Bona sealer gives subtle amber tone to century-old maple, blending new with original patina" loading="lazy"></a>
    <a href="/water-based-polyurethane-drying.png"><img src="/water-based-polyurethane-drying.png" alt="Hardwood floor refinishing San Diego — water-based polyurethane dries fast so homeowners return sooner after sanding" loading="lazy"></a>
    <a href="/satin-sheen-kensington-maple-floor.png"><img src="/satin-sheen-kensington-maple-floor.png" alt="Wood floor refinish Kensington San Diego — satin sheen on restored 100-year-old maple, smooth durable surface" loading="lazy"></a>
    <a href="/red-oak-kitchen-before-refinish.png"><img src="/red-oak-kitchen-before-refinish.png" alt="Floor sanding service San Diego — kitchen red oak blackened from heavy use before refinishing and hand-scraped restoration" loading="lazy"></a>
    <a href="/hand-scraped-red-oak-san-diego.png"><img src="/hand-scraped-red-oak-san-diego.png" alt="San Diego hardwood floor refinishing — random-width red oak hand-scraped for vintage character in historical kitchen" loading="lazy"></a>
    <a href="/decorative-oak-plug-installation.png"><img src="/decorative-oak-plug-installation.png" alt="Restore wood floors San Diego — decorative oak plug installation creates custom look on refinished kitchen flooring" loading="lazy"></a>
    <a href="/clear-sealer-lighten-red-oak.png"><img src="/clear-sealer-lighten-red-oak.png" alt="Floor sanding company Kensington — clear sealer lightens red oak, reduces bright tones for modern desirable finish" loading="lazy"></a>
    <a href="/threshold-restoration-maple-to-oak.png"><img src="/threshold-restoration-maple-to-oak.png" alt="Hardwood floor refinishing San Diego — threshold restoration between maple dining room and refinished kitchen oak floors" loading="lazy"></a>
    <a href="/dust-containment-kitchen-sanding.png"><img src="/dust-containment-kitchen-sanding.png" alt="Wood floor refinish service — dust containment protects adjacent rooms during kitchen floor sanding in historical home" loading="lazy"></a>
    <a href="/bona-traffic-hd-finish-san-diego.png"><img src="/bona-traffic-hd-finish-san-diego.png" alt="San Diego Hardwood floor refinishing — Bona Traffic HD finish for durability, low-VOC on century-old restored flooring" loading="lazy"></a>
    <a href="/maple-floor-before-after-kensington.png"><img src="/maple-floor-before-after-kensington.png" alt="Floor sanding San Diego before-after — 100-year-old maple reclaimed from severe yellowing to natural beauty Kensington" loading="lazy"></a>
    <a href="/refinished-red-oak-matches-dining.png"><img src="/refinished-red-oak-matches-dining.png" alt="Restore wood floors kitchen San Diego — refinished red oak matches dining room with seamless transitions throughout home" loading="lazy"></a>
    <a href="/bona-cleaning-kit-floor-care.png"><img src="/bona-cleaning-kit-floor-care.png" alt="Floor sanding company San Diego — Bona cleaning kit and maintenance instructions for long-lasting restored hardwood floors" loading="lazy"></a>
    <a href="/wood-floor-refinisher-san-diego-1990.png"><img src="/wood-floor-refinisher-san-diego-1990.png" alt="Wood floor refinish San Diego since 1990 — extreme craftsmanship on historical maple and red oak throughout San Diego County" loading="lazy"></a>
  </div>
</section>

<section class="block">
  <h2>Refinish Wood Floor in San Diego — Free Phone &amp; Photo Assessment</h2>
  <p>If you want to refinish wood floor in San Diego, the quickest way to a real answer is to text photos of the floor. Send clear overall shots plus close-ups of the worst areas and we can usually tell whether the floor can be sanded, how many passes it will need, what repairs are involved and which finishing options make sense — before anyone drives out. That Free Phone &amp; Photo Assessment costs nothing.</p>
  <p>We work throughout San Diego County from the border with Mexico up to Oceanside and into south Orange County. Whether it's a century-old maple floor in Kensington or red oak kitchen restoration, the same standard applies: dustless sanding, honest repair work, and a hardwood floor finish put on thick enough and clean enough to last.</p>
  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call for a Free Assessment</a>
    <a class="btn btn-outline" href="https://www.sdhardwoods.com/floor-assessments-inspections.html">View Our Floor Assessment Services</a>
  </div>
</section>

<section class="block">
  <h2>Related Projects &amp; Resources</h2>
  <p>More hardwood floor refinishing and floor finishing work from San Diego Hardwoods, plus the process filmed on real jobs:</p>
  <ul style="max-width:700px;margin:0 auto;font-size:16px;line-height:1.8;">
    <li><a href="https://www.sdhardwoods.com/" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">San Diego Hardwoods &mdash; Hardwood Floor Refinishing, Finishing and Installation</a></li>
    <li><a href="https://www.sdhardwoods.com/blog.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Floor Refinishing Case Studies &amp; Blog</a></li>
    <li><a href="https://www.sdhardwoods.com/recent_project_photo_gallery_1.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Gallery 1 &mdash; Recent Hardwood Floor Refinishing Projects</a></li>
    <li><a href="https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Solid Wood Floor Installation and Finishing Gallery</a></li>
    <li><a href="https://www.sdhardwoods.com/videos_of_refinishing_process.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Videos of Dustless Hardwood Floor Sanding and Finishing</a></li>
    <li><a href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Hardwood Floor Deep Cleaning &mdash; When Sanding Is Not Needed</a></li>
    <li><a href="https://www.sdhardwoods.com/floor-assessments-inspections.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Free Phone &amp; Photo Floor Assessment</a></li>
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

assemble(HEAD_META, JSONLD, GA, VCARD, "Maple Floor Refinishing Kensington", MAIN,
         str(Path(__file__).resolve().parent.parent.parent.parent / "maple-floor-refinishing-kensington.html"))
