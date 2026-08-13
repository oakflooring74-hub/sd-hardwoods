# Production Launch Report — sdhardwoods.com live on Cloudflare (2026-07-25)

The remake site went live on the real domain the evening of 2026-07-25 (Pacific). Both
`https://www.sdhardwoods.com` and `https://sdhardwoods.com` now serve the redesigned site from
the Cloudflare Worker `sd-hardwoods` over HTTPS. Email was preserved. Downtime during cutover
was seconds.

## What was done, in order

1. **DNS replicated into Cloudflare before any switch.** The zone `sdhardwoods.com` was added
   to the Cloudflare account (`sandiegohardwoods@gmail.com`, account ID
   `623e2e56fbe1cefa694aec1061438b91`; zone ID `6cbd37f61b65417d2e70a1ed079008e4`).
   Cloudflare's import captured the legacy Turbify records; verified against Turbify's Domain
   Control Panel:
   - Both MX records (`mx-biz.mail.am0.yahoodns.net`, priorities 20/30) — business email intact.
   - `google-site-verification` TXT — Search Console verification survives.
   - Added by hand: `mail` and `ftp` CNAMEs → `cpanel287.turbify.biz`, set **DNS only**
     (grey cloud), since the Cloudflare proxy cannot carry IMAP/SMTP/FTP traffic.
   - Wildcard `*`, apex A, and `www` CNAME initially left pointing at Turbify hosting so the
     old site kept serving until the deliberate cutover moment.
2. **Nameservers changed at Turbify** from `ns1/ns2.turbify.com` to
   `clara.ns.cloudflare.com` / `karl.ns.cloudflare.com`. Zone went Active the same day.
3. **Custom domains attached to the production Worker** (`sd-hardwoods`) via the Cloudflare API
   (`PUT /accounts/{id}/workers/domains`), authenticated with the local Wrangler OAuth session.
   The API refuses while conflicting records exist (error 100117), and the Wrangler token has
   no DNS-write scope, so the owner deleted the two legacy records in the dashboard — apex A
   `52.186.183.172` and `www` CNAME `cpanel287.turbify.biz` — while a retry loop
   (10-second interval) attached each hostname the moment its record was gone:
   - `sdhardwoods.com` attached 20:29:38 PT
   - `www.sdhardwoods.com` attached 20:31:12 PT
   Cloudflare auto-created the Worker DNS records and issued certificates.

## Verification performed

- Both hostnames return HTTP 200 over HTTPS with the remake homepage
  (title "Hardwood Floor Refinishing San Diego | San Diego Hardwoods", ~155 KB).
- Production serves `master` (`5540432`, Milestone 3.2) as deployed by CI per Milestone 3.3;
  spot-checked that the Milestone-2.15 gallery schema is present on live gallery pages.
- **`verify_url_matrix.py https://www.sdhardwoods.com` (Milestone 3.3 step 4): 87/88 PASSED**,
  the single "failure" being the noindex check, which the script documents as EXPECTED to
  fail on production — `X-Robots-Tag` is correctly ABSENT on the custom domain (and remains
  on the workers.dev hosts by the host-scoped `_headers` rule). Production is indexable.
- MX/mail records untouched by the cutover; owner to sanity-check with a test email.
- Live sitemaps confirmed serving:
  - `https://www.sdhardwoods.com/sitemap.xml` — 13 page URLs + 704 `image:loc` entries
  - `https://www.sdhardwoods.com/sitemap-videos.xml` — 106 video entries
  - `robots.txt` references both.

## Deployment topology (for future sessions)

- **Production:** Worker `sd-hardwoods` → now bound to `sdhardwoods.com` + `www.sdhardwoods.com`
  (workers.dev URL still enabled; canonical tags point to `www`).
- **Preview:** Worker `sd-hardwoods-preview` (`redesign` branch).
- **Dormant:** Cloudflare Pages project `sd-hardwoods` (`sd-hardwoods.pages.dev`) is
  rollback-only per Milestone 3.0 — its preview is frozen at Milestone-2.15 content, and the
  standing CRITICAL warning applies: never deploy this repo to Pages again (the committed
  `_redirects` + Pages' `.html` normalization would create an infinite redirect loop).

## Discoveries / open items (owner decisions, none urgent)

1. **Cloudflare is injecting a managed block into the live robots.txt** ("BEGIN Cloudflare
   Managed content") that disallows AI crawlers (GPTBot, ClaudeBot, Google-Extended, CCBot,
   Amazonbot, Bytespider, meta-externalagent, Applebot-Extended) and adds
   `Content-Signal: search=yes,ai-train=no`. Googlebot/search indexing is unaffected, but this
   reduces AI-assistant visibility, which cuts against the Google-search-footprint-preservation
   strategy. Toggle lives at zone Overview → "Manage your robots.txt" / AI Crawl Control.
   Owner to decide keep vs. remove.
2. **RESOLVED during this session's push:** an apparent mismatch between the checkout's
   `sitemap.xml` and the live one was simply this Desktop checkout being 9 commits behind
   `origin/redesign` (Milestones 3.0–3.3, including the image/video sitemaps, were pushed
   from another machine). Reconciled by rebasing this docs commit onto `8e248c2`.
3. **Search Console submission** of `sitemap.xml` and `sitemap-videos.xml` handed to the owner
   with instructions (existing DNS TXT verification still valid).
4. **Turbify:** web hosting can eventually be cancelled, but domain registration and business
   email must stay with Turbify — mail still runs through their servers.
5. **CLAUDE.md project-root note updated for multi-machine use:** the repo is checked out in
   different locations per machine (`C:\FLOORING_SITE\...` on one; on the Desktop machine it
   is `C:\Users\oakfl\Desktop\SAN DIEGO HARDWOODS WEBSITE REMAKE JULY 2026`, where
   `C:\FLOORING_SITE` does not exist). CLAUDE.md now says to treat the current checkout as
   project root.

## Approved next work (owner, 2026-07-25 — "soon, not today")

- Fix a few spelling errors.
- A few schema items.
- Add more photos to the galleries, with alt text and captions — subject to the standing
  alt-text policy (existing accurate alt text preserved verbatim; additions owner-approved and
  evidence-grounded) and the media-fact confirmation policy.
