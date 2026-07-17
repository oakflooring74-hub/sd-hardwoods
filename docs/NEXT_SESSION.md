# Start here — project status as of 2026-07-16

Read this file first when picking this project back up. It links to everything else and tells you what's done, what's approved next, and what to ask the owner before doing anything.

## The site, in one paragraph

sdhardwoods.com is a legacy Yahoo/Turbify "Site Solution" site for a San Diego hardwood-flooring contractor. All 12 pages have been rebuilt with a consistent modern design system (see `build/README.md` for the full generator/tooling architecture). Everything lives in the GitHub repo **oakflooring74-hub/sd-hardwoods**, on the **`redesign` branch** (production/`master` still holds the prior owner's earlier, different rebuild attempt — do not merge without the owner's explicit go-ahead). This is still NOT the production site; sdhardwoods.com itself is untouched.

See also `docs/VISION.md` for the longer-term mission/goals this project is working toward.

## Milestone 1 — COMPLETE (2026-07-16): first interactive site-improvement batch

All 8 items approved in the prior session's QA pass, plus the blog/deep-cleaning mobile overflow bug, are implemented, built, and locally tested. Committed on `redesign` as **"Complete first interactive site-improvement milestone"** (`5d911a6`), pushed to `origin/redesign`, and manually deployed to the Cloudflare preview via `wrangler pages deploy` — verified live at `redesign.sd-hardwoods.pages.dev`. Production (`master`) was not touched.

**What shipped:**
- ✅ Sticky header foundation — replaced the two independently `position:fixed` elements (brand chip + nav button) with a single in-flow, sticky `<header id="sdhHeader">`. This **fixes the overlap bug** (nav/toggle no longer float on top of arbitrary scrolled content), but **the header itself is only a functional foundation, not a finished redesign** — see Milestone 2 below.
- ✅ Gallery image crop fix — `.gallery img` changed from fixed `height:320px;object-fit:cover` to `height:420px;object-fit:contain`, so tall vertical before/after photos are no longer cropped 60–85%.
- ✅ Homepage numbered badges (`#1`–`#96`) on the homepage gallery only, per the owner's scoping.
- ✅ Site-wide in-page lightbox (`build/chrome/lightbox.html`) — clicking a gallery photo now opens a JS overlay with next/prev/close, instead of navigating to a bare image file on a different domain. No new URLs/pages. Correctly ignores the blog/deep-cleaning "Home/Contact/Next Page" button widgets (which also use the `.gallery` class but link to real pages, not images) via an image-extension check on the href.
- ✅ Persistent "jump to gallery" progress indicator ("Gallery N of 5" + numbered jump links + prev/next) on all 5 before/after gallery pages (`recent_project_photo_gallery_1–4`, `recent_project_gallery_5`).
- ✅ Footer email/phone overflow fix, site-wide.
- ✅ Touch targets increased to ≥44px (nav button, flyout links, dark-mode toggle).
- ✅ Dark-mode toggle no longer overlaps the footer — an `IntersectionObserver` fades it out while the footer is on screen.
- ✅ Blog and deep-cleaning mobile horizontal-overflow bug fixed — the hardcoded `minmax(480px,1fr)` / `minmax(520px,1fr)` inline grid rules changed to `minmax(min(Npx,100%),1fr)`, which was the open question from the prior session (resolved: this was a real bug, distinct from the intentional 2-column squeeze on galleries 1–5, and is now fixed independently of that decision).
- ✅ All 12 pages regenerated via `build/scripts/build_all.py` and locally tested with real Chromium (Playwright) at mobile/tablet/desktop widths: zero horizontal overflow anywhere, header/touch-target/footer/lightbox/badge/progress-indicator checks all passed.

**Environment changes made to get this done:**
- **Python 3.12 was installed on this laptop** via `winget install Python.Python.3.12` — the machine previously had no real Python, only a Windows Store stub alias, so the build pipeline (which is Python stdlib-only) could not run before this. See the updated Prerequisites section in `build/README.md`.
- **Playwright + Chromium were installed and used *outside* the repository** (in a scratch temp directory, not committed) to drive the pages in a real browser for testing — served locally via `python -m http.server`. Nothing was added to the project for this; if a future session wants repeatable browser testing, it would need its own `package.json`/`node_modules` decision.

**Preserved, verified via diff:** URLs, headings, SEO utility-bar paragraph, meta descriptions, image `src`/`alt` (byte-identical), watermarks (no changes to `raw-source/` or `data/`), and the 2-column before/after grid on galleries 1–4.

## Deployment Automation Milestone — COMPLETE (2026-07-16): GitHub Actions → Cloudflare Pages

A separate milestone, done between Milestone 1 and Milestone 2: manual `wrangler pages deploy` is no longer required for normal work. A GitHub Actions workflow now deploys automatically on every push.

**What shipped:**
- ✅ `.github/workflows/deploy-cloudflare-pages.yml` — two jobs, `build` (checkout exact pushed commit → install Python 3.12 → `python build/scripts/build_all.py` → **fail if regeneration produces any uncommitted diff**, so generated HTML can never silently drift from `build/` source templates) and `deploy` (needs `build`; deploys the **committed** repo root via `cloudflare/wrangler-action`, using the pushed branch name as `--branch`).
- ✅ Push to `redesign` → automatic **Preview** deploy. Push to `master` → automatic **Production** deploy. This is enforced by Cloudflare's own project config (production branch = `master`, already set before this milestone — confirmed via `wrangler pages deployment list`), not by anything this workflow does — the workflow just passes the pushed branch name through.
- ✅ Pull requests targeting `redesign` or `master` run the `build` job only (`if: github.event_name != 'pull_request'` gates the `deploy` job) — validation never deploys, to either environment.
- ✅ `workflow_dispatch` supported for a controlled manual rerun.
- ✅ Concurrency group per branch (`${{ github.workflow }}-${{ github.ref }}`, `cancel-in-progress: false`) so overlapping pushes to the same branch queue instead of racing or being interrupted mid-deploy.
- ✅ Least-privilege: top-level `permissions: contents: read`; commit message is passed to Wrangler via an `env:` var (not interpolated directly into the shell command) to avoid injection from special characters in commit messages; secrets are never echoed anywhere in the workflow.
- ✅ All third-party actions (`actions/checkout`, `actions/setup-python`, `cloudflare/wrangler-action`) pinned to exact commit SHA, with the version tag as a comment.
- ✅ `.wrangler/` (local Wrangler cache/metadata, not build output) added to `.gitignore`.
- ✅ `build/README.md` has a new "Deployment" section: normal workflow, required secrets, manual emergency-deploy command, production safety rule, how to find Actions logs, how to verify a deployment URL.

**Credential setup:**
- A dedicated Cloudflare API token was created — **not** the local Wrangler OAuth login credential — scoped to the minimum permission needed (Cloudflare Pages: Edit, this account only). Programmatic token creation was not possible from the existing authenticated session (Cloudflare's `wrangler login` OAuth grant deliberately excludes token-management permissions — creating a new token requires the dashboard), so this one step was done by the owner in the browser per the assistant's precise instructions, then entered directly via `gh secret set` — the token value itself was never written to disk, committed, or echoed anywhere.
- Repo secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set on `oakflooring74-hub/sd-hardwoods` (Settings → Secrets and variables → Actions). Only names are ever referenced in docs/workflow — never values.

**Actual first-run test results (2026-07-16):**
- Two real bugs surfaced and were fixed before the pipeline worked in CI — both were pre-existing latent issues in `build/scripts`, not something wrong with the workflow itself:
  1. **Path separators.** Every write/read in `build/scripts` joins paths with a hardcoded backslash (e.g. `CHROME + r"\site_css.html"`), which only resolves on Windows. The first CI run failed immediately with `FileNotFoundError` on `ubuntu-latest`. Fixed by running the `build` job on `windows-latest` instead of rewriting the existing generator scripts (see commit `a8abb91`).
  2. **Line endings.** All 22 write-mode `open(path, "w", encoding="utf-8")` calls across `build/scripts` used Python's default text-mode writing, which emits `\r\n` on Windows. The committed pages are LF (this repo normalizes to LF on commit). Regenerating on a Windows runner with `autocrlf` disabled therefore produced a full-file CRLF-vs-LF mismatch on every single line (8,460 insertions / 8,460 deletions across 19 files, despite zero real content change) — correctly caught and failed by the "fail if build changed committed output" gate, exactly as designed. Fixed by adding `newline="\n"` to all 22 calls, forcing deterministic LF output on any OS (commit `8f622b5`). Verified locally afterward: regenerating produces byte-for-byte identical output to HEAD (confirmed via `git diff --cached` / `cmp`, not plain `git status`, since this machine's own `core.autocrlf=true` gives a misleading "modified" signal on an unrelated axis when the file's on-disk EOL convention doesn't match what a fresh checkout would produce, even though the actual committed content is unchanged).
  3. **Cloudflare token rejected on the first deploy attempt** — `Authentication error [code: 10000]`, "Failed to automatically retrieve account IDs." The originally-created token was invalid/misconfigured; the owner created a replacement token and updated the `CLOUDFLARE_API_TOKEN` secret directly (bypassing this conversation entirely, the safest of the two options offered). No workflow change was needed — the second token authenticated successfully on the immediate rerun.
- **First fully green run:** GitHub Actions run [`29546738449`](https://github.com/oakflooring74-hub/sd-hardwoods/actions/runs/29546738449) (rerun after the token fix) — both `build` and `deploy` jobs succeeded.
- **Cloudflare deployment:** ID `47dc66ec-b62e-48cb-8078-d1e715357aac`, Environment `Preview`, Branch `redesign`, Source commit `8f622b5a00e3460670d6dff49e1dd6d32124535d` — **the exact same commit SHA the GitHub Actions run built from**, confirmed via both the workflow's own job summary and `wrangler pages deployment list`.
- **Live verification:** `https://redesign.sd-hardwoods.pages.dev` returns HTTP 200 and serves the new markup (`sdhLightbox`, `gallery-progress`, etc.) — confirmed pointing at this deployment. `https://sd-hardwoods.pages.dev` (production) returns HTTP 200 with none of that markup — confirmed untouched; `wrangler pages deployment list` shows Production deployments still pinned to `master` at `c3e8e0c`/`b6ac6a1`, unchanged throughout this entire milestone.
- **Conclusion:** the automation works end-to-end. Future pushes to `redesign` deploy automatically with no manual `wrangler` invocation needed.

## Milestone 2 — NEXT: site-wide header & navigation redesign

**Nothing from this milestone has been implemented yet.** Milestone 1's sticky header is a functional fix (no more overlap), not the redesign itself.

**Why this is next:** a screenshot review of the current live-preview look (post Milestone 1) found:
- The brand/wordmark is too small and doesn't read as a real masthead relative to the rest of the header.
- The SEO utility-bar strip visually dominates the top of the page — it's more prominent than the brand and nav combined.
- Navigation is inadequate as a single "☰ Explore Our Services" button hiding all 12 pages in one undifferentiated flyout list.

**What the owner wants for this milestone:**
- Organize all 12 pages into clear groups in the navigation, rather than one flat "Explore Our Services" flyout. (Exact grouping/labels not yet decided — this is a design decision for next session, not implemented.)
- A prominent link to the YouTube channel (`https://www.youtube.com/@SANDIEGOHARDWOODS`) with a recognizable YouTube visual treatment (not just a plain text link buried in the flyout, as it is today).
- A real visual hierarchy fix: brand should read as the dominant visual element it should be; the SEO utility-bar strip should be de-emphasized relative to brand + nav, without removing or rewriting its text.

**Hard constraints for this milestone (same as always):**
- Preserve all URLs, headings, SEO copy, metadata, image sources, and watermarks.
- Preserve the two-column before/after gallery layout on galleries 1–5 (still an intentional "billboard CTA" choice — see below).
- **The long SEO paragraph (the keyword-heavy utility-bar text) is still protected — do not move, shrink, hide, or rewrite it without explicit owner approval.** De-emphasizing its visual *dominance* is in scope; touching its *content or presence* is not.
- Don't start this milestone speculatively — confirm the navigation grouping/labels with the owner before building, since "organize into clear groups" is a direction, not a spec.

## Decisions still standing from prior sessions

**DO NOT CHANGE:**
- SEO paragraph (the keyword-heavy utility-bar text) — content/presence protected; visual de-emphasis is the Milestone 2 goal, see above.
- Watermarks (owner adds these in Photoshop).
- Two-column before/after galleries (intentional "billboard CTA" feel, even on mobile).
- Legacy hosted images (still served live from Turbify via the `<base href>` shim).

**DEFERRED — not now, not dismissed:**
- CMS (a way for the owner to add projects without a dev session).
- Desktop app (see prior discussion — feasible, but scoped out for now).
- Migration toolkit (turning this system into a general legacy-site-migration tool).
- Image optimization.
- Cloudflare image migration (moving images off Turbify hosting).
- Google Search Console optimization (waiting on the data export).

## Blocked / waiting on the owner

- **Google Search Console export** (Query, Page, Clicks, Impressions, CTR, Position — full history, ideally per-page) — needed before any heading-level changes or meta-description rewrites on pages that already have one. See `docs/2026-07-seo-heading-audit.md` for exactly what this unlocks and why pulling it *before* the redesign goes live matters (it's the only way to get a clean pre-launch ranking baseline).
- **Image optimization** — deferred, but not dismissed. See the "Image optimization feasibility" section of `docs/2026-07-qa-report.md`: it's genuinely harder right now because images are still served live from Turbify hosting via a `<base href>` shim, not because image compression itself is hard. Worth revisiting if/when images move to being repo-hosted.
- **Milestone 2 navigation grouping/labels** — direction is set (see above), specifics are not. Confirm with the owner before building.

## Safe to do without waiting on GSC data

Adding meta descriptions to the 6 pages that currently have **none at all** (about_us, contact_us, videos_of_refinishing_process, blog, recent_project_photo_gallery_4, recent_project_gallery_5) — confirmed missing on the legacy site, not something the redesign removed, so there's no existing snippet performance to protect. Still needs the owner's go-ahead to actually write and add them (this was a discussion session, nothing was implemented), but doesn't need to wait on the GSC export the way changes to pages that already have a meta description do.

## Reference docs in this folder

- `docs/2026-07-qa-report.md` — full QA findings, owner decisions, **now updated with Milestone 1 completion status and current remaining issues**
- `docs/2026-07-seo-heading-audit.md` — GSC strategy discussion, meta-description categorization, full legacy-vs-redesign heading data and analysis (unchanged, still discussion-only)
- `build/README.md` — how the site is actually built/regenerated, including the Python prerequisite note; read this before touching any `build/` script

## Key facts worth not re-deriving

- GitHub: `oakflooring74-hub/sd-hardwoods`, branch `redesign`.
- `gh` CLI has two logged-in accounts on this machine; make sure `oakflooring74-hub` is the active one before pushing (`gh auth switch --hostname github.com --user oakflooring74-hub`).
- The redesigned pages still depend on Turbify hosting for images/video/theme CSS via a `<base href="https://www.sdhardwoods.com/">` tag — this is a deliberate bridge, not an oversight, but it's the reason image optimization is currently hard and worth remembering when it comes up again.
- Python 3.12 is now installed on this laptop (see Milestone 1 above) — the build pipeline can be run directly; no need to re-solve the missing-Python problem.
- Milestone 1 (`5d911a6`) and the deployment-automation milestone (`c759cf9`, `a8abb91`, `8f622b5`) are all **committed and pushed** to `origin/redesign` as of 2026-07-16, and the automation has been proven working end-to-end (first green run: Actions `29546738449`, Cloudflare deployment `47dc66ec`).
- **`build/scripts` write calls now force `newline="\n"`** (22 call sites, fixed in `8f622b5`) so generated output is deterministically LF on any OS — needed because this repo's commits normalize to LF but Python's default text-mode write emits CRLF on Windows. Don't remove this when touching those files; without it, the CI diff-check gate will spuriously fail on every regeneration.
- **The `build` job in `.github/workflows/deploy-cloudflare-pages.yml` runs on `windows-latest`, not `ubuntu-latest`** — because `build/scripts` still joins paths with hardcoded backslashes (e.g. `CHROME + r"\site_css.html"`). This works but is a latent portability debt: if a future session has time to spare, switching those to `pathlib`-style joins would let the job run on (cheaper, faster) `ubuntu-latest` instead. Not urgent — public repo, so Actions minutes are free either way.
- **Deployments are now automated** — see the "Deployment Automation Milestone" section above and the "Deployment" section in `build/README.md`. Don't reach for manual `wrangler pages deploy` for normal work; just push to `redesign` (preview) or `master` (production, owner-approved only) and let GitHub Actions handle it. Manual deploy is documented as the emergency-only fallback.
- Cloudflare Pages project `sd-hardwoods` has **no native Git integration** (`wrangler pages project list` shows "Git Provider: No") — the GitHub Actions workflow is a from-scratch deploy pipeline built specifically because that native integration isn't (and per this milestone's scope, still isn't) connected. Don't assume pushing alone triggers anything without checking the Actions tab if this workflow is ever removed/disabled.
