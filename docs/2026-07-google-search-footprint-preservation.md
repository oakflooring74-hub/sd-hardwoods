# Google Search Footprint Preservation & Final Prelaunch Alignment

Owner-approved requirements doc for a single controlled implementation pass across the
approved 13-page remake, added 2026-07-20. This is **not** a redesign, a new research
project, a schema restart, or a generic SEO rewrite — it is targeted, evidence-based
preservation and strengthening of Google signals the live site has already earned.

Read alongside `CLAUDE.md`, `docs/PROJECT_QUALITY_BAR.md`, `docs/PROJECT_DECISIONS.md`, and
`docs/2026-07-prelaunch-audit.md`. This file is the requirements record for this milestone;
implementation status and outcomes go in `docs/NEXT_SESSION.md` as usual.

## Baseline that must not be redone

- All 13 pages already build from authoritative source/data/templates (see `build/README.md`).
- Site images and legacy CSS already localized (Milestone 2.10 + prelaunch-audit blocker fix).
- Shared service-area schema already centralized (`build/data/seo/service_areas.json`,
  Milestone 2.9) across all 13 pages.
- Shared business entity stays `https://www.sdhardwoods.com/#local` — do not touch.
- Orange County stays invisible in all marketing copy; exists only in the shared `#local`
  entity's `areaServed` (Milestone 2.9 rule). Do not re-litigate.
- Do not remove legitimate San Diego County service areas.
- Videos page already has one server-rendered hero + all 58 unique public YouTube IDs
  (Milestone 2.9) — preserve that architecture exactly.
- No new pages, no video watch pages, no new auditing framework, no image renaming/reorg.

## Goal

Preserve and strengthen what Google already understands about San Diego Hardwoods (organic,
AI Overview/AI Mode, local, Images, Video) while making the remake clearer. Correct
query-to-page relationships matter more than page-level keyword coverage — don't paste every
topic onto every page; use internal links so pages support each other.

## Owner-authoritative facts (state accurately, only where relevant to the page)

- Owner-operated since 1990; Bona Certified Craftsman; licensed, bonded, insured.
- Primary visible market: San Diego / San Diego County.
- Hardwood + bamboo sanding, refinishing, restoration, deep cleaning, maintenance recoating,
  repairs, installation.
- **True 100% dust containment** — a sealed commercial dust-containment system that captures
  sanding dust at the source. Keep the natural phrase "dustless hardwood-floor sanding and
  refinishing" but pair it with the precise claim. Never soften to "dust-contained" alone or
  adopt generic 95–99% figures.
- Installation: real solid + engineered flooring; nail-down, glue-down, floating, nail-assist;
  unfinished flooring installed/sanded/finished onsite; prefinished flooring; cork/acoustic
  underlayment + sound-control; moisture/subfloor evaluation.
- Water-damage repair, selective replacement, vintage/historic restoration, era-specific
  matching (species, cut, dimensions, mill profile, grade, character).
- Free phone/photo assessment first; paid onsite evaluation + written findings for uncertain,
  damaged, historic, engineered, technically complex, or high-risk floors.
- Never invent generic AI prices, dust percentages, DIY steps, guarantees, competitor claims,
  or unsupported technical assumptions.

## Search evidence → required page relationship (condensed)

| # | Query | Owning page(s) | Preserve / strengthen |
|---|---|---|---|
| 1 | dust free hardwood floor refinishing san diego county | Home, About, Videos, galleries | Precise "true 100% dust containment"; since 1990; Bona; licensing |
| 2 | deep clean my hardwood floors san diego | Home (broad) → Deep Cleaning (detail) | Homepage sentence: restores/refinishes/deep cleans/recoats/installs hardwood+bamboo w/ true 100% dust containment; strengthen link to Deep Cleaning |
| 3 | clean my wire brushed hardwood floors san diego | Deep Cleaning | Wire-brushed/textured cleaning, embedded grime, wax/polish/residue removal, maintenance recoating, evaluation before full sanding. Owner-locked title/meta/H1 below |
| 4 | install nail down real oak floor san diego | Solid & Engineered Installation | Real oak/strip/plank, engineered, nail-down/glue-down/floating/nail-assist, onsite sand/finish, prefinished, cork/underlayment/sound control, subfloor/moisture eval |
| 5 | restore my vintage hardwood floors san diego | Home + galleries | Historic captions/species/locations/paths preserved; route complex matching to Assessments (no new historic page) |
| 6 | bamboo floor refinishing service san diego | Home + supporting images/videos | Bamboo refinish/restore/clean/recoat, dustless/true 100% containment, Bona; no bamboo page |
| 7 | floor refinishing service del mar ca | Home, GBP, galleries | Real Del Mar project refs/captions/alt/paths/links; no Del Mar page, no title stuffing |
| 8 | hardwood floor installer san diego | Home (broad) → Installation (detail) | Keep homepage broad, strengthen link to Installation page |
| 9 | wood floor deep cleaning company san diego | Deep Cleaning | Make it the clearest commercial-intent destination via opening text, internal links, page schema (no new page) |
| 10 | sand and refinish wooden floors san diego | Home, About, Deep Cleaning, galleries | "sand and refinish", hardwood+bamboo, true 100% dust containment, custom stain/water-based finish, expert eval of necessity |
| 11 | re-oil engineered wood floors san diego | Installation / Assessments | Solid vs. engineered distinction, wear layer, oil/hard-wax-oil finishes, compatibility, cleaning, maintenance oil/recoat, localized repair, possible conversion — not every floor qualifies |
| 12 | repair water damaged hardwood floors san diego | Home + galleries | Water-damage repair, selective replacement, species/cut/dimensions/profile/grade/character matching, blending; route complex diagnosis to Assessments |
| 13 | can my hardwood floors in san diego be refinished | Home → Assessments | Homepage authority + clear path to Assessments (construction, wear layer, prior sanding, fasteners, finish compatibility, damage, texture, matching, realistic outcomes) |
| 14 | pre purchase floor inspection san diego | Floor Assessments | **New opportunity, no current visibility.** Make Assessments the primary destination for pre-purchase inspection + written findings |

## Page-specific requirements

**Homepage** — broad authority for refinishing, restoration, deep cleaning, recoating,
installation, hardwood + bamboo, water-damage repair, true 100% dust containment, free
phone/photo assessment. Preserve a sentence close to: *"San Diego Hardwoods restores,
refinishes, deep cleans, recoats and installs hardwood and bamboo floors with true 100% dust
containment throughout San Diego County."* Vary phrasing naturally elsewhere ("dustless
sanding", "dust-containment system", "captures sanding dust at the source") — don't repeat
mechanically. Clear internal links to Deep Cleaning, Solid & Engineered Installation, relevant
galleries/videos, and Floor Assessments & Inspections.

**Deep Cleaning** — owner-locked verbatim (Milestone 2.9, reconfirmed here):
- Title: `Hardwood Floor Deep Cleaning & Maintenance Recoating | San Diego`
- Meta: `Professional hardwood, engineered wood and bamboo floor deep cleaning, wax and polish removal, and maintenance recoating throughout San Diego County.`
- H1: `Hardwood Floor Deep Cleaning, Wax & Polish Removal and Maintenance Recoating in San Diego`

Opening content + page schema must support hardwood/engineered/bamboo, wire-brushed/textured
floors, embedded grime/wax/polish/residue, cleaning-only service, cleaning before recoating,
compatibility evaluation, oil/hard-wax-oil finish ID, cleaning vs. recoating vs. repair vs.
full refinishing, phone/photo CTA.

**Solid & Engineered Installation** (`solid_wood_floor_photo_gallery` page) — must read as a
real service-authority page, not just a gallery: solid + engineered install, nail-down,
glue-down over concrete, floating, nail-assist, unfinished-onsite-finish, prefinished, cork/
underlayment/sound-control, moisture/subfloor/transition/feasibility evaluation.

**About** — owner-operated since 1990, 35+ years, second-generation, Bona certification,
licensing/bonding/insurance, craftsmanship, repairs, installation, true 100% dust-containment
capability.

**Galleries (1–5 + Solid Wood)** — preserve filenames, public paths, order, alt text,
captions, species, processes, authentic locations, landing-page relationships. Only correct
confirmed defects — no broad rewrite. Natural support for historic restoration, water-damage
repair, installation methods, Del Mar/local relevance, Images.

**Videos** — preserve the server-rendered hero, CollectionPage/video architecture, filters,
all 58 YouTube IDs. Useful as process proof for dustless sanding, refinishing, restoration,
deep cleaning, repairs, installation. No watch pages, no broad rewrite.

**Floor Assessments & Inspections** — the diagnostic destination, without cannibalizing
service pages. Must cover: pre-purchase hardwood/bamboo inspection; evaluation before buying a
home with existing wood floors; can this floor be refinished; solid vs. engineered; remaining
wear layer/prior sanding; finish/coating compatibility; oil/hard-wax-oil maintenance options;
water damage/movement/staining/repair feasibility; matching by species/grade/dimensions/cut/
profile/character; subfloor/moisture/sound-control/installation limitations; realistic
restoration options and limitations; photos/measurements/written findings. Report structure:
**Existing Condition → Probable Cause → Feasibility or Limitations → Recommended Next Step.**
State plainly: a general home inspector may flag visible flooring issues; SDH provides a
flooring-specialist evaluation of condition, construction, restoration feasibility, repair
options, and likely limitations. Never imply structural engineering, mold inspection, general
home inspection, or environmental lab testing.

## Titles, meta, H1, schema rules

- Audit all 13 pages against the current authoritative source, `docs/2026-07-prelaunch-audit.md`,
  live-page evidence in-repo, and the query-to-page table above. Implement only the smallest
  evidence-based changes needed to preserve/strengthen protected topics.
- One correct canonical, one H1, one page-specific title, one natural meta description per page.
  Don't rewrite copy just to make it different or chase character counts.
- Where evidence is insufficient, keep current/live wording — don't invent a "better" version.
- Keep the centralized schema architecture and stable `#local` entity; only adjust page-specific
  schema to match visible content/page role. Never paste the full service catalog or area list
  into every page. OC stays invisible in titles/descriptions/H1s/headings/body copy.

## Verification checklist (run once, existing tools only)

- [ ] Rebuild all 13 pages, confirm deterministic (double-build byte-identical)
- [ ] Parse all JSON-LD
- [ ] Confirm stable `#local` identity + correct page/canonical URLs
- [ ] Confirm unique, page-specific titles/meta/H1s
- [ ] Confirm no visible Orange County wording
- [ ] Confirm all 58 YouTube IDs + server-rendered hero intact
- [ ] Confirm no unintended image filename/path/order/alt/caption changes
- [ ] Confirm internal links route broad topics to correct detail/assessment pages
- [ ] Run existing link/asset/accessibility/regression checks
- [ ] `git diff --check`; review final diff for unrelated changes
- [ ] Browser-check desktop + mobile: homepage, Deep Cleaning, Solid & Engineered Installation,
      one restoration gallery, Videos, Floor Assessments
- [ ] Preview noindex protection, production-only GA4 gating, branch/deployment separation intact

Out of scope for this milestone: DNS changes, production deployment, post-launch Search
Console work.
