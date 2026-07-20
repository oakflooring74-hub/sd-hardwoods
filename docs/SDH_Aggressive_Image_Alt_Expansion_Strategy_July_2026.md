# San Diego Hardwoods
## Aggressive, Evidence-Grounded Image Alt-Text Expansion Strategy
**Date:** July 20, 2026

## Purpose

This milestone is owner-directed and ranking-first. It deliberately does **not** optimize image alt text for textbook brevity. The goal is to use the extensive verified project information already present in the rebuilt 13-page San Diego Hardwoods site to create long, detailed, unique, semantically dense alt text for meaningful project images and video thumbnails.

The strategy is aggressive, but it is not permission to invent facts. Every added phrase must be grounded in one or more of these existing sources:

- the current image itself;
- the current alt text;
- owner-dictated homepage image descriptions;
- visible lightbox captions and `data-caption` values;
- gallery pair descriptions and project captions;
- page headings and nearby visible project text;
- verified project metadata already stored in repository data files;
- curated video titles and original YouTube titles already stored by the site;
- owner-approved business facts and service language.

## Owner decision

The owner has consciously chosen a rule-bending image SEO strategy based on the historical performance of the live legacy site. Claude must not automatically shorten, sanitize, or remove long keyword-rich alt text merely to follow conventional best-practice guidance.

This is an intentional controlled experiment:

- preserve existing quality alt text;
- append additional accurate, relevant detail to the end;
- expand short, generic, repeated, or empty alt text;
- create meaningful alt text for project and video thumbnails;
- preserve known ranking images and their existing metadata signals;
- maintain a full before-and-after ledger for rollback and owner review.

No ranking outcome is guaranteed. The implementation must remain factual, reversible, and isolated to the `redesign` branch.

---

## Non-negotiable preservation rules

1. Do not rename, move, replace, resize, re-encode, crop, or reorder images.
2. Do not change public image URLs or filename capitalization.
3. Do not change gallery order, homepage numbering, before/after pairing, video IDs, or thumbnails.
4. Do not change page URLs, canonicals, titles, meta descriptions, H1s, page design, or navigation in this milestone.
5. Do not modify or commit `assets/ALL_IMAGES/`.
6. Do not touch `master` or production.
7. Do not reintroduce Yahoo/Turbify runtime dependencies.
8. Do not delete a quality existing alt description. Use it as the preserved prefix and append to it.
9. Any removal of existing words, phrases, locations, business names, service terms, or competitor references requires an explicit owner-review entry.
10. Do not invent species, construction, finish products, locations, damage, installation methods, results, dates, equipment, or customer facts.

---

## Authoritative source hierarchy

Use the strongest available source in this order:

1. Owner-dictated or owner-approved project facts in repository data files.
2. Existing image-specific alt text and visible caption.
3. Existing gallery pair description or project narrative.
4. Curated video display title and original YouTube title.
5. Nearby visible page text describing the exact project or process.
6. Details plainly visible in the image or thumbnail.
7. Broad page-level service context, used only when it genuinely applies to the image.

When sources disagree, preserve the current wording and flag the discrepancy for owner review. Do not guess.

---

## Expansion model

### Existing quality alt text

Treat it as an immutable factual prefix. Append one or more sentences that add relevant project, service, material, process, condition, result, and verified location context.

Example pattern:

> [Existing accurate description.] This San Diego Hardwoods project involved [verified service/process], [verified flooring type or construction], [verified condition or result], and [verified local/project context]. The image supports searches related to [coherent service concepts that genuinely match the image].

Do not mechanically include the phrase “supports searches related to.” Write natural descriptive prose.

### Short or generic alt text

Expand it into a unique multi-sentence description using all verified facts available for that specific image or project.

### Repeated alt text

Keep the shared project facts, but distinguish each image by:

- room or viewpoint;
- before, during, or after stage;
- visible equipment or process;
- floor area, transition, border, pattern, grain, texture, or finish appearance;
- damage, repair area, installation detail, or completed result;
- relationship to the paired image.

### Empty alt text on meaningful images or video thumbnails

Create detailed alt text from the existing project description, video title, thumbnail subject, and page context. For video thumbnails, title redundancy is an intentional owner decision in this milestone. Do not leave a meaningful video thumbnail empty solely because an adjacent linked title already exists.

### Decorative images

Purely decorative icons, background flourishes, and redundant brand marks may remain empty when they do not carry meaningful project or service information. Do not force keyword text into decorative interface assets.

---

## Aggressive length and density

There is no arbitrary character limit. Alt text may be long or multi-sentence when the repository contains enough verified facts.

Typical target:

- simple meaningful image: roughly 200–450 characters;
- information-rich project image: roughly 350–800 characters;
- complex before/after, installation, repair, water-damage, historic-restoration, or video thumbnail: 500–1,000+ characters when supported by verified information.

Length must come from accurate detail, not meaningless repetition. Do not pad alt text with random city lists, unsupported product names, or unrelated services.

---

## Search concepts to distribute across relevant images

Use these terms naturally only where they match the image, project, page, and verified facts:

- San Diego Hardwoods
- San Diego County
- hardwood floor refinishing
- sand and refinish wooden floors
- dustless hardwood-floor sanding
- true 100% dust containment
- hardwood and bamboo floor restoration
- professional hardwood-floor deep cleaning
- maintenance recoating
- wire-brushed and textured hardwood floors
- embedded grime and residue removal
- oil-finished and hard-wax-oil floors
- engineered hardwood wear-layer evaluation
- re-oiling, recoating, or finish conversion
- water-damaged hardwood-floor repair
- selective board replacement and matching
- vintage and historic hardwood restoration
- Douglas fir and classic oak restoration
- solid and engineered wood-floor installation
- nail-down installation
- glue-down installation over concrete
- floating and nail-assist installation
- unfinished flooring sanded and finished onsite
- cork, underlayment, and sound-control systems
- floor assessments and inspections
- can this floor be refinished
- pre-purchase floor inspection
- free phone and photo assessment

Do not put every concept into every image. Build a distributed semantic network across the site, with each image carrying the terms that actually belong to it.

---

## Competitor-name policy

Existing competitor-name references are protected unless they are factually false, defamatory, or clearly broken. Do not remove them merely because they are unconventional.

New competitor references may be appended only when:

- the current Deep Cleaning page or existing metadata already establishes the comparison;
- the image genuinely shows specialized hardwood-floor cleaning, extraction, recoating, or a result relevant to the comparison;
- the wording is coherent and descriptive rather than a disconnected keyword list;
- no unsupported claim is made about the competitor.

Established comparison names may include COIT, Stanley Steemer, and Zerorez where already supported by the current page or metadata. Every new use must be listed in the implementation report.

---

## Page-specific strategy

### Homepage

The owner personally dictated the descriptions for the homepage project images. Treat the existing homepage alt text and lightbox captions as authoritative image-specific facts. Preserve the current alt text verbatim and append richer service, process, material, condition, result, and verified-location language.

Do not change image numbers, captions, order, paths, or lightbox behavior.

### Gallery pages

Use the existing pair descriptions, captions, alt text, and project narratives. Each image in a pair must retain the shared project facts while clearly distinguishing its view and stage.

Do not invent facts to make paired images sound different. Use visible differences and existing descriptions.

### Deep Cleaning page

Retain and expand established aggressive terminology around professional deep cleaning, wire-brushed and textured flooring, embedded grime, wax/polish/residue removal, maintenance recoating, oil-finished floors, and comparison with general cleaning companies where already supported.

Do not automatically remove competitor names or long service comparisons.

### Solid & Engineered Installation page

Expand relevant images with verified details about solid or engineered construction, nail-down, glue-down, floating, nail-assist, concrete, subfloor, moisture, cork, underlayment, sound control, onsite sanding, and custom finishing.

### About, Assessments, Contact, and Blog

Use only the facts relevant to each meaningful image. Do not turn logos, credentials, or decorative imagery into unrelated service keyword containers.

### Videos page

Use the existing curated display title, original YouTube title, thumbnail subject, and nearby description to create unique long alt text for every meaningful video thumbnail.

Preserve all video IDs, titles, order, dates, thumbnails, embeds, and VideoObject schema. Alt-text work must not alter video metadata fields.

---

## Audit and rollback ledger

Create a durable ledger at:

`build/data/image_alt_expansion_ledger.csv`

Required columns:

- page_url
- source_file
- image_path
- image_role
- project_or_video_id
- current_alt
- current_alt_length
- authoritative_sources_used
- appended_text
- final_alt
- final_alt_length
- retained_existing_alt_verbatim
- competitor_names_retained
- competitor_names_added
- confidence
- owner_review_required
- notes

Also create:

`docs/2026-07-aggressive-image-alt-expansion-report.md`

The report must summarize coverage, lengths, duplicates, empty alts, source files changed, protected ranking assets, competitor-name handling, unresolved facts, tests, commit, and preview deployment.

---

## Quality controls

- Every final alt must accurately describe or contextualize the specific image or thumbnail.
- Existing quality alt text must appear verbatim at the start of the final alt.
- No existing keyword or phrase may be silently removed.
- No unverified location, species, product, finish, method, or result may be added.
- Distinguish repeated images by visible viewpoint or stage.
- Escape HTML entities and quotation marks correctly.
- Ensure multiline source data emits valid single `alt` attributes in generated HTML.
- Avoid accidental duplicate final alts.
- Do not let the build pipeline truncate generated values.
- Do not alter visible captions unless fixing a confirmed rendering defect.

---

## Verification standard

After implementation:

1. Rebuild all 13 pages.
2. Confirm a second rebuild is byte-identical.
3. Confirm every meaningful project image and video thumbnail has nonempty alt text.
4. Confirm decorative empty alts are intentional and documented.
5. Confirm existing quality alt strings remain verbatim prefixes.
6. Confirm no image path, filename, order, dimensions, caption, or source changed.
7. Confirm no page URL, canonical, title, meta description, H1, or navigation changed.
8. Confirm no broken HTML attributes, quotes, entities, images, links, videos, or JSON-LD.
9. Report duplicate final alts, but do not shorten or rewrite them automatically when the duplication is justified.
10. Browser-check representative homepage, gallery, deep-cleaning, solid/engineered, assessment, and videos pages on desktop and mobile.
11. Run `git diff --check` and review the complete diff.
12. Commit and push only to `redesign`; confirm GitHub Actions and the protected Cloudflare preview succeed.
13. Keep `master` untouched.

---

## Success standard

The completed site should retain every accurate high-value image description already created, append substantially richer and longer verified context, give every meaningful video thumbnail a detailed alt description, distribute the proven San Diego Hardwoods service vocabulary across relevant images, preserve ranking asset URLs and page relationships, and provide a complete rollback ledger.
