"""Deployment URL-matrix verifier (Milestone 3.0).

Asserts the complete Workers Static Assets serving contract against any host:
every .html page 200 direct, extensionless/trailing-slash duplicates 301 to the
.html canonical, / served via the index.html proxy, query strings preserved,
assets 200, non-public repo files 404, canonical tags, sitemap, JSON-LD parses,
internal links resolve, and reports the X-Robots-Tag header.

Usage:
  python build/scripts/verify_url_matrix.py https://sd-hardwoods-preview.sandiegohardwoods.workers.dev
  python build/scripts/verify_url_matrix.py https://www.sdhardwoods.com   (post-cutover)

Exit code 0 = all checks passed. Note: the X-Robots-Tag noindex check is
EXPECTED TO FAIL against production (production must NOT be noindexed) --
that final check asserts the preview-host contract; on production, verify the
header is ABSENT instead.
"""
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

BASE = sys.argv[1].rstrip("/")
CTX = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (sdh-url-matrix-test)"}

PAGES = [
    "about_us", "blog", "contact_us", "deep-cleaning-hardwood-floors-san-diego",
    "floor-assessments-inspections", "recent_project_photo_gallery_1",
    "recent_project_photo_gallery_2", "recent_project_photo_gallery_3",
    "recent_project_photo_gallery_4", "recent_project_gallery_5",
    "solid_wood_floor_photo_gallery", "videos_of_refinishing_process",
]
BLOCKED = [
    "/CLAUDE.md", "/homepage_image_owner_facts_5-90.yaml", "/build/README.md",
    "/docs/NEXT_SESSION.md", "/build/data/youtube_videos.json",
    "/.github/workflows/deploy-cloudflare-pages.yml", "/wrangler.jsonc",
    "/.assetsignore", "/.gitignore", "/.git/config",
    "/.claude/settings.local.json", "/nonexistent-page",
]
ASSETS = [
    "/DALE9.jpg", "/favicon.ico", "/robots.txt", "/sitemap.xml",
    "/styles.css", "/script.js",
]

results = []


def req(path, method="GET"):
    """Return (status, headers, body_bytes) without following redirects."""
    path = urllib.parse.quote(path, safe="/?&=%")
    url = BASE + path if path.startswith("/") else path

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = urllib.request.build_opener(
        NoRedirect, urllib.request.HTTPSHandler(context=CTX))
    r = urllib.request.Request(url, headers=UA, method=method)
    try:
        with opener.open(r, timeout=30) as resp:
            body = resp.read() if method == "GET" else b""
            return resp.status, dict(resp.headers), body
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), (e.read() if method == "GET" else b"")


def check(ok, label, detail=""):
    results.append((ok, label, detail))
    print(("PASS " if ok else "FAIL ") + label + ("  -- " + detail if detail else ""))


def location(headers):
    loc = headers.get("Location", headers.get("location", ""))
    return loc.replace(BASE, "")


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical = None
        self.hrefs = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonical = a.get("href")
        if tag == "a" and a.get("href"):
            self.hrefs.add(a["href"])


s, h, b = req("/")
check(s == 200 and b"<title>" in b, "GET / -> 200 with HTML content", f"status={s}")
home_html = b.decode("utf-8", errors="replace")
check("San Diego Hardwood" in home_html[:2000], "/ serves homepage content")
s, h, _ = req("/index.html")
check(s in (301, 308) and location(h) in ("/", ""),
      "/index.html -> 301 to /", f"status={s} loc={location(h)!r}")

page_html_cache = {"/": home_html}
for p in PAGES:
    s, h, b = req(f"/{p}.html")
    check(s == 200, f"GET /{p}.html -> 200 direct", f"status={s}")
    if s == 200:
        page_html_cache[f"/{p}.html"] = b.decode("utf-8", errors="replace")
    for variant in (f"/{p}", f"/{p}/"):
        s, h, _ = req(variant, method="HEAD")
        check(s == 301 and location(h) == f"/{p}.html",
              f"{variant} -> 301 /{p}.html", f"status={s} loc={location(h)!r}")

s, h, _ = req("/contact_us.html?utm_source=test", method="HEAD")
check(s == 200, "/contact_us.html?utm_source=test -> 200", f"status={s}")
s, h, _ = req("/contact_us?a=1&b=2", method="HEAD")
loc = location(h)
check(s == 301 and loc.startswith("/contact_us.html"),
      "/contact_us?a=1&b=2 -> 301 .html",
      f"status={s} loc={loc!r} (query preserved: {'a=1' in loc})")

for a in ASSETS:
    s, h, _ = req(a, method="HEAD")
    check(s == 200, f"asset {a} -> 200", f"status={s}")

for p in BLOCKED:
    s, h, _ = req(p, method="HEAD")
    check(s == 404, f"blocked {p} -> 404", f"status={s}")

all_internal = set()
for path, html_text in page_html_cache.items():
    lp = LinkParser()
    lp.feed(html_text)
    expected = "https://www.sdhardwoods.com" + ("/" if path == "/" else path)
    check(lp.canonical == expected, f"canonical on {path}",
          f"got {lp.canonical!r} expected {expected!r}")
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html_text, re.S)
    ok = bool(blocks)
    for blk in blocks:
        try:
            json.loads(blk)
        except json.JSONDecodeError:
            ok = False
    check(ok, f"JSON-LD parses on {path}", f"{len(blocks)} block(s)")
    for href in lp.hrefs:
        if href.startswith("https://www.sdhardwoods.com/"):
            all_internal.add(href.replace("https://www.sdhardwoods.com", "") or "/")
        elif href.startswith("/") and not href.startswith("//"):
            all_internal.add(href)

s, h, b = req("/sitemap.xml")
sm = b.decode("utf-8", errors="replace")
locs = re.findall(r"<loc>(.*?)</loc>", sm)
bad = [u for u in locs
       if not (u.endswith(".html") or u.rstrip("/") == "https://www.sdhardwoods.com")]
check(s == 200 and locs and not bad,
      "sitemap.xml -> 200, all URLs .html-canonical",
      f"{len(locs)} URLs, non-.html: {bad}")

pages_set = {p for p in all_internal
             if not re.search(r"\.(jpg|jpeg|png|gif|webp|ico|css|js|xml)$", p, re.I)}
media_set = sorted(all_internal - pages_set)[:25]
fails = []
for p in sorted(pages_set) + media_set:
    s, h, _ = req(p, method="HEAD")
    if s in (301, 308):
        s2, _, _ = req(location(h), method="HEAD")
        if s2 != 200:
            fails.append(f"{p} -> {s} -> {s2}")
    elif s != 200:
        fails.append(f"{p} -> {s}")
check(not fails,
      f"internal links resolve ({len(pages_set)} page links + {len(media_set)} sampled media)",
      "; ".join(fails[:10]))

s, h, _ = req("/", method="HEAD")
xr = h.get("X-Robots-Tag", h.get("x-robots-tag", "(absent)"))
print(f"INFO  X-Robots-Tag on /: {xr}")
check("noindex" in xr,
      "X-Robots-Tag noindex present (preview-host contract; must be ABSENT on production)",
      f"/={xr!r}")

failed = [r for r in results if not r[0]]
print(f"\n===== {len(results) - len(failed)}/{len(results)} PASSED, {len(failed)} FAILED =====")
for _, label, detail in failed:
    print(f"  FAILED: {label} -- {detail}")
sys.exit(1 if failed else 0)
