import json, sys, re

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

def cta_button_figure(img):
    # for nav-style image buttons (no alt caption needed, no lazy-figcaption)
    cls = f' class="{esc_attr(img["class"])}"' if img.get("class") else ""
    href = img.get("href") or img.get("src")
    return f'<a class="btn-img-link" href="{esc_attr(href)}"><img src="{esc_attr(img["src"])}" alt="{esc_attr(img["alt"])}"{cls} loading="lazy" style="max-width:220px;border-radius:10px;"></a>'

def deepclean_cta_card(img, heading, body_html):
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

def main():
    in_json = sys.argv[1]
    out_html = sys.argv[2]
    with open(in_json, encoding="utf-8") as f:
        data = json.load(f)

    modules = data["modules"]
    standalone = data["standalone"]

    real_modules = [m for m in modules if m["title"]]
    nav_button_imgs = []  # CALL OR TEXT NOW / NEXT PAGE buttons
    ultra_clean_imgs = []  # deep-clean CTA images

    for m in modules:
        if m["title"] is None:
            for img in m["images"]:
                nav_button_imgs.append(img)
    for m in real_modules:
        # any image beyond the first 2 in a titled module is an extra nav-style image
        for img in m["images"][2:]:
            nav_button_imgs.append(img)

    for img in standalone:
        src_l = img["src"].lower()
        if "ultra clean" in src_l:
            ultra_clean_imgs.append(img)
        else:
            nav_button_imgs.append(img)

    lines = []

    # top deep-clean CTA (first ultra-clean image, if any)
    if ultra_clean_imgs:
        lines.append("<!-- TOP_DEEPCLEAN_CTA -->")
        lines.append(json.dumps(ultra_clean_imgs[0]))

    lines.append("<!-- PROJECT_CARDS_START -->")
    for m in real_modules:
        before = m["images"][0]
        after = m["images"][1] if len(m["images"]) > 1 else None
        title = m["title"]
        lines.append('<div class="card" style="margin-bottom:28px;">')
        lines.append(f'  <h3 style="text-align:left;">{title}</h3>')
        lines.append('  <div class="gallery" style="grid-template-columns:1fr 1fr;">')
        lines.append('    ' + figure(before))
        if after:
            lines.append('    ' + figure(after))
        lines.append('  </div>')
        lines.append('</div>')
    lines.append("<!-- PROJECT_CARDS_END -->")

    if len(ultra_clean_imgs) > 1:
        lines.append("<!-- BOTTOM_DEEPCLEAN_CTA -->")
        lines.append(json.dumps(ultra_clean_imgs[1]))

    lines.append("<!-- NAV_BUTTONS -->")
    for img in nav_button_imgs:
        lines.append('  ' + cta_button_figure(img))

    with open(out_html, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # also dump summary counts
    with open(out_html + ".summary.txt", "w", encoding="utf-8") as f:
        total_rendered = sum(len(m["images"][:2]) for m in real_modules) + len(nav_button_imgs) + len(ultra_clean_imgs)
        f.write(f"real_modules: {len(real_modules)}\n")
        f.write(f"ultra_clean_imgs: {len(ultra_clean_imgs)}\n")
        f.write(f"nav_button_imgs: {len(nav_button_imgs)}\n")
        f.write(f"total images rendered (should equal doc total): {total_rendered}\n")
        f.write(f"doc total from extraction: {data['total_img_tags_in_doc']}\n")

if __name__ == "__main__":
    main()
