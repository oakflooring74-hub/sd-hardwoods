# -*- coding: utf-8 -*-
"""
Videos page builder (Milestone 2.1 rebuild).

Renders the complete public-video archive of the San Diego Hardwoods YouTube
channel from the checked-in snapshot build/data/youtube_videos.json -- no
network access, deterministic output. Featured videos render as larger cards
in their own section; every other public upload renders exactly once in the
library grid below, with client-side category filters. No YouTube iframe
exists on initial page load: thumbnails are lazy-loaded facades, and a
privacy-enhanced (youtube-nocookie.com) embed is created only when the
visitor activates a video, inside one accessible modal player (Escape closes,
focus returns to the activating card).

To refresh the snapshot itself: python build/scripts/update_youtube_videos.py
"""
import html
import json
import re
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import assemble
from public_business_rules import replace_area_served, FULL_SAN_DIEGO_AREAS, SOUTH_ORANGE_COUNTY
from alt_expand import append_sentences

HEAD_META = """<title>Hardwood Floor Refinishing &amp; Dustless Sanding Videos | San Diego</title>
<meta name="description" content="Watch real San Diego hardwood floor refinishing, sanding, repair, staining and restoration videos from actual customer projects.">
<link href="https://www.sdhardwoods.com/videos_of_refinishing_process.html" rel="canonical">
<link href="/favicon.ico" rel="icon" type="image/x-icon">
<link href="/favicon-192.ico" rel="icon" sizes="192x192" type="image/x-icon">
<link href="/favicon-512.ico" rel="icon" sizes="512x512" type="image/x-icon">
<link href="/LOGO-2025.png" rel="apple-touch-icon" sizes="180x180">
<meta name="theme-color" content="#4b2e06">
<link href="/LOGO-2025.png" rel="logo" type="image/png">
<link href="/assets/legacy-css/mc_global.195798.css" id="globalCSS" media="screen" rel="stylesheet" type="text/css">
<link href="/assets/legacy-css/theme.css" id="themeCSS" media="screen" rel="stylesheet" type="text/css">"""

# Milestone 2.6: the shared GA4 implementation (build/chrome/analytics.html) is
# injected by assemble() -- leave this empty; never add a per-page loader.
GA = ""

VCARD = "THE BEST HARDWOOD FLOOR REFINISHING IN SAN DIEGO CALL TODAY 858-699-0072 LICENSED CONTRACTOR WITH OVER 30 YEARS EXPERIENCE WITH ALL TYPES OF SOLID AND ENGINEERED WOOD FLOORS. ALL WORK IS GUARANTEED AND PERFORMED BY A SMALL CREW OF SKILLED AND COURTEOUS CRAFTSMEN. TEXT PHOTOS FOR QUICK ASSESSMENT OF YOUR FLOORING PROJECT. CSLB LICENSED FLOORING CONTRACTOR IN SAN DIEGO. DUST CONTAINMENT SANDING EQUIPMENT USED FOR ALL PHASES OF EACH PROJECT."

# ---------------- snapshot ----------------
with open(BUILD / "data" / "youtube_videos.json", encoding="utf-8") as f:
    SNAPSHOT = json.load(f)
VIDEOS = SNAPSHOT["videos"]
CHANNEL_URL = SNAPSHOT["channel_url"]

ids = [v["id"] for v in VIDEOS]
assert len(ids) == len(set(ids)), "duplicate YouTube IDs in snapshot"

featured = sorted([v for v in VIDEOS if v["featured"]], key=lambda v: v["featured_rank"])
library = [v for v in VIDEOS if not v["featured"]]

# Milestone 2.9: one server-rendered hero video above the featured/library
# sections, for Rich Results video eligibility (a real playable iframe must
# exist in the initial HTML, not only a click-to-play facade). Reuses the
# video already established as this page's #1 featured video -- no new
# research, no change to the other 57 videos or the featured/library grids.
HERO = featured[0]
HERO_ID = "https://www.sdhardwoods.com/videos_of_refinishing_process.html#hero-video"

CATEGORY_ORDER = [
    ("dust-contained-refinishing", "Dust-Contained Sanding & Refinishing"),
    ("repairs-restoration", "Repairs & Restoration"),
    ("deep-cleaning-recoating", "Deep Cleaning & Recoating"),
]

MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def esc(s):
    return html.escape(s or "", quote=True)


def display_title(v):
    """Milestone 2.6: the page (and its VideoObject names) show
    `site_display_title` when the snapshot carries one -- used only where the
    live YouTube title is blank or date-only, with a restrained owner-confirmed
    fallback. The original live title is always preserved in `title`."""
    return v.get("site_display_title") or v["title"]


def nice_date(iso):
    try:
        y, m, _ = iso.split("-")
        return f"{MONTHS[int(m)]} {y}"
    except (ValueError, IndexError):
        return iso


def card_desc(v):
    if v.get("site_description"):
        return v["site_description"]
    d = re.sub(r"\s+", " ", v.get("description") or "").strip()
    if len(d) > 180:
        d = d[:180].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    return d


def thumb_alt(v):
    """Aggressive alt-text expansion (2026-07-20): every thumbnail on this page
    previously rendered alt="" (confirmed by inventory scan). Built entirely from
    this video's own already-verified snapshot fields (title, curated display
    title, category, real site/YouTube description, upload date) -- nothing
    invented. Title/description redundancy between the thumbnail alt and the
    adjacent visible <h3>/<p> is an intentional owner decision for this milestone."""
    title_sentence = display_title(v)
    desc = v.get("site_description") or ""
    if not desc:
        d = re.sub(r"\s+", " ", v.get("description") or "").strip()
        # first sentence/paragraph only, not the full raw YouTube description body
        d = d.split("\n\n")[0].strip()
        if len(d) > 320:
            d = d[:320].rsplit(" ", 1)[0].rstrip(",.;:") + "..."
        desc = d
    kind = "San Diego Hardwoods YouTube Short video thumbnail" if v.get("is_short") else "San Diego Hardwoods YouTube video thumbnail"
    closing = (f"{kind} showing {v['category_label'].lower()} filmed on a real customer "
               f"hardwood or bamboo floor project in San Diego County, uploaded {v['publish_date']}.")
    return append_sentences(title_sentence, desc, closing)


def video_card(v, big=False):
    cls = "vid-card vid-card--featured" if big else "vid-card"
    badge = '<span class="vid-flag">Featured</span>' if big else ""
    short_badge = '<span class="vid-flag vid-flag--short">Short</span>' if v["is_short"] else ""
    desc = card_desc(v)
    desc_html = f'<p class="vid-desc">{esc(desc)}</p>' if desc else ""
    gallery_html = ""
    if v.get("gallery_href"):
        gallery_html = (f'<a class="vid-gallery" href="{esc(v["gallery_href"])}">'
                        f'{esc(v["gallery_label"])} &rarr;</a>')
    t = esc(display_title(v))
    return f'''<article class="{cls}" data-cat="{v["category"]}" data-short="{'1' if v["is_short"] else '0'}">
  <button type="button" class="vid-thumb" data-yt="{v["id"]}" data-vtitle="{t}" aria-label="Play video: {t}">
    <img src="{esc(v["thumbnail_url"])}" alt="{esc(thumb_alt(v))}" loading="lazy" width="480" height="360">
    <span class="vid-dur" aria-hidden="true">{esc(v["duration_text"])}</span>
    <span class="vid-play" aria-hidden="true"><svg viewBox="0 0 68 48" width="52" height="37" focusable="false"><path fill="rgba(20,14,7,.82)" d="M66.5 7.7c-.8-2.9-3-5.2-5.9-6C55.4.3 34 .3 34 .3S12.6.3 7.4 1.7c-2.9.8-5.1 3.1-5.9 6C.1 13 .1 24 .1 24s0 11 1.4 16.3c.8 2.9 3 5.2 5.9 6 5.2 1.4 26.6 1.4 26.6 1.4s21.4 0 26.6-1.4c2.9-.8 5.1-3.1 5.9-6C67.9 35 67.9 24 67.9 24s0-11-1.4-16.3z"/><path fill="#fff" d="M27 34.6 44.6 24 27 13.4z"/></svg></span>
  </button>
  <div class="vid-body">
    <p class="vid-tags"><span class="vid-cat">{esc(v["category_label"])}</span>{badge}{short_badge}</p>
    <h3 class="vid-title">{t}</h3>
    {desc_html}
    <p class="vid-meta">{nice_date(v["publish_date"])} &bull; {esc(v["duration_text"])}</p>
    <p class="vid-actions"><button type="button" class="vid-watch" data-yt="{v["id"]}" data-vtitle="{t}">&#9654;&#xFE0E; Watch Video</button><a class="vid-yt-link" href="{esc(v["watch_url"])}" target="_blank" rel="noopener">Watch on YouTube &#8599;</a></p>
    {gallery_html}
  </div>
</article>'''


featured_cards = "\n".join(video_card(v, big=True) for v in featured)
library_cards = "\n".join(video_card(v) for v in library)

# library-only counts drive the filter buttons (featured cards are also filtered,
# and the featured section hides itself when none of its cards match)
def lib_count(pred):
    return sum(1 for v in VIDEOS if pred(v))

filter_buttons = ['<button type="button" class="vid-filter active" data-filter="all" aria-pressed="true">All Videos <span class="vf-n">%d</span></button>' % len(VIDEOS)]
for key, label in CATEGORY_ORDER:
    n = lib_count(lambda v, k=key: v["category"] == k)
    if n:
        filter_buttons.append(
            f'<button type="button" class="vid-filter" data-filter="{key}" aria-pressed="false">{esc(label)} <span class="vf-n">{n}</span></button>')
n_shorts = lib_count(lambda v: v["is_short"])
if n_shorts:
    filter_buttons.append(
        f'<button type="button" class="vid-filter" data-filter="shorts" aria-pressed="false">Shorts <span class="vf-n">{n_shorts}</span></button>')
filters_html = "\n    ".join(filter_buttons)

# ---------------- structured data ----------------
# Keep the page's original schema blocks (FlooringContractor, CollectionPage, ...)
# but REPLACE the legacy VideoObject @graph -- it covered only the 14 videos the
# old page embedded and carried an invented placeholder uploadDate
# ("2024-01-01T12:00:00Z"). The replacement graph is generated from the snapshot:
# every public upload, real publish dates, real ISO-8601 durations. Fields come
# straight from YouTube metadata; nothing is fabricated, and empty descriptions
# are omitted rather than invented.
with open(BUILD / "data" / "videos_of_refinishing_process" / "jsonld_fixed.html", encoding="utf-8") as f:
    jsonld_raw = f.read()

blocks = re.findall(r"<script type=\"application/ld\+json\">.*?</script>", jsonld_raw, re.S)
kept_blocks = [b for b in blocks if '"VideoObject"' not in b]

# Milestone 2.9: give the CollectionPage a `video` reference to the hero's
# VideoObject (by @id -- see below), so the hero is connected to the page as
# its primary video without declaring a second, conflicting VideoObject.
_new_kept_blocks = []
for b in kept_blocks:
    body = re.match(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', b, re.S).group(1)
    node = json.loads(body)
    if node.get("@type") == "CollectionPage":
        node["video"] = {"@id": HERO_ID}
        b = '<script type="application/ld+json">\n' + json.dumps(node, indent=1, ensure_ascii=False) + '\n</script>'
    _new_kept_blocks.append(b)
kept_blocks = _new_kept_blocks

video_objects = []
for v in VIDEOS:
    obj = {
        "@type": "VideoObject",
        "name": display_title(v),
        "thumbnailUrl": v["thumbnail_url"],
        "uploadDate": v["publish_date"],
        "duration": v["duration_iso8601"],
        "contentUrl": v["watch_url"],
        "embedUrl": v["embed_url"],
    }
    if v["id"] == HERO["id"]:
        # The one primary VideoObject, connected to the page via
        # CollectionPage.video above -- same entry as its ItemList position,
        # not a second duplicate declaration.
        obj["@id"] = HERO_ID
    desc = re.sub(r"\s+", " ", (v.get("site_description") or v.get("description") or "")).strip()
    if desc:
        obj["description"] = desc[:300]
    video_objects.append(obj)

# Rich Results milestone (2026-07-19): wrap the 58 real VideoObjects in a
# proper ItemList (position-ordered) instead of leaving them as flat @graph
# siblings, and give it the stable @id the page's CollectionPage.mainEntity
# (set in jsonld_fixed.html) already points to -- this is the structure
# Google's Video rich-result / ItemList guidance expects for a video gallery
# page, and the priority page for reaching full Rich Results eligibility.
video_itemlist = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "@id": "https://www.sdhardwoods.com/videos_of_refinishing_process.html#videolist",
    "name": "Hardwood & Bamboo Floor Refinishing Process Videos",
    "numberOfItems": len(video_objects),
    "itemListElement": [
        {"@type": "ListItem", "position": i, "item": obj}
        for i, obj in enumerate(video_objects, start=1)
    ],
}
video_graph = json.dumps(video_itemlist, indent=1, ensure_ascii=False)
JSONLD = "\n".join(kept_blocks) + '\n<script type="application/ld+json">\n' + video_graph + "\n</script>"
# Milestone 2.9: this page's #local declaration had no areaServed at all --
# add the complete, centralized San Diego + South Orange County list so the
# shared entity carries the full location footprint on every page it's
# declared on, not just the homepage.
JSONLD = replace_area_served(JSONLD, FULL_SAN_DIEGO_AREAS + SOUTH_ORANGE_COUNTY)

# ---------------- page ----------------
PAGE_CSS = """<style>
.vid-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:22px;margin-top:26px;}
.vid-grid--featured{grid-template-columns:repeat(auto-fill,minmax(min(360px,100%),1fr));}
.vid-card{display:flex;flex-direction:column;background:var(--card-bg);border:1px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.06);}
.vid-card--featured{border-top:3px solid var(--brass);}
.vid-thumb{position:relative;display:block;width:100%;padding:0;border:none;background:#0e0b07;cursor:pointer;}
.vid-thumb img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;}
.vid-thumb:hover .vid-play svg path:first-child,.vid-thumb:focus-visible .vid-play svg path:first-child{fill:#c00;}
.vid-thumb:focus-visible{outline:3px solid var(--brass);outline-offset:-3px;}
.vid-play{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);line-height:0;}
.vid-dur{position:absolute;right:8px;bottom:8px;background:rgba(10,8,5,.85);color:#fff;font:700 12px/1 var(--font-sans);padding:5px 8px;border-radius:5px;}
.vid-body{display:flex;flex-direction:column;gap:8px;padding:16px 18px 18px;flex:1;}
.vid-tags{display:flex;flex-wrap:wrap;gap:8px;margin:0;}
.vid-cat{font:700 11px/1.4 var(--font-sans);letter-spacing:1.2px;text-transform:uppercase;color:var(--brass-deep);}
.vid-flag{font:700 11px/1.4 var(--font-sans);letter-spacing:1.2px;text-transform:uppercase;color:#fff;background:var(--walnut);padding:2px 8px;border-radius:10px;}
body.darkmode .vid-flag{background:var(--brass);color:#1b1712;}
.vid-flag--short{background:var(--cta-red);color:#fff;}
body.darkmode .vid-flag--short{background:var(--cta-red);color:#1b1712;}
.vid-title{font-family:var(--font-serif);font-size:18.5px;line-height:1.35;margin:0;color:var(--ink);}
.vid-desc{font-size:14.5px;line-height:1.55;color:var(--ink-soft);margin:0;}
.vid-meta{font-size:13px;color:var(--ink-soft);opacity:.85;margin:0;}
.vid-actions{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:auto 0 0;padding-top:6px;}
.vid-watch{display:inline-flex;align-items:center;gap:7px;min-height:44px;padding:8px 16px;border:none;border-radius:9px;background:var(--cta-red);color:#fff;font:700 14px/1.2 var(--font-sans);cursor:pointer;box-shadow:0 4px 14px rgba(179,38,30,.28);}
.vid-watch:hover{background:var(--cta-red-dark);}
body.darkmode .vid-watch{color:#1b1712;}
.vid-yt-link{font:700 13.5px/1.3 var(--font-sans);color:var(--brass-deep);text-decoration:underline;min-height:44px;display:inline-flex;align-items:center;}
.vid-gallery{font:700 14px/1.4 var(--font-sans);color:var(--brass-deep);text-decoration:underline;}
.vid-filters{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:24px 0 4px;}
.vid-filter{display:inline-flex;align-items:center;gap:7px;min-height:44px;padding:8px 16px;border:1px solid var(--line);border-radius:22px;background:var(--card-bg);color:var(--ink);font:600 14px/1.2 var(--font-sans);cursor:pointer;}
.vid-filter .vf-n{font-size:12px;font-weight:700;color:var(--brass-deep);}
.vid-filter.active{background:var(--walnut);border-color:var(--walnut);color:#fff;}
.vid-filter.active .vf-n{color:#eadfc7;}
body.darkmode .vid-filter.active{background:var(--brass);border-color:var(--brass);color:#1b1712;}
body.darkmode .vid-filter.active .vf-n{color:#4b2e06;}
.vid-count{text-align:center;font-size:14px;color:var(--ink-soft);margin:14px 0 0;}
#sdhVideoModal{position:fixed;inset:0;z-index:1000010;background:rgba(10,8,5,.94);display:none;align-items:center;justify-content:center;padding:22px;}
#sdhVideoModal.open{display:flex;}
#sdhVideoModal .vm-frame{width:min(1100px,96vw);}
#sdhVideoModal .vm-player{position:relative;padding-top:56.25%;height:0;background:#000;border-radius:10px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.5);}
#sdhVideoModal .vm-player iframe{position:absolute;inset:0;width:100%;height:100%;border:0;}
#sdhVideoModal .vm-foot{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-top:14px;}
#sdhVideoModal .vm-title{color:#f3ead9;font-family:var(--font-sans);font-size:15px;margin:0;flex:1 1 320px;}
#sdhVideoModal .vm-yt{color:#e7c98d;font:700 14px/1.3 var(--font-sans);text-decoration:underline;min-height:44px;display:inline-flex;align-items:center;}
#sdhVideoModal .vm-close{position:fixed;top:18px;right:18px;width:48px;height:48px;border-radius:50%;border:1px solid rgba(255,255,255,.35);background:rgba(255,255,255,.12);color:#fff;font-size:22px;cursor:pointer;display:flex;align-items:center;justify-content:center;}
#sdhVideoModal .vm-close:hover{background:rgba(255,255,255,.24);}
#sdhVideoModal .vm-close:focus-visible,#sdhVideoModal .vm-yt:focus-visible{outline:2px solid #e7c98d;outline-offset:2px;}
</style>"""

PAGE_JS = """<script>
(function(){
  "use strict";
  var d = document;

  /* ---- category filters (library + featured share the same card markup) ---- */
  var cards = Array.prototype.slice.call(d.querySelectorAll(".vid-card"));
  var buttons = Array.prototype.slice.call(d.querySelectorAll(".vid-filter"));
  var featuredSection = d.getElementById("featured-videos");
  var countEl = d.getElementById("vidCount");
  function applyFilter(key){
    var shown = 0, featuredShown = 0;
    cards.forEach(function(c){
      var ok = key === "all" ||
               (key === "shorts" ? c.getAttribute("data-short") === "1"
                                 : c.getAttribute("data-cat") === key);
      c.style.display = ok ? "" : "none";
      if (ok) { shown++; if (featuredSection && featuredSection.contains(c)) featuredShown++; }
    });
    if (featuredSection) featuredSection.style.display = featuredShown ? "" : "none";
    if (countEl) countEl.textContent = key === "all"
      ? "Showing all " + shown + " videos"
      : "Showing " + shown + " of " + cards.length + " videos";
    buttons.forEach(function(b){
      var active = b.getAttribute("data-filter") === key;
      b.classList.toggle("active", active);
      b.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }
  buttons.forEach(function(b){
    b.addEventListener("click", function(){ applyFilter(b.getAttribute("data-filter")); });
  });

  /* ---- modal player: one youtube-nocookie iframe, created on demand ---- */
  var modal = d.getElementById("sdhVideoModal");
  var playerBox = modal.querySelector(".vm-player");
  var titleEl = modal.querySelector(".vm-title");
  var ytLink = modal.querySelector(".vm-yt");
  var closeBtn = modal.querySelector(".vm-close");
  var lastOpener = null;

  function openVideo(id, title, opener){
    lastOpener = opener || null;
    playerBox.innerHTML = "";
    var iframe = d.createElement("iframe");
    iframe.src = "https://www.youtube-nocookie.com/embed/" + id + "?rel=0&modestbranding=1&playsinline=1";
    iframe.title = title || "San Diego Hardwoods video";
    iframe.setAttribute("allow", "accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen");
    iframe.setAttribute("allowfullscreen", "allowfullscreen");
    iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    playerBox.appendChild(iframe);
    titleEl.textContent = title || "";
    ytLink.href = "https://www.youtube.com/watch?v=" + id;
    modal.classList.add("open");
    modal.removeAttribute("hidden");
    d.body.style.overflow = "hidden";
    closeBtn.focus();
  }
  function closeVideo(){
    modal.classList.remove("open");
    modal.setAttribute("hidden", "");
    playerBox.innerHTML = ""; /* stop playback */
    d.body.style.overflow = "";
    if (lastOpener && lastOpener.focus) lastOpener.focus();
  }
  Array.prototype.slice.call(d.querySelectorAll("[data-yt]")).forEach(function(btn){
    btn.addEventListener("click", function(){
      openVideo(btn.getAttribute("data-yt"), btn.getAttribute("data-vtitle"), btn);
    });
  });
  closeBtn.addEventListener("click", closeVideo);
  modal.addEventListener("click", function(e){ if (e.target === modal) closeVideo(); });
  d.addEventListener("keydown", function(e){
    if (!modal.classList.contains("open")) return;
    if (e.key === "Escape") { closeVideo(); return; }
    if (e.key !== "Tab") return;
    var f = [closeBtn, ytLink].filter(function(el){ return el.offsetParent !== null || el === closeBtn; });
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
  });
})();
</script>"""

HERO_TITLE = esc(display_title(HERO))
HERO_DESC = esc(re.sub(r"\s+", " ", (HERO.get("site_description") or HERO.get("description") or "")).strip())
HERO_IFRAME_SRC = HERO["embed_url"] + "?rel=0&modestbranding=1&playsinline=1"

MAIN = f"""{PAGE_CSS}
<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>Real Hardwood Floor Refinishing, Dustless Sanding &amp; Restoration Videos</h1>
  <p>This page documents <strong>real San Diego Hardwoods projects</strong> &mdash; every public video from our YouTube channel in one place. Watch our equipment at work on actual customer floors: true 100% dust-containment sanding with the <strong>Bona DCS 2.0 sealed system</strong> (dustless hardwood-floor sanding and refinishing), hardwood floor repairs, restoration of vintage and historic floors, custom staining, intensive deep cleaning and recoating, installation, and premium Bona finish work &mdash; the same craftsmanship behind our refinishing, restoration, and installation projects across San Diego County.</p>
  <div class="cta-row">
    <a class="btn btn-call" href="sms:+18586990072">Text Photos for a Free Assessment</a>
    <a class="btn btn-outline" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
  </div>
</section>

<section class="block" id="hero-video">
  <p class="eyebrow">Watch Now</p>
  <h2>{HERO_TITLE}</h2>
  <div class="video-frame">
    <div style="position:relative;padding-top:56.25%;height:0;overflow:hidden;">
      <iframe src="{esc(HERO_IFRAME_SRC)}" title="{HERO_TITLE}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen loading="lazy"></iframe>
    </div>
  </div>
  <p class="lede" style="margin-top:16px;">{HERO_DESC}</p>
  <p class="vid-meta">{nice_date(HERO["publish_date"])} &bull; {esc(HERO["duration_text"])} &bull; <a class="vid-yt-link" href="{esc(HERO["watch_url"])}" target="_blank" rel="noopener">Watch on YouTube &#8599;</a></p>
</section>

<section class="block" id="featured-videos">
  <p class="eyebrow">Start Here</p>
  <h2>Featured Project Videos</h2>
  <p class="lede">Six representative projects: true 100% dust-containment sanding with the Bona DCS 2.0 system, dramatic restorations, hardwood repairs, deep cleaning with visible results, and specialty finish work.</p>
  <div class="vid-grid vid-grid--featured">
{featured_cards}
  </div>
</section>

<section class="block" id="video-library">
  <h2>Complete Video Library &mdash; Every Public Upload</h2>
  <p class="lede">All {len(VIDEOS)} public videos from the San Diego Hardwoods YouTube channel, including Shorts. Filter by the kind of work you want to see, and click any video to watch it right here.</p>
  <div class="vid-filters" role="group" aria-label="Filter videos by category">
    {filters_html}
  </div>
  <p class="vid-count" id="vidCount" aria-live="polite">Showing all {len(VIDEOS)} videos</p>
  <div class="vid-grid">
{library_cards}
  </div>
  <div class="cta-row" style="justify-content:center;margin-top:34px;">
    <a class="btn btn-yt" href="{CHANNEL_URL}" target="_blank" rel="noopener"><span class="yt-ico" aria-hidden="true"><svg viewBox="0 0 28 20" width="22" height="16" focusable="false"><path fill="#FF0000" d="M27.4 3.1A3.5 3.5 0 0 0 25 .6C22.9 0 14 0 14 0S5.1 0 3 .6A3.5 3.5 0 0 0 .6 3.1 36.6 36.6 0 0 0 0 10a36.6 36.6 0 0 0 .6 6.9A3.5 3.5 0 0 0 3 19.4c2.1.6 11 .6 11 .6s8.9 0 11-.6a3.5 3.5 0 0 0 2.4-2.5A36.6 36.6 0 0 0 28 10a36.6 36.6 0 0 0-.6-6.9z"/><path fill="#fff" d="M11.2 14.3 18.5 10l-7.3-4.3z"/></svg></span>View All Videos on YouTube</a>
  </div>
</section>

<section class="block">
  <h2>Why Homeowners Throughout San Diego Watch Our Videos Before Hiring a Hardwood Floor Contractor</h2>
  <p class="lede">For more than <strong>35 years</strong>, San Diego Hardwoods has helped homeowners restore <strong>hardwood, engineered hardwood, bamboo, cork, and historic wood floors</strong> throughout San Diego County. These videos feature actual customer projects&mdash;not stock footage or demonstrations&mdash;so you can see our <strong>dust-contained sanding equipment</strong>, hardwood floor repair techniques, professional restoration process, and premium Bona finishing systems being used in real homes. All work is guaranteed, performed by a small crew of skilled and courteous craftsmen, and backed by a CSLB-licensed San Diego flooring contractor.</p>
  <p class="lede">Whether your floors need <strong>hardwood floor refinishing</strong>, repairs, deep cleaning, recoating, color changes, engineered hardwood restoration, or complete hardwood floor installation, we provide free phone &amp; photo assessments throughout <strong>La Jolla, Del Mar, Rancho Santa Fe, Encinitas, Carmel Valley, Solana Beach, Point Loma, Mission Hills, Coronado, Poway, Escondido</strong>, and communities across San Diego County.</p>

  <div class="cta-row" style="justify-content:center;">
    <a class="btn btn-call" href="tel:+18586990072">Call 858-699-0072</a>
    <a class="btn btn-outline" href="sms:+18586990072">Text Floor Photos</a>
  </div>

  <p style="text-align:center;margin:26px auto 0;font-size:15.5px;">
  <a href="https://www.sdhardwoods.com/recent_project_photo_gallery_1.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Real Hardwood Floor Refinishing Projects &rarr;</a>
  &nbsp;&bull;&nbsp; <a href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Professional Hardwood Floor Deep Cleaning &rarr;</a>
  &nbsp;&bull;&nbsp; <a href="https://www.sdhardwoods.com/contact_us.html" style="color:var(--brass-deep);font-weight:700;text-decoration:underline;">Contact San Diego Hardwoods</a>
  </p>
</section>

<div id="sdhVideoModal" role="dialog" aria-modal="true" aria-label="Video player" hidden>
  <button type="button" class="vm-close" aria-label="Close video player">&#10005;</button>
  <div class="vm-frame">
    <div class="vm-player"></div>
    <div class="vm-foot">
      <p class="vm-title"></p>
      <a class="vm-yt" href="{CHANNEL_URL}" target="_blank" rel="noopener">Watch on YouTube &#8599;</a>
    </div>
  </div>
</div>
{PAGE_JS}
"""

assemble(HEAD_META, JSONLD, GA, VCARD, "Our Refinishing Process Videos", MAIN,
         str(BUILD.parent / "videos_of_refinishing_process.html"))
