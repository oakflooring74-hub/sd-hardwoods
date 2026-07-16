# -*- coding: utf-8 -*-
import re, json, sys
from pathlib import Path

# build/scripts/common/build_page.py
BUILD = Path(__file__).resolve().parent.parent.parent   # -> build/
REPO_ROOT = BUILD.parent                                 # -> repo root (where the live .html pages live)
CHROME = str(BUILD / "chrome")
RAW = BUILD / "raw-source"
DATA = BUILD / "data"

def rd(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def esc_attr(s):
    if s is None:
        return ""
    return s.replace('"', "&quot;")

def figure(img):
    cls = f' class="{esc_attr(img["class"])}"' if img.get("class") else ""
    href = img.get("href") or img.get("src")
    fig = f'<figure><a href="{esc_attr(href)}"><img src="{esc_attr(img["src"])}" alt="{esc_attr(img["alt"])}"{cls} loading="lazy"></a>'
    if img.get("caption"):
        fig += f'<figcaption>{img["caption"]}</figcaption>'
    fig += '</figure>'
    return fig

def cta_button(img, extra_style=""):
    cls = f' class="{esc_attr(img["class"])}"' if img.get("class") else ""
    href = img.get("href") or img.get("src")
    return (f'<a class="btn-img-link" href="{esc_attr(href)}">'
            f'<img src="{esc_attr(img["src"])}" alt="{esc_attr(img["alt"])}"{cls} loading="lazy" '
            f'style="max-width:220px;border-radius:10px;{extra_style}"></a>')

def deepclean_cta(img, heading, body_html):
    href = img.get("href") or img.get("src")
    return f'''  <div class="card cta-card">
    <div class="cta-copy">
      <h3>{heading}</h3>
      {body_html}
    </div>
    <div class="cta-media">
      <a href="{esc_attr(href)}">
        <img src="{esc_attr(img["src"])}" alt="{esc_attr(img["alt"])}" loading="lazy">
      </a>
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
                           bottom_cta_heading, bottom_cta_body):
    with open(gallery_json_path, encoding="utf-8") as f:
        data = json.load(f)
    modules = data["modules"]
    standalone = data["standalone"]

    real_modules = [m for m in modules if m["title"]]
    nav_button_imgs = []
    ultra_clean_imgs = []

    for m in modules:
        if m["title"] is None:
            for img in m["images"]:
                nav_button_imgs.append(img)
    for m in real_modules:
        for img in m["images"][2:]:
            nav_button_imgs.append(img)
    for img in standalone:
        if "ultra clean" in img["src"].lower():
            ultra_clean_imgs.append(img)
        else:
            nav_button_imgs.append(img)

    parts = []
    parts.append('<section class="block">')
    parts.append('  <div class="gallery-intro">')
    parts.append(intro_html)
    parts.append('  </div>')

    if ultra_clean_imgs:
        parts.append(deepclean_cta(ultra_clean_imgs[0], top_cta_heading, top_cta_body))

    for m in real_modules:
        before = m["images"][0]
        after = m["images"][1] if len(m["images"]) > 1 else None
        parts.append('  <div class="card" style="margin:28px 0;">')
        parts.append(f'    <h3 style="text-align:left;">{m["title"]}</h3>')
        parts.append('    <div class="gallery" style="grid-template-columns:1fr 1fr;">')
        parts.append('      ' + figure(before))
        if after:
            parts.append('      ' + figure(after))
        parts.append('    </div>')
        parts.append('  </div>')

    if len(ultra_clean_imgs) > 1:
        parts.append(deepclean_cta(ultra_clean_imgs[1], bottom_cta_heading, bottom_cta_body))

    if nav_button_imgs:
        parts.append('  <div class="cta-row" style="justify-content:center;flex-wrap:wrap;margin-top:12px;">')
        for img in nav_button_imgs:
            parts.append('    ' + cta_button(img))
        parts.append('  </div>')

    parts.append('</section>')

    total_rendered = sum(min(2, len(m["images"])) for m in real_modules) + len(nav_button_imgs) + len(ultra_clean_imgs)
    check = {
        "real_modules": len(real_modules),
        "ultra_clean_imgs": len(ultra_clean_imgs),
        "nav_button_imgs": len(nav_button_imgs),
        "total_rendered": total_rendered,
        "doc_total": data["total_img_tags_in_doc"],
        "match": total_rendered == data["total_img_tags_in_doc"],
    }
    return "\n".join(parts), check


def extract_head_pieces(raw_doc):
    pieces = {}
    pieces["title"] = extract_one(r'<title>(.*?)</title>', raw_doc, group=1)
    pieces["desc_meta"] = extract_one(r'<meta[^>]+name="[Dd][Ee][Ss][Cc][Rr][Ii][Pp][Tt][Ii][Oo][Nn]"[^>]*/?>', raw_doc)
    pieces["canonical"] = extract_one(r'<link[^>]+rel="canonical"[^>]*/?>', raw_doc)
    pieces["uacompat"] = extract_one(r'<meta http-equiv="X-UA-Compatible"[^>]*/?>', raw_doc, required=False) or ""
    pieces["generator"] = extract_one(r'<meta name="Generator"[^>]*/?>', raw_doc, required=False) or ""
    css_links = []
    for cid in ["globalCSS", "themeCSS", "listCSS", "extensionsCSS"]:
        tag = extract_one(r'<link[^>]+id="%s"[^>]*/?>' % cid, raw_doc, required=False)
        if tag:
            css_links.append(tag)
    pieces["css_links"] = "\n\t".join(css_links)
    pieces["yahoo_script"] = extract_one(
        r'<script type="text/javascript">\s*var \$D.*?</script>', raw_doc, required=False) or ""
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

    top_html = top_html.replace("__VCARD_DESC__", head["vcard_desc"])
    scrollhint_html = scrollhint_html.replace("__SCROLL_TOPIC__", cfg["scroll_topic"])

    jsonld = "\n".join(head["jsonld_blocks"])

    gallery_html, check = build_gallery_section(
        cfg["gallery_json"], cfg["intro_html"],
        cfg["top_cta_heading"], cfg["top_cta_body"],
        cfg["bottom_cta_heading"], cfg["bottom_cta_body"],
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

    html = f'''<!DOCTYPE html><html lang="en">
<head xmlns="">
  <meta charset="utf-8"><base href="https://www.sdhardwoods.com/">{head["uacompat"]}{head["generator"]}{head["desc_meta"]}
\t{head["canonical"]}
\t{head["css_links"]}{head["yahoo_script"]}
\t<title>{head["title"]}</title>
{jsonld}{head["ga_script"]}
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
    <a class="btn btn-call" href="tel:8586990072">&#9742; Call or Text 858-699-0072</a>
    <a class="btn btn-outline" href="{cfg['sms_href']}">Text Photos for a Free Assessment</a>
  </div>
</section>

<section class="block">
  <div class="video-frame">
    <div id="heroVideoMount"></div>
  </div>
  <div class="video-cta">
    <p><strong style="color:var(--cta-red);">{cfg['video_cta_strong']}</strong> Text photos of your project to start your professional assessment.</p>
    <a class="btn btn-call" href="{cfg['sms_href']}">Schedule a Phone Consultation</a>
  </div>
</section>
{video_script}

{gallery_html}

</main>
{footer_html}
{scrollhint_html}
</body>
</html>
'''

    with open(cfg["out_path"], "w", encoding="utf-8") as f:
        f.write(html)

    return check


CONFIGS = [
    {
        "name": "gallery3",
        "raw_path": str(RAW / "recent_project_photo_gallery_3.html"),
        "gallery_json": str(DATA / "recent_project_photo_gallery_3" / "modules.json"),
        "out_path": str(REPO_ROOT / "recent_project_photo_gallery_3.html"),
        "scroll_topic": "Real Hardwood Floor Projects #41&ndash;50",
        "h1": "Recent San Diego Hardwood Flooring Projects Featuring Expert Refinishing, Restoration, Dust Containment Sanding &amp; Custom Installation",
        "hero_p1": "Explore recent San Diego hardwood flooring transformations featuring expert refinishing, restoration, repairs, custom installation, dust containment sanding, deep cleaning, engineered hardwood, bamboo flooring, and the craftsmanship that has earned homeowners&rsquo; trust for more than 35 years.",
        "hero_p2": "Need advice on refinishing, repairs or installation? <strong>Call or text 858-699-0072</strong> to discuss your project.",
        "sms_href": "sms:+18586990072?&body=Hi%20San%20Diego%20Hardwoods,%20I%20have%20photos%20of%20my%20floors%20I%20would%20like%20to%20send%20for%20a%20consultation.",
        "video_cta_strong": "Professional Refinishing Results.",
        "yt_id": "hq0rLWe1C8o",
        "yt_params": "rel=0&modestbranding=1&playsinline=1&autoplay=0&mute=1&controls=1&loop=1&playlist=hq0rLWe1C8o&start=14&enablejsapi=1",
        "video_name": "Hardwood Floor Refinishing Process in San Diego",
        "video_desc": "See the professional hardwood floor refinishing process in San Diego. Expert craftsmanship for beautiful, durable floors.",
        "video_thumb": "https://www.sdhardwoods.com/images/thumbnails/Refinish_wood_floors_san_diego.png",
        "intro_html": '''    <h2>Real San Diego Hardwood Floor Projects: #41&ndash;#50</h2>
    <p class="lede">Before-and-after results from homes across Solana Beach, La Jolla, Rancho Santa Fe, Del Mar, Encinitas, Pacific Beach, and throughout San Diego County.</p>''',
        "top_cta_heading": "Think Your Hardwood Floors Need Sanding?",
        "top_cta_body": "<p>Many hardwood floors that appear dull, dirty, sticky, cloudy or worn can often be restored without sanding. Our commercial-grade Bona Power Scrubber removes embedded dirt, old cleaners, wax buildup, grease, haze and contaminants that ordinary mopping leaves behind. We professionally deep clean hardwood, engineered wood, bamboo, luxury vinyl plank (LVP), laminate and specialty wood flooring throughout San Diego County.</p><p>Before spending thousands on refinishing, find out if professional deep cleaning is all your floors really need.</p>",
        "bottom_cta_heading": "Deep Cleaning for Hardwood, Wire-Brushed &amp; Matte Floors",
        "bottom_cta_body": "<p>Professional deep cleaning and protective recoating remove embedded dirt, revive the natural beauty of hardwood floors, and help extend the life of your finish. See when deep cleaning is the right solution before investing in full refinishing.</p>",
    },
    {
        "name": "gallery4",
        "raw_path": str(RAW / "recent_project_photo_gallery_4.html"),
        "gallery_json": str(DATA / "recent_project_photo_gallery_4" / "modules.json"),
        "out_path": str(REPO_ROOT / "recent_project_photo_gallery_4.html"),
        "scroll_topic": "Real Hardwood Floor Projects #61&ndash;80",
        "h1": "Recent San Diego Hardwood Flooring Projects Featuring Expert Restoration, Deep Cleaning, Dust Containment Sanding, Repairs &amp; Custom Installation",
        "hero_p1": "Browse real hardwood flooring projects completed throughout San Diego County, including professional deep cleaning, dustless refinishing, restoration, repairs, custom installations, and premium Bona finishing systems. Every project shown was completed by San Diego Hardwoods using over 35 years of hands-on hardwood flooring experience.",
        "hero_p2": "Explore recent San Diego hardwood flooring projects featuring expert restoration, refinishing, repairs, dust containment sanding, deep cleaning, custom installation, and specialty finishes. <strong>Call or text 858-699-0072</strong> to discuss your project.",
        "sms_href": "sms:+18586990072?&body=Hi%20San%20Diego%20Hardwoods,%20I%20have%20photos%20of%20my%20engineered%20maple%20floors%20I%20would%20like%20to%20send%20for%20a%20consultation.",
        "video_cta_strong": "Expert Engineered Floor Refinishing.",
        "yt_id": "7mhqGYozb1o",
        "yt_params": "rel=0&modestbranding=1&playsinline=1&autoplay=0&mute=1&controls=1&loop=1&playlist=7mhqGYozb1o&enablejsapi=1",
        "video_name": "Engineered Maple Floor Refinishing in San Diego",
        "video_desc": "Expert refinishing for engineered maple hardwood floors in San Diego. Restore your floors with our professional dust-free process.",
        "video_thumb": "https://www.sdhardwoods.com/images/thumbnails/engineered_maple_floor_refinishing_san_diego.png",
        "intro_html": '''    <h2>San Diego Hardwood Flooring Gallery: Projects #61&ndash;#80</h2>
    <p class="lede">Before-and-after results from homes across Del Mar, Rancho Santa Fe, Carmel Valley, Golden Hill, Encinitas, Coronado, Pacific Beach, and throughout San Diego County.</p>''',
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
    with open(str(DATA / "build_page_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
