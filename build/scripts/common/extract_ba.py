import re, json, sys, html

def load(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def block(doc, start_after, tagname):
    """Given position right after the opening '>' of a tag, find the matching
    close tag (balanced), return (content, end_index_after_close_tag)."""
    open_re = re.compile(r'<' + tagname + r'\b', re.IGNORECASE)
    close_re = re.compile(r'</' + tagname + r'>', re.IGNORECASE)
    depth = 1
    i = start_after
    while depth > 0:
        om = open_re.search(doc, i)
        cm = close_re.search(doc, i)
        if cm is None:
            raise Exception("no matching close for " + tagname)
        if om and om.start() < cm.start():
            depth += 1
            i = om.end()
        else:
            depth -= 1
            i = cm.end()
    close_len = len(close_re.search(doc, 0).group(0)) if False else None
    return doc[start_after:i - len(("</%s>" % tagname))], i

IMG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
A_HREF_RE = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>', re.IGNORECASE)
H3_RE = re.compile(r'<h3\b[^>]*>(.*?)</h3>', re.DOTALL | re.IGNORECASE)
P_TITLE_RE = re.compile(r'<p\b[^>]*data-(?:start|end)[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)
DESC_RE = re.compile(r'<p\s+class="modfield\s+(before|after)description[^"]*"[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)

def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def find_images_in(segment):
    """Return list of dicts for every <img> in segment, with nearest wrapping <a href>."""
    results = []
    for im in IMG_RE.finditer(segment):
        tag = im.group(0)
        attrs = dict(ATTR_RE.findall(tag))
        preceding = segment[:im.start()]
        a_matches = list(A_HREF_RE.finditer(preceding))
        href = None
        if a_matches:
            last_a = a_matches[-1]
            between = preceding[last_a.end():]
            if '</a>' not in between:
                href = last_a.group(1)
        results.append({
            "src": attrs.get("src", ""),
            "alt": attrs.get("alt", ""),
            "class": attrs.get("class", ""),
            "href": href,
            "start": im.start(),
            "end": im.end(),
        })
    return results

def extract_modules(doc):
    modules = []
    module_ranges = []
    for m in re.finditer(r'<li\s+class="module beforenafter\s*"[^>]*>', doc, re.IGNORECASE):
        start_after = m.end()
        content, end_idx = block(doc, start_after, "li")
        module_ranges.append((m.start(), end_idx))

        # title: try <h3>, else a <p data-start/data-end> (module #78 pattern)
        title = None
        hm = H3_RE.search(content)
        if hm:
            title = strip_tags(hm.group(1))
        else:
            pm = P_TITLE_RE.search(content)
            if pm:
                title = strip_tags(pm.group(1))

        imgs = find_images_in(content)
        # try to attach a caption to each image: nearest following description <p>
        for img in imgs:
            after_seg = content[img["end"]:img["end"] + 1200]
            dm = DESC_RE.search(after_seg)
            img["caption"] = strip_tags(dm.group(2)) if dm else None

        modules.append({
            "title": title,
            "images": imgs,
        })
    return modules, module_ranges

def extract_standalone(doc, module_ranges):
    """All <img> tags anywhere in doc that fall outside any module range."""
    def in_module(pos):
        return any(s <= pos < e for s, e in module_ranges)
    results = []
    for im in IMG_RE.finditer(doc):
        if in_module(im.start()):
            continue
        tag = im.group(0)
        attrs = dict(ATTR_RE.findall(tag))
        preceding = doc[:im.start()]
        a_matches = list(A_HREF_RE.finditer(preceding))
        href = None
        if a_matches:
            last_a = a_matches[-1]
            between = preceding[last_a.end():]
            if '</a>' not in between:
                href = last_a.group(1)
        results.append({
            "src": attrs.get("src", ""),
            "alt": attrs.get("alt", ""),
            "class": attrs.get("class", ""),
            "href": href,
            "start": im.start(),
        })
    return results

def main():
    in_path = sys.argv[1]
    out_json = sys.argv[2]
    doc = load(in_path)

    total_imgs = len(IMG_RE.findall(doc))

    modules, module_ranges = extract_modules(doc)
    standalone = extract_standalone(doc, module_ranges)

    module_img_count = sum(len(m["images"]) for m in modules)

    result = {
        "source": in_path,
        "total_img_tags_in_doc": total_imgs,
        "module_count": len(modules),
        "module_img_count": module_img_count,
        "standalone_img_count": len(standalone),
        "sum_check": module_img_count + len(standalone),
        "modules": modules,
        "standalone": standalone,
    }

    with open(out_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    with open(out_json + ".log.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"total <img> in doc: {total_imgs}\n")
        f.write(f"modules found: {len(modules)}\n")
        f.write(f"images inside modules: {module_img_count}\n")
        f.write(f"standalone images: {len(standalone)}\n")
        f.write(f"sum (modules+standalone): {module_img_count + len(standalone)}\n")
        f.write(f"match: {module_img_count + len(standalone) == total_imgs}\n\n")
        for i, m in enumerate(modules):
            f.write(f"--- module {i}: {len(m['images'])} imgs ---\n")
            f.write(f"title: {m['title']}\n")
            for img in m["images"]:
                f.write(f"  src={img['src']!r} href={img['href']!r} class={img['class']!r}\n")
        f.write("\n--- standalone images ---\n")
        for img in standalone:
            f.write(f"  src={img['src']!r} href={img['href']!r} alt={img['alt'][:60]!r}\n")

if __name__ == "__main__":
    main()
