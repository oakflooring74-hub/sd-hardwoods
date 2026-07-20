# -*- coding: utf-8 -*-
"""
Shared helpers for the Aggressive Image Alt-Text Expansion milestone (2026-07-20).
See docs/SDH_Aggressive_Image_Alt_Expansion_Strategy_July_2026.md.

Every helper here only rearranges/cleans text that already exists in the site's own
data (module titles, legacy per-image alt fields, short captions) -- nothing here
invents species, location, stage, or process facts. Callers are responsible for
choosing which already-verified fields to pass in.
"""
import html as htmllib
import re

_SMALL_WORDS = {"in", "with", "for", "the", "to", "a", "an", "near", "by",
                "of", "and", "or", "at", "on", "from"}

_JUNK_MARKERS = ("YAHOO.", "function(", "buttons[", "moduleGuid", "javascript:")


def is_junk(text):
    """Detect leftover legacy-extraction JS/script fragments that sometimes ended
    up inside a caption field. Never treated as real content."""
    if not text:
        return True
    return any(m in text for m in _JUNK_MARKERS)


def smart_titlecase(text):
    """Convert an ALL-CAPS legacy caption into readable sentence-style text without
    mangling place names (San Diego, La Jolla, Del Mar, ...). Pure formatting -- the
    words themselves are unchanged."""
    if not text:
        return text
    words = text.split(" ")
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if i > 0 and lw in _SMALL_WORDS:
            out.append(lw)
        else:
            out.append(lw[:1].upper() + lw[1:] if lw else lw)
    return " ".join(out)


def clean_caption(cap):
    """Return a usable sentence-style caption, or None if empty/junk."""
    if not cap or not cap.strip() or is_junk(cap):
        return None
    text = smart_titlecase(cap.strip())
    if not text.endswith((".", "!", "?")):
        text += "."
    return text


def unescape(s):
    return htmllib.unescape(s or "")


_BARE_AMP_RE = re.compile(r"&(?!amp;|quot;|lt;|gt;|apos;|#\d+;|#x[0-9a-fA-F]+;|[a-zA-Z][a-zA-Z0-9]*;)")


def escape_bare_amp(s):
    """Escape a literal '&' that isn't already a valid HTML entity, so newly
    appended text is well-formed inside an attribute value. Never touches
    already-valid entities (&mdash; &frac34; &rsquo; ... stay untouched)."""
    return _BARE_AMP_RE.sub("&amp;", s or "")


def ensure_sentence(s):
    s = (s or "").strip()
    if not s:
        return s
    s = escape_bare_amp(s)
    if not s.endswith((".", "!", "?")):
        s += "."
    return s


def append_sentences(base, *sentences):
    """Join `base` (the preserved, verbatim-prefix alt) with additional sentences,
    skipping any that are empty, None, or already substantially duplicated.

    `base` is never trimmed, reformatted, or punctuation-adjusted -- it is required
    to survive byte-for-byte as the literal prefix of the return value (even a
    trailing space in the original alt is preserved exactly), per the milestone's
    "no existing words silently deleted/altered" rule. Only the newly appended
    sentences are cleaned up (trimmed, sentence-punctuated)."""
    base = base or ""
    seen_lower = {base.strip().lower()} if base.strip() else set()
    pieces = []
    for s in sentences:
        s = ensure_sentence(s)
        if not s:
            continue
        if s.lower() in seen_lower:
            continue
        pieces.append(s)
        seen_lower.add(s.lower())
    if not pieces:
        return base
    joined_new = " ".join(pieces)
    if not base:
        return joined_new
    sep = "" if base[-1].isspace() else " "
    return base + sep + joined_new


def strip_html_tags(s):
    return re.sub(r"<[^>]+>", "", s or "")
