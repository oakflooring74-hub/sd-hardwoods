# CLAUDE.md — San Diego Hardwoods

## Purpose

This repository rebuilds the San Diego Hardwoods website with a deterministic static-site generator.

Goals:
- Preserve established SEO, URLs, search intent, and valuable technical content.
- Keep business and flooring facts accurate.
- Improve usability, accessibility, performance, maintainability, and conversion.
- Maintain one unified generator system.
- Improve the established design; do not restart open-ended design exploration.

## Read order

For normal work, read:
1. `CLAUDE.md`
2. `docs/NEXT_SESSION.md`
3. `docs/PROJECT_QUALITY_BAR.md` — the site's final-goal definition and the standing rule to
   question any task that leaves out pages or doesn't clearly unify/progress toward that goal.
   Mandatory for any site-wide or multi-page task (schema, meta, titles, CTAs, navigation).
4. Only the files and reference documents relevant to the assigned task

Use when relevant:
- `build/README.md` — architecture, build commands, page map, deployment
- `docs/PROJECT_OPERATING_MANUAL.md` — detailed permanent policy
- `docs/2026-07-milestone-2.4-technical-seo.md` — canonical and technical SEO rules
- `docs/2026-07-seo-heading-audit.md` — evidence-based SEO policy
- Dated QA and milestone reports — historical evidence

Do not load the entire manual or all historical reports for routine work. Verify current facts because older reports may be superseded. Clear owner instructions for the current task take priority.

## Start of session

Before editing:
- Confirm the working directory.
- Run `git status --short`, `git branch --show-current`, and inspect recent relevant commits.
- Read `docs/NEXT_SESSION.md`.
- Identify and preserve pre-existing uncommitted work.
- Inspect only the relevant source and architecture.
- For broad or high-risk work, state a short plan before implementation.
- Ask when owner facts, scope, or production intent are ambiguous.

Keep sessions focused and milestone-sized. Do not drift into adjacent cleanup, redesign, or refactoring.

## Architecture

Project root:
`C:\FLOORING_SITE\SAN DIEGO HARDWOODS SITE REMAKE JULY 2026`

Full build:
`python build/scripts/build_all.py`

`build/` is the permanent source and generator system.

Permanent site changes belong in appropriate generator sources such as:
- `build/chrome/`
- `build/scripts/`
- `build/data/`

Repo-root HTML files, `sitemap.xml`, and `robots.txt` are generated output. Never permanently hand-edit them; change the generator and rebuild.

`build/raw-source/` is a frozen legacy reference. Do not casually edit it.
`build/archive/` is historical and must not be used as active implementation source.

Do not add a CMS, database, framework, backend, external SaaS dependency, or unnecessary package without explicit approval.

## Factual authority

The owner is the authority for:
- Business identity, credentials, prices, policies, and service boundaries
- Flooring species, construction, damage, causes, limitations, and work performed
- Project locations, products, stains, colors, finishes, equipment, testing, and deliverables
- Before/after status, project sequence, reports, and legal or expert-service boundaries

Claude may organize and improve confirmed facts but must not invent facts from images, filenames, nearby text, keywords, assumptions, or general flooring knowledge.

Flag unknown facts for owner confirmation. Never invent or placeholder analytics IDs, addresses, credentials, prices, services, testing capabilities, report excerpts, or project details.

## SEO and URLs

Preserve established search intent, useful technical content, and historically valuable URLs.

Do not make broad SEO rewrites from generic best practices alone. Use Search Console evidence and the documented page-intent strategy before materially changing titles, meta descriptions, headings, body content, internal links, canonicals, schema, or image metadata.

All 13 pages keep `.html` canonical URLs -- the 12 legacy pages, and (owner
instruction, 2026-07-23) the assessment page too:
`https://www.sdhardwoods.com/floor-assessments-inspections.html`

Do not globally convert legacy URLs to extensionless form, rename established URLs for aesthetics, or create redirects without an approved milestone.

Consult the technical SEO report before changing canonical or URL behavior.

## Design and content

Preserve the established logo, Bona badge, masthead, navigation, mobile drawer, mini-header, theme system, service cards, galleries, lightbox, assessment-page architecture, and responsive behavior unless the assigned task justifies a change.

Preserve valuable technical explanations, real project details, service distinctions, repair limitations, installation detail, and finish-system information.

Do not replace expert content with generic marketing copy.

Existing accurate image alt text is a protected ranking asset. Image-alt milestones must
preserve it verbatim and append owner-approved, evidence-grounded context rather than
automatically shortening or replacing it.

Use direct, practical contractor language. Avoid unsupported claims such as flawless, invisible repair, guaranteed exact match, or that every floor can be repaired or refinished. **Dust containment (2026-07-20, owner-confirmed, see `docs/2026-07-google-search-footprint-preservation.md`):** the sanding/refinishing system provides owner-confirmed **true 100% dust containment** — a sealed commercial system that captures sanding dust at the source. Use "true 100% dust containment" / "true 100% dust-containment sanding" as the precise claim; "dustless hardwood-floor sanding and refinishing" remains valid as the natural customer phrase alongside it. Do not weaken this to plain "dust-contained" (that was a stale claims-policy guess, since superseded by direct owner confirmation) and do not adopt generic 95–99% figures from AI-generated summaries.

## Work and review

For substantial work:
1. Inspect relevant code and documents.
2. Identify uncertainties and meaningful choices.
3. Present a short plan when needed.
4. Implement only the approved scope.
5. Build and validate.
6. Review the milestone diff.
7. Report the exact result and Git state.

Any task described as spanning the site, a page type, or a category of pages must explicitly
account for all 13 pages (the canonical URL map in `docs/PROJECT_DECISIONS.md`) before
implementing -- each page is either in scope or named and deferred with a stated reason, never
silently skipped. See `docs/PROJECT_QUALITY_BAR.md`.

For narrow approved work, proceed without unnecessary questions.

Review only the current milestone diff. Report material, high-confidence issues: regressions, factual violations, broken behavior, SEO risks, accessibility failures, security/deployment risks, or explicit instruction violations. Do not flood the owner with stylistic preferences or unrelated legacy issues.

## Validation

For website or generator changes:
- Run the relevant build during development when useful.
- Run the full build before completion.
- Inspect `git diff` and run `git diff --check`.
- Confirm generated output matches generator changes.
- Confirm no unrelated files changed.
- Preserve deterministic output.
- Run browser, responsive, accessibility, link, schema, metadata, and performance checks proportional to the task.

For documentation-only changes:
- Do not rebuild the site merely to create activity.
- Run `git diff --check`.
- Confirm only intended documentation files changed.

If a build changes unrelated output, stop and report it instead of absorbing it into the task.

## Git and deployment

`redesign` is the development and Cloudflare preview branch.
`master` is production-sensitive.

A push to `redesign` verifies and deploys preview.
A push to `master` verifies and deploys production.
Pull requests verify but do not deploy.
Manual workflow dispatch can deploy the selected branch; dispatching `master` is a production action.

Never infer permission to commit, push, merge, dispatch, or deploy.

Every task must end in one explicitly authorized state:
- Leave uncommitted
- Commit locally only
- Commit and push to `redesign`
- Separately authorized production action

Permission to edit is not permission to commit. Permission to commit is not permission to push. Permission to push `redesign` is not permission to touch production.

Do not use generic automatic commit/push/PR commands. Do not use Wrangler unless explicitly authorized for an emergency deployment. Never expose credentials or discard unrelated owner work.

## Continuity and completion

Keep durable rules here, current status in `docs/NEXT_SESSION.md`, detailed policy in the operating manual, and completed evidence in dated reports.

Do not turn `NEXT_SESSION.md` into an endless history. Update it after meaningful work. When context becomes very large, leave a clean handoff and start a fresh session.

At completion report:
- Summary and exact files changed
- Validation and results
- Material assumptions or unresolved questions
- Final `git status`
- Commit, push, preview, and production state

Never claim a build, test, commit, push, or deployment unless verified.