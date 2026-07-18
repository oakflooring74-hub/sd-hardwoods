# -*- coding: utf-8 -*-
"""Builds floor-assessments-inspections.html (Milestone 2.3).

This is the site's 13th page and the only one with no legacy raw-source snapshot:
it was created new in this rebuild (public URL /floor-assessments-inspections), so
unlike the other pages there is nothing to extract -- the head metadata, JSON-LD,
and body content are authored here directly, and the page is assembled through the
same shared chrome as every other page.

The full paid-assessment presentation moved here from the homepage's former
#professional-floor-assessments section; the homepage now carries only a short
introduction linking to this page. Business facts in the JSON-LD reuse the
established entities (@id https://www.sdhardwoods.com/#local and #org from the
homepage's committed schema) -- do not add addresses, hours, coordinates, ratings,
or credentials here; the homepage's LocalBusiness node is the authority.
"""
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble

HEAD_META = """<title>Hardwood Floor Assessments &amp; Inspections San Diego | San Diego Hardwoods</title>
<meta name="description" content="Hardwood floor assessments, pre-purchase inspections, written reports, and damage or insurance analysis in San Diego. Start with a free phone and photo review.">
<link href="https://www.sdhardwoods.com/floor-assessments-inspections" rel="canonical">
<link href="https://www.sdhardwoods.com/favicon.ico" rel="icon" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="https://www.sdhardwoods.com/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="https://www.sdhardwoods.com/LOGO-2025.png" rel="logo" type="image/png">
<link href="https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

# One connected graph: the WebPage and its five visible Service entities, each
# provided by the business entity the homepage already declares (@id .../#local).
# Prices in the Offers match the prices visible on the page, nothing more.
JSONLD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["LocalBusiness","HomeAndConstructionBusiness","FlooringContractor"],
      "@id": "https://www.sdhardwoods.com/#local",
      "name": "San Diego Hardwoods",
      "url": "https://www.sdhardwoods.com",
      "telephone": "+1-858-699-0072",
      "email": "sandiegohardwoods@gmail.com",
      "image": "https://www.sdhardwoods.com/LOGO-2025.png",
      "logo": "https://www.sdhardwoods.com/LOGO-2025.png",
      "sameAs": ["https://www.youtube.com/@SD-1974"]
    },
    {
      "@type": "WebPage",
      "@id": "https://www.sdhardwoods.com/floor-assessments-inspections#webpage",
      "url": "https://www.sdhardwoods.com/floor-assessments-inspections",
      "name": "Hardwood Floor Assessments & Inspections San Diego | San Diego Hardwoods",
      "description": "Hardwood floor assessments, pre-purchase inspections, written reports, and damage or insurance analysis in San Diego. Start with a free phone and photo review.",
      "inLanguage": "en",
      "about": {"@id": "https://www.sdhardwoods.com/#local"}
    },
    {
      "@type": "Service",
      "@id": "https://www.sdhardwoods.com/floor-assessments-inspections#free-phone-photo-assessment",
      "name": "Free Phone & Photo Assessment",
      "serviceType": "Hardwood floor assessment",
      "description": "A free phone conversation and review of customer-supplied photos, video, or a public real-estate listing to share preliminary guidance, discuss likely flooring options, and determine the appropriate next step.",
      "url": "https://www.sdhardwoods.com/floor-assessments-inspections",
      "areaServed": {"@type": "Place", "name": "San Diego County"},
      "provider": {"@id": "https://www.sdhardwoods.com/#local"},
      "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    },
    {
      "@type": "Service",
      "@id": "https://www.sdhardwoods.com/floor-assessments-inspections#in-home-project-assessment",
      "name": "In-Home Project Assessment",
      "serviceType": "Hardwood floor assessment",
      "description": "An on-site visit for owners considering San Diego Hardwoods for flooring work: visual assessment of the proposed project, basic floor and finish identification, project-planning measurements, discussion of realistic options, and a proposal when the work is a suitable fit.",
      "url": "https://www.sdhardwoods.com/floor-assessments-inspections",
      "areaServed": {"@type": "Place", "name": "San Diego County"},
      "provider": {"@id": "https://www.sdhardwoods.com/#local"},
      "offers": {"@type": "Offer", "price": "95", "priceCurrency": "USD"}
    },
    {
      "@type": "Service",
      "@id": "https://www.sdhardwoods.com/floor-assessments-inspections#pre-purchase-inspection-verbal",
      "name": "Pre-Purchase Floor Inspection — Verbal Assessment",
      "serviceType": "Hardwood floor inspection",
      "description": "An on-site floor inspection of a property being evaluated before purchase: apparent identification of flooring type, construction, and finish, evaluation of visible condition and wear, and a verbal explanation of realistic cleaning, repair, restoration, refinishing, or replacement options.",
      "url": "https://www.sdhardwoods.com/floor-assessments-inspections",
      "areaServed": {"@type": "Place", "name": "San Diego County"},
      "provider": {"@id": "https://www.sdhardwoods.com/#local"},
      "offers": {"@type": "Offer", "price": "350", "priceCurrency": "USD"}
    },
    {
      "@type": "Service",
      "@id": "https://www.sdhardwoods.com/floor-assessments-inspections#pre-purchase-inspection-written",
      "name": "Pre-Purchase Inspection with Written Documentation",
      "serviceType": "Hardwood floor inspection",
      "description": "The full on-site pre-purchase inspection plus two professional PDF documents: a Floor Identification & Condition Report and a Recommended Scope & Estimate for servicing the flooring after the buyer takes ownership.",
      "url": "https://www.sdhardwoods.com/floor-assessments-inspections",
      "areaServed": {"@type": "Place", "name": "San Diego County"},
      "provider": {"@id": "https://www.sdhardwoods.com/#local"},
      "offers": {"@type": "Offer", "price": "750", "priceCurrency": "USD"}
    },
    {
      "@type": "Service",
      "@id": "https://www.sdhardwoods.com/floor-assessments-inspections#complex-damage-dispute-insurance-analysis",
      "name": "Complex Damage, Dispute & Insurance Analysis",
      "serviceType": "Hardwood floor damage analysis",
      "description": "A customizable professional service for insurance claims, water or moisture damage, landlord-tenant and security-deposit disputes, conflicting condition opinions, and complex repairability questions, with scope, deliverables, and third-party communication agreed in writing before work begins.",
      "url": "https://www.sdhardwoods.com/floor-assessments-inspections",
      "areaServed": {"@type": "Place", "name": "San Diego County"},
      "provider": {"@id": "https://www.sdhardwoods.com/#local"},
      "offers": {
        "@type": "Offer",
        "priceCurrency": "USD",
        "priceSpecification": {"@type": "PriceSpecification", "minPrice": 1500, "priceCurrency": "USD"}
      }
    }
  ]
}
</script>"""

# Milestone 2.4: obsolete Universal Analytics (UA-20793161-1 / _gaq / ga.js) removed
# site-wide. GA4 is blocked pending the owner's confirmed Measurement ID.
GA = ""

VCARD = "SAN DIEGO LICENSED WOOD FLOOR RESTORATION/REFINISHING CONTRACTOR 858-699-0072 EXPERIENCE EXCEPTIONAL DUSTLESS HARDWOOD AND BAMBOO FLOOR REFINISHING IN SAN DIEGO. ALL WORK PERFORED BY A HIGHLY EXPERIENCED FLOORING EXPERT WITH OVER 30 YEARS EXPERIENCE RESTORING AND REPAIRING SOLID AND ENGINEERED HARDWOOD AND BAMBOO FLOORING. CALL TODAY TO SCHEDULE A CONSULTATION. TEXT PHOTOS OF YOUR PROJECT FOR AN IMMEDIATE ASSESSMENT."

MAIN = """
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Professional Hardwood Floor Assessments, Inspections &amp; Consultation</h1>
  <p>Our core business is the flooring work itself &mdash; refinishing, restoration, deep cleaning and recoating, repairs, and installation. When a floor or a property decision calls for professional expertise on site, we also offer a clear set of paid assessment and inspection services: an in-home project assessment, pre-purchase floor inspections with optional written documentation, and complex damage, dispute, and insurance analysis. Every one of them begins the same way: with a conversation that is free.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>
</section>

<section class="block" id="free-assessment">
  <p class="eyebrow">The Right First Step &mdash; Always Free</p>
  <h2>Start With a Free Phone &amp; Photo Assessment</h2>
  <div class="consult-card consult-free">
    <div class="consult-head">
      <h3>Free Phone &amp; Photo Assessment</h3>
      <span class="consult-price">Free</span>
    </div>
    <p>Start with a free phone and photo assessment. We can review the flooring, discuss your concerns, share preliminary guidance, and help determine the most appropriate next step. Initial contact may include a phone conversation; review of photos or a short video you text or email; or review of a public Zillow, Redfin, Realtor.com, or similar listing for a property you are considering. We will discuss likely flooring options, whether San Diego Hardwoods is a suitable fit, and which type of property visit or professional service &mdash; if any &mdash; makes sense for your situation.</p>
    <div class="cta-row" style="justify-content:flex-start;margin-top:6px;">
      <a class="btn btn-call" href="tel:+18586990072" style="padding:11px 22px;font-size:15.5px;">&#9742; Call 858-699-0072</a>
      <a class="btn btn-outline" href="sms:+18586990072" style="padding:11px 22px;font-size:15.5px;">Text Floor Photos</a>
    </div>
  </div>
</section>

<section class="block" id="in-home-project-assessment">
  <p class="eyebrow">Planning a Flooring Project</p>
  <h2>In-Home Project Assessment &mdash; $95</h2>
  <div class="consult-card consult-primary">
    <div class="consult-head">
      <h3>In-Home Project Assessment</h3>
      <span class="consult-price">$95</span>
    </div>
    <p>For owners and authorized decision-makers considering San Diego Hardwoods for their flooring work. We travel to the property, visually assess the proposed flooring project, identify the floor and finish when reasonably determinable, take the measurements needed for project planning, and discuss realistic flooring-service options. When the project is a suitable fit, we prepare a San Diego Hardwoods proposal.</p>
    <p><strong>Some or all of the assessment fee may be credited toward the approved flooring project under written agreement.</strong></p>
    <p class="consult-fine">This is a project-planning visit, not a formal inspection or damage-analysis service &mdash; it does not include formal written inspection reports, purchase-negotiation documents, insurance or dispute documentation, detailed causation analysis, or communication with third parties.</p>
  </div>
</section>

<section class="block" id="pre-purchase-inspections">
  <p class="eyebrow">Buying a Home</p>
  <h2>Pre-Purchase Hardwood Floor Inspections</h2>
  <p class="lede">Both pre-purchase services are for someone evaluating a property they do not yet own. An experienced hardwood flooring specialist inspects the floors before you commit, so the flooring's real condition &mdash; and its realistic future &mdash; is part of your purchase decision.</p>
  <div class="consult-grid">
    <div class="consult-card">
      <div class="consult-head">
        <h3>Pre-Purchase Floor Inspection &mdash; Verbal Assessment</h3>
        <span class="consult-price">$350</span>
      </div>
      <p>An on-site floor inspection of a property you are evaluating before purchase. Includes apparent identification of the flooring type, construction, and finish; evaluation of visible condition, wear, damage, and maintenance concerns; and a verbal explanation of realistic cleaning, repair, restoration, refinishing, or replacement options, along with apparent limitations and likely future flooring needs.</p>
      <p class="consult-fine">This service is primarily verbal and does not include formal written reports or negotiation documents. The fee covers the inspection and professional analysis whether or not you purchase the property, the transaction closes, or you later hire San Diego Hardwoods.</p>
    </div>

    <div class="consult-card">
      <div class="consult-head">
        <h3>Pre-Purchase Inspection with Written Documentation</h3>
        <span class="consult-price">$750</span>
      </div>
      <p>The full on-site pre-purchase inspection, plus two professional PDF documents:</p>
      <ul>
        <li><strong>Floor Identification &amp; Condition Report</strong> &mdash; what the floor appears to be (and does not appear to be), its apparent construction and finish, what appears sound, serviceable, or properly maintained versus worn, damaged, questionable, or improperly maintained, apparent repairability, restoration or refinishing feasibility, and important limitations and uncertainties &mdash; with supporting photographs, observations, measurements, or moisture readings when relevant.</li>
        <li><strong>Recommended Scope &amp; Estimate</strong> &mdash; recommended cleaning, recoating, repair, restoration, refinishing, or replacement work, a proposed scope of work, and, when appropriate, an estimate or proposal for San Diego Hardwoods to service the flooring after you take ownership.</li>
      </ul>
      <p class="consult-fine">The estimate is based on the accessible conditions observed during the inspection and may require confirmation after closing, full access, furniture removal, demolition, or changed site conditions. The documentation may assist with purchase planning, budgeting, or negotiations, but it is not legal, appraisal, engineering, or real-estate representation.</p>
    </div>
  </div>
</section>

<section class="block" id="complex-analysis">
  <p class="eyebrow">Complex &amp; Customized Matters</p>
  <h2>Complex Damage, Dispute &amp; Insurance Analysis &mdash; From $1,500</h2>
  <div class="consult-card">
    <div class="consult-head">
      <h3>Complex Damage, Dispute &amp; Insurance Analysis</h3>
      <span class="consult-price">From $1,500</span>
    </div>
    <p>A customizable professional service for matters involving insurance claims, water or moisture damage, landlord-tenant and security-deposit disputes, neighbor or contractor damage, conflicting opinions about floor condition, complicated repairability or damage questions, third-party communication, and customized documentation.</p>
    <p>When specifically agreed in writing, this service can include on-site professional evaluation; multiple scheduled phone consultations; multiple PDFs or customized written documents; professional photographs; measurements and moisture readings when relevant; forensic-style analysis of flooring construction, finish, wear, damage, repairability, restoration feasibility, and realistic limitations; repair, restoration, refinishing, or replacement recommendations; scope or cost documentation; and communication with specifically identified insurers, property managers, tenants, landlords, contractors, neighbors, designers, real-estate professionals, or other involved parties.</p>
    <p class="consult-fine">The exact scope and deliverables are customized and agreed upon before work begins, and work beyond the agreed scope requires separate written authorization. This is professional flooring analysis &mdash; not laboratory analysis, engineering services, or legal representation.</p>
  </div>
</section>

<section class="block" id="who-these-services-help">
  <h2>Who These Services Help</h2>
  <p class="lede">Homeowners planning flooring work, prospective buyers evaluating a property, landlords and tenants, property managers, real-estate professionals, designers and contractors seeking a second opinion, and clients with insurance-related flooring questions &mdash; especially when floors are affected by water, moisture, repair, finish-failure, or damage concerns, or are simply confusing to diagnose.</p>

  <figure style="max-width:520px;margin:0 auto 30px;border-radius:10px;overflow:hidden;border:1px solid var(--line);">
    <a href="/LARK56.jpg"><img src="/LARK56.jpg" alt="Hardwood floor refinishing in Encinitas — deep cleaning and prep on wide-plank oak before a durable, dust-contained recoat for a coastal North County home." style="width:100%;display:block;" loading="lazy"></a>
  </figure>

  <div class="info-grid">
    <div class="card">
      <h3>Specialty &amp; European Oak Floors</h3>
      <p>For wide-plank, wire-brushed European and French oak and other specialty floors, an expert evaluation may identify meaningful restoration or upgrade options. Floors that appear dry, thirsty, scratched, scuffed, worn, neglected, or improperly maintained can sometimes be transformed with professional deep cleaning, controlled abrasion, color correction, stain or sealing where appropriate, recoating, or conversion to an appropriate low-sheen, low-VOC waterborne finish system.</p>
    </div>
    <div class="card">
      <h3>An Honest Answer, Either Way</h3>
      <p>Not every damaged or worn floor can be restored &mdash; construction, wear layer, finish, contamination, damage, and existing condition all affect what is realistically possible. That is exactly why an accurate professional assessment matters before committing to a plan: it tells you what your floor is, what it needs, and what it can honestly become.</p>
    </div>
  </div>
</section>

<section class="block" id="service-area">
  <h2>Serving San Diego County</h2>
  <p class="lede">These assessment, inspection, and consultation services are offered throughout our established service area: La Jolla, Del Mar, Rancho Santa Fe, Encinitas, Solana Beach, Carmel Valley, Carlsbad, Oceanside, Poway, Rancho Bernardo, and communities across San Diego County. Whether you need a wood-floor damage assessment, a water-damaged floor evaluation, documentation for an insurance claim or a landlord-tenant matter, or an honest read on repair and refinishing feasibility, it starts with the same free phone and photo conversation.</p>
</section>

<section class="block" id="appointments-payment">
  <h2>Appointments &amp; Payment</h2>
  <p class="lede">The process is simple and confirmed in writing before any paid service begins:</p>
  <div class="info-grid">
    <div class="card">
      <h3>1. Free Conversation First</h3>
      <p>Every client starts with the free phone and photo assessment. We determine together which professional service &mdash; if any &mdash; actually fits your situation.</p>
    </div>
    <div class="card">
      <h3>2. Written Scope &amp; Fee</h3>
      <p>You receive written confirmation of the agreed scope and fee before anything is scheduled, so there are no surprises about what the service includes.</p>
    </div>
    <div class="card">
      <h3>3. Payment Reserves Your Appointment</h3>
      <p>Payment may be requested through a Square invoice sent by email or text, or through another directly approved method such as Zelle. Payment reserves the scheduled professional service.</p>
    </div>
  </div>
</section>

<section class="block" id="faq">
  <h2>Floor Assessment &amp; Inspection Questions, Answered</h2>

  <div class="card" style="margin-bottom:18px;">
    <h3>Is the first phone conversation free?</h3>
    <p>Yes. Every client relationship starts with a free phone and photo assessment &mdash; a conversation, a review of the photos or video you send (or a public real-estate listing), and honest preliminary guidance about the most appropriate next step.</p>
  </div>
  <div class="card" style="margin-bottom:18px;">
    <h3>Why is there a $95 charge for an in-home project assessment?</h3>
    <p>The in-home visit puts more than three decades of hardwood flooring experience on site: travel to the property, a visual assessment of the proposed project, identification of the floor and finish when reasonably determinable, the measurements needed for planning, and a discussion of realistic options &mdash; with a San Diego Hardwoods proposal when the work is a suitable fit.</p>
  </div>
  <div class="card" style="margin-bottom:18px;">
    <h3>Is the $95 assessment fee credited toward flooring work?</h3>
    <p>It can be. When San Diego Hardwoods performs the approved flooring project, part or all of the fee may be applied to that project under a written agreement confirmed before the work begins.</p>
  </div>
  <div class="card" style="margin-bottom:18px;">
    <h3>What is included in the $350 pre-purchase inspection?</h3>
    <p>An on-site inspection of a property you are evaluating before purchase: apparent identification of the flooring type, construction, and finish; an evaluation of visible condition, wear, damage, and maintenance concerns; and a verbal explanation of realistic options and likely future flooring needs. It is primarily verbal &mdash; written reports are part of the $750 service.</p>
  </div>
  <div class="card" style="margin-bottom:18px;">
    <h3>What written reports are included with the $750 service?</h3>
    <p>Two professional PDFs: a <strong>Floor Identification &amp; Condition Report</strong> covering what the floor appears to be, its apparent condition, repairability, and restoration feasibility with important limitations; and a <strong>Recommended Scope &amp; Estimate</strong> describing recommended work and, when appropriate, a proposal for San Diego Hardwoods to service the flooring after you take ownership. The documentation may assist with purchase planning, budgeting, or negotiations.</p>
  </div>
  <div class="card" style="margin-bottom:18px;">
    <h3>What situations call for the complex damage, dispute, or insurance service?</h3>
    <p>Insurance claims, water or moisture damage, landlord-tenant or security-deposit disputes, neighbor or contractor damage, conflicting opinions about a floor's condition, complicated repairability questions, and matters that need customized documentation or communication with specifically identified third parties. The exact scope is agreed in writing before work begins.</p>
  </div>
  <div class="card" style="margin-bottom:18px;">
    <h3>How are appointments and payments arranged?</h3>
    <p>After the free phone and photo assessment, you receive written confirmation of the scope and fee. Payment may be requested through a Square invoice sent by email or text, or another directly approved method such as Zelle, and payment reserves the scheduled service.</p>
  </div>
  <div class="card">
    <h3>Can every damaged or worn floor be restored?</h3>
    <p>No &mdash; and a professional assessment is how you find out before spending real money. Construction, wear layer, finish, contamination, and existing damage all affect feasibility. Many floors that look tired have meaningful restoration options; some do not. Either way, you get an honest, experienced answer.</p>
  </div>
</section>

<section class="block" id="get-started">
  <h2>Ready to Get Started?</h2>
  <p class="lede">Text or email clear photos of your floors &mdash; or send a listing link for a property you are considering &mdash; and we will take it from there with a free phone and photo assessment.</p>
  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
    <a class="btn btn-outline" href="mailto:sandiegohardwoods@gmail.com">Email San Diego Hardwoods</a>
  </div>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Assessments &amp; Inspections", MAIN,
         str(BUILD.parent / "floor-assessments-inspections.html"))
