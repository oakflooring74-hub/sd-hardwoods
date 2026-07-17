import re, json, sys, html
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent.parent  # -> build/
RAW = str(BUILD / "raw-source" / "deep-cleaning-hardwood-floors-san-diego.html")
CHROME = str(BUILD / "chrome")
OUT = str(BUILD.parent / "deep-cleaning-hardwood-floors-san-diego.html")
LOG = str(BUILD / "data" / "deep-cleaning-hardwood-floors-san-diego" / "build_log.txt")

with open(RAW, encoding="utf-8") as f:
    raw = f.read()

log = []
def L(x):
    log.append(str(x))

# ---------- head bits (verbatim, extracted programmatically) ----------
title = re.search(r"<title>(.*?)</title>", raw, re.DOTALL).group(1).strip()
meta_desc = re.search(r'<meta name="DESCRIPTION" id="mDescription" content="([^"]*)"', raw).group(1)
canonical = re.search(r'<link href="([^"]+)" rel="canonical"', raw).group(1)
jsonld_block = re.search(r'<script type="application/ld\+json">.*?</script>', raw, re.DOTALL).group(0)
gaq_block = re.search(r'<!--Google Analytics Tracking Code-->.*?</script>', raw, re.DOTALL).group(0)
vcard_desc = re.search(r'<span class="organization-name">(.*?)</span>', raw, re.DOTALL).group(1).strip()

L(f"title: {title!r}")
L(f"meta_desc: {meta_desc!r}")
L(f"canonical: {canonical!r}")
L(f"jsonld_block length: {len(jsonld_block)}")
L(f"gaq present: {'_gaq' in gaq_block}")
L(f"vcard_desc: {vcard_desc!r}")

# ---------- gallery extraction ----------
start_marker = '<ul class="module_bd_container" id="mbdcontainer_zA.1">'
start = raw.index(start_marker)
content_start = raw.index(">", start) + 1

def find_matching_close(html_text, open_tag_re, close_tag, i):
    depth = 1
    pos = i
    while depth > 0:
        nxt_open = re.compile(open_tag_re).search(html_text, pos)
        nxt_close = html_text.find(close_tag, pos)
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
zA_ul_inner = raw[content_start:ul_close]

# split top-level <li ...>...</li> blocks (balanced on <li / </li>)
def top_level_li_blocks(text):
    blocks = []
    i = 0
    n = len(text)
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

modules = top_level_li_blocks(zA_ul_inner)
L(f"top-level li (module) blocks found: {len(modules)}")

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

def extract_img(li_html):
    """Return (href, src, alt, cls) for the first <img> in li_html, or None."""
    im = img_re.search(li_html)
    if not im:
        return None
    tag = im.group(0)
    attrs = dict(attr_re.findall(tag))
    preceding = li_html[:im.start()]
    a_matches = list(a_href_re.finditer(preceding))
    href = None
    if a_matches:
        last_a = a_matches[-1]
        if "</a>" not in preceding[last_a.end():]:
            href = last_a.group(1)
    return {
        "href": href,
        "src": attrs.get("src", ""),
        "alt": attrs.get("alt", ""),
        "class": attrs.get("class", ""),
    }

records = []
all_img_count = 0
for idx, block in enumerate(modules, start=1):
    rec = {"index": idx, "title": None, "before": None, "after": None, "note_text": None, "note_imgs": []}

    m = re.search(r'<h3 class="modfield title[^"]*"[^>]*>(.*?)</h3>', block, re.DOTALL)
    if m:
        rec["title"] = clean_text(m.group(1))

    fieldgrp_re = re.compile(r'<li class="modfieldgrp (before|after)"[^>]*>(.*?)</li>', re.DOTALL)
    fg_matches = list(fieldgrp_re.finditer(block))

    before_img = None
    after_img = None
    before_desc = None
    after_desc = None
    fallback_note_bits = []

    for fm in fg_matches:
        kind = fm.group(1)
        li_html = fm.group(2)
        img = extract_img(li_html)
        desc_m = re.search(r'<p class="modfield (?:before|after)description[^"]*"[^>]*>(.*?)</p>', li_html, re.DOTALL)
        desc_text = clean_text(desc_m.group(1)) if desc_m else None

        if img:
            all_img_count += 1
            if kind == "before" and before_img is None:
                before_img = img
                if desc_text:
                    before_desc = desc_text
            elif kind == "after" and after_img is None:
                after_img = img
                if desc_text:
                    after_desc = desc_text
            else:
                # extra image beyond the expected one before/after slot (shouldn't normally happen)
                fallback_note_bits.append(clean_text(li_html))
        else:
            # no image in this li: could be leftover title/description text (malformed module e.g. #5)
            txt = clean_text(li_html)
            if txt:
                fallback_note_bits.append(txt)

    # title fallback for malformed modules (no h3): use first fallback text chunk that looks like a heading
    if rec["title"] is None and fallback_note_bits:
        rec["title"] = fallback_note_bits[0]
        fallback_note_bits = fallback_note_bits[1:]

    if before_desc is None and fallback_note_bits:
        # use next available fallback text as shared before/after caption
        before_desc = fallback_note_bits[0]
        fallback_note_bits = fallback_note_bits[1:]

    rec["before"] = {"img": before_img, "desc": before_desc}
    rec["after"] = {"img": after_img, "desc": after_desc}

    # trailing "modfield description" div (module-level note), applies to remainder of block after the ul
    ul_end = 0
    ul_m = re.search(r"</ul>", block)
    remainder = block[ul_m.end():] if ul_m else ""
    note_div_m = re.search(r'<div class="modfield description[^"]*"[^>]*>(.*?)</div>', remainder, re.DOTALL)
    if note_div_m:
        note_html = note_div_m.group(1)
        # capture any images (e.g. CTA buttons) inside the note div
        for nim in img_re.finditer(note_html):
            tag = nim.group(0)
            attrs = dict(attr_re.findall(tag))
            preceding = note_html[:nim.start()]
            a_matches = list(a_href_re.finditer(preceding))
            href = None
            if a_matches:
                last_a = a_matches[-1]
                if "</a>" not in preceding[last_a.end():]:
                    href = last_a.group(1)
            rec["note_imgs"].append({
                "href": href, "src": attrs.get("src", ""),
                "alt": attrs.get("alt", ""), "class": attrs.get("class", ""),
            })
            all_img_count += 1
        note_text = clean_text(note_html)
        if note_text:
            rec["note_text"] = note_text

    if fallback_note_bits and rec["note_text"] is None:
        rec["note_text"] = " ".join(fallback_note_bits)

    records.append(rec)

L(f"records built: {len(records)}")
L(f"total <img> extracted via module parsing: {all_img_count}")

with open(BUILD / "data" / "deep-cleaning-hardwood-floors-san-diego" / "gallery_records.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

# raw <img> count sanity check across whole zA
raw_img_count_zA = len(img_re.findall(zA_ul_inner))
L(f"raw <img> count found by direct regex over zA: {raw_img_count_zA}")

with open(LOG, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(log))

print("done - see log file", file=sys.stderr)
