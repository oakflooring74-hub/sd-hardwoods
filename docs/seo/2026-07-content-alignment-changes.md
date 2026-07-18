# Milestone 2.5 content-alignment change log (before / after)

**Date:** 2026-07-18 · **Branch:** `redesign`

Every material visible-wording change made in Milestone 2.5, with the exact before/after text,
the page affected, and the search or visitor reason. All changes were made in generator
sources (`build/data/`, `build/scripts/pages/`), never by hand-editing generated HTML.
**No titles, meta descriptions, or H1s changed on any page.** Galleries 2, 3, 4, Blog, and
Contact are byte-identical to their Milestone 2.4 output.

## 1. Homepage (`index.html`)

### 1a–1d. Corrected false walnut image identities (owner-confirmed facts)

Source: `build/data/index/gallery.json`. The owner confirmed all four photos are one walnut
refinishing project at Bing Crosby Ranch, San Diego. Stage/angle per photo remains
unconfirmed, so the new alts are deliberately restrained and marked
`owner_confirmed_project_identity` (stage pending) in the media inventory.

| # | Image | Before (false) | After (provisional, confirmed identity) |
|---|---|---|---|
| 1a | TRICIA WALNUT102.jpg | " Walnut floors sanded dust-contained and refinished to satin in San Diego, finished with museum grade Bona water based finish" | "Walnut floor refinishing project at Bing Crosby Ranch in San Diego" |
| 1b | TRICIA WALNUT110.jpg | "Deep clean and recoat of bamboo flooring with dust contained prep, Bona Traffic HD finish by a licensed San Diego contractor" | "Alternate view of walnut flooring during the Bing Crosby Ranch refinishing project" |
| 1c | TRICIA WALNUT54.jpg | "High end parquet resurfaced and upgraded to Bona polyurethane in Rancho Santa Fe, texture removed for a flatter modern look" | "Walnut flooring from a refinishing project at Bing Crosby Ranch, San Diego" |
| 1d | TRICIA WALNUT23.jpg | "La Jolla maple floors scratched and dull restored smooth with dustless sanding by hardwood floor refinishing San Diego experts." | "Additional view of the Bing Crosby Ranch walnut floor project" |

Reason: factual correction (bamboo/parquet/maple/Rancho Santa Fe/La Jolla identities were
false); removes unsupported "museum grade" claim; avoids keyword-stuffing four alts.

### 1e. Gallery intro lede

- **Before:** "Before-and-after results from homes across La Jolla, Del Mar, Rancho Santa Fe, Encinitas, Carmel Valley, and throughout San Diego County."
- **After:** "Ninety real hardwood floor refinishing, sanding, repair, deep-cleaning and restoration projects from homes across La Jolla, Del Mar, Rancho Santa Fe, Encinitas, Carmel Valley, and throughout San Diego County."
- Reason: names the page's core GSC themes (refinishing/sanding/repair) naturally where 90 proof photos actually sit; helps visitors understand what the grid contains.

### 1f. Hero video iframe title (accessibility label)

- **Before:** `100% dust-free hardwood floor refinishing in San Diego`
- **After:** `Dust-contained hardwood floor refinishing in San Diego`
- Reason: claims policy — "dust-contained", never absolute "100% dust-free".

## 2. Deep-Cleaning (`deep-cleaning-hardwood-floors-san-diego.html`)

### 2a. Hero opening sentence

- **Before:** "Restore dull, worn floors without the cost, dust, or disruption of full sanding. Our professional Bona PowerScrubber system deep cleans, removes wax and polish buildup, and prepares hardwood floors…"
- **After:** "Professional hardwood floor cleaning without the cost, dust, or disruption of full sanding. Our Bona PowerScrubber wood floor deep cleaning system removes embedded dirt, wax and polish buildup, and prepares hardwood floors…"
- Reason: "professional hardwood floor cleaning" and "wood floor deep cleaning" are this page's two strongest actual GSC query themes; used once each, naturally.

### 2b. New "When Cleaning Isn't Enough" card (added, nothing removed)

- **After (new):** "Deep cleaning cannot repair a finish that is worn through, deep scratches into raw wood, or gray, water-damaged boards. When a floor has reached that point, it needs full sanding and refinishing — see our **dust-contained hardwood floor refinishing in San Diego** [links to homepage]. We'll tell you honestly which service your floor actually needs."
- Reason: required page distinction #4 (situations where cleaning cannot repair worn-through finish) plus the required internal link back to general refinishing.

### 2c. Closing link row

- **Before:** "See Before & After Project Galleries →" (Gallery 1) + call + text.
- **After:** "Real Hardwood Floor Refinishing Projects →" (Gallery 1) · "Restoration & Deep-Cleaning Projects →" (Gallery 4) · "Contact San Diego Hardwoods" + call + text.
- Reason: descriptive anchors; links cleaning visitors to the gallery that actually owns restoration/deep-cleaning proof; adds the Contact path.

## 3. Gallery 1 (`recent_project_photo_gallery_1.html`)

### 3a. Hero intro

- **Before:** "…featuring dustless sanding, hardwood floor repairs, restoration, color changes, custom stain work…"
- **After:** "…featuring dust-contained floor sanding, hardwood floor repairs, deep cleaning, restoration, color changes, custom stain work…"
- Reason: §7 requires the intro to convey refinishing/sanding/repair/cleaning/restoration breadth; "dust-contained" replaces the absolute "dustless" per the voice policy.

### 3b. Bottom CTA anchor

- **Before:** "Learn More →"
- **After:** "Professional Hardwood Floor Deep Cleaning →"
- Reason: descriptive anchor text instead of generic "Learn More" (§5.3 / §20).

## 4. Gallery 5 (`recent_project_gallery_5.html`)

### 4a. Closing navigation

- **Before:** "Back to Home →" + call + text.
- **After:** "Hardwood Floor Refinishing in San Diego — Home →" · "Solid & Engineered Wood Floor Installation →" + call + text.
- Reason: descriptive anchors; adds the installation-gallery pathway from the last gallery in the browsing sequence. No projects touched.

## 5. Solid Wood Gallery (`solid_wood_floor_photo_gallery.html`)

### 5a. Hero intro (installation-first)

- **Before:** "Custom nail-down and glue-down hardwood installation throughout San Diego County, alongside our dust-contained refinishing, repair, and restoration services. Below: four complete installation projects…"
- **After:** "Professional hardwood floor installation in San Diego — custom nail-down and glue-down installation of solid and unfinished engineered wood floors, acclimated, sanded, and finished on site throughout San Diego County, alongside our dust-contained refinishing, repair, and restoration services. Below: four complete installation projects…"
- Reason: leads with the page's dominant GSC theme (hardwood floor installation San Diego) and its required technical concepts (solid/engineered, acclimation, on-site finishing) without letting refinishing overpower installation.

### 5b–5e. Claims-policy corrections (`build/data/solid_wood_floor_photo_gallery/projects.json`)

| | Before | After |
|---|---|---|
| 5b intro | "…wide plank flooring for **perfectly** flat surfaces, and a **100% dust containment** option…" | "…wide plank flooring for exceptionally flat surfaces, and dust-contained sanding…" |
| 5c sourcing | "…lumber from trusted mills **that far exceeds big-box store quality**… provide the **flawless** installation…" | "…lumber from trusted mills… provide expert installation…" |
| 5d sourcing note | "We source **these exact** premium mill-direct hardwoods…" | "We source premium mill-direct hardwoods and high-spec engineered planks **like these**…" |
| 5e outro | "…custom colors, **dust-free** sanding…" | "…custom colors, dust-contained sanding…" |

- Reason: §12 explicitly forbids "flawless", "exact", "far exceeds" without owner confirmation; the operating manual forbids absolute dust and perfection claims. (The per-project notes "buy this exact style/look" were left as shopping phrasing, not performance claims.)

### 5f. Closing CTA + link row

- **Before:** "Call 858-699-0072" + text.
- **After:** "Call 858-699-0072 — Discuss Your Installation Project" + text, plus new links: "Hardwood Floor Refinishing in San Diego →" (home) · "More Installation & Refinishing Projects →" (Gallery 2) · "Contact San Diego Hardwoods".
- Reason: required internal-link hierarchy for the installation page; CTA matches page purpose.

## 6. Videos (`videos_of_refinishing_process.html`)

### 6a. Hero intro breadth

- **Before:** "…restoration of vintage and historic floors, intensive deep cleaning and recoating, and premium Bona finish work…"
- **After:** "…restoration of vintage and historic floors, custom staining, intensive deep cleaning and recoating, installation, and premium Bona finish work…"
- Reason: §13 — the intro must convey refinishing, sanding, repairs, staining, installation and restoration; staining/installation were missing.

### 6b. New closing link row

- **After (new):** "Real Hardwood Floor Refinishing Projects →" (Gallery 1) · "Professional Hardwood Floor Deep Cleaning →" · "Contact San Diego Hardwoods".
- Reason: required videos-page links to relevant services, galleries and Contact (YouTube links already existed).

## 7. About (`about_us.html`)

| | Before | After | Reason |
|---|---|---|---|
| 7a | "Text photos for a fast, expert assessment — **same-day replies**." | "…— most replies the same day." | Unqualified turnaround promise → qualified. |
| 7b | "…is a CSLB-licensed, bonded and insured California flooring contractor and proud member…" | "…is a CSLB-licensed, bonded and insured California flooring contractor — **California contractor license #1017549** — and a proud member…" | §14 requires the license number visible; owner-confirmed fact. |
| 7c | "**100% Dust Containment Sanding**" | "**Dust-Contained Sanding on Every Project**" | Claims policy (no absolute dust claims). |

## 8. Assessments (`floor-assessments-inspections.html`)

### 8a. Closing section links (added; pricing architecture and limitations untouched)

- **After (new):** lede now ends "…All of our contact options are on the **Contact San Diego Hardwoods** page." plus a new proof row: "See the work behind these evaluations: Real Hardwood Floor Refinishing Projects → · Hardwood Floor Refinishing Process Videos →".
- Reason: required assessment-page links to Contact and to project/service evidence; keeps the page from being a dead end without making it a refinishing destination.

## Explicitly *not* changed

- All titles, meta descriptions, H1s (13 pages) — preserved from Milestone 2.4.
- Contact page (entirely), Blog, Galleries 2/3/4 — byte-identical output.
- Gallery project write-ups, module titles, captions, and every existing photo/video.
- The approved assessment pricing tiers, fee-credit sentence, and limitation language.
- The deep-cleaning meta description (2.4's "mojibake" flag proved to be a display artifact —
  the committed bytes are a correct UTF-8 em dash).
- The legacy inline Yahoo `var $D` script on galleries 3/4 (throws a harmless
  "YAHOO is not defined" console error inherited from the live Turbify source; noted as a
  cleanup candidate for the performance/hardening milestone).
