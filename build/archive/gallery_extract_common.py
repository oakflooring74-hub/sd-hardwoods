import re

attr_re = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')
img_re = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
a_open_re = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>', re.IGNORECASE)


def find_balanced_blocks(html, start_pattern, tag):
    """Find all top-level blocks starting with literal start_pattern (marking the opening
    <tag ...>) and ending at the matching close tag, tracking nested <tag>/</tag> depth."""
    open_re = re.compile(r'<' + tag + r'\b', re.IGNORECASE)
    close_re = re.compile(r'</' + tag + r'\s*>', re.IGNORECASE)
    blocks = []
    pos = 0
    while True:
        start = html.find(start_pattern, pos)
        if start == -1:
            break
        tag_end = html.index(">", start) + 1
        depth = 1
        i = tag_end
        while depth > 0:
            nopen = open_re.search(html, i)
            nclose = close_re.search(html, i)
            if not nclose:
                raise Exception("unbalanced tag, no close found for " + start_pattern)
            if nopen and nopen.start() < nclose.start():
                depth += 1
                i = nopen.end()
            else:
                depth -= 1
                i = nclose.end()
        blocks.append(html[start:i])
        pos = i
    return blocks


def get_tag_text(block, tag_open_pattern):
    """Extract inner text (subtags stripped) of FIRST tag matching tag_open_pattern regex
    (which must have one capture group = the tag name)."""
    m = re.search(tag_open_pattern, block, re.DOTALL)
    if not m:
        return None
    # tag_open_pattern only matches a distinguishing PREFIX of the opening tag (e.g. up to
    # class="modfield title") -- the real content starts after the tag's closing '>', which may
    # be many attributes further along (multi-line class strings, id=, rel=, etc).
    start = block.index(">", m.end()) + 1
    tagname = m.group(1)
    close = re.search(r'</' + tagname + r'\s*>', block[start:], re.IGNORECASE)
    if not close:
        return None
    inner = block[start:start + close.start()]
    inner = re.sub(r'<script\b.*?</script>', '', inner, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', inner)
    text = re.sub(r'\s+', ' ', text).strip()
    return text if text else None


def get_all_tag_texts(block, tag_open_pattern):
    """Like get_tag_text but returns a list of ALL non-overlapping matches' inner text."""
    results = []
    pos = 0
    while True:
        m = re.search(tag_open_pattern, block[pos:], re.DOTALL)
        if not m:
            break
        rel_end = m.end()
        abs_start = block.index(">", pos + rel_end) + 1
        tagname = m.group(1)
        close = re.search(r'</' + tagname + r'\s*>', block[abs_start:], re.IGNORECASE)
        if not close:
            break
        inner = block[abs_start:abs_start + close.start()]
        text_only = re.sub(r'<script\b.*?</script>', '', inner, flags=re.DOTALL | re.IGNORECASE)
        text_only = re.sub(r'<[^>]+>', '', text_only)
        text_only = re.sub(r'\s+', ' ', text_only).strip()
        if text_only:
            results.append(text_only)
        pos = abs_start + close.end()
    return results


def extract_imgs_with_href(snippet):
    """Return list of (raw_img_tag, attrs_dict, href_or_None) in document order."""
    results = []
    for im in img_re.finditer(snippet):
        img_tag = im.group(0)
        attrs = dict(attr_re.findall(img_tag))
        preceding = snippet[:im.start()]
        a_matches = list(a_open_re.finditer(preceding))
        href = None
        if a_matches:
            last_a = a_matches[-1]
            between = preceding[last_a.end():]
            if '</a>' not in between:
                href = last_a.group(1)
        results.append((img_tag, attrs, href))
    return results


def img_item(attrs, href, desc=None):
    # class attribute values in this raw source often span multiple lines with erratic
    # indentation (a copy-editing artifact of the Turbify CMS, not a meaningful token) --
    # collapse to single spaces for output tidiness. This changes zero class TOKENS, only
    # incidental whitespace between them, consistent with how the already-approved homepage
    # rebuild normalized its own multi-line class attributes.
    cls = re.sub(r'\s+', ' ', attrs.get("class", "")).strip()
    return {
        "src": attrs.get("src", ""),
        "alt": attrs.get("alt", ""),
        "class": cls,
        "href": href,
        "desc": desc,
    }


def figure_html(item, label=None, class_extra=""):
    """Render one <figure> for a gallery image item (dict with src/alt/class/href/desc)."""
    cls_attr = f' class="{item["class"]}{class_extra}"' if item.get("class") else (
        f' class="{class_extra.strip()}"' if class_extra else "")
    href = item.get("href") or item["src"]
    cap_text = None
    if item.get("desc"):
        cap_text = f"{label} &mdash; {item['desc']}" if label else item["desc"]
    elif label:
        cap_text = label
    cap = f"<figcaption>{cap_text}</figcaption>" if cap_text else ""
    return (f'<figure><a href="{href}"><img src="{item["src"]}" alt="{item["alt"]}"'
            f'{cls_attr} loading="lazy"></a>{cap}</figure>')


def project_html(project, index):
    parts = []
    title = project.get("title") or f"Project #{index}"
    parts.append(f'<div class="project">\n<h3>{title}</h3>')
    if project.get("extra_desc"):
        parts.append(f'<p class="lede" style="margin:-6px 0 16px;">{project["extra_desc"]}</p>')
    figs = []
    for item in project["before"]:
        figs.append(figure_html(item, "Before"))
    for item in project["after"]:
        figs.append(figure_html(item, "After"))
    for item in project.get("extra_imgs", []):
        figs.append(figure_html(item, None))
    parts.append('<div class="gallery">' + "".join(figs) + '</div>')
    parts.append('</div>')
    return "\n".join(parts)


def render_all_projects(projects):
    out = []
    for i, p in enumerate(projects, 1):
        out.append(project_html(p, i))
    return "\n".join(out)


def parse_modules(modules_raw):
    """Parse a list of raw module <li> block strings into structured project dicts,
    guaranteeing every single <img> found anywhere in the block is captured exactly once
    (via a captured-tag dedup set), regardless of how malformed/hand-edited the block is."""
    projects = []
    total_img_count = 0
    for block in modules_raw:
        captured_tags = set()

        # primary/likely title: first h3.modfield.title
        titles = get_all_tag_texts(block, r'<(h3)\s+class="modfield title')

        # module-level extra description div(s) -- may also embed CTA images
        extra_desc_texts = []
        extra_imgs = []
        for dm in re.finditer(r'<div\s+class="modfield description', block):
            desc_blocks = find_balanced_blocks(block[dm.start():], '<div class="modfield description', 'div')
            if not desc_blocks:
                continue
            dblock = desc_blocks[0]
            dtext = get_tag_text(dblock, r'<(div)\s+class="modfield description')
            if dtext:
                extra_desc_texts.append(dtext)
            for raw_tag, attrs, href in extract_imgs_with_href(dblock):
                if raw_tag in captured_tags:
                    continue
                captured_tags.add(raw_tag)
                extra_imgs.append(img_item(attrs, href))
                total_img_count += 1

        # before/after sub-items
        subitems_raw = find_balanced_blocks(block, '<li class="modfieldgrp', 'li')
        befores, afters = [], []
        for sub in subitems_raw:
            kind = ("before" if re.match(r'<li\s+class="modfieldgrp before', sub)
                    else "after" if re.match(r'<li\s+class="modfieldgrp after', sub)
                    else None)
            imgs = extract_imgs_with_href(sub)
            if not imgs:
                # text-only modfieldgrp li (e.g. hand-edited "#5a ..." / "#5b ..." pseudo-caption
                # rows with no image) -- don't silently drop the marketing copy, fold it into the
                # project's extra description text instead.
                txt = re.sub(r'<script\b.*?</script>', '', sub, flags=re.DOTALL | re.IGNORECASE)
                txt = re.sub(r'<[^>]+>', '', txt)
                txt = re.sub(r'\s+', ' ', txt).strip()
                if txt:
                    extra_desc_texts.append(txt)
                continue
            desc = get_tag_text(sub, r'<(p)\s+class="modfield (?:before|after)description')
            for raw_tag, attrs, href in imgs:
                if raw_tag in captured_tags:
                    continue
                captured_tags.add(raw_tag)
                item = img_item(attrs, href, desc)
                total_img_count += 1
                (befores if kind == "before" else afters if kind == "after" else befores).append(item)

        # fallback: catch ANY remaining images anywhere in the block not yet captured
        # (handles hand-edited/malformed modules, e.g. images embedded directly inside <h3>)
        for raw_tag, attrs, href in extract_imgs_with_href(block):
            if raw_tag in captured_tags:
                continue
            captured_tags.add(raw_tag)
            extra_imgs.append(img_item(attrs, href))
            total_img_count += 1

        # also collect any plain-text <li class="module beforenafter"> caption lines with no h3
        # wrapper (anomaly rows) as extra description text
        for m in re.finditer(r'<li class="module beforenafter\s*"[^>]*>(.*?)</li>', block, re.DOTALL):
            inner = m.group(1)
            if '<h3' in inner or '<ul' in inner:
                continue
            t = re.sub(r'<[^>]+>', '', inner)
            t = re.sub(r'\s+', ' ', t).strip()
            if t:
                extra_desc_texts.append(t)

        title = titles[0] if titles else None
        other_titles = titles[1:] if len(titles) > 1 else []
        if not title and extra_desc_texts:
            # no proper <h3 class="modfield title"> in this (hand-edited/anomalous) module --
            # fall back to the first recovered plain-text caption as the title so the marketing
            # copy still surfaces as a heading instead of a generic placeholder.
            title = extra_desc_texts.pop(0)

        projects.append({
            "title": title,
            "other_titles": other_titles,
            "extra_desc": " | ".join(extra_desc_texts) if extra_desc_texts else None,
            "before": befores,
            "after": afters,
            "extra_imgs": extra_imgs,
        })
    return projects, total_img_count
