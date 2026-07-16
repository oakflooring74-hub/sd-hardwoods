"""
Re-fetch all 12 live pages from sdhardwoods.com into raw-source/.

Use this if the live Turbify site has changed and you want a fresh baseline to extract
from (e.g. the owner edited copy directly in Turbify's editor since the last crawl).
This OVERWRITES raw-source/*.html -- the extraction scripts in build/scripts/pages/ read
from those files, not from the live site directly, so re-running extraction after a
re-crawl will pick up whatever changed.

Usage:
    python crawl_live_site.py

Stdlib only (urllib), no third-party packages required.
"""
import urllib.request
import ssl
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
RAW = BUILD / "raw-source"

# slug -> live URL. A couple of slugs redirect (about_us -> about_us.html, blog -> blog.html
# on the live site) -- urllib follows redirects by default, so this just works.
PAGES = {
    "index": "https://www.sdhardwoods.com/",
    "about_us": "https://www.sdhardwoods.com/about_us",
    "contact_us": "https://www.sdhardwoods.com/contact_us",
    "recent_project_photo_gallery_1": "https://www.sdhardwoods.com/recent_project_photo_gallery_1",
    "solid_wood_floor_photo_gallery": "https://www.sdhardwoods.com/solid_wood_floor_photo_gallery",
    "deep-cleaning-hardwood-floors-san-diego": "https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html",
    "blog": "https://www.sdhardwoods.com/blog",
    "videos_of_refinishing_process": "https://www.sdhardwoods.com/videos_of_refinishing_process",
    "recent_project_photo_gallery_2": "https://www.sdhardwoods.com/recent_project_photo_gallery_2",
    "recent_project_photo_gallery_3": "https://www.sdhardwoods.com/recent_project_photo_gallery_3",
    "recent_project_photo_gallery_4": "https://www.sdhardwoods.com/recent_project_photo_gallery_4",
    "recent_project_gallery_5": "https://www.sdhardwoods.com/recent_project_gallery_5",
}

# NOTE: if you hit an SSL/schannel "CRYPT_E_NO_REVOCATION_CHECK" error on Windows (a
# corporate-network/Windows-cert-store quirk, not a real cert problem), the workaround
# used originally was `curl --ssl-no-revoke`. The equivalent here is disabling revocation
# checking on the SSL context -- only do this if you hit that specific error.
ctx = ssl.create_default_context()

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return resp.read()
    except ssl.SSLError:
        relaxed = ssl.create_default_context()
        relaxed.check_hostname = False
        relaxed.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, context=relaxed, timeout=30) as resp:
            return resp.read()


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for slug, url in PAGES.items():
        out_path = RAW / f"{slug}.html"
        try:
            content = fetch(url)
        except Exception as e:
            print(f"FAILED {slug} <- {url}: {e}")
            continue
        out_path.write_bytes(content)
        print(f"OK  {slug}.html  ({len(content)} bytes)  <- {url}")


if __name__ == "__main__":
    main()
