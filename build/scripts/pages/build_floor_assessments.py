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
from public_business_rules import (
    PRIORITY_COASTAL_SD, replace_area_served, FULL_SAN_DIEGO_AREAS, SOUTH_ORANGE_COUNTY,
)
import json as _json

# Milestone 2.9: South Orange County removed from this page's Service area --
# per owner direction it appears only in the shared #local schema entity.
_ASSESSMENT_AREA = _json.dumps(["San Diego County"] + PRIORITY_COASTAL_SD)

HEAD_META = """<title>Hardwood &amp; Bamboo Floor Assessments, Inspections &amp; Pre-Purchase Reports | San Diego</title>
<meta name="description" content="Pre-purchase hardwood and bamboo floor inspections, condition assessments, and written specialist findings throughout San Diego. Start with a free phone and photo review.">
<link href="https://www.sdhardwoods.com/floor-assessments-inspections" rel="canonical">
<link href="/favicon.ico" rel="icon" type="image/x-icon">
<link href="/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="/LOGO-2025.png" rel="logo" type="image/png">
<link href="/assets/legacy-css/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="/assets/legacy-css/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

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
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "reviewCount": "16"
      }
    },
    {
      "@type": "WebPage",
      "@id": "https://www.sdhardwoods.com/floor-assessments-inspections#webpage",
      "url": "https://www.sdhardwoods.com/floor-assessments-inspections",
      "name": "Hardwood & Bamboo Floor Assessments, Inspections & Pre-Purchase Reports | San Diego",
      "description": "Pre-purchase hardwood and bamboo floor inspections, condition assessments, and written specialist findings throughout San Diego. Start with a free phone and photo review.",
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
    },
    {
      "@type": "FAQPage",
      "@id": "https://www.sdhardwoods.com/floor-assessments-inspections#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Is the first phone conversation free?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. Every client relationship starts with a free phone and photo assessment — a conversation, a review of the photos or video you send (or a public real-estate listing), and honest preliminary guidance about the most appropriate next step."
          }
        },
        {
          "@type": "Question",
          "name": "Why is there a $95 charge for an in-home project assessment?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The in-home visit puts more than three decades of hardwood flooring experience on site: travel to the property, a visual assessment of the proposed project, identification of the floor and finish when reasonably determinable, the measurements needed for planning, and a discussion of realistic options — with a San Diego Hardwoods proposal when the work is a suitable fit."
          }
        },
        {
          "@type": "Question",
          "name": "Is the $95 assessment fee credited toward flooring work?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "It can be. When San Diego Hardwoods performs the approved flooring project, part or all of the fee may be applied to that project under a written agreement confirmed before the work begins."
          }
        },
        {
          "@type": "Question",
          "name": "What is included in the $350 pre-purchase inspection?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "An on-site inspection of a property you are evaluating before purchase: apparent identification of the flooring type, construction, and finish; an evaluation of visible condition, wear, damage, and maintenance concerns; and a verbal explanation of realistic options and likely future flooring needs. It is primarily verbal — written reports are part of the $750 service."
          }
        },
        {
          "@type": "Question",
          "name": "What written reports are included with the $750 service?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Two professional PDFs: a Floor Identification & Condition Report covering what the floor appears to be, its apparent condition, repairability, and restoration feasibility with important limitations; and a Recommended Scope & Estimate describing recommended work and, when appropriate, a proposal for San Diego Hardwoods to service the flooring after you take ownership. The documentation may assist with purchase planning, budgeting, or negotiations."
          }
        },
        {
          "@type": "Question",
          "name": "What situations call for the complex damage, dispute, or insurance service?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Insurance claims, water or moisture damage, landlord-tenant or security-deposit disputes, neighbor or contractor damage, conflicting opinions about a floor's condition, complicated repairability questions, and matters that need customized documentation or communication with specifically identified third parties. The exact scope is agreed in writing before work begins."
          }
        },
        {
          "@type": "Question",
          "name": "How are appointments and payments arranged?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "After the free phone and photo assessment, you receive written confirmation of the scope and fee. Payment may be requested through a Square invoice sent by email or text, or another directly approved method such as Zelle, and payment reserves the scheduled service."
          }
        },
        {
          "@type": "Question",
          "name": "Can every damaged or worn floor be restored?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No — and a professional assessment is how you find out before spending real money. Construction, wear layer, finish, contamination, and existing damage all affect feasibility. Many floors that look tired have meaningful restoration options; some do not. Either way, you get an honest, experienced answer."
          }
        }
      ]
    }
  ]
}
</script>"""

# Schema milestone (2026-07-19, refined 2.9): expand each service's
# areaServed from the original bare "San Diego County" to the site's real
# priority-coastal list (San Diego only -- South Orange County lives on the
# shared #local entity, never on a per-page Service).
JSONLD = JSONLD.replace('{"@type": "Place", "name": "San Diego County"}', _ASSESSMENT_AREA)
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
  <h1>Professional Hardwood &amp; Bamboo Floor Assessments, Pre-Purchase Inspections &amp; Consultation</h1>
  <p>Our core business is the flooring work itself &mdash; refinishing, restoration, deep cleaning and recoating, repairs, and installation of hardwood and bamboo floors. When a floor or a property decision calls for professional expertise on site, we also offer a clear set of paid assessment and inspection services: an in-home project assessment, pre-purchase floor inspections with optional written documentation, and complex damage, dispute, and insurance analysis. Every one of them begins the same way: with a conversation that is free.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="sms:+18586990072">Text Photos for a Free Assessment</a>
    <a class="btn btn-outline" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
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
    <p><strong>An initial conversation and review of submitted photographs to identify likely options and determine whether an on-site service may be worthwhile.</strong> Text clear overall and close-up photos for the fastest initial review. You are also welcome and encouraged to call, and photos may be emailed when texting is not practical.</p>
    <p>Initial contact may include a phone conversation; review of photos or a short video you text or email; or review of a public Zillow, Redfin, Realtor.com, or similar listing for a property you are considering. We will discuss likely flooring options, whether San Diego Hardwoods is a suitable fit, and which type of property visit or professional service &mdash; if any &mdash; makes sense for your situation. Many questions are answered completely in this free conversation; a paid visit is never a requirement for getting an initial answer.</p>
    <div class="cta-row" style="justify-content:flex-start;margin-top:6px;">
      <a class="btn btn-call" href="sms:+18586990072" style="padding:11px 22px;font-size:15.5px;">Text Photos for a Free Assessment</a>
      <a class="btn btn-outline" href="tel:+18586990072" style="padding:11px 22px;font-size:15.5px;">&#9742; Call to Discuss Your Floor</a>
      <a class="btn btn-outline" href="mailto:sandiegohardwoods@gmail.com" style="padding:11px 22px;font-size:15.5px;">Email Photos</a>
    </div>
  </div>
</section>

<section class="block" id="can-this-floor-be-refinished">
  <p class="eyebrow">The Question We're Asked Most</p>
  <h2>Can This Floor Be Refinished?</h2>
  <p class="lede">Whether a hardwood or bamboo floor can be refinished &mdash; and what it would take &mdash; depends on several specific things we evaluate, not a guess from a photo alone.</p>
  <div class="info-grid">
    <div class="card">
      <h3>Solid vs. Engineered Construction</h3>
      <p>Solid wood floors can typically be sanded and refinished multiple times over their lifespan. Engineered floors have a thinner wear layer of real wood over a plywood or composite core &mdash; how much wear layer remains, and whether it has already been sanded before, determines whether another full sanding is possible.</p>
    </div>
    <div class="card">
      <h3>Existing Finish &amp; Coating Compatibility</h3>
      <p>Oil, hard-wax-oil, polyurethane, and factory-applied aluminum-oxide finishes all behave differently. We identify the existing finish system and evaluate whether it can be cleaned, recoated, or is compatible with a new product &mdash; including whether an oil or hard-wax-oil floor is a candidate for conversion to a durable, low-sheen waterborne finish.</p>
    </div>
    <div class="card">
      <h3>Wire-Brushed, Textured &amp; Hand-Scraped Surfaces</h3>
      <p>Textured floors can usually be cleaned, recoated, or refinished, but sanding a heavily textured surface requires judgment about how much character to preserve versus remove.</p>
    </div>
    <div class="card">
      <h3>Damage, Repairs &amp; Matching</h3>
      <p>Water damage, exposed fasteners, movement, staining, and prior repairs all affect feasibility. When boards need to be matched, we evaluate species, cut, dimensions, mill profile, grade, and character to determine how closely a repair can blend with the surrounding floor &mdash; and where it realistically cannot.</p>
    </div>
  </div>
  <p class="lede" style="margin-top:20px;">The realistic outcome is different for every floor. A free phone and photo assessment gives a preliminary read; an in-home visit or pre-purchase inspection below gives you a specific, evaluated answer.</p>
</section>

<section class="block" id="in-home-project-assessment">
  <p class="eyebrow">Planning a Flooring Project</p>
  <h2>In-Home Project Assessment &mdash; $95</h2>
  <div class="consult-card consult-primary">
    <div class="consult-head">
      <h3>In-Home Project Assessment</h3>
      <span class="consult-price">$95</span>
    </div>
    <p><strong>An on-site review of visible condition, probable project scope, feasibility, and practical next steps. Findings are primarily verbal unless another deliverable is agreed in advance.</strong></p>
    <p>For owners and authorized decision-makers considering San Diego Hardwoods for their flooring work. We travel to the property, visually assess the proposed flooring project, identify the floor and finish when reasonably determinable, take the measurements needed for project planning, and discuss realistic flooring-service options. When the project is a suitable fit, we prepare a San Diego Hardwoods proposal.</p>
    <p><strong>Some or all of the assessment fee may be credited toward the approved flooring project under written agreement.</strong></p>
    <p class="consult-fine">This is a project-planning visit, not a formal inspection or damage-analysis service &mdash; it does not include formal written inspection reports, purchase-negotiation documents, insurance or dispute documentation, detailed causation analysis, or communication with third parties.</p>
  </div>
</section>

<section class="block" id="pre-purchase-inspections">
  <p class="eyebrow">Buying a Home</p>
  <h2>Pre-Purchase Hardwood &amp; Bamboo Floor Inspections</h2>
  <p class="lede">Both pre-purchase services are for someone evaluating a property they do not yet own. An experienced hardwood and bamboo flooring specialist inspects the floors before you commit, so the flooring's real condition &mdash; and its realistic future &mdash; is part of your purchase decision. A pre-purchase inspection can help distinguish ordinary wear from conditions that may require moisture correction, board replacement, or a larger restoration budget before closing.</p>
  <p class="lede"><strong>This is not a substitute for a general home inspection.</strong> A general home inspector may identify visible flooring concerns as part of a broader property inspection. San Diego Hardwoods provides a flooring-specialist evaluation of condition, construction, restoration feasibility, repair options, and likely limitations &mdash; not structural engineering, mold inspection, general home inspection, or environmental laboratory testing.</p>
  <div class="consult-grid">
    <div class="consult-card">
      <div class="consult-head">
        <h3>Pre-Purchase Floor Inspection &mdash; Verbal Assessment</h3>
        <span class="consult-price">$350</span>
      </div>
      <p><strong>An on-site review focused on visible condition, refinishing feasibility, damage, and practical purchase risks, followed by verbal findings.</strong></p>
      <p>Includes apparent identification of the flooring type, construction, and finish; evaluation of visible condition, wear, damage, and maintenance concerns; and a verbal explanation of realistic cleaning, repair, restoration, refinishing, or replacement options, along with apparent limitations and likely future flooring needs.</p>
      <p class="consult-fine">This service is primarily verbal and does not include formal written reports or negotiation documents. The fee covers the inspection and professional analysis whether or not you purchase the property, the transaction closes, or you later hire San Diego Hardwoods.</p>
    </div>

    <div class="consult-card">
      <div class="consult-head">
        <h3>Pre-Purchase Inspection with Written Documentation</h3>
        <span class="consult-price">$750</span>
      </div>
      <p><strong>A written summary of observed conditions, photographs, measurements when included in the agreed scope, limitations, and recommended next steps.</strong></p>
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
  <h2>Complex Damage, Dispute &amp; Insurance Analysis &mdash; Starting at $1,500</h2>
  <div class="consult-card">
    <div class="consult-head">
      <h3>Complex Damage, Dispute &amp; Insurance Analysis</h3>
      <span class="consult-price">Starting at $1,500</span>
    </div>
    <p><strong>A custom scope for technically difficult or potentially multi-cause conditions. Scope, limitations, and deliverables are confirmed before scheduling.</strong></p>
    <p>A customizable professional service for matters involving insurance claims, water or moisture damage, landlord-tenant and security-deposit disputes, neighbor or contractor damage, conflicting opinions about floor condition, complicated repairability or damage questions, third-party communication, and customized documentation.</p>
    <p>When specifically agreed in writing, this service can include on-site professional evaluation; multiple scheduled phone consultations; multiple PDFs or customized written documents; professional photographs; measurements and moisture readings when relevant; forensic-style analysis of flooring construction, finish, wear, damage, repairability, restoration feasibility, and realistic limitations; repair, restoration, refinishing, or replacement recommendations; scope or cost documentation; and communication with specifically identified insurers, property managers, tenants, landlords, contractors, neighbors, designers, real-estate professionals, or other involved parties.</p>
    <p class="consult-fine">The exact scope and deliverables are customized and agreed upon before work begins, and work beyond the agreed scope requires separate written authorization. This is professional flooring analysis &mdash; not laboratory analysis, engineering services, or legal representation.</p>
  </div>
  <p class="consult-fine" style="max-width:860px;margin:22px auto 0;">These assessment and inspection services do not automatically include engineering, laboratory analysis, real-estate appraisal, legal opinions, insurance coverage decisions, destructive testing, testimony, or expert-witness services. Any specialized scope beyond professional flooring analysis must be specifically agreed in writing before scheduling.</p>
</section>

<section class="block" id="what-an-evaluation-clarifies">
  <p class="eyebrow">Report-Style Examples</p>
  <h2>What a Professional Evaluation Can Clarify</h2>
  <p class="lede">The examples below are <strong>illustrative report-style examples</strong> written to show the kind of clarity a professional evaluation is meant to deliver. They are not excerpts from actual client reports, and they are not a promise that every service includes testing, measurements, photographs, or written documentation &mdash; each service's deliverables are confirmed before scheduling.</p>
  <div class="info-grid">
    <div class="card">
      <h3>Existing Condition</h3>
      <p><em>&ldquo;Localized cupping and finish breakdown are visible near the exterior door and refrigerator run. Much of the surrounding floor may remain refinishable, but the affected area should not be sanded until moisture conditions and the source of exposure are evaluated.&rdquo;</em></p>
    </div>
    <div class="card">
      <h3>Probable Cause</h3>
      <p><em>&ldquo;The pattern is more consistent with repeated moisture exposure and restricted drying than with ordinary finish wear. An on-site evaluation may narrow the likely cause, but concealed conditions can require access beyond the visible flooring surface.&rdquo;</em></p>
    </div>
    <div class="card">
      <h3>Feasibility or Limitations</h3>
      <p><em>&ldquo;Sanding and refinishing may improve the overall surface and color, but replaced boards may remain visible because of age, oxidation, grain, prior coatings, and natural wood variation. An invisible match should not be promised.&rdquo;</em></p>
    </div>
    <div class="card">
      <h3>Recommended Next Step</h3>
      <p><em>&ldquo;Correct the moisture source, document readings when included in the agreed service, inspect accessible transitions and subfloor conditions, then choose between selective board replacement, localized repair, or full refinishing.&rdquo;</em></p>
    </div>
  </div>
  <p class="lede" style="margin-top:26px;">This is the difference between guessing and knowing: the free phone and photo assessment identifies likely options, and a paid on-site evaluation turns them into findings you can act on &mdash; stated plainly, with their limitations.</p>
</section>

<section class="block" id="who-these-services-help">
  <h2>Who These Services Help</h2>
  <p class="lede">Homeowners planning flooring work, prospective buyers evaluating a property, landlords and tenants, property managers, real-estate professionals, designers and contractors seeking a second opinion, and clients with insurance-related flooring questions &mdash; especially when floors are affected by water, moisture, repair, finish-failure, or damage concerns, or are simply confusing to diagnose.</p>

  <figure style="max-width:520px;margin:0 auto 30px;border-radius:10px;overflow:hidden;border:1px solid var(--line);">
    <a href="/LARK56.jpg"><img src="/LARK56.jpg" alt="Hardwood floor refinishing in Encinitas — deep cleaning and prep on wide-plank oak before a durable, dust-contained recoat for a coastal North County home. Deciding whether a hardwood floor needs deep cleaning, maintenance recoating, or full sanding and refinishing — as with this Encinitas wide-plank oak project — is exactly the kind of condition and feasibility evaluation San Diego Hardwoods provides through its free phone and photo assessment and in-home floor evaluations throughout San Diego County." style="width:100%;display:block;" loading="lazy"></a>
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
  <p class="lede">Text clear overall and close-up photos of your floors &mdash; or send a listing link for a property you are considering &mdash; and we will take it from there with a Free Phone &amp; Photo Assessment. You are also welcome and encouraged to call, and photos may be emailed when texting is not practical. All of our contact options are on the <a href="https://www.sdhardwoods.com/contact_us.html" style="color:var(--brass-deep);font-weight:700;">Contact San Diego Hardwoods</a> page.</p>
  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="sms:+18586990072">Text Photos for a Free Assessment</a>
    <a class="btn btn-outline" href="tel:+18586990072">&#9742; Call to Discuss Your Floor</a>
    <a class="btn btn-outline" href="mailto:sandiegohardwoods@gmail.com">Email Photos</a>
  </div>
  <p style="text-align:center;margin:26px auto 0;font-size:15.5px;">
  See the work behind these evaluations:
  <a href="https://www.sdhardwoods.com/recent_project_photo_gallery_1.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Real Hardwood Floor Refinishing Projects &rarr;</a>
  &nbsp;&bull;&nbsp; <a href="https://www.sdhardwoods.com/videos_of_refinishing_process.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Hardwood Floor Refinishing Process Videos &rarr;</a>
  </p>
</section>
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Assessments &amp; Inspections", MAIN,
         str(BUILD.parent / "floor-assessments-inspections.html"))
