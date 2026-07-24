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
import html
import json
import re
import urllib.parse
from pathlib import Path

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

# Body-only variant (no capture of the surrounding tags) used by the
# canonical-business-entity functions below, which always rebuild the
# `<script>` wrapper themselves.
_JSONLD_BLOCK_RE_BODY = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL
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


# ---------------------------------------------------------------------------
# Canonical business-entity consolidation (owner-approved schema milestone,
# 2026-07-19). Prior to this, most pages re-declared the business from
# scratch as brand-new, unlinked JSON-LD nodes (a standalone FlooringContractor,
# a standalone Organization, and five more Organization stubs nested in each
# Service's `provider`) instead of referencing the one canonical entity by
# `@id`, the way floor-assessments-inspections.html already did. That meant
# ~40 duplicate, disconnected "San Diego Hardwoods" declarations site-wide,
# with inconsistent priceRange/phone formatting between them -- diluting
# entity confidence instead of presenting Google one confident local
# business. `consolidate_business_jsonld()` fixes this: on every page it's
# applied to, every unlinked business node is dropped, every Service
# `provider` is rewritten to a bare `{"@id": ...}` reference, and exactly one
# canonical declaration (below) is prepended once.
#
# Facts below are owner-confirmed 2026-07-19 from the live Google Business
# Profile dashboard (5.0 rating / 16 reviews) and Google Maps share link;
# `alternateName` is the long-form GBP listing name, active for years.
CANONICAL_LOCAL_ID = "https://www.sdhardwoods.com/#local"

CANONICAL_LOCAL_STUB = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "HomeAndConstructionBusiness", "FlooringContractor"],
    "@id": CANONICAL_LOCAL_ID,
    "name": "San Diego Hardwoods",
    "alternateName": "San Diego Hardwoods Dustless Hardwood and Bamboo Floor Refinishing Installation Repairs and Deep Cleaning",
    "url": "https://www.sdhardwoods.com",
    "telephone": "+18586990072",
    "email": "sandiegohardwoods@gmail.com",
    "image": "/LOGO-2025.png",
    "logo": "/LOGO-2025.png",
    "priceRange": "$$$",
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+18586990072",
        "contactType": "sales",
        "availableLanguage": ["en"],
        "areaServed": "US",
    },
    "hasCredential": {
        "@type": "EducationalOccupationalCredential",
        "name": "Bona Certified Craftsman",
        "url": "https://www.bona.com/en-us/homeowner/find-a-contractor/contractor-details/?storeid=83667",
        "image": "/bonacc.jpeg",
        "issuer": {"@type": "Organization", "name": "Bona"},
    },
    "sameAs": [
        "https://www.youtube.com/@sandiegohardwoods",
        "https://maps.app.goo.gl/hbNaSo2guARgrZTa8",
    ],
}
# `areaServed` is attached below, once FULL_SAN_DIEGO_AREAS/SOUTH_ORANGE_COUNTY are built
# (Milestone 2.9), so CANONICAL_LOCAL_STUB carries the complete location footprint -- the
# only place OC service areas appear anywhere on the site.

# Same facts, as a plain dict for pages that add them to an *existing*
# richer entity (index.html's #local, which also carries areaServed,
# openingHoursSpecification, and its own description) instead of getting the
# full stub above.
CANONICAL_LOCAL_EXTRAS = {
    "alternateName": CANONICAL_LOCAL_STUB["alternateName"],
    "telephone": CANONICAL_LOCAL_STUB["telephone"],
    "priceRange": CANONICAL_LOCAL_STUB["priceRange"],
    "contactPoint": CANONICAL_LOCAL_STUB["contactPoint"],
    "hasCredential": CANONICAL_LOCAL_STUB["hasCredential"],
    "sameAs": CANONICAL_LOCAL_STUB["sameAs"],
}

_BUSINESS_TYPES = {"LocalBusiness", "HomeAndConstructionBusiness", "FlooringContractor", "Organization"}


def _types_of(node):
    t = node.get("@type")
    if t is None:
        return set()
    return set(t) if isinstance(t, list) else {t}


def _is_unlinked_business_node(node):
    return isinstance(node, dict) and "@id" not in node and bool(_types_of(node) & _BUSINESS_TYPES)


def _rewrite_providers(node):
    """Recursively replace any inline duplicate-business `provider` value
    with a bare @id reference to the canonical #local entity."""
    if isinstance(node, dict):
        if isinstance(node.get("provider"), dict) and _is_unlinked_business_node(node["provider"]):
            node["provider"] = {"@id": CANONICAL_LOCAL_ID}
        for v in node.values():
            _rewrite_providers(v)
    elif isinstance(node, list):
        for v in node:
            _rewrite_providers(v)


def _contains_full_canonical_declaration(node, target_id=CANONICAL_LOCAL_ID):
    """True if `node` contains a *full* declaration of the canonical entity
    (an "@id": target_id node that also carries "@type"), as opposed to a
    bare `{"@id": target_id}` reference -- the shape `_rewrite_providers()`
    intentionally creates, which must not itself count as a duplicate."""
    if isinstance(node, dict):
        if node.get("@id") == target_id and "@type" in node:
            return True
        return any(_contains_full_canonical_declaration(v, target_id) for v in node.values())
    if isinstance(node, list):
        return any(_contains_full_canonical_declaration(v, target_id) for v in node)
    return False


def consolidate_business_jsonld(jsonld_html):
    """Drop every unlinked business declaration from `jsonld_html`, rewrite
    every Service `provider` to reference the canonical entity by `@id`, and
    prepend exactly one canonical declaration. Non-business blocks
    (VideoObject, FAQPage, CollectionPage, ...) pass through untouched aside
    from the same (no-op, for these types) provider rewrite. Call this
    *after* `sanitize_public_jsonld()` -- consolidation's list-field dedupe
    (e.g. sameAs) compares exact strings, so the legacy YouTube handle must
    already be normalized to the official channel first, or the same
    channel URL can end up listed twice.
    """
    kept_objs = []
    for raw in _JSONLD_BLOCK_RE_BODY.findall(jsonld_html):
        obj = json.loads(raw)
        if isinstance(obj, list):
            obj = [item for item in obj if not _is_unlinked_business_node(item)]
            _rewrite_providers(obj)
            if not obj:
                continue
        elif isinstance(obj, dict) and isinstance(obj.get("@graph"), list):
            obj["@graph"] = [item for item in obj["@graph"] if not _is_unlinked_business_node(item)]
            _rewrite_providers(obj["@graph"])
            if not obj["@graph"]:
                continue
        elif _is_unlinked_business_node(obj):
            continue
        else:
            _rewrite_providers(obj)
        kept_objs.append(obj)

    # Guard against double-consolidation: this is called once, at build time,
    # on raw/duplicate-laden source. If it's ever accidentally re-run on
    # already-consolidated output, blindly prepending a second canonical
    # declaration would create a duplicate `@id` on the page instead of
    # silently doing nothing -- fail loudly so that can never slip through.
    # Must check for a *full* declaration (has @type), not just any node
    # carrying "@id": CANONICAL_LOCAL_ID -- the bare {"@id": ...} references
    # `_rewrite_providers()` just created above legitimately match by @id
    # alone and are not duplicates.
    if _contains_full_canonical_declaration(kept_objs):
        raise AssertionError(
            f"consolidate_business_jsonld: a full node with @id={CANONICAL_LOCAL_ID!r} "
            "already exists in this input -- it looks like this content has "
            "already been consolidated once; re-running would duplicate it.")

    kept_blocks = [
        f'<script type="application/ld+json">\n{json.dumps(obj, indent=1, ensure_ascii=False)}\n</script>'
        for obj in kept_objs
    ]
    canonical_body = json.dumps(CANONICAL_LOCAL_STUB, indent=1, ensure_ascii=False)
    canonical_block = f'<script type="application/ld+json">\n{canonical_body}\n</script>'
    return "\n".join([canonical_block] + kept_blocks)


def _merge_into_id(node, target_id, extra_fields):
    """Recursively find the node with `"@id": target_id` and merge
    `extra_fields` into it (list-valued fields are appended-to, not
    replaced, so already-present entries like an existing sameAs survive).
    Returns True if a merge happened anywhere in `node`."""
    if isinstance(node, dict):
        if node.get("@id") == target_id:
            for k, v in extra_fields.items():
                if isinstance(node.get(k), list) and isinstance(v, list):
                    node[k] = node[k] + [x for x in v if x not in node[k]]
                else:
                    node[k] = v
            return True
        return any(_merge_into_id(v, target_id, extra_fields) for v in node.values())
    if isinstance(node, list):
        return any(_merge_into_id(v, target_id, extra_fields) for v in node)
    return False


def augment_local_entity(jsonld_html, extra_fields=None, local_id=CANONICAL_LOCAL_ID):
    """Merge `extra_fields` (default CANONICAL_LOCAL_EXTRAS) into the
    existing node identified by `"@id": local_id`, wherever it appears.
    Unlike `consolidate_business_jsonld()`, this does not touch any other
    block and does not drop or replace anything -- for pages (index.html)
    that already have exactly one, correctly-linked canonical declaration
    and just need the new fields added to it. Raises if no matching node is
    found, so a silent no-op can never slip through. Call this *after*
    `sanitize_public_jsonld()`, for the same reason as
    `consolidate_business_jsonld()` above.
    """
    if extra_fields is None:
        extra_fields = CANONICAL_LOCAL_EXTRAS
    out_blocks = []
    touched = False
    for raw in _JSONLD_BLOCK_RE_BODY.findall(jsonld_html):
        obj = json.loads(raw)
        if _merge_into_id(obj, local_id, extra_fields):
            touched = True
        out_blocks.append(f'<script type="application/ld+json">\n{json.dumps(obj, indent=1, ensure_ascii=False)}\n</script>')
    if not touched:
        raise AssertionError(f"augment_local_entity: no node with @id={local_id!r} found")
    return "\n".join(out_blocks)


def _set_field(node, target_id, field, value):
    if isinstance(node, dict):
        if node.get("@id") == target_id:
            node[field] = value
            return True
        return any(_set_field(v, target_id, field, value) for v in node.values())
    if isinstance(node, list):
        return any(_set_field(v, target_id, field, value) for v in node)
    return False


def replace_area_served(jsonld_html, area_served, local_id=CANONICAL_LOCAL_ID):
    """Overwrite (not append/merge) the `areaServed` field of the node with
    `"@id": local_id`, wherever it appears. Used instead of
    `augment_local_entity()` for this one field because that function's
    list-merge logic appends to whatever is already there -- correct for
    `sameAs`, wrong for `areaServed` on pages (the homepage) that already
    carry a legacy, since-superseded area list: appending would keep the
    old list alongside the new one instead of replacing it. Raises if no
    matching node is found, same safety contract as `augment_local_entity`.
    """
    out_blocks = []
    touched = False
    for raw in _JSONLD_BLOCK_RE_BODY.findall(jsonld_html):
        obj = json.loads(raw)
        if _set_field(obj, local_id, "areaServed", area_served):
            touched = True
        out_blocks.append(f'<script type="application/ld+json">\n{json.dumps(obj, indent=1, ensure_ascii=False)}\n</script>')
    if not touched:
        raise AssertionError(f"replace_area_served: no node with @id={local_id!r} found")
    return "\n".join(out_blocks)


# ---------------------------------------------------------------------------
# Centralized service-area source (Milestone 2.9), replacing the drifting
# per-page/per-milestone area lists. Single source of truth:
# build/data/seo/service_areas.json -- the owner's detailed San Diego
# regional/enclave lists plus every broader San Diego County area already
# in the shared schema before this milestone (owner direction 2026-07-19:
# leave every area already in the site's data alone, only add to it -- the
# coastal/estate regions are ordered first for internal structured-data
# emphasis reasons that must never be stated or made visible on the site).
_SERVICE_AREAS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "seo" / "service_areas.json"
with open(_SERVICE_AREAS_PATH, encoding="utf-8") as _f:
    _SERVICE_AREAS = json.load(_f)


def _dedupe_keep_first(items):
    seen, out = set(), []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


# The complete San Diego location footprint for the shared #local entity only
# -- never repeated in full on any individual page's Service.areaServed.
FULL_SAN_DIEGO_AREAS = _dedupe_keep_first(
    ["San Diego County"]
    + [area for region in _SERVICE_AREAS["regions"] for area in region["areas"]]
    + _SERVICE_AREAS["additional_legacy_areas"]
)

# Owner's exact South Orange County list (2026-07-19). Attached only to the
# shared #local entity's areaServed -- never to a per-page Service, and
# never in visible copy anywhere on the site.
SOUTH_ORANGE_COUNTY = list(_SERVICE_AREAS["south_orange_county"])

# Short San-Diego-only priority tier for per-page Service.areaServed (each
# page uses its own flavor of this, never the full county list, never OC).
PRIORITY_COASTAL_SD = [
    "La Jolla", "Del Mar", "Solana Beach", "Encinitas", "Cardiff-by-the-Sea",
    "Rancho Santa Fe", "Carmel Valley", "Fairbanks Ranch", "Santaluz",
    "Coronado", "Point Loma",
]

CANONICAL_LOCAL_STUB["areaServed"] = FULL_SAN_DIEGO_AREAS + SOUTH_ORANGE_COUNTY


def build_webpage_service_graph(page_url, page_id_slug, page_name, page_description,
                                 service_name, service_description, service_types,
                                 area_served, offer_catalog_name, offer_items):
    """Build just the WebPage + Service (+ OfferCatalog) entities for one
    page, `@id`-linked to each other and referencing the canonical business
    by `@id` only (no local-entity declaration included) -- for pages that
    already declare `#local` themselves elsewhere on the page (index.html's
    augmented raw-source entity; floor-assessments-inspections.html's own
    inline entity). Using this instead of `build_service_page_jsonld()` on
    those pages avoids re-declaring `#local` a second time, which would
    recreate the exact duplicate-entity problem the 2026-07-19 consolidation
    milestone fixed.

    `offer_items` is a list of (name, description) tuples -- real,
    already-approved copy only, never invented here. `area_served` is
    deliberately this page's own list (see PRIORITY_COASTAL_SD /
    SOUTH_ORANGE_COUNTY above), not one blanket list repeated everywhere.
    Returns the list of graph entities (not yet wrapped in a `<script>` tag
    or `@context`/`@graph` envelope) so callers can merge it into an
    existing graph.
    """
    webpage_id = f"{page_url}#webpage"
    service_id = f"{page_url}#{page_id_slug}"
    return [
        {
            "@type": "WebPage",
            "@id": webpage_id,
            "url": page_url,
            "name": page_name,
            "description": page_description,
            "inLanguage": "en",
            "about": {"@id": CANONICAL_LOCAL_ID},
            "mainEntity": {"@id": service_id},
        },
        {
            "@type": "Service",
            "@id": service_id,
            "name": service_name,
            "url": page_url,
            "mainEntityOfPage": {"@id": webpage_id},
            "provider": {"@id": CANONICAL_LOCAL_ID},
            "areaServed": area_served,
            "serviceType": service_types,
            "description": service_description,
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": offer_catalog_name,
                "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d}}
                    for n, d in offer_items
                ],
            },
        },
    ]


def build_service_page_jsonld(page_url, page_id_slug, page_name, page_description,
                               service_name, service_description, service_types,
                               area_served, offer_catalog_name, offer_items,
                               extra_local_fields=None, extra_entities=None):
    """Like `build_webpage_service_graph()`, but for pages that do NOT
    already declare `#local` themselves -- this one also prepends a full
    canonical business declaration, returned as a ready-to-use `<script>`
    block. See `build_webpage_service_graph()` for the parameter contract;
    still needs to pass through `sanitize_public_jsonld()` afterward
    (harmless/idempotent here, but keeps the same safety net every page's
    schema goes through). `extra_entities`, if given, is appended to the
    same `@graph` array (e.g. `build_gallery_media_graph()`'s output).
    """
    local = dict(CANONICAL_LOCAL_STUB)
    if extra_local_fields:
        local.update(extra_local_fields)
    graph = [local] + build_webpage_service_graph(
        page_url, page_id_slug, page_name, page_description,
        service_name, service_description, service_types,
        area_served, offer_catalog_name, offer_items,
    ) + (extra_entities or [])
    body = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=1, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{body}\n</script>'


def wrap_jsonld_graph(entities):
    """Wrap a list of graph entities in their own standalone `<script>` block
    with its own `@context`/`@graph` envelope -- for pages whose existing
    JSON-LD is a frozen fragment or an inline string that isn't a Python
    list to merge into directly. Appending an independent block is valid
    JSON-LD (parsers combine every `<script type="application/ld+json">` on
    a page into one graph) and avoids touching the frozen fragment itself.
    """
    body = json.dumps({"@context": "https://schema.org", "@graph": entities}, indent=1, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{body}\n</script>'


def split_title_desc(title, sep=" &mdash; "):
    """Split a module heading of the form '#N Short Title &mdash; longer
    sentence...' into (name, description) on the first em-dash -- these
    titles are extracted HTML, so the literal separator is the HTML entity,
    not a unicode em-dash character. Falls back to the whole title as name
    (no description) when the separator isn't present. Restructures
    already-published text only; invents nothing.
    """
    if not title:
        return "", None
    parts = title.split(sep, 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return title.strip(), None


def _abs_media_url(src):
    """Absolute, percent-encoded URL for a root-relative image src (e.g.
    '/WHITE MAPLE1.jpg') -- matches the form Google's structured-data
    guidance expects for ImageObject contentUrl/url."""
    return "https://www.sdhardwoods.com" + urllib.parse.quote(src, safe="/")


def build_gallery_media_graph(page_url, projects):
    """Build ItemList + one CreativeWork per documented project + one
    ImageObject per photo, for a gallery-shaped page's real before/after (or
    multi-stage) project photos. This is the schema.org pattern already
    proven working on the live production site's Gallery 1 page (2026-07-23
    schema audit) -- ported here and generalized to also cover Solid Wood's
    variable-length, non-before/after project image groups.

    `projects`: [{"name": str, "description": str|None,
                  "images": [{"url": str (root-relative src), "name": str,
                              "caption": str|None}, ...]}]
    Every `name`/`description`/`caption` must already be real, published
    page copy (title/alt/caption text) -- this function only restructures
    it into schema and HTML-unescapes it (the source data is extracted HTML,
    so entities like `&amp;` would otherwise land literally in the JSON-LD
    string instead of being decoded), never invents anything.

    `contentLocation` is deliberately not included: no reliably
    owner-confirmed, per-project structured location data exists yet for
    these pages (checked `build/data/media/owner_facts_confirmed.json` and
    every `build/data/media/placements/*.json` -- see docs/PROJECT_DECISIONS.md,
    "Media-fact policy"). Parsing a location out of free-text titles was
    considered and rejected: some titles name two different locations for
    two different photos in the same project, and this project's own rules
    prohibit inferring facts from nearby text.

    Returns a list of graph entities referencing {"@id": CANONICAL_LOCAL_ID}
    for `creator` and {"@id": f"{page_url}#webpage"} for `isPartOf` -- never
    redeclaring either, matching `build_webpage_service_graph()`'s convention.
    """
    def clean(s):
        return html.unescape(s).strip() if s else s

    webpage_id = f"{page_url}#webpage"
    list_id = f"{page_url}#project-list"
    entities = []
    list_items = []
    for i, proj in enumerate(projects, start=1):
        project_id = f"{page_url}#project-{i}"
        n_images = len(proj["images"])
        image_refs = []
        for j, img in enumerate(proj["images"], start=1):
            if n_images == 2:
                suffix = "before-image" if j == 1 else "after-image"
            else:
                suffix = f"image-{j}"
            image_id = f"{project_id}-{suffix}"
            image_refs.append({"@id": image_id})
            image_entity = {
                "@type": "ImageObject",
                "@id": image_id,
                "contentUrl": _abs_media_url(img["url"]),
                "url": _abs_media_url(img["url"]),
                "name": clean(img["name"]),
            }
            if img.get("caption"):
                image_entity["caption"] = clean(img["caption"])
            entities.append(image_entity)
        creative_work = {
            "@type": "CreativeWork",
            "@id": project_id,
            "name": clean(proj["name"]),
            "creator": {"@id": CANONICAL_LOCAL_ID},
            "isPartOf": {"@id": webpage_id},
            "image": image_refs,
        }
        if proj.get("description"):
            creative_work["description"] = clean(proj["description"])
        entities.append(creative_work)
        list_items.append({"@type": "ListItem", "position": i, "item": {"@id": project_id}})
    item_list = {
        "@type": "ItemList",
        "@id": list_id,
        "name": "San Diego Hardwood Floor Projects",
        "numberOfItems": len(projects),
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": list_items,
    }
    return [item_list] + entities
