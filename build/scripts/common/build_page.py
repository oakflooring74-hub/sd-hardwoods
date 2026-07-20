# -*- coding: utf-8 -*-
import re, json, sys
from pathlib import Path

# build/scripts/common/build_page.py
BUILD = Path(__file__).resolve().parent.parent.parent   # -> build/
REPO_ROOT = BUILD.parent                                 # -> repo root (where the live .html pages live)
CHROME = str(BUILD / "chrome")
RAW = BUILD / "raw-source"
DATA = BUILD / "data"

sys.path.insert(0, str(BUILD / "scripts" / "common"))
from assemble_page import gallery_progress_html
from public_business_rules import (
    sanitize_public_jsonld, consolidate_business_jsonld, build_webpage_service_graph,
)
from alt_expand import clean_caption, append_sentences, strip_html_tags


def _replace_generic_service_array(jsonld_html, new_graph):
    """Swap the generic, identical-on-every-page 5-Service array that
    `consolidate_business_jsonld()` leaves behind for a real, page-specific
    WebPage + Service (+ OfferCatalog) graph (2026-07-19 schema milestone).
    `new_graph` entities reference the canonical #local entity by @id
    (already present elsewhere in `jsonld_html`), so nothing is re-declared.
    """
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', jsonld_html, re.DOTALL)
    out_blocks = []
    replaced = False
    for b in blocks:
        obj = json.loads(b)
        if isinstance(obj, list) and obj and all(isinstance(x, dict) and x.get("@type") == "Service" for x in obj):
            for entity in new_graph:
                out_blocks.append('<script type="application/ld+json">\n' + json.dumps(entity, indent=1, ensure_ascii=False) + '\n</script>')
            replaced = True
        else:
            out_blocks.append('<script type="application/ld+json">\n' + json.dumps(obj, indent=1, ensure_ascii=False) + '\n</script>')
    if not replaced:
        raise AssertionError("_replace_generic_service_array: no generic Service array found to replace")
    return "\n".join(out_blocks)

def rd(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def esc_attr(s):
    if s is None:
        return ""
    return s.replace('"', "&quot;")

def figure(img, project_title=None):
    cls = f' class="{esc_attr(img["class"])}"' if img.get("class") else ""
    href = img.get("href") or img.get("src")
    # Aggressive alt-text expansion (2026-07-20): this image's own per-image alt
    # (already rich) is preserved verbatim as the prefix. Appended: the project's
    # own module heading (already visible directly above as <h3>, describing both
    # photos and the project as a whole) and this image's own visible caption --
    # both already-verified, already-published text about this exact project.
    base_alt = img["alt"]
    cap = clean_caption(img.get("caption"))
    title_sentence = strip_html_tags(project_title) if project_title else None
    alt = append_sentences(base_alt, title_sentence, cap)
    fig = f'<figure><a href="{esc_attr(href)}"><img src="{esc_attr(img["src"])}" alt="{esc_attr(alt)}"{cls} loading="lazy"></a>'
    if img.get("caption"):
        fig += f'<figcaption>{img["caption"]}</figcaption>'
    fig += '</figure>'
    return fig

def deepclean_cta(heading, body_html):
    # Milestone 2.1: text-only card -- the legacy "ultra clean button" graphic that used
    # to sit beside this copy is excluded from generated output (see LEGACY-ASSET notes).
    return f'''  <div class="card cta-card">
    <div class="cta-copy">
      <h3>{heading}</h3>
      {body_html}
      <p><a class="btn btn-outline" href="https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html">See Our Deep Cleaning &amp; Recoating Service &rarr;</a></p>
    </div>
  </div>'''

def extract_one(pattern, doc, flags=re.IGNORECASE | re.DOTALL, group=0, required=True):
    m = re.search(pattern, doc, flags)
    if not m:
        if required:
            raise Exception("pattern not found: " + pattern[:80])
        return None
    return m.group(group)

def extract_all(pattern, doc, flags=re.IGNORECASE | re.DOTALL):
    return [m.group(0) for m in re.finditer(pattern, doc, flags)]

def build_gallery_section(gallery_json_path, intro_html, top_cta_heading, top_cta_body,
                           bottom_cta_heading, bottom_cta_body, gallery_index=None):
    with open(gallery_json_path, encoding="utf-8") as f:
        data = json.load(f)
    modules = data["modules"]
    standalone = data["standalone"]

    real_modules = [m for m in modules if m["title"]]

    # Milestone 2.1: legacy image-buttons (NEXT PAGE / CALL OR TEXT / ultra clean, etc.)
    # are excluded from generated output entirely. They used to be collected from
    # title-less modules, trailing module images, and standalone records and rendered
    # at the bottom of the page; their navigation jobs are covered by the site's real
    # navigation and the text CTA cards. Counted here only for the build check.
    excluded_imgs = []
    for m in modules:
        if m["title"] is None:
            excluded_imgs.extend(m["images"])
    for m in real_modules:
        excluded_imgs.extend(m["images"][2:])
    excluded_imgs.extend(standalone)

    parts = []
    parts.append('<section class="block">')
    parts.append('  <div class="gallery-intro">')
    parts.append(intro_html)
    parts.append('  </div>')

    if gallery_index is not None:
        parts.append(gallery_progress_html(gallery_index))

    parts.append(deepclean_cta(top_cta_heading, top_cta_body))

    for m in real_modules:
        before = m["images"][0]
        after = m["images"][1] if len(m["images"]) > 1 else None
        parts.append('  <div class="card" style="margin:28px 0;">')
        parts.append(f'    <h3 style="text-align:left;">{m["title"]}</h3>')
        parts.append('    <div class="gallery" style="grid-template-columns:1fr 1fr;">')
        parts.append('      ' + figure(before, m["title"]))
        if after:
            parts.append('      ' + figure(after, m["title"]))
        parts.append('    </div>')
        parts.append('  </div>')

    parts.append(deepclean_cta(bottom_cta_heading, bottom_cta_body))

    parts.append('</section>')

    total_rendered = sum(min(2, len(m["images"])) for m in real_modules)
    check = {
        "real_modules": len(real_modules),
        "excluded_legacy_imgs": len(excluded_imgs),
        "total_rendered": total_rendered,
        "doc_total": data["total_img_tags_in_doc"],
        "match": total_rendered + len(excluded_imgs) == data["total_img_tags_in_doc"],
    }
    return "\n".join(parts), check


def extract_head_pieces(raw_doc):
    pieces = {}
    pieces["title"] = extract_one(r'<title>(.*?)</title>', raw_doc, group=1)
    desc_meta = extract_one(r'<meta[^>]+name="[Dd][Ee][Ss][Cc][Rr][Ii][Pp][Tt][Ii][Oo][Nn]"[^>]*/?>', raw_doc)
    # Milestone 2.9: normalize the legacy uppercase `name="DESCRIPTION"` attribute
    # and drop the unused `id="mDescription"` -- technically-clean consistency
    # with the other 8 pages' `name="description"`; content is untouched.
    desc_meta = re.sub(r'name="[Dd][Ee][Ss][Cc][Rr][Ii][Pp][Tt][Ii][Oo][Nn]"', 'name="description"', desc_meta)
    desc_meta = re.sub(r'\s+id="mDescription"', '', desc_meta)
    pieces["desc_meta"] = desc_meta
    pieces["canonical"] = extract_one(r'<link[^>]+rel="canonical"[^>]*/?>', raw_doc)
    css_links = []
    for cid in ["globalCSS", "themeCSS", "listCSS"]:
        tag = extract_one(r'<link[^>]+id="%s"[^>]*/?>' % cid, raw_doc, required=False)
        if tag:
            css_links.append(tag)
    css_links = "\n\t".join(css_links)
    # Turbify-CSS-localization milestone (2026-07-20): globalCSS/themeCSS/listCSS were live
    # requests to s.turbifycdn.com on every page load; their exact served content is now
    # preserved verbatim in assets/legacy-css/ (see docs/2026-07-prelaunch-audit.md).
    # extensionsCSS (a mislabeled .js file loaded via rel="stylesheet") is no longer extracted
    # at all -- Turbify/Yahoo-remnants-removal milestone (2026-07-20): confirmed unused (never
    # parsed as CSS, never referenced by anything on the page) and dropped.
    css_links = css_links.replace(
        "https://s.turbifycdn.com/lm/lib/smb/css/hosting/yss/v2/mc_global.195798.css",
        "/assets/legacy-css/mc_global.195798.css",
    ).replace(
        "https://s.turbifycdn.com/lm/themes/yhoo/ga/evident/vanilla_bean/palette1/1.0.1/en-us/theme.css",
        "/assets/legacy-css/theme.css",
    ).replace(
        "https://s.turbifycdn.com/lm/css/hosting/yss/v2/apps/beforenafter_1.css",
        "/assets/legacy-css/beforenafter_1.css",
    )
    pieces["css_links"] = css_links
    # Turbify/Yahoo-remnants-removal milestone (2026-07-20): the raw source's inline
    # `var $D = YAHOO.util.Dom; ...` block (previously extracted here as "yahoo_script" and
    # emitted verbatim) referenced a `window.YAHOO` global that no script on this page ever
    # defines -- its first statement always threw ReferenceError, so none of it (including the
    # custom Logger namespace) ever ran, and nothing else on the page reads any of the
    # variables it declared. Confirmed dead; no longer extracted or emitted.
    pieces["jsonld_blocks"] = extract_all(r'<script type="application/ld\+json">.*?</script>', raw_doc)
    ga = extract_one(
        r'<!--Google Analytics Tracking Code-->\s*<script[^>]*>.*?</script>',
        raw_doc, required=False)
    pieces["ga_script"] = ga or ""
    org = extract_one(r'<span class="organization-name">(.*?)</span>', raw_doc, group=1)
    pieces["vcard_desc"] = org.strip()
    return pieces


def build_page(cfg):
    raw = rd(cfg["raw_path"])
    head = extract_head_pieces(raw)

    site_css = rd(CHROME + r"\site_css.html")
    darkmode_boot = rd(CHROME + r"\darkmode_boot_scripts.html")
    top_html = rd(CHROME + r"\top.html")
    footer_html = rd(CHROME + r"\footer.html")
    scrollhint_html = rd(CHROME + r"\scrollhint_and_toggle.html")
    lightbox_html = rd(CHROME + r"\lightbox.html")

    top_html = top_html.replace("__VCARD_DESC__", head["vcard_desc"])
    scrollhint_html = scrollhint_html.replace("__SCROLL_TOPIC__", cfg["scroll_topic"])

    # Milestone 2.6: raw-source schema passes through the shared
    # public-business-rules filter (no PostalAddress, official YouTube channel).
    # Schema milestone (2026-07-19): consolidate the raw source's duplicate,
    # unlinked business declarations into references to the one canonical
    # #local entity (see public_business_rules.py) -- must run after sanitize
    # so YouTube-handle normalization happens before the sameAs dedupe.
    jsonld = sanitize_public_jsonld("\n".join(head["jsonld_blocks"]))
    jsonld = consolidate_business_jsonld(jsonld)
    # Image-localization milestone (2026-07-19): the raw-source VideoObject block
    # kept above (see the "do NOT duplicate video_jsonld" note below) still carries
    # its thumbnailUrl as an absolute Turbify URL; `cfg["video_thumb"]` already
    # holds the correct local path for this same file, so reuse it as the target.
    jsonld = jsonld.replace(
        "https://www.sdhardwoods.com" + cfg["video_thumb"], cfg["video_thumb"])
    if "service_content" in cfg:
        new_graph = build_webpage_service_graph(page_url=cfg["canonical"], **cfg["service_content"])
        jsonld = _replace_generic_service_array(jsonld, new_graph)
    analytics_html = rd(CHROME + r"\analytics.html")

    gallery_html, check = build_gallery_section(
        cfg["gallery_json"], cfg["intro_html"],
        cfg["top_cta_heading"], cfg["top_cta_body"],
        cfg["bottom_cta_heading"], cfg["bottom_cta_body"],
        gallery_index=cfg.get("gallery_index"),
    )

    video_script = f'''<script type="text/javascript">
(function () {{
    var YT_ID = "{cfg['yt_id']}";
    var params = "{cfg['yt_params']}";
    var src = "https://www.youtube-nocookie.com/embed/" + YT_ID + "?" + params;

    var mount = document.getElementById("heroVideoMount");
    var iframe = document.createElement("iframe");
    iframe.src = src;
    iframe.style.position = "absolute";
    iframe.style.top = "0";
    iframe.style.left = "0";
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.setAttribute("allowfullscreen", "allowfullscreen");

    mount.appendChild(iframe);
}})();
</script>'''

    video_jsonld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "{cfg['video_name']}",
  "description": "{cfg['video_desc']}",
  "thumbnailUrl": "{cfg['video_thumb']}",
  "uploadDate": "2026-07-04",
  "contentUrl": "https://www.youtube-nocookie.com/embed/{cfg['yt_id']}",
  "embedUrl": "https://www.youtube-nocookie.com/embed/{cfg['yt_id']}"
}}
</script>'''

    # jsonld already includes the VideoObject block (it's one of the extracted script tags),
    # so we do NOT duplicate video_jsonld -- just reuse extracted jsonld directly.

    # Milestone 2.4: canonical comes from the approved canonical map (cfg), not from the
    # raw source -- gallery 3's live page carries a wrong canonical URL
    # (recent_project_gallery_3.html, a URL that 301s to the real page). The obsolete
    # Universal Analytics snippet (UA-20793161-1 / _gaq / ga.js) extracted from the raw
    # source is likewise no longer emitted; since Milestone 2.6 the one shared GA4
    # implementation (chrome/analytics.html) is injected instead.
    html = f'''<!DOCTYPE html><html lang="en">
<head xmlns="">
  <meta charset="utf-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">{head["desc_meta"]}
\t<link href="{cfg["canonical"]}" rel="canonical">
\t{head["css_links"]}
\t<title>{head["title"]}</title>
{jsonld}
{analytics_html}
{site_css}
{darkmode_boot}
</head>
<body class="lo_layout2wt" dir="ltr" spellcheck="false">
{top_html}
<main>

<section class="hero">
  <div class="kicker">Est. 1990 &bull; San Diego's Finest Hardwood Flooring Specialist</div>
  <h1>{cfg['h1']}</h1>
  <p>{cfg['hero_p1']}</p>
  <p>{cfg['hero_p2']}</p>
  <div class="cta-row">
    <a class="btn btn-call" href="tel:+18586990072">&#9742; Call 858-699-0072</a>
    <a class="btn btn-outline" href="{cfg['sms_href']}">Text Floor Photos</a>
  </div>
</section>

<section class="block">
  <div class="video-frame">
    <div id="heroVideoMount"></div>
  </div>
  <div class="video-cta">
    <p><strong style="color:var(--cta-red);">{cfg['video_cta_strong']}</strong> Text photos of your project to start your professional assessment.</p>
    <a class="btn btn-call" href="{cfg['sms_href']}">Text Floor Photos</a>
  </div>
</section>
{video_script}

{gallery_html}

</main>
{footer_html}
{scrollhint_html}
{lightbox_html}
</body>
</html>
'''

    with open(cfg["out_path"], "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    return check


CONFIGS = [
    {
        "name": "gallery3",
        "gallery_index": 2,
        "canonical": "https://www.sdhardwoods.com/recent_project_photo_gallery_3.html",
        "service_content": {
            "page_id_slug": "service",
            "page_name": "Recent San Diego Hardwood Flooring Projects Featuring Expert Refinishing, Restoration, Dust Containment Sanding & Custom Installation",
            "page_description": "Before-and-after results from homes across Solana Beach, La Jolla, Rancho Santa Fe, Del Mar, Encinitas, and Pacific Beach, including rare solid yellow birch restoration and wide-plank French oak installation.",
            "service_name": "Hardwood Floor Refinishing, Restoration & Custom Installation Proof Gallery",
            "service_description": "Real completed hardwood flooring projects (#41-#50) showing refinishing, restoration, dust containment sanding, and custom installation throughout San Diego County.",
            "service_types": ["Hardwood floor refinishing", "Hardwood floor restoration", "Dust-contained sanding", "Custom hardwood installation", "Wide-plank hardwood installation", "Solid yellow birch restoration"],
            "area_served": ["San Diego County", "Solana Beach", "La Jolla", "Rancho Santa Fe", "Del Mar", "Encinitas", "Pacific Beach"],
            "offer_catalog_name": "Project Types Shown",
            "offer_items": [
                ("Hardwood Floor Refinishing & Sanding", "Dust-contained sanding and refinishing shown in real completed San Diego projects."),
                ("Hardwood Floor Restoration", "Restoration projects including rare species such as solid yellow birch."),
                ("Custom Hardwood Installation", "Wide-plank French oak and other custom installation projects over concrete and traditional subfloors."),
            ],
        },
        "raw_path": str(RAW / "recent_project_photo_gallery_3.html"),
        "gallery_json": str(DATA / "recent_project_photo_gallery_3" / "modules.json"),
        "out_path": str(REPO_ROOT / "recent_project_photo_gallery_3.html"),
        "scroll_topic": "Real Hardwood Floor Projects #41&ndash;50",
        "h1": "Recent San Diego Hardwood Flooring Projects Featuring Expert Refinishing, Restoration, Dust Containment Sanding &amp; Custom Installation",
        "hero_p1": "Explore recent San Diego hardwood flooring transformations featuring expert refinishing, restoration, repairs, custom installation, dust containment sanding, deep cleaning, engineered hardwood, bamboo flooring, and the craftsmanship that has earned homeowners&rsquo; trust for more than 35 years.",
        "hero_p2": "Need advice on refinishing, repairs or installation? <strong>Call or text 858-699-0072</strong> to discuss your project.",
        "sms_href": "sms:+18586990072",
        "video_cta_strong": "Professional Refinishing Results.",
        "yt_id": "hq0rLWe1C8o",
        "yt_params": "rel=0&modestbranding=1&playsinline=1&autoplay=0&mute=1&controls=1&loop=1&playlist=hq0rLWe1C8o&start=14&enablejsapi=1",
        "video_name": "Hardwood Floor Refinishing Process in San Diego",
        "video_desc": "See the professional hardwood floor refinishing process in San Diego. Expert craftsmanship for beautiful, durable floors.",
        "video_thumb": "/images/thumbnails/Refinish_wood_floors_san_diego.png",
        "intro_html": '''    <h2>Real San Diego Hardwood Floor Projects: #41&ndash;#50</h2>
    <p class="lede">Before-and-after results from homes across Solana Beach, La Jolla, Rancho Santa Fe, Del Mar, Encinitas, Pacific Beach, and throughout San Diego County &mdash; including rare solid yellow birch restored in Del Mar, wide-plank French oak installed over concrete in a La Jolla estate, and dust-contained refinishing with custom stain and finish work.</p>''',
        "top_cta_heading": "Think Your Hardwood Floors Need Sanding?",
        "top_cta_body": "<p>Many hardwood floors that appear dull, dirty, sticky, cloudy or worn can often be restored without sanding. Our commercial-grade Bona Power Scrubber removes embedded dirt, old cleaners, wax buildup, grease, haze and contaminants that ordinary mopping leaves behind. We professionally deep clean hardwood, engineered wood, bamboo, luxury vinyl plank (LVP), laminate and specialty wood flooring throughout San Diego County.</p><p>Before spending thousands on refinishing, find out if professional deep cleaning is all your floors really need.</p>",
        "bottom_cta_heading": "Deep Cleaning for Hardwood, Wire-Brushed &amp; Matte Floors",
        "bottom_cta_body": "<p>Professional deep cleaning and protective recoating remove embedded dirt, revive the natural beauty of hardwood floors, and help extend the life of your finish. See when deep cleaning is the right solution before investing in full refinishing.</p>",
    },
    {
        "name": "gallery4",
        "gallery_index": 3,
        "canonical": "https://www.sdhardwoods.com/recent_project_photo_gallery_4.html",
        "service_content": {
            "page_id_slug": "service",
            "page_name": "Recent San Diego Hardwood Flooring Projects Featuring Expert Restoration, Deep Cleaning, Dust Containment Sanding, Repairs & Custom Installation",
            "page_description": "Before-and-after results from homes across Del Mar, Rancho Santa Fe, Carmel Valley, Golden Hill, Encinitas, Coronado, Pacific Beach, La Jolla Shores, and Santa Luz.",
            "service_name": "Hardwood Floor Restoration, Deep Cleaning & Custom Installation Proof Gallery",
            "service_description": "Real completed hardwood flooring projects (#61-#80) showing restoration, deep cleaning, dust containment sanding, repairs, and custom installation throughout San Diego County.",
            "service_types": ["Hardwood floor restoration", "Hardwood floor deep cleaning", "Dust-contained sanding", "Hardwood floor repairs", "Custom hardwood installation", "Bamboo floor restoration"],
            "area_served": ["San Diego County", "Del Mar", "Rancho Santa Fe", "Carmel Valley", "Golden Hill", "Encinitas", "Coronado", "Pacific Beach", "La Jolla Shores", "Santaluz", "Black Mountain Ranch", "Rancho Penasquitos"],
            "offer_catalog_name": "Project Types Shown",
            "offer_items": [
                ("Hardwood Floor Restoration", "Restoration projects shown in real before-and-after pairs, including confirmed walnut restoration work."),
                ("Hardwood Floor Deep Cleaning", "Deep-cleaning and recoating projects shown alongside full restoration work."),
                ("Custom Hardwood Installation", "Custom installation projects shown in real completed San Diego homes."),
            ],
        },
        "raw_path": str(RAW / "recent_project_photo_gallery_4.html"),
        "gallery_json": str(DATA / "recent_project_photo_gallery_4" / "modules.json"),
        "out_path": str(REPO_ROOT / "recent_project_photo_gallery_4.html"),
        "scroll_topic": "Real Hardwood Floor Projects #61&ndash;80",
        "h1": "Recent San Diego Hardwood Flooring Projects Featuring Expert Restoration, Deep Cleaning, Dust Containment Sanding, Repairs &amp; Custom Installation",
        "hero_p1": "Browse real hardwood flooring projects completed throughout San Diego County, including professional deep cleaning, dustless refinishing, restoration, repairs, custom installations, and premium Bona finishing systems. Every project shown was completed by San Diego Hardwoods using over 35 years of hands-on hardwood flooring experience.",
        "hero_p2": "Explore recent San Diego hardwood flooring projects featuring expert restoration, refinishing, repairs, dust containment sanding, deep cleaning, custom installation, and specialty finishes. <strong>Call or text 858-699-0072</strong> to discuss your project.",
        "sms_href": "sms:+18586990072",
        "video_cta_strong": "Expert Engineered Floor Refinishing.",
        "yt_id": "7mhqGYozb1o",
        "yt_params": "rel=0&modestbranding=1&playsinline=1&autoplay=0&mute=1&controls=1&loop=1&playlist=7mhqGYozb1o&enablejsapi=1",
        "video_name": "Engineered Maple Floor Refinishing in San Diego",
        "video_desc": "Expert refinishing for engineered maple hardwood floors in San Diego. Restore your floors with our professional dust-free process.",
        "video_thumb": "/images/thumbnails/engineered_maple_floor_refinishing_san_diego.png",
        "intro_html": '''    <h2>San Diego Hardwood Flooring Gallery: Projects #61&ndash;#80</h2>
    <p class="lede">Before-and-after results from homes across Del Mar, Rancho Santa Fe, Carmel Valley, Golden Hill, Encinitas, Coronado, Pacific Beach, and throughout San Diego County &mdash; including solid hickory refinished with matching butcher-block countertops in Rancho Santa Fe, a major termite-damage repair blended into vintage oak near La Jolla Shores, and sun-faded engineered oak restored in Santa Luz.</p>''',
        "top_cta_heading": "Not Every Hardwood Floor Needs Refinishing",
        "top_cta_body": "<p>Many dull, dirty, lightly scratched, or worn hardwood floors can be dramatically improved with our Bona Power Scrubber deep cleaning system and protective low-VOC recoat. We clean hardwood, engineered hardwood, bamboo, cork, laminate, and luxury vinyl plank floors throughout San Diego County. Discover when deep cleaning is the smarter alternative to full refinishing.</p>",
        "bottom_cta_heading": "Not Every Hardwood Floor Needs Refinishing",
        "bottom_cta_body": "<p>Many dull, dirty, lightly scratched, or worn hardwood floors can be restored with our Bona Power Scrubber deep cleaning system and protective low-VOC recoat. We clean hardwood, engineered hardwood, bamboo, cork, laminate, and luxury vinyl plank floors throughout San Diego County. Learn when deep cleaning is the smarter alternative to full refinishing.</p>",
    },
]


def main():
    results = {}
    for cfg in CONFIGS:
        check = build_page(cfg)
        results[cfg["name"]] = check
    with open(str(DATA / "build_page_results.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
