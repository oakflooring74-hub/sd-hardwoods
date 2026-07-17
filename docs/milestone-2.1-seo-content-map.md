# Milestone 2.1 — SEO strip inventory & content-relocation map

Date: 2026-07-17. Companion to `docs/2026-07-milestone-2.1-qa-report.md`.

## What was removed, and why

Every generated page used to render two elements at the top of the page chrome:

1. **Top utility strip** (`#sdhUtilityBar`): `San Diego, CA 92130 | 858-699-0072 | sandiegohardwoods@gmail.com` — identical on all 12 pages.
2. **Tiny SEO strip** (`#sdhSeoStrip`): the legacy Turbify "vcard" business-description paragraph, rendered at 10.5px/62% opacity below the navigation, with per-page wording (inventoried below).

Both were removed from `build/chrome/top.html` at the owner's request (Milestone 2.1 brief, items 2–3). They are **not hidden with CSS** — the markup no longer exists in generated output. The `__VCARD_DESC__` placeholder no longer appears in the chrome; build scripts still pass their vcard strings to `assemble()` for compatibility, but nothing renders them.

### Where the business information (NAP) still lives

- **Masthead** (every page): business name, tagline, phone, email, "Free Phone Assessment" CTA.
- **Footer** (every page): name, "Owner Operated Since 1990", *"Licensed, Bonded & Insured California Flooring Contractor • Bona Certified Craftsman"*, service list, service-area list, phone, email, Bona verification link, and — **added in this milestone** — `San Diego, CA 92130 • CSLB-Licensed California Flooring Contractor` (the address/ZIP and CSLB wording previously only carried by the removed strips).
- **Contact page**: full contact block, plus a new readable service-area paragraph (see below).
- **JSON-LD structured data**: unchanged on every page (FlooringContractor/LocalBusiness blocks with address, phone, areas served).
- Legacy `vcard.txt` extraction files in `build/data/` are untouched (frozen source records).

## Per-page strip inventory and disposition

The strips shared a common core across all 12 pages: *licensed contractor; 25/30+ years experience; all types of solid and engineered wood (and bamboo) floors; all work guaranteed; small crew of skilled and courteous craftsmen; text photos for quick assessment; CSLB/California licensed; dust-containment sanding equipment used for all phases; call to schedule an estimate/consultation in San Diego and Orange County.*

That shared core is retained **once, site-wide, in readable form**: footer (licensed/bonded/insured, Bona Certified, CSLB, ZIP, service area), homepage "Why Homeowners Choose San Diego Hardwoods" card (guaranteed work, small crew, text photos), About "Professional Credentials" card (CSLB, guarantee, small crew, dust containment on every phase), and Contact's new intro (text-photos assessment, service area, Orange County). It is deliberately **not** repeated as boilerplate on every page — repeating an identical block on all 12 pages is exactly the pattern this milestone removes.

| Page | Original strip text (distinctive parts) | Disposition |
|---|---|---|
| index | "SAN DIEGO HARDWOOD FLOOR REFINISHING. TRADITIONAL DUST-FREE WOOD AND BAMBOO FLOOR REFINISHING / RESTORATION. FULLY LICENSED… 30 YEARS… GUARANTEED… TEXT PHOTOS… CALIFORNIA LEGITIMATE LICENSED… DUST CONTAINMENT SANDING EQUIPMENT USED FOR ALL PHASES… SAN DIEGO AND ORANGE COUNTY" | Core subjects now carried by the **new hero copy** (since 1990; solid/engineered/bamboo; repair, dust-contained sanding/refinishing, deep cleaning, recoating, nail-down & glue-down installation), the new **Bona DCS 2.0 dust-containment section**, and the guaranteed-work/small-crew/text-photos sentence added to "Why Homeowners Choose San Diego Hardwoods". |
| about_us | Same core + "…WOOD **AND BAMBOO** FLOORS… LEGETIMATE LICENSED… CALL TO SCHEDULE A CONSULTATION…" | Already covered by the page body (since 1990, Bona certification, dust containment, species incl. bamboo). Guarantee + small crew + CSLB + dust containment on every phase **added to the "Professional Credentials" card**. |
| contact_us | "SAN DIEGO LICENSED WOOD FLOOR RESTORATION/REFINISHING CONTRACTOR… DUSTLESS HARDWOOD AND BAMBOO… TEXT PHOTOS OF YOUR PROJECT FOR AN IMMEDIATE ASSESSMENT." | New readable lede under the contact H2: based in San Diego (92130); solid/engineered hardwood and bamboo; serves San Diego County with select projects in Orange County; text photos for a same-day assessment. |
| videos | "THE BEST HARDWOOD FLOOR REFINISHING IN SAN DIEGO… GUARANTEED… SMALL CREW… CSLB LICENSED… DUST CONTAINMENT… ALL PHASES." | "All work is guaranteed, performed by a small crew of skilled and courteous craftsmen, and backed by a CSLB-licensed San Diego flooring contractor" added to the "Why Homeowners Watch Our Videos" lede; dust containment covered throughout the new page intro/featured copy. |
| gallery 1 | Same core as deep-cleaning page ("HEPA DUST CONTAINMENT…") | Core kept site-wide (footer). Page keeps its own unique hero intro (dustless sanding, repairs, restoration, color changes, custom stain work). |
| gallery 2 | Readable sentence-case variant (refinishing, restoration, repairs, custom installation, dust containment, deep cleaning, bamboo, engineered; 35 years; text photos) | Substantively identical to the page's existing hero paragraph — retained there. |
| gallery 3 | Same core (25 years variant) | Core kept site-wide. **Intro enriched** with page-specific work: yellow birch (Del Mar), wide-plank French oak over concrete (La Jolla), custom stain/finish work. |
| gallery 4 | Same core (25 years variant) | Core kept site-wide. **Intro enriched**: solid hickory + butcher-block (Rancho Santa Fe), termite-damage repair (La Jolla Shores), sun-faded engineered oak (Santa Luz). |
| gallery 5 | Same core (30 years variant) | Core kept site-wide. **New hero intro** describes the five restored projects (#81–#85) by neighborhood and floor type. |
| solid wood gallery | Same core (25 years variant) | Core kept site-wide. Page's topical relevance now carried by the restored four project write-ups + original intro/sourcing/outro prose (see QA report). |
| deep-cleaning | Same core + "HEPA DUST CONTAINMENT SANDING EQUIPMENT" | Core kept site-wide. Page gained three readable cards: Cleaning-Only Service; Intensive Cleaning Before Recoating; Wire-Brushed, Textured & Oil-Finished Floors (incl. oiled-floor conversion to waterborne finish). |
| blog | "Professional Hardwood Floor Refinishing, Restoration & Floor Care in San Diego" (unique, sentence case) | This exact string still renders as the blog's first section H2 (it always did, independently of the strip). |

## Wording deliberately removed (and why)

- **All-caps keyword phrasing** ("THE BEST…", "LEGETIMATE LICENSED" [sic], "FIX YOUR WOOD FLOOR TODAY NEAR ME", "FREE ESTIMATES") — keyword-stuffed, typo-carrying, or superlative-claim text; replaced by the sentence-case equivalents above. The blog hero's all-caps line "REFINISH RESTORE REPAIR WOOD HARDWOOD BAMBOO…BONA CERTIFIED CRAFTSMAN" was rewritten as a normal sentence with the same subjects.
- **"CALL TO SCHEDULE AN ESTIMATE"** — the site's CTA language was standardized to "free phone assessment" in Milestone 2 (owner-approved); the strips predated that.
- **Duplicate repetition** — the same core paragraph no longer repeats on 12 pages; it lives once in the footer/relevant pages as described.
- **Orange County** — retained once, readably, on the Contact page ("select projects in Orange County") instead of in every strip.
- **hCard microformat markup** (`class="vcard"`, `organization-name`, etc.) — removed with the strip. Machine-readable business data is fully carried by the JSON-LD structured data, which Google prefers; hCard is legacy.

## Also part of this milestone's content work

- **Legacy image-button alt text**: removing the button graphics also removed their keyword-stuffed alt text (e.g. "SEE BEFORE AND AFTER PHOTOS … NEAR ME FREE ESTIMATES …"). These were image-level SEO text on navigation graphics, not page content; their destinations remain fully crawlable through the real navigation and new text links.
- **Videos page structured data**: the legacy `VideoObject` `@graph` (14 videos, placeholder `uploadDate: 2024-01-01T12:00:00Z`) was replaced by a generated graph covering **all 58 public uploads** with real titles, publish dates, ISO-8601 durations, thumbnails, and watch/embed URLs from the checked-in snapshot. The page's other schema blocks (FlooringContractor, CollectionPage, …) are byte-preserved.
- **Homepage H1** (owner-directed, Milestone 2.1 item 4): "Hardwood Floor Installation, Deep Cleaning & Refinishing in San Diego" → "Dust-Contained Hardwood & Bamboo Floor Refinishing, Restoration, Deep Cleaning & Installation in San Diego". All other titles, meta descriptions, canonicals, and H1s are unchanged (verified by diff against the previous build).
- **Dust claims** were made precise in readable copy ("100% dustless" → "dust-contained" / "virtually dust-free in most normal project conditions") per the owner's DCS 2.0 positioning. Protected surfaces (meta titles/descriptions, image alt text, JSON-LD, frozen vcard files) were not touched.
