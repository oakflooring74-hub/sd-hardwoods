import re, json, html, sys

from pathlib import Path
BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
RAW = str(BUILD / "raw-source" / "blog.html")
LOG = str(BUILD / "data" / "blog" / "build_log.txt")
OUT_JSON = str(BUILD / "data" / "blog" / "case_studies.json")

with open(RAW, encoding="utf-8") as f:
    raw = f.read()

log = []
def L(x): log.append(str(x))

attr_re = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
img_re = re.compile(r"<img\b[^>]*/?>", re.IGNORECASE)
a_href_re = re.compile(r'<a\s+href="([^"]+)"')
script_strip_re = re.compile(r"<script\b.*?</script>", re.DOTALL)
tag_strip_re = re.compile(r"<[^>]+>")

def clean_text(s):
    s = script_strip_re.sub("", s)
    s = tag_strip_re.sub("", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def extract_imgs(chunk_html):
    """Return list of {href,src,alt,class} for every <img> in chunk_html, in order."""
    out = []
    for im in img_re.finditer(chunk_html):
        tag = im.group(0)
        attrs = dict(attr_re.findall(tag))
        preceding = chunk_html[:im.start()]
        a_matches = list(a_href_re.finditer(preceding))
        href = None
        if a_matches:
            last_a = a_matches[-1]
            if "</a>" not in preceding[last_a.end():]:
                href = last_a.group(1)
        out.append({
            "href": href, "src": attrs.get("src", ""),
            "alt": attrs.get("alt", ""), "class": attrs.get("class", ""),
        })
    return out

# ---- locate the module_bd_container ul ----
start_marker = '<ul class="module_bd_container" id="mbdcontainer_zA.1">'
start = raw.index(start_marker)
content_start = raw.index(">", start) + 1

def find_matching_close(text, open_tag_re, close_tag, i):
    depth = 1
    pos = i
    rex = re.compile(open_tag_re)
    while depth > 0:
        nxt_open = rex.search(text, pos)
        nxt_close = text.find(close_tag, pos)
        if nxt_close == -1:
            raise Exception("no closing tag found")
        if nxt_open and nxt_open.start() < nxt_close:
            depth += 1
            pos = nxt_open.end()
        else:
            depth -= 1
            pos = nxt_close + len(close_tag)
    return pos - len(close_tag)

ul_close = find_matching_close(raw, r"<ul\b", "</ul>", content_start)
ul_inner = raw[content_start:ul_close]

def top_level_li_blocks(text):
    blocks = []
    i = 0
    li_open_re = re.compile(r"<li\b")
    while True:
        m = li_open_re.search(text, i)
        if not m:
            break
        block_start = m.start()
        tag_end = text.index(">", m.end()) + 1
        depth = 1
        pos = tag_end
        while depth > 0:
            nxt_open = li_open_re.search(text, pos)
            nxt_close = text.find("</li>", pos)
            if nxt_close == -1:
                raise Exception("unbalanced li")
            if nxt_open and nxt_open.start() < nxt_close:
                depth += 1
                pos = text.index(">", nxt_open.end()) + 1
            else:
                depth -= 1
                pos = nxt_close + 5
        blocks.append(text[block_start:pos])
        i = pos
    return blocks

li_blocks = top_level_li_blocks(ul_inner)
L(f"top-level li blocks in module_bd_container: {len(li_blocks)}")

# top-level block splitter for a description div's inner html: h2/h3/p/ul/hr in document order
block_re = re.compile(r'<h2\b[^>]*>.*?</h2>|<h3\b[^>]*>.*?</h3>|<p\b[^>]*>.*?</p>|<ul\b[^>]*>.*?</ul>|<hr\s*/?>', re.DOTALL)

def parse_description(desc_html):
    """Return (prose_paragraphs, images, short_captions_by_position)."""
    chunks = block_re.findall(desc_html)
    prose = []
    images = []
    # sequence of ('text', str) or ('img', [imgs]) in order, to allow caption pairing
    seq = []
    for chunk in chunks:
        imgs = extract_imgs(chunk)
        if imgs:
            images.extend(imgs)
            seq.append(("img", imgs))
            # also capture any leftover text in the same chunk (rare)
            no_img_chunk = img_re.sub("", chunk)
            no_img_chunk = re.sub(r'<a\b[^>]*>\s*</a>', '', no_img_chunk)
            txt = clean_text(no_img_chunk)
            if txt:
                seq.append(("text", txt))
        else:
            txt = clean_text(chunk)
            if txt:
                seq.append(("text", txt))
    # classify text entries: long (>50 chars) => prose ; short => caption candidate
    captions = []  # list of (caption_text, nearest_img_index)
    img_counter = 0
    for idx, (kind, val) in enumerate(seq):
        if kind == "img":
            img_counter += len(val)
        elif kind == "text":
            if len(val) <= 60:
                # short: try to associate with nearest adjacent img block (prefer preceding, i.e. the img right before this text)
                captions.append((val, img_counter - 1))
            else:
                prose.append(val)
    return prose, images, captions

records = []
total_imgs = 0
for block in li_blocks:
    rec = {"id": None, "title": None, "prose": [], "images": [], "captions": []}
    idm = re.search(r'<li class="module caseStudy"\s+id="([^"]*)"', block)
    if idm:
        rec["id"] = idm.group(1)

    h2m = re.search(r'<h2 class="modfield title[^"]*"[^>]*>(.*?)</h2>', block, re.DOTALL)
    if h2m:
        rec["title"] = clean_text(h2m.group(1))

    descm = re.search(r'<div class="modfield description[^"]*"[^>]*>(.*?)</div>\s*</li>', block, re.DOTALL)
    if not descm:
        descm = re.search(r'<div class="modfield description[^"]*"[^>]*>(.*)', block, re.DOTALL)
    if descm:
        desc_html = descm.group(1)
        prose, images, captions = parse_description(desc_html)
        rec["prose"] = prose
        rec["images"] = images
        rec["captions"] = captions
    else:
        # anonymous li (no h2 title, no modfield description div) - e.g. the Del Mar ash photo-only entry
        images = extract_imgs(block)
        rec["images"] = images

    total_imgs += len(rec["images"])
    records.append(rec)

L(f"records parsed: {len(records)}")
L(f"total images across all records: {total_imgs}")
for i, r in enumerate(records):
    L(f"  [{i}] id={r['id']!r} title={r['title']!r} n_images={len(r['images'])} n_prose={len(r['prose'])} n_captions={len(r['captions'])}")

# ---- standalone h3.module.caseStudy (item #3) sitting OUTSIDE the ul, right after the big intro widget ----
h3cs_m = re.search(r'<h3 class="module caseStudy">(.*?)</h3>', raw, re.DOTALL)
standalone_title_html = h3cs_m.group(1) if h3cs_m else None
L(f"standalone h3.module.caseStudy found: {bool(h3cs_m)}")
if h3cs_m:
    L(f"standalone raw (first 300 chars): {standalone_title_html[:300]!r}")

with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
    json.dump({"records": records, "standalone_html": standalone_title_html}, f, indent=2, ensure_ascii=False)

with open(LOG, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(log))

print("done", file=sys.stderr)
