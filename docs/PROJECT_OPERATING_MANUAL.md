# SAN DIEGO HARDWOODS WEBSITE REMAKE
# PERMANENT PROJECT OPERATING MANUAL
# BINDING ARCHITECTURE, SEO, CONTENT, MEDIA, QA, LAUNCH, AND CONTINUITY DOCUMENT

This document is the permanent operating authority for the San Diego Hardwoods website-remake project.

It exists to prevent:

- Context-window drift
- Repeated investigation
- Forgotten decisions
- Accidental redesign
- Lost SEO value
- Destructive URL changes
- Unsupported factual claims
- Unnecessary side projects
- Tiny low-value token-wasting tasks
- Changes to generated output instead of source files
- Uncoordinated work across new Claude sessions
- Damage to the live Turbify website
- Damage to the master branch
- Loss of approved functionality or content

Every Claude session working on this repository must read and obey this document before making changes.

This document governs all milestone prompts unless a later owner-approved amendment explicitly replaces a specific provision.

Do not reinterpret or casually rewrite this operating manual.

Update project status, decisions and completed-milestone records in the designated continuity files rather than rewriting the governing rules.

==================================================
1. PROJECT IDENTITY
==================================================

Business:

San Diego Hardwoods

Business model:

Owner-operated hardwood-flooring specialist serving San Diego County.

Core experience and credibility:

- Owner operated since 1990
- More than 35 years of flooring experience
- California flooring contractor
- California contractor license number 1017549
- Bona Certified Craftsman
- Licensed, bonded and insured
- Real project photography and technical experience
- Direct owner involvement rather than an anonymous sales organization

Primary contact information:

Phone:
858-699-0072

Call URI:
tel:+18586990072

Text URI:
sms:+18586990072

Email:
sandiegohardwoods@gmail.com

Public street-address publication remains subject to owner confirmation.

Do not publish, standardize or place a full street address into visible content or structured data until the owner has explicitly confirmed the exact public NAP information.

==================================================
2. REPOSITORY AND ENVIRONMENT
==================================================

Local project directory:

C:\FLOORING_SITE\SAN DIEGO HARDWOODS SITE REMAKE JULY 2026

GitHub repository:

oakflooring74-hub/sd-hardwoods

Active development branch:

redesign

Protected branch:

master

Cloudflare redesign preview:

https://redesign.sd-hardwoods.pages.dev

Primary build command:

python build/scripts/build_all.py

The architecture is a deterministic static-site generator.

There is no approved CMS, database or runtime application framework.

The generated root HTML files are build output, not the permanent source of truth.

Permanent changes belong in:

- Shared generator sources
- Shared chrome
- Page generators
- Page data
- SEO data
- Structured media data
- Schema data
- Navigation data
- Sitemap and robots generation
- Supporting scripts
- Documentation

Do not permanently patch generated root HTML files.

Do not introduce:

- WordPress
- A CMS
- A database
- React
- Vue
- Angular
- A frontend framework
- A backend framework
- A build service
- An external SaaS dependency
- An unnecessary npm package
- An unnecessary Python dependency
- A hosting migration
- A deployment-platform rewrite

unless the owner explicitly authorizes a separate architecture milestone.

==================================================
3. RESPONSIBILITY MODEL
==================================================

The owner is the factual authority for:

- Project locations
- Wood species
- Construction type
- Floor condition
- Damage
- Cause
- Work performed
- Stain or color
- Finish system
- Equipment
- Before-and-after status
- Project sequence
- Pricing
- Service boundaries
- Business claims
- Credentials
- Service-delivery timing
- Report content
- Visit duration
- Client deliverables
- Legal or technical limitations

Claude is responsible for:

- Repository implementation
- Generator maintenance
- Code quality
- Structured data
- Content organization
- Natural-language synthesis
- Search-intent preservation
- Internal links
- Accessibility
- Performance
- QA
- Git commits
- Documentation
- Preview verification
- Deterministic builds

Claude must never invent owner facts.

When a factual field is unknown, record it as requiring owner review.

Do not guess from:

- Image filenames
- Visual appearance
- Existing questionable alt text
- Existing questionable captions
- Search keywords
- Nearby project text
- Similar photographs
- General flooring knowledge

Claude may convert confirmed owner facts into concise, natural, visitor-friendly and search-friendly wording, but it may not fabricate the facts used to produce that wording.

==================================================
4. BUSINESS STRATEGY
==================================================

The business is transitioning away from:

- Free in-home estimates for every inquiry
- Commodity bidding
- High-volume, low-value leads
- Unqualified site visits
- Competing mainly on price

The website must support:

- Free preliminary phone and photo assessment
- Paid professional project assessment
- Paid pre-purchase inspection
- Written documentation
- Complex floor-condition and damage analysis
- Better-qualified clients
- Lower lead volume with higher value
- Professional expertise as a paid deliverable
- High-value flooring projects
- Owner-operated credibility
- Strong project proof
- Clear boundaries between free contact and paid professional evaluation

This transition must not destroy existing search relevance for “estimate,” “refinishing,” “repair,” “installation,” “cleaning” or other established service searches.

The visitor journey should normally begin with:

1. Call
2. Text clear floor photographs
3. Email
4. Free phone and photo assessment

Paid on-site or written services should be presented when the problem, decision, property transaction or documentation requirement genuinely justifies them.

Do not make the website hostile to ordinary flooring clients.

Do not imply that every conversation or quote requires a paid inspection.

==================================================
5. APPROVED ASSESSMENT SERVICE ARCHITECTURE
==================================================

The new professional service page is:

Generated file:

floor-assessments-inspections.html

Approved public canonical URL:

https://www.sdhardwoods.com/floor-assessments-inspections

Do not use:

- /Consultation_Assessment
- /floor-assessments-inspections.html as the public canonical
- Capitalized variants
- Underscore variants
- Homepage anchors as substitutes
- Contact-page anchors as substitutes
- “This service moved” language
- “Floor assessments has moved” language
- Any legacy-migration explanation

This is a new standalone page.

Approved service structure:

1. Free Phone & Photo Assessment

2. $95 In-Home Project Assessment

3. $350 Pre-Purchase Verbal Inspection

4. $750 Pre-Purchase Inspection with Written Documentation

5. Complex Damage, Dispute & Insurance Analysis
   Starting at $1,500

Approved fee-credit language:

“Some or all of the inspection and report fee may be credited toward the approved flooring project under written agreement.”

Do not casually alter that sentence.

The assessment page must explain:

- Who each service is for
- What is examined
- What the client receives
- Whether findings are verbal or written
- Whether photographs, measurements or testing are included
- What decisions the service helps the client make
- What limitations apply
- Why paid professional evaluation has value

The page must eventually include short anonymized excerpts from professional floor-evaluation reports under labels such as:

- Existing Condition
- Probable Cause
- Feasibility or Limitations
- Recommended Next Step

Do not place multiple complete reports directly on the page.

A single optional anonymized sample PDF may later demonstrate report format and depth.

Do not invent report excerpts.

Do not imply automatic:

- Engineering services
- Laboratory services
- Legal opinions
- Real-estate appraisal
- Court testimony
- Deposition testimony
- Expert-witness services
- Litigation support
- Destructive testing
- Insurance coverage determinations

unless the owner explicitly defines and approves those services.

==================================================
6. APPROVED DESIGN AND FUNCTIONALITY
==================================================

The current redesign is substantially approved.

Preserve:

- San Diego Hardwoods primary logo
- Bona Certified Craftsman credibility badge
- Current masthead architecture
- Current desktop navigation
- Current mobile drawer
- Current mini-header behavior
- Current dark and light mode system
- Current typography direction
- Current overall visual identity
- Current service-card system
- Current gallery structure
- Current lightbox behavior
- Current project navigation
- Current assessment-page visual architecture
- Current responsive behavior
- Current page hierarchy unless a documented usability or SEO reason requires adjustment

Branding asset directory:

C:\FLOORING_SITE\SAN DIEGO HARDWOODS SITE REMAKE JULY 2026\assets\branding

Do not omit either the San Diego Hardwoods logo or the Bona Certified Craftsman badge from the intended brand system.

This project is no longer in open-ended design exploration.

Future milestones should improve:

- Accuracy
- Search preservation
- Conversion
- Accessibility
- Performance
- Structured data
- Media metadata
- Content clarity
- Technical stability
- Launch readiness

They should not repeatedly reinvent the visual design.

==================================================
7. CONTENT-PRESERVATION PRINCIPLE
==================================================

The live website contains long-form technical and project-specific material with search history and real expertise.

Preserve that substance.

Do not:

- Delete long technical explanations merely for cleaner design
- Replace expert content with generic marketing copy
- Convert detailed projects into thin captions
- Remove useful local references
- Remove species or process terminology that is factually accurate
- Remove service distinctions
- Remove repair limitations
- Remove installation detail
- Remove maintenance and finish-system detail
- Collapse multiple real projects into generic galleries
- Remove all older video content
- Rewrite every page into the same tone and structure
- Repeat the same keyword paragraph on every page
- turn the site into a generic flooring template

Allowed improvements include:

- Better hierarchy
- Better headings
- Better introductions
- Better summaries
- Better internal links
- Better calls to action
- Better mobile scanning
- Better accessibility
- Removal of exact duplication
- Correction of false claims
- Correction of wrong project facts
- Correction of malformed product names
- Correction of unsupported absolutes
- Better distinction among services
- Better visitor guidance

Search optimization must preserve useful meaning, not merely preserve old wording character for character.

==================================================
8. VOICE AND POSITIONING
==================================================

The writing should sound like:

- An experienced working flooring contractor
- Technically knowledgeable
- Direct
- Specific
- Honest about limitations
- Practical
- Owner operated
- Professional without sounding corporate
- Confident without making impossible promises

Avoid:

- Empty slogans
- Corporate filler
- Generic luxury language
- Exaggerated claims
- “Best in the world”
- “Perfect”
- “Flawless”
- “Guaranteed exact match”
- “Completely dust-free”
- “All damage can be repaired”
- “Every floor can be refinished”
- “Invisible repairs”
- Unsupported turnaround promises
- Keyword-stuffed local copy
- Artificially repeated city names

Use “dust-contained sanding” or similarly accurate wording rather than unsupported absolute dust claims.

==================================================
9. APPROVED CANONICAL URL MAP
==================================================

The following URL map is binding unless later owner-approved live testing proves a specific change is necessary.

1. Homepage

File:
index.html

Canonical:
https://www.sdhardwoods.com/

2. Deep Cleaning

File:
deep-cleaning-hardwood-floors-san-diego.html

Canonical:
https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html

3. Gallery 1

File:
recent_project_photo_gallery_1.html

Canonical:
https://www.sdhardwoods.com/recent_project_photo_gallery_1.html

4. Gallery 2

File:
recent_project_photo_gallery_2.html

Canonical:
https://www.sdhardwoods.com/recent_project_photo_gallery_2.html

5. Gallery 3

File:
recent_project_photo_gallery_3.html

Canonical:
https://www.sdhardwoods.com/recent_project_photo_gallery_3.html

Never use the incorrect path:

https://www.sdhardwoods.com/recent_project_gallery_3.html

6. Gallery 4

File:
recent_project_photo_gallery_4.html

Canonical:
https://www.sdhardwoods.com/recent_project_photo_gallery_4.html

7. Gallery 5

File:
recent_project_gallery_5.html

Canonical:
https://www.sdhardwoods.com/recent_project_gallery_5.html

Preserve the unusual established filename.

8. Solid Wood and Installation Gallery

File:
solid_wood_floor_photo_gallery.html

Canonical:
https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html

9. Refinishing Process Videos

File:
videos_of_refinishing_process.html

Canonical:
https://www.sdhardwoods.com/videos_of_refinishing_process.html

10. About

File:
about_us.html

Canonical:
https://www.sdhardwoods.com/about_us.html

11. Blog

File:
blog.html

Canonical:
https://www.sdhardwoods.com/blog.html

12. Contact

File:
contact_us.html

Canonical:
https://www.sdhardwoods.com/contact_us.html

13. Floor Assessments and Inspections

Generated file:
floor-assessments-inspections.html

Canonical:
https://www.sdhardwoods.com/floor-assessments-inspections

The 12 legacy pages retain established `.html` canonical URLs.

The new 13th assessment page intentionally uses an extensionless public canonical.

Do not globally convert legacy URLs to extensionless form.

Do not change these filenames for aesthetic reasons.

==================================================
10. SEARCH CONSOLE BASELINE
==================================================

A Search Console baseline was collected before launch changes.

Data range represented in the consolidated export:

Approximately 2025-08-27 through 2026-07-16.

Domain-property totals in the collected period:

- Approximately 1,049 clicks
- Approximately 143,234 impressions

The homepage is the dominant organic asset.

Known homepage variants collectively produced approximately:

- 862 clicks
- 132,190 impressions

The HTTPS www homepage produced approximately:

- 542 clicks
- 115,691 impressions

The HTTP www homepage produced approximately:

- 320 clicks
- 16,348 impressions

This proves that host, protocol and canonical behavior must be handled deliberately.

The site has had substantial ranking fragmentation involving:

- HTTP and HTTPS
- www and non-www
- `.html` and extensionless forms
- index.html
- Image URLs appearing in Web search

The collected Search Console data is sufficient for preservation planning.

Do not repeatedly request new historical exports unless a later audit identifies a specific unanswered question.

Search Console limitations must be remembered:

- Query exports may be capped
- Anonymous queries are withheld
- Query totals may not equal page totals
- Average position must not be summed
- Page variants may have different histories
- Impressions do not prove that a query should be targeted
- Irrelevant impressions should not dictate services

==================================================
11. PRIMARY SEARCH THEMES
==================================================

Actual important sitewide query concepts include:

- San Diego Hardwoods
- hardwood floor refinishing San Diego
- wood floor refinishing San Diego
- San Diego hardwood floor refinishing
- San Diego hardwood flooring
- hardwood floors San Diego
- wood floor refinishing
- floor refinishing near me
- hardwood floor repair San Diego
- hardwood floor installation San Diego
- wood floor installation San Diego
- hardwood floor cleaning service
- professional hardwood floor cleaning
- wood floor deep cleaning
- floor sanding San Diego
- wood floor sanding San Diego

These are search-intent concepts, not a phrase list to paste repeatedly.

Use natural English.

Do not keyword-stuff titles, headings, paragraphs, alt text or footer links.

Do not create irrelevant services based solely on accidental impressions.

==================================================
12. PAGE-INTENT OWNERSHIP
==================================================

Each page must have a defined purpose.

The homepage owns broad commercial intent involving:

- Hardwood-floor refinishing
- Wood-floor refinishing
- Hardwood flooring
- Restoration
- Repairs
- Installation
- Deep cleaning
- Dust-contained sanding
- General San Diego hardwood-flooring services
- Brand searches

The deep-cleaning page owns:

- Professional hardwood-floor cleaning
- Deep cleaning
- Maintenance recoating
- The difference between cleaning, recoating and full refinishing
- Situations where cleaning is insufficient

Gallery 1 owns:

- Before-and-after refinishing proof
- Restoration examples
- Repair examples
- Real San Diego project evidence

Gallery 2 owns:

- Installation
- Repair
- Refinishing
- Specialty finishes
- Project proof

Gallery 3 owns:

- Refinishing
- Sanding
- Repair
- Installation
- Additional local project proof

Gallery 4 owns:

- Restoration
- Deep cleaning
- Maintenance recoating
- Bamboo and hardwood project evidence where factually supported

Gallery 5 owns:

- Refinishing
- Sanding
- Repair
- Installation
- Additional project evidence

The Solid Wood Gallery owns:

- Solid hardwood installation
- Unfinished engineered installation
- Nail-down installation
- Glue-down installation
- Installation over concrete
- Acclimation
- Sanding and site finishing
- Installation expertise

The Videos page owns:

- Real refinishing-process video proof
- Dust-contained sanding video
- Repairs
- Staining
- Installation
- Restoration
- Educational process footage

The About page owns:

- Company history
- Owner-operated trust
- Credentials
- Experience
- Licensing
- Certification
- Business identity

The Blog owns:

- Informational flooring content
- Technical education
- Floor care
- Refinishing decisions
- Repair decisions
- Installation information
- Finish systems
- Maintenance

The Contact page owns:

- Call
- Text photographs
- Email
- Free preliminary phone/photo assessment
- Lead intake
- Natural referral to the assessment page

The Assessment page owns:

- Hardwood-floor assessment
- Floor inspection
- Professional consultation
- Pre-purchase inspection
- Written floor-condition documentation
- Damage analysis
- Repairability evaluation
- Refinishing feasibility
- Insurance or dispute-related floor-condition analysis

The assessment page must not replace the homepage as the primary destination for generic refinishing, repair, installation or cleaning searches.

==================================================
13. CURRENT TECHNICAL-SEO FOUNDATION
==================================================

Milestone 2.4 was reported implemented and validated.

The next session must confirm the final Milestone 2.4 Git commit and record its hash in the continuity documentation.

Expected completed Milestone 2.4 state:

- Exactly one standard viewport tag on all 13 pages
- Exactly one canonical on every page
- Gallery 3 canonical corrected
- Homepage title and description corrected
- Five previously missing descriptions added
- Legacy canonical map aligned
- Internal navigation aligned with canonical `.html` URLs
- Separate call, text and email actions
- No `tel:` link labeled as a text action
- Obsolete Universal Analytics removed
- GA4 left unimplemented pending the confirmed Measurement ID
- Deterministic sitemap generator
- sitemap.xml containing exactly 13 canonical URLs
- robots.txt generated with allow-all crawling and sitemap pointer
- No accidental noindex
- Deterministic double-build validation
- Strict JSON-LD parsing
- Local internal-link validation

Do not redo this work without evidence of a regression.

Verify it at milestone boundaries through automated checks rather than repeatedly rebuilding the entire strategy.

==================================================
14. ROBOTS AND SITEMAP POLICY
==================================================

Production robots.txt should remain:

User-agent: *
Allow: /

Sitemap: https://www.sdhardwoods.com/sitemap.xml

Do not add:

- Crawl-delay
- noindex
- Unsupported directives
- CSS blocking
- JavaScript blocking
- Image blocking
- Canonical-page blocking
- Private credentials
- Development-only paths

The sitemap must contain exactly the approved canonical production URLs.

Do not include:

- HTTP URLs
- Non-www URLs
- Legacy extensionless duplicates
- Cloudflare preview URLs
- Image URLs
- Incorrect consultation URLs
- A `.html` canonical for the new assessment page
- Invented lastmod dates

If accurate last-modified dates cannot be generated, omit them.

==================================================
15. CONTACT AND CTA SYSTEM
==================================================

Approved actions:

Call:

Label:
Call 858-699-0072

URI:
tel:+18586990072

Text:

Label:
Text Floor Photos

URI:
sms:+18586990072

Email:

Label:
Email San Diego Hardwoods

URI:
mailto:sandiegohardwoods@gmail.com

Do not label a `tel:` URI as “Call or Text.”

Primary CTA hierarchy should normally be:

1. Call
2. Text Floor Photos
3. Email
4. View the relevant service or assessment information

CTA wording should match page purpose.

Examples:

Homepage:
- Call About Your Floor
- Text Floor Photos
- View Floor Assessments

Deep Cleaning:
- Ask Whether Cleaning, Recoating or Refinishing Fits Your Floor

Installation:
- Discuss Your Installation Project

Galleries:
- Text Photos of Your Floor
- View the Relevant Service
- Call About a Similar Project

Assessment page:
- Start with a Free Phone & Photo Assessment
- Schedule the appropriate professional service

Do not place the same large generic promotional block after every project.

Do not make paid services feel like hidden fees.

Explain the outcome and value.

==================================================
16. MEDIA FACT SYSTEM
==================================================

The project must have a permanent structured system for every image and video.

The same asset may appear in multiple places.

The system must distinguish:

- The underlying media asset
- Each placement of that asset

Recommended source structure:

build/data/media/assets.json

build/data/media/placements/index.json

build/data/media/placements/deep-cleaning-hardwood-floors-san-diego.json

build/data/media/placements/recent_project_photo_gallery_1.json

build/data/media/placements/recent_project_photo_gallery_2.json

build/data/media/placements/recent_project_photo_gallery_3.json

build/data/media/placements/recent_project_photo_gallery_4.json

build/data/media/placements/recent_project_gallery_5.json

build/data/media/placements/solid_wood_floor_photo_gallery.json

build/data/media/placements/videos_of_refinishing_process.json

build/data/media/placements/about_us.json

build/data/media/placements/blog.json

build/data/media/placements/contact_us.json

build/data/media/placements/floor-assessments-inspections.json

Every asset should receive a stable asset ID.

Every placement should receive a stable placement ID.

Suggested stable IDs:

- HOME-IMG-001
- DEEP-IMG-001
- G1-P01-BEFORE
- G1-P01-AFTER
- VIDEOS-VID-001
- ASSESS-IMG-001

The owner should be able to identify media by a simple stable ID rather than dictating long filenames or URLs.

Asset records should support:

- asset_id
- media_type
- filename
- source path
- public URL
- full-size URL
- thumbnail URL
- width
- height
- duplicate relationships
- verification status
- do-not-infer flag

Placement records should support:

- placement_id
- asset_id
- page
- project or section
- order
- current heading
- current caption
- current alt text
- current link
- visible context
- owner facts
- proposed heading
- proposed caption
- proposed alt text
- approval status
- SEO context
- accessibility context
- notes
- last verified date

Owner facts should support:

- Project name
- Property location
- City or neighborhood
- Floor species
- Floor construction
- Existing condition
- Damage or problem
- Probable cause when confirmed
- Stage shown
- Work performed
- Stain or color
- Finish system
- Equipment or process
- Before/after status
- Limitations
- Additional notes

Unconfirmed records must be marked:

needs_owner_review

Do not publish generated factual metadata automatically when facts remain unconfirmed.

==================================================
17. CONFIRMED TRICIA WALNUT FACT
==================================================

The following filenames belong to one real project:

- TRICIA WALNUT102.jpg
- TRICIA WALNUT110.jpg
- TRICIA WALNUT54.jpg
- TRICIA WALNUT23.jpg

Confirmed owner facts:

- All four images are from the same walnut-floor refinishing project.
- The project was at Bing Crosby Ranch in San Diego.
- They show different stages or angles of the same project.
- They are not separate bamboo, parquet, maple, Rancho Santa Fe or La Jolla projects.

Remove unrelated false identities attached to these images.

The exact stage or angle of each image remains unconfirmed.

Do not automatically label individual images as:

- Before
- After
- Sanding
- Bare wood
- Finish application

until confirmed or visually indisputable.

Provisional restrained wording may identify:

- Walnut floor refinishing project
- Bing Crosby Ranch
- San Diego
- Alternate angle or project view

Do not repeat the identical keyword-rich alt text four times.

==================================================
18. IMAGE ALT-TEXT POLICY
==================================================

Final alt text must:

- Describe the image’s relevant content
- Use confirmed facts
- Be concise
- Be useful to a screen-reader user
- Distinguish before and after when confirmed
- Distinguish stages and angles when known
- Avoid repeating the complete caption
- Avoid business slogans
- Avoid keyword lists
- Avoid forcing “San Diego” into every image
- Avoid “image of” or “photo of” unless needed
- Avoid unsupported species
- Avoid unsupported finish claims
- Avoid unsupported locations
- Avoid invented damage causes
- Avoid invented project stages

Decorative images may use empty alt text when appropriate.

The San Diego Hardwoods logo should have appropriate brand alt text.

The Bona Certified Craftsman badge should have appropriate certification alt text when it communicates credentials.

==================================================
19. OWNER MEDIA-REVIEW WORKFLOW
==================================================

Create and maintain:

docs/media-review/README.md

Create a page-specific owner-review document for every page.

Each review entry should show:

- Stable placement ID
- Thumbnail or clickable reference
- Filename
- Page and position
- Current heading
- Current caption
- Current alt text
- Current full-size link
- Verification status
- Existing owner facts
- Missing facts
- Detected conflicts
- Duplicate uses

A local static review index may be created at:

docs/media-review/index.html

It must remain:

- Static
- Read only
- Local
- Framework free
- Database free
- Easy to scan
- Organized by page
- Generated from structured data

The process is:

1. Claude inventories assets and placements.
2. Owner identifies factual information.
3. Facts are entered into structured data.
4. Claude drafts natural headings, captions and alt text.
5. Meaningful wording is reviewed.
6. Approved content is injected through the generator.
7. Validators ensure no placement is missed.

Do not interrupt high-priority launch work with random one-image questions.

Media review should occur in organized page batches.

==================================================
20. VIDEO SYSTEM
==================================================

Inventory every visible video and every VideoObject.

Records should support:

- Stable video placement ID
- YouTube video ID
- Visible title
- Current description
- Thumbnail
- Upload date
- Duration
- Content URL
- Embed URL
- Project facts
- Owner-confirmed summary
- Schema status
- Verification status

Validate:

- Visible video matches the video ID
- Title matches the intended video
- Thumbnail is valid
- Description is not malformed
- Upload date is supported
- Duration is supported
- Content URL and embed URL are correct
- VideoObject corresponds to visible content

Flag:

- Duplicate titles
- Titles starting with “Title:”
- Obvious spelling errors
- “Sold Cherry” or other possible malformed species names
- Truncated descriptions
- Repeated channel boilerplate
- Missing durations
- Unverified dates
- Schema-only videos
- Visible videos missing schema

Do not invent video details.

The owner must confirm uncertain project facts.

The official YouTube channel URL must be confirmed before final sameAs and channel references are standardized.

==================================================
21. STRUCTURED DATA POLICY
==================================================

Structured data must describe visible, factual content.

Appropriate entity types may include:

- Organization or LocalBusiness
- WebSite
- WebPage
- Service
- BreadcrumbList
- FAQPage
- Blog
- CollectionPage
- Article
- VideoObject
- ImageObject where justified

Do not add schema merely to maximize the number of schema types.

Requirements:

- Every JSON-LD block parses as strict JSON
- Canonical URLs match visible page canonicals
- WebPage IDs are consistent
- Breadcrumb URLs are correct
- Service descriptions match visible services
- FAQ schema exactly matches visible FAQs
- VideoObject records match visible videos
- Business details remain consistent
- Phone and email remain consistent
- License and certification claims remain accurate
- sameAs URLs are confirmed
- Address is not invented
- Hours are not invented
- Reviews are not invented
- Ratings are not invented
- Awards are not invented
- Price ranges are not invented
- Expert-witness claims are not invented

Do not create fake local relevance through unsupported addresses or city claims.

==================================================
22. LOCAL SEO POLICY
==================================================

The site should establish genuine San Diego County relevance through:

- Accurate business identity
- Accurate service area
- Real project locations
- Real local project examples
- Accurate NAP
- Google Business Profile consistency
- Local internal context
- Real client reviews where legally and factually available
- Relevant local citations
- Bona and contractor credentials
- Useful local flooring expertise

Do not create dozens of thin doorway pages for every neighborhood.

Do not insert long city lists into every page.

City and neighborhood references should be based on:

- Actual service areas
- Actual projects
- Real logistical relevance
- Useful visitor context

==================================================
23. ANALYTICS AND CONVERSION MEASUREMENT
==================================================

Obsolete Universal Analytics must remain removed.

Do not restore:

- UA-20793161-1
- _gaq
- ga.js

The real GA4 Measurement ID remains required from the owner.

Do not invent a GA4 ID.

After the confirmed ID is provided, implement restrained event tracking for:

- Call clicks
- SMS clicks
- Email clicks
- Assessment-page CTA clicks
- Pricing-card interactions where useful
- Contact-form submission if a form exists
- Report-example or sample-PDF downloads
- Important outbound video/channel interactions

Use understandable event names.

Do not create invasive tracking.

Avoid counting preview traffic as production traffic where practical.

Analytics must answer business questions such as:

- Which pages produce calls?
- Which pages produce texts?
- Which pages produce assessment inquiries?
- Which projects attract qualified clients?
- Which assessment tier generates interest?
- Which search traffic creates profitable work?

Page views alone are not the primary profitability metric.

==================================================
24. PERFORMANCE POLICY
==================================================

The new site must be measurably faster and more stable than the legacy site where feasible.

Optimize:

- Oversized images
- Image dimensions
- Image aspect ratios
- Layout stability
- Lazy loading
- Below-the-fold media
- Thumbnail/full-size separation
- Video loading
- YouTube embeds
- Duplicate CSS
- Duplicate JavaScript
- Render-blocking resources
- Font loading
- Unused assets
- Cache-friendly file organization

Do not visibly damage project photography through excessive compression.

Do not replace original full-size proof images with unusably small images.

Use:

- Width and height attributes
- Responsive image behavior
- Lazy loading below the fold
- Appropriate eager loading for critical visual content
- Stable aspect-ratio containers
- Lightweight video loading where compatible

Test:

- Core Web Vitals
- Mobile performance
- Desktop performance
- Layout shift
- Interaction responsiveness
- Largest Contentful Paint
- Broken assets

Do not optimize for a laboratory score at the expense of visitor usefulness.

==================================================
25. ACCESSIBILITY POLICY
==================================================

Target strong practical WCAG AA accessibility.

Validate:

- One meaningful H1 per page
- Logical heading order
- Keyboard navigation
- Visible focus
- Mobile-drawer keyboard behavior
- Lightbox keyboard behavior
- Escape behavior
- Theme-toggle labeling
- Button names
- Link purpose
- Color contrast
- Dark-mode contrast
- Light-mode contrast
- Text scaling
- Responsive zoom behavior
- Meaningful alt text
- Decorative empty alt text
- Form labels
- Error messaging
- Landmark structure
- Skip navigation where appropriate
- Reduced-motion respect where appropriate

Do not add inaccessible custom controls merely for visual effect.

==================================================
26. INTERNAL-LINK POLICY
==================================================

Internal links should:

- Use approved canonical destinations
- Use natural descriptive anchor text
- Help visitors move from education to proof to contact
- Reinforce page intent
- Avoid keyword stuffing
- Avoid generic “click here” where more descriptive text is practical
- Avoid repeated sitewide blocks of keyword links
- Avoid broken anchors
- Avoid extensionless legacy duplicates

Expected relationships:

Homepage links to:

- Deep cleaning
- Installation
- Galleries
- Videos
- Assessments
- About
- Contact

Deep Cleaning links to:

- General refinishing when cleaning is insufficient
- Relevant project proof
- Contact

Galleries link to:

- Relevant service pages
- Adjacent galleries
- Contact
- Text Floor Photos

Solid Wood Gallery links to:

- Installation/refinishing context
- Relevant galleries
- Contact

Videos link to:

- Relevant service pages
- Project galleries
- Official YouTube channel
- Contact

Assessment page links to:

- Contact
- Text Floor Photos
- Relevant technical/project proof
- Free phone/photo starting point

Contact links to:

- Assessment page
- Relevant starting actions

The Contact page should not duplicate the entire assessment pricing page.

==================================================
27. CLAIMS AND FACTUAL SAFETY
==================================================

Review and remove or qualify unsupported claims involving:

- Flawless results
- Exact color matching
- Invisible repairs
- Total dust elimination
- Universal repairability
- Universal refinishing feasibility
- Guaranteed project duration
- Guaranteed drying or curing
- Guaranteed finish performance
- Guaranteed insurance outcomes
- Legal conclusions
- Engineering conclusions
- Laboratory conclusions
- Perfect completion percentages
- Unsupported product superiority
- Unsupported health or environmental claims

Product and process names must be accurate.

Examples may include:

- Bona Traffic HD
- Bona Traffic Naturale
- Bona Traffic HD Raw
- Bona Mega
- Bona Mega One
- Bona Certified Craftsman
- Dust containment

Do not fabricate product relationships or certifications.

==================================================
28. PAGE-SPECIFIC CONTENT COMPLETION
==================================================

Homepage:

- Preserve broad service intent
- Preserve real project proof
- Strengthen service clarity
- Keep assessment as a specialized secondary pathway
- Correct media descriptions through the structured review process
- Maintain strong calls and texts
- Avoid turning the homepage into a video page or assessment page

Deep Cleaning:

- Explain cleaning versus recoating versus refinishing
- Preserve local search relevance
- Avoid implying cleaning fixes finish loss or exposed wood
- Use accurate product and process descriptions

Gallery pages:

- Preserve all real projects
- Preserve useful technical explanations
- Use concise project titles plus readable detailed summaries
- Correct factual identities only from owner-confirmed data
- Maintain before/after clarity
- Improve internal links without promotional clutter

Solid Wood Gallery:

- Preserve technical installation content
- Distinguish solid and engineered flooring
- Preserve nail-down and glue-down concepts
- Preserve acclimation, concrete and site-finishing knowledge
- Avoid unsupported absolutes

Videos:

- Preserve the archive
- Validate media identity
- Improve loading
- Correct malformed metadata
- Preserve process relevance

About:

- Preserve owner-operated identity
- Preserve history and credentials
- Avoid sounding like a large anonymous organization
- Confirm all business facts

Blog:

- Preserve useful informational content
- Improve structure and internal links
- Avoid thin mass-generated articles
- Avoid publishing content merely for keyword volume

Contact:

- Maintain low-friction contact
- Explain free preliminary phone/photo assessment
- Clarify when paid evaluation is appropriate
- Use separate call, SMS and email actions

Assessment:

- Complete value explanation
- Add report excerpts after owner supplies them
- Add visit preparation and delivery expectations after confirmation
- Keep tier distinctions clear
- Preserve careful limitations
- Emphasize decisions and deliverables rather than merely time spent

==================================================
29. REQUIRED CONTINUITY DOCUMENTS
==================================================

Maintain:

docs/PROJECT_OPERATING_MANUAL.md

This governing document.

Maintain:

docs/NEXT_SESSION.md

It must contain:

- Current branch
- Current commit
- Last completed milestone
- What changed
- What remains
- Known blockers
- Exact next milestone
- Files the next session must read
- Commands the next session should run
- Explicit things not to redo

Maintain:

docs/2026-07-qa-report.md

or the latest dated successor.

Maintain:

docs/PROJECT_DECISIONS.md

Create it if absent.

Record binding decisions such as:

- Canonical map
- New assessment URL
- Business positioning
- Pricing architecture
- Fee-credit sentence
- Design-lock decisions
- Media-fact policy
- Analytics blocker
- Address blocker
- YouTube blocker
- Redirect decisions
- Launch decisions

Maintain:

docs/seo/search-console-content-preservation-map.md

Maintain:

docs/seo/2026-07-content-alignment-changes.md

Maintain:

docs/media-review/README.md

Do not spread critical decisions across dozens of obscure files.

==================================================
30. SESSION-START PROTOCOL
==================================================

At the start of every new Claude session:

1. Confirm the repository directory.

2. Confirm branch:

redesign

3. Run:

git status

4. Fetch:

git fetch origin redesign

5. Report:

- Local HEAD
- origin/redesign HEAD
- Clean or dirty working tree
- Ahead/behind status

6. Read:

- docs/PROJECT_OPERATING_MANUAL.md
- docs/NEXT_SESSION.md
- docs/PROJECT_DECISIONS.md
- Latest QA report
- Latest milestone commit
- Relevant milestone-specific files

7. Do not repeat completed audits unless:

- A validator fails
- A regression appears
- The current milestone depends on rechecking a specific item
- Documentation and repository state conflict

8. If unexplained uncommitted work exists:

- Do not reset
- Do not discard
- Do not overwrite
- Report it and stop

9. If the repository is clean and synchronized:

Proceed with the assigned milestone.

==================================================
31. MILESTONE-SIZING POLICY
==================================================

Milestones should maximize useful Fable 5 work without becoming uncontrolled.

Each milestone should be:

- Large enough to produce meaningful progress
- Coherent
- Generator first
- Fully testable
- Fully documentable
- Committable as one logical unit

Avoid:

- One-line micro-milestones
- Repeated status-only sessions
- Re-running completed work without cause
- Broad speculative research
- Unrelated tooling
- Side projects
- New architecture experiments
- Unbounded redesign
- “While I am here” changes outside scope

A strong milestone may combine related work such as:

- Content alignment plus internal links
- Media inventory plus owner-review generation
- Schema alignment plus verified business data
- Performance plus accessibility validation
- Prelaunch URL verification plus deployment packaging

Do not combine unrelated high-risk operations merely to consume tokens.

==================================================
32. IMPLEMENTATION PROTOCOL
==================================================

For every milestone:

1. Read the relevant source architecture.

2. Identify the actual source of truth.

3. Make permanent changes only in source and generator files.

4. Preserve approved design and functionality unless the milestone authorizes a change.

5. Build using:

python build/scripts/build_all.py

6. Confirm deterministic output where appropriate.

7. Run milestone-specific validators.

8. Test through a local HTTP server, not file://.

9. Test the Cloudflare redesign preview after local QA passes.

10. Update continuity documents.

11. Create one clear milestone commit.

12. Push only to:

origin/redesign

13. Do not merge to master.

14. Stop after the requested milestone.

Do not begin the next milestone automatically unless the owner explicitly includes it in the same prompt.

==================================================
33. STANDARD QA GATE
==================================================

Every significant milestone must validate relevant portions of:

Build:

- Build completes
- Expected files exist
- Deterministic output
- No source/output drift

HTML:

- Valid structure
- One title
- One H1
- One viewport
- One canonical
- No accidental noindex

Links:

- No broken internal links
- No wrong legacy variants
- No incorrect consultation URLs
- No broken gallery navigation
- No broken asset paths
- Correct call, SMS and email schemes

Structured data:

- Strict JSON
- Correct canonicals
- Visible-content consistency
- Correct video references
- Correct FAQ references
- No invented facts

Sitemap and robots:

- Exactly 13 canonical URLs
- Correct robots pointer
- No duplicate variants
- No preview URLs
- No blocked pages

Responsive behavior:

- Desktop
- Tablet
- Mobile
- No horizontal overflow
- Drawer works
- Mini-header works
- CTA controls work

Themes:

- Dark default
- Forced light
- Theme persistence
- Correct contrast

Media:

- Images load
- Lightbox works
- Videos load
- Thumbnails match
- No missing assets
- No accidental project removal

Accessibility:

- Keyboard use
- Focus
- Escape behavior
- Alt handling
- Heading structure
- Labeling

Content:

- No long-form sections disappear
- No project disappears
- No unsupported facts are introduced
- Search-intent ownership remains intact

==================================================
34. GIT AND COMMIT POLICY
==================================================

Each completed milestone should produce one clear commit unless a documented technical reason requires more than one.

Commit messages should identify the milestone and result.

Example:

Milestone 2.5: preserve search intent and add structured media facts

After committing:

- Push only to origin/redesign
- Confirm the pushed hash
- Confirm the working tree is clean
- Confirm preview deployment corresponds to the intended commit
- Record the hash in NEXT_SESSION

Do not:

- Force push
- Rewrite shared history
- Delete unexplained work
- Merge master
- Commit credentials
- Commit private personal data
- Commit generated junk or temporary test artifacts

==================================================
35. REMAINING MASTER MILESTONE ROADMAP
==================================================

The numbering may be adjusted only if documentation already establishes a different number, but the sequence and workstreams should remain.

NEXT MAJOR MILESTONE:

Search Console content preservation and structured media-fact system.

Objectives:

- Natural page-specific query alignment
- Search-intent ownership
- Internal-link improvements
- Page-intent data
- Media asset inventory
- Placement inventory
- Owner-review files
- Video inventory
- Confirmed Tricia walnut correction
- No guessed image facts

FOLLOWING MILESTONE:

Assessment-page content completion and consultation-card optimization.

Objectives:

- Report excerpts
- Visit expectations
- Report-delivery expectations
- Preparation and access
- Tier differentiation
- Written deliverables
- Outcome-based value
- Pricing clarity
- Credit language
- Limitations
- Conversion review

FOLLOWING MILESTONE:

Page-by-page owner media review and approved metadata injection.

Objectives:

- Correct project identities
- Correct species
- Correct locations
- Correct before/after stages
- Correct captions
- Correct alt text
- Correct video metadata
- Validate all placements

FOLLOWING MILESTONE:

Structured data, local-business data and analytics completion.

Objectives:

- Confirm NAP
- Confirm official YouTube
- Confirm GA4
- Complete schema
- Validate service entities
- Add conversion events
- Verify visible/schema consistency

FOLLOWING MILESTONE:

Performance, accessibility and cross-browser hardening.

Objectives:

- Image optimization
- Video optimization
- Core Web Vitals
- Keyboard behavior
- Contrast
- Screen-reader semantics
- Browser coverage
- Mobile stability
- Turbify-compatible output

FOLLOWING MILESTONE:

SEO preservation and prelaunch validation.

Objectives:

Compare every redesign page against its live equivalent for:

- Exact URL
- Title
- Meta description
- H1
- Headings
- Important wording
- Search intent
- Internal links
- Images
- Alt text
- Structured data
- Calls to action
- Content preservation
- Improvements

Create:

- Final URL matrix
- Redirect requirements
- Canonical matrix
- Production sitemap
- Production robots
- Backup plan
- Upload package
- Rollback plan
- Production verification checklist

FOLLOWING MILESTONE:

Owner-controlled launch.

Claude prepares:

- Final build
- Checksums
- Upload map
- Deployment checklist
- Verification checklist
- Rollback files
- Post-launch checks

The owner performs or controls production publishing through the available Turbify workflow.

Claude must not assume production upload access.

FOLLOWING MILESTONE:

Post-launch monitoring.

Review at:

- Immediate launch
- 24 hours
- 7 days
- 30 days
- 90 days

Monitor:

- Indexing
- Canonical selection
- 404s
- Redirects
- Missing assets
- Search clicks
- Search impressions
- CTR
- Ranking queries
- Calls
- Texts
- Assessment inquiries
- Qualified leads
- Paid consultations
- Revenue quality

==================================================
36. PRODUCTION URL AND REDIRECT POLICY
==================================================

Before launch:

- Preserve every valuable legacy URL
- Test all legacy variants
- Document server behavior
- Avoid redirect chains
- Avoid loops
- Avoid mass URL changes
- Avoid deleting pages with ranking history
- Verify HTTP behavior
- Verify HTTPS behavior
- Verify www behavior
- Verify non-www behavior
- Verify index.html behavior
- Verify extensionless behavior
- Verify `.html` behavior

Where server-level redirect control is limited, document the exact available Turbify behavior and use the safest achievable combination of:

- Existing redirect behavior
- Correct canonical
- Consistent internal links
- Sitemap preference
- Content parity

Do not invent unsupported server functionality.

==================================================
37. LAUNCH-READINESS DEFINITION
==================================================

The redesign is ready for launch only when:

- All 13 pages build successfully
- All canonical URLs are correct
- Sitemap is complete
- robots.txt is correct
- No accidental noindex exists
- Internal links resolve
- Important legacy content is preserved
- Search-intent ownership is documented
- Major metadata is accurate
- Assessment page is complete enough for real clients
- CTAs work
- Contact paths work
- Media facts are sufficiently accurate
- Critical image descriptions are not false
- Structured data is valid
- Business facts are confirmed
- GA4 is implemented or explicitly deferred with a documented immediate follow-up
- Performance is acceptable
- Accessibility is acceptable
- Mobile behavior is acceptable
- Browser QA passes
- Production files are backed up
- Rollback is possible
- Production verification plan exists
- Owner approves the final preview

A visually attractive preview alone is not launch readiness.

==================================================
38. SUCCESS METRICS
==================================================

The goal is not merely to produce a newer-looking website.

The redesign should improve:

Design:

- Clarity
- Credibility
- Mobile usability
- Visual hierarchy
- Professional appearance
- Project presentation

Function:

- Navigation
- Calls
- Texting
- Email
- Galleries
- Lightbox
- Video access
- Theme behavior
- Contact flow

SEO:

- URL consolidation
- Crawlability
- Indexing
- Content relevance
- Internal links
- Structured data
- Local relevance
- Image understanding
- Video understanding

Click-through rate:

- Accurate titles
- Accurate descriptions
- Clear brand identity
- Strong service alignment
- Better search-result expectations

Conversion:

- Low-friction phone and photo start
- Clear service choices
- Better project proof
- Professional assessment value
- Fewer unqualified visits
- More high-value inquiries

Profitability:

- Higher-quality leads
- More paid evaluations
- Better project selection
- Reduced unpaid travel
- Better expectation setting
- Higher trust
- Better close rate
- Better average project value

No one may claim proven ranking or profitability improvement until post-launch measurement confirms it.

==================================================
39. POST-LAUNCH GROWTH
==================================================

After launch stability is proven, future growth may include:

- Search Console-driven content improvement
- Better report examples
- Stronger case studies
- Google Business Profile optimization
- Review acquisition
- Local citation consistency
- Relevant contractor, design and real-estate relationships
- Authoritative links
- Useful technical articles
- Additional high-value consultation content
- Better conversion testing
- Better service qualification
- Seasonal maintenance content
- Additional project galleries only when facts and media are strong

Do not mass-produce thin AI articles.

Do not build doorway pages.

Do not chase traffic unrelated to profitable services.

==================================================
40. STOP CONDITIONS
==================================================

Stop and report rather than proceeding when:

- Branch is not redesign
- Working tree contains unexplained changes
- A requested change conflicts with this manual
- A factual claim cannot be verified
- A URL decision conflicts with the approved map
- A build fails
- A validator fails
- Structured data becomes invalid
- Required media is missing
- A change would remove substantial content
- A change would alter approved design outside scope
- A change requires production access Claude does not possess
- A secret or credential is required
- The owner must make a business decision
- An unresolved contradiction exists in documentation
- Master would be affected
- A milestone would drift into an unrelated workstream

Do not hide failures.

Do not claim completion when required QA has not run.

Do not consume an entire session repeatedly investigating a non-blocking issue. Report it clearly and continue with the remaining in-scope work when safe.

==================================================
41. REQUIRED FINAL REPORT FOR EVERY MILESTONE
==================================================

At the end of each milestone, provide:

- Milestone name
- Starting commit
- Ending commit
- Branch
- Files changed
- Source/generator changes
- Generated-output changes
- Content changes
- SEO changes
- Media changes
- Schema changes
- QA commands
- QA results
- Browser-test results
- Preview verification
- Remaining owner decisions
- Remaining blockers
- Documentation updated
- Commit hash
- Push confirmation
- Working-tree status
- Confirmation that master was untouched
- Confirmation that the live production site was untouched
- Exact recommended next milestone

Do not bury failures or unresolved items inside long prose.

==================================================
42. CURRENT STATE UPDATE REQUIREMENT
==================================================

Immediately after this operating manual is first added to the repository:

1. Record the final Milestone 2.4 commit hash.

2. Update docs/NEXT_SESSION.md.

3. Update docs/PROJECT_DECISIONS.md.

4. Record the current 13-page canonical map.

5. Record that the next major milestone is:

Search Console content preservation, internal-link alignment and structured media-fact system.

6. Record current blockers:

- GA4 Measurement ID
- Public address decision
- Official YouTube URL
- Image and video owner facts
- Assessment visit duration
- Assessment report-delivery range
- Anonymized report excerpts
- Any unresolved service limitations

7. Do not begin implementation work beyond the assigned milestone.

==================================================
43. FINAL GOVERNING PRINCIPLE
==================================================

Every change must answer at least one of these questions:

- Does it preserve or improve existing search value?
- Does it help visitors understand the business?
- Does it help visitors select the right service?
- Does it improve trust?
- Does it improve conversion?
- Does it improve profitability?
- Does it improve accessibility?
- Does it improve performance?
- Does it improve technical reliability?
- Does it make future factual maintenance safer?
- Does it reduce launch risk?

If a proposed task does not materially support one of those outcomes, it is probably a distraction and should not be added to the milestone.

The objective is a controlled, technically strong, content-rich, owner-authentic, highly credible San Diego hardwood-flooring website that preserves existing rankings while building a more profitable professional-service business.

END OF PERMANENT PROJECT OPERATING MANUAL