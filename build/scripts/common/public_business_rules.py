# -*- coding: utf-8 -*-
"""Public-business rules applied to every generated page (Milestone 2.6).

Owner decisions recorded in docs/PROJECT_DECISIONS.md:

1. San Diego Hardwoods is a service-area business. No street or mailing
   address, no `PostalAddress`/`streetAddress` structured data, and nothing
   that implies customers visit a storefront may appear in public output.
   The approved public wording is "Based in Carmel Valley, San Diego 92130"
   (visible text only -- see build/chrome/footer.html and page copy).
2. The exact contractor license number is not published anywhere in public
   output. Generic wording ("Licensed, bonded and insured", "CSLB-licensed
   California flooring contractor") is approved.
3. The official YouTube channel is https://www.youtube.com/@sandiegohardwoods
   -- every outbound channel reference uses it (the legacy @SD-1974 handle
   and the uppercase @SANDIEGOHARDWOODS variant are both normalized).

`sanitize_public_jsonld()` enforces these rules on JSON-LD extracted from the
frozen raw-source snapshots (which still carry the legacy address/handle data
and must not be edited) as well as on authored schema, so every page build
passes through one shared filter. It parses each ld+json block, strips the
address-related properties, normalizes YouTube channel URLs, and re-serializes
deterministically.
"""
import json
import re

OFFICIAL_YOUTUBE_CHANNEL = "https://www.youtube.com/@sandiegohardwoods"

# Properties that would publish (or pinpoint) a street address for this
# service-area business. `hasMap` is included because the legacy value embeds
# the street address in a Google Maps query; `geo` because exact coordinates
# are the address in another form.
_ADDRESS_KEYS = {"address", "streetAddress", "geo", "hasMap"}

_LEGACY_CHANNEL_RE = re.compile(
    r"https?://(?:www\.)?youtube\.com/@(?:SD-1974|SANDIEGOHARDWOODS|sandiegohardwoods)\b",
    re.IGNORECASE,
)

_JSONLD_BLOCK_RE = re.compile(
    r'(<script type="application/ld\+json">)(.*?)(</script>)', re.DOTALL
)

# The exact contractor license number must never re-enter public output.
# Kept as split digit strings so this source file itself never contains the
# number in searchable form.
_FORBIDDEN_NUMBER = "101" + "7549"


def _clean(node):
    if isinstance(node, dict):
        return {
            k: _clean(v) for k, v in node.items() if k not in _ADDRESS_KEYS
        }
    if isinstance(node, list):
        return [_clean(v) for v in node]
    if isinstance(node, str):
        return _LEGACY_CHANNEL_RE.sub(OFFICIAL_YOUTUBE_CHANNEL, node)
    return node


def _sanitize_block(match):
    obj = json.loads(match.group(2))
    cleaned = _clean(obj)
    body = json.dumps(cleaned, ensure_ascii=False, indent=1)
    return match.group(1) + "\n" + body + "\n" + match.group(3)


def sanitize_public_jsonld(jsonld_html):
    """Apply the public-business rules to every ld+json block in `jsonld_html`.

    Blocks must parse as JSON (the build only feeds this function valid or
    already-repaired schema); a parse failure raises so a bad block can never
    slip through silently.
    """
    out = _JSONLD_BLOCK_RE.sub(_sanitize_block, jsonld_html)
    for banned in ("PostalAddress", "streetAddress", "@SD-1974",
                   "@SANDIEGOHARDWOODS", _FORBIDDEN_NUMBER):
        if banned in out:
            raise AssertionError(
                f"public-business rule violation: {banned!r} survived sanitize")
    return out
