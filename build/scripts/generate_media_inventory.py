# -*- coding: utf-8 -*-
"""Milestone 2.5 structured media-fact inventory generator.

Scans the 13 generated root pages plus the generator's own structured data
(build/data/youtube_videos.json) and builds/updates:

  build/data/media/assets.json                 one record per unique image/video asset
  build/data/media/placements/<page>.json      one record per placement of an asset on a page
  docs/media-review/<page>.md                  human-readable owner-review file per page
  docs/media-review/index.html                 static, read-only review index with thumbnails

Rules (binding - see docs/PROJECT_OPERATING_MANUAL.md sections 3, 16-19):
  * Python standard library only. No network access. Deterministic output.
  * Owner-confirmed facts come ONLY from build/data/media/owner_facts_confirmed.json
    and from owner_facts/proposed_*/approval_status fields already present in the
    placement files. They are preserved on every regeneration and are never
    overwritten with text extracted from pages.
  * Nothing here infers species, location, stage, or finish. Unconfirmed records
    are marked "needs_owner_review".
  * current_* fields always reflect the latest page scan; placements that vanish
    from a page are kept with status "missing_from_page" (flagged, not deleted).

Run:  python build/scripts/generate_media_inventory.py
Then: python build/scripts/validate_media_inventory.py
"""
import json
import re
import html as htmllib
from html.parser import HTMLParser
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent          # -> build/
ROOT = BUILD.parent                                     # -> repo root
MEDIA = BUILD / "data" / "media"
PLACEMENTS_DIR = MEDIA / "placements"
REVIEW_DIR = ROOT / "docs" / "media-review"

# Fixed inventory date: bump manually on meaningful re-inventories so that
# re-running the script never introduces nondeterministic output.
INVENTORY_DATE = "2026-07-18"

# (page html file at repo root, placement-ID prefix, placements/<slug>.json)
PAGES = [
    ("index.html", "HOME", "index"),
    ("deep-cleaning-hardwood-floors-san-diego.html", "DEEP", "deep-cleaning-hardwood-floors-san-diego"),
    ("recent_project_photo_gallery_1.html", "G1", "recent_project_photo_gallery_1"),
    ("recent_project_photo_gallery_2.html", "G2", "recent_project_photo_gallery_2"),
    ("recent_project_photo_gallery_3.html", "G3", "recent_project_photo_gallery_3"),
    ("recent_project_photo_gallery_4.html", "G4", "recent_project_photo_gallery_4"),
    ("recent_project_gallery_5.html", "G5", "recent_project_gallery_5"),
    ("solid_wood_floor_photo_gallery.html", "SOLID", "solid_wood_floor_photo_gallery"),
    ("videos_of_refinishing_process.html", "VIDEOS", "videos_of_refinishing_process"),
    ("about_us.html", "ABOUT", "about_us"),
    ("blog.html", "BLOG", "blog"),
    ("contact_us.html", "CONTACT", "contact_us"),
    ("floor-assessments-inspections.html", "ASSESS", "floor-assessments-inspections"),
]

OWNER_FACT_FIELDS = [
    "project_name", "property_location", "city_or_neighborhood", "floor_species",
    "floor_construction", "finish_type", "original_condition", "damage_or_problem",
    "stage_shown", "work_performed", "stain_or_color", "final_finish",
    "equipment_or_process", "before_or_after", "limitations", "additional_notes",
]

VOID_TAGS = {"img", "br", "hr", "meta", "link", "input", "source", "wbr", "base", "col", "area", "track", "embed"}


def slugify(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def image_asset_id(filename):
    return "img-" + slugify(filename)


def video_asset_id(youtube_id):
    return "vid-" + youtube_id


def clean_ws(s):
    return re.sub(r"\s+", " ", s or "").strip()


class PageScanner(HTMLParser):
    """Collects every static <img> (and its context) from a generated page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []            # open (tag, attrs) pairs
        self.in_main = False
        self.current_heading = None
        self._heading_tag = None
        self._heading_buf = []
        self._figcaption_depth = 0
        self._figcaption_buf = []
        self._figure_imgs = []     # imgs collected inside the current <figure>
        self._in_figure = 0
        self.images = []           # ordered records

    def ancestor_href(self):
        for tag, attrs in reversed(self.stack):
            if tag == "a" and attrs.get("href"):
                return attrs.get("href")
        return None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.in_main = True
        if tag in ("h1", "h2", "h3") and self.in_main:
            self._heading_tag = tag
            self._heading_buf = []
        if tag == "figure":
            self._in_figure += 1
            self._figure_imgs = []
        if tag == "figcaption":
            self._figcaption_depth += 1
            self._figcaption_buf = []
        if tag == "img":
            src = a.get("src") or ""
            brand = a.get("data-brand-src") or ""
            if not src and not brand:
                return  # JS placeholder (e.g. the lightbox's #sdhLightboxImg), not a media placement
            rec = {
                "src": src or brand,
                "is_brand_asset": bool(brand and not src),
                "alt": a.get("alt", ""),
                "class": a.get("class", ""),
                "link_href": self.ancestor_href(),
                "region": "main" if self.in_main else "chrome",
                "heading": self.current_heading if self.in_main else None,
                "caption": None,
                "width": a.get("width"),
                "height": a.get("height"),
            }
            self.images.append(rec)
            if self._in_figure:
                self._figure_imgs.append(rec)
            return
        if tag not in VOID_TAGS:
            self.stack.append((tag, a))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if tag == "main":
            self.in_main = False
        if tag == self._heading_tag:
            self.current_heading = clean_ws("".join(self._heading_buf))
            self._heading_tag = None
        if tag == "figcaption" and self._figcaption_depth:
            self._figcaption_depth -= 1
            caption = clean_ws("".join(self._figcaption_buf))
            for rec in self._figure_imgs:
                if rec["caption"] is None:
                    rec["caption"] = caption
        if tag == "figure" and self._in_figure:
            self._in_figure -= 1
            self._figure_imgs = []

    def handle_data(self, data):
        if self._heading_tag is not None:
            self._heading_buf.append(data)
        if self._figcaption_depth:
            self._figcaption_buf.append(data)


def scan_page(path):
    doc = path.read_text(encoding="utf-8")
    scanner = PageScanner()
    scanner.feed(doc)

    # ---- video placements ----
    videos = []
    # visible video cards (videos page): one .vid-thumb button per card
    for m in re.finditer(r'<button type="button" class="vid-thumb" data-yt="([^"]+)" data-vtitle="([^"]*)"', doc):
        videos.append({"youtube_id": m.group(1), "visible_title": htmllib.unescape(m.group(2)), "kind": "video_card"})
    # hero/inline iframe embeds built by page scripts
    for m in re.finditer(r'var YT_ID = "([A-Za-z0-9_-]{6,})"', doc):
        videos.append({"youtube_id": m.group(1), "visible_title": None, "kind": "inline_embed"})

    # ---- JSON-LD VideoObject entities (schema cross-check) ----
    schema_video_ids = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', doc, re.DOTALL):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue  # validator reports strict-JSON failures separately
        nodes = []
        def walk(x):
            if isinstance(x, dict):
                nodes.append(x)
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(data)
        for n in nodes:
            if n.get("@type") == "VideoObject":
                url = n.get("embedUrl") or n.get("contentUrl") or ""
                idm = re.search(r'(?:embed/|watch\?v=)([A-Za-z0-9_-]{6,})', url)
                schema_video_ids.append({
                    "youtube_id": idm.group(1) if idm else None,
                    "name": n.get("name"),
                    "uploadDate": n.get("uploadDate"),
                    "duration": n.get("duration"),
                })
    return scanner.images, videos, schema_video_ids


def load_json(path, default):
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")


def blank_owner_facts():
    return {k: None for k in OWNER_FACT_FIELDS}


def main():
    snapshot = load_json(BUILD / "data" / "youtube_videos.json", {"videos": [], "channel_url": None})
    yt_by_id = {v["id"]: v for v in snapshot["videos"]}
    confirmed = load_json(MEDIA / "owner_facts_confirmed.json", {"confirmed_assets": {}, "known_conflicts": {}})
    confirmed_assets = confirmed.get("confirmed_assets", {})
    known_conflicts = confirmed.get("known_conflicts", {})

    # video snapshot quality flags (duplicate titles etc.)
    title_count = {}
    for v in snapshot["videos"]:
        title_count[v["title"]] = title_count.get(v["title"], 0) + 1

    def video_flags(v):
        flags = []
        if title_count.get(v["title"], 0) > 1:
            flags.append("duplicate_title_on_channel")
        if re.match(r"^\s*title\s*:", v["title"], re.IGNORECASE):
            flags.append("title_begins_with_Title:")
        if "sold cherry" in v["title"].lower():
            flags.append("possible_typo_Sold_Cherry")
        if not v.get("duration_iso8601"):
            flags.append("missing_duration")
        if not v.get("publish_date"):
            flags.append("missing_upload_date")
        return flags

    assets = {}          # asset_id -> record
    per_page_placements = {}

    def ensure_image_asset(src, is_brand):
        filename = src.lstrip("/")
        aid = image_asset_id(filename)
        if aid not in assets:
            if is_brand:
                source_url = "/" + filename  # committed repo asset served from the deploy origin
            else:
                source_url = "https://www.sdhardwoods.com/" + filename.replace(" ", "%20")
            assets[aid] = {
                "asset_id": aid,
                "media_type": "image",
                "filename": filename,
                "source_url": source_url,
                "local_source_path": ("assets/branding/web/" + Path(filename).name) if is_brand else None,
                "full_size_url": source_url,
                "thumbnail_url": source_url,
                "width": None,
                "height": None,
                "duplicate_placements": [],
                "verification_status": ("owner_confirmed_project_identity"
                                        if Path(filename).name in confirmed_assets else "needs_owner_review"),
                "do_not_infer": True,
                "conflict_note": known_conflicts.get(Path(filename).name),
            }
        return aid

    def ensure_video_asset(youtube_id):
        aid = video_asset_id(youtube_id)
        if aid not in assets:
            v = yt_by_id.get(youtube_id)
            assets[aid] = {
                "asset_id": aid,
                "media_type": "video",
                "youtube_video_id": youtube_id,
                "filename": None,
                "source_url": (v or {}).get("watch_url") or ("https://www.youtube.com/watch?v=" + youtube_id),
                "title": (v or {}).get("title"),
                "description": (v or {}).get("description"),
                "site_description": (v or {}).get("site_description"),
                "upload_date": (v or {}).get("publish_date"),
                "duration_iso8601": (v or {}).get("duration_iso8601"),
                "thumbnail_url": (v or {}).get("thumbnail_url") or ("https://i.ytimg.com/vi/%s/hqdefault.jpg" % youtube_id),
                "content_url": (v or {}).get("watch_url"),
                "embed_url": (v or {}).get("embed_url") or ("https://www.youtube-nocookie.com/embed/" + youtube_id),
                "in_channel_snapshot": youtube_id in yt_by_id,
                "duplicate_placements": [],
                "metadata_flags": video_flags(v) if v else ["not_in_channel_snapshot"],
                "verification_status": "needs_owner_review",
                "do_not_infer": True,
                "conflict_note": None,
            }
        return aid

    for page_file, prefix, slug in PAGES:
        images, videos, schema_videos = scan_page(ROOT / page_file)
        existing = load_json(PLACEMENTS_DIR / (slug + ".json"), {"placements": []})
        old_by_key = {}
        for p in existing.get("placements", []):
            old_by_key[(p.get("media_type"), p.get("scan_key"))] = p
        used_old_keys = set()

        placements = []
        img_seq = 0
        vid_seq = 0
        occurrence = {}

        def merge_old(new_rec, old_rec):
            """current_* comes from the fresh scan; owner-entered fields are preserved."""
            if not old_rec:
                return new_rec
            for field in ("placement_id", "owner_facts", "proposed_alt", "proposed_caption",
                          "proposed_heading", "approval_status", "notes", "owner_confirmed_summary"):
                if field in old_rec and old_rec[field] not in (None, "", {}):
                    if field == "owner_facts":
                        merged = blank_owner_facts()
                        merged.update({k: v for k, v in old_rec["owner_facts"].items() if v is not None})
                        # seed-file facts still win over stale placement-file copies
                        merged.update({k: v for k, v in new_rec["owner_facts"].items() if v is not None})
                        new_rec["owner_facts"] = merged
                    else:
                        new_rec[field] = old_rec[field]
            return new_rec

        for img in images:
            filename = img["src"].lstrip("/")
            base = Path(filename).name
            aid = ensure_image_asset(img["src"], img["is_brand_asset"])
            occ_key = ("img", img["src"])
            occurrence[occ_key] = occurrence.get(occ_key, 0) + 1
            scan_key = "%s#%d" % (img["src"], occurrence[occ_key])
            img_seq += 1
            seed = confirmed_assets.get(base)
            owner_facts = blank_owner_facts()
            verification = "needs_owner_review"
            seed_notes = None
            if seed:
                owner_facts.update({k: v for k, v in seed["owner_facts"].items() if v is not None})
                verification = seed["verification_status"]
                seed_notes = seed.get("notes")
            rec = {
                "placement_id": "%s-IMG-%03d" % (prefix, img_seq),
                "asset_id": aid,
                "media_type": "image",
                "scan_key": scan_key,
                "current_src": img["src"],
                "page_file": page_file,
                "project_or_section": img["heading"] if img["region"] == "main" else "site chrome (header/footer/drawer)",
                "position_order": img_seq,
                "is_site_chrome": img["region"] == "chrome",
                "current_alt": img["alt"],
                "current_caption": img["caption"],
                "current_heading": img["heading"],
                "current_link_destination": img["link_href"],
                "current_lightbox_source": img["link_href"] if (img["link_href"] or "").lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")) else None,
                "visible_context": "chrome" if img["region"] == "chrome" else "page content",
                "owner_facts": owner_facts,
                "proposed_alt": None,
                "proposed_caption": None,
                "proposed_heading": None,
                "approval_status": "not_submitted",
                "seo_context": None,
                "verification_status": verification,
                "conflict_note": known_conflicts.get(base),
                "notes": seed_notes,
                "status": "present",
                "last_verified": INVENTORY_DATE,
            }
            rec = merge_old(rec, old_by_key.get(("image", scan_key)))
            used_old_keys.add(("image", scan_key))
            placements.append(rec)

        schema_ids_here = [s["youtube_id"] for s in schema_videos if s["youtube_id"]]
        for vid in videos:
            youtube_id = vid["youtube_id"]
            aid = ensure_video_asset(youtube_id)
            occ_key = ("vid", youtube_id)
            occurrence[occ_key] = occurrence.get(occ_key, 0) + 1
            scan_key = "%s#%d" % (youtube_id, occurrence[occ_key])
            vid_seq += 1
            v = yt_by_id.get(youtube_id)
            rec = {
                "placement_id": "%s-VID-%03d" % (prefix, vid_seq),
                "asset_id": aid,
                "media_type": "video",
                "scan_key": scan_key,
                "page_file": page_file,
                "youtube_video_id": youtube_id,
                "placement_kind": vid["kind"],
                "position_order": vid_seq,
                "current_visible_title": vid["visible_title"] or (v or {}).get("title"),
                "current_description": (v or {}).get("site_description") or (v or {}).get("description"),
                "upload_date": (v or {}).get("publish_date"),
                "duration_iso8601": (v or {}).get("duration_iso8601"),
                "thumbnail_url": (v or {}).get("thumbnail_url"),
                "content_url": (v or {}).get("watch_url"),
                "embed_url": (v or {}).get("embed_url"),
                "in_page_schema": youtube_id in schema_ids_here,
                "metadata_flags": (video_flags(v) if v else ["not_in_channel_snapshot"]),
                "owner_facts": blank_owner_facts(),
                "owner_confirmed_summary": None,
                "proposed_caption": None,
                "approval_status": "not_submitted",
                "verification_status": "needs_owner_review",
                "notes": None,
                "status": "present",
                "last_verified": INVENTORY_DATE,
            }
            rec = merge_old(rec, old_by_key.get(("video", scan_key)))
            used_old_keys.add(("video", scan_key))
            placements.append(rec)

        # keep (flag) records whose media disappeared from the page
        for key, old_rec in sorted(old_by_key.items(), key=lambda kv: str(kv[0])):
            if key not in used_old_keys:
                old_rec = dict(old_rec)
                old_rec["status"] = "missing_from_page"
                placements.append(old_rec)

        # schema-only videos: VideoObject with no visible placement (flag)
        visible_ids = {v["youtube_id"] for v in videos}
        schema_only = sorted({s for s in schema_ids_here if s not in visible_ids})

        per_page_placements[slug] = {
            "_comment": "Generated by build/scripts/generate_media_inventory.py - regenerate rather than hand-editing current_* fields. owner_facts / proposed_* / approval_status fields ARE meant to be edited (by agreement with the owner) and survive regeneration.",
            "page_file": page_file,
            "placement_id_prefix": prefix,
            "generated": INVENTORY_DATE,
            "image_placements": sum(1 for p in placements if p["media_type"] == "image"),
            "video_placements": sum(1 for p in placements if p["media_type"] == "video"),
            "schema_only_video_ids": schema_only,
            "placements": placements,
        }

    # duplicate-placement references on assets
    for slug, data in per_page_placements.items():
        for p in data["placements"]:
            if p.get("status") == "present" and p["asset_id"] in assets:
                assets[p["asset_id"]]["duplicate_placements"].append(p["placement_id"])
    for a in assets.values():
        a["duplicate_placements"].sort()
        a["is_duplicate"] = len(a["duplicate_placements"]) > 1

    assets_sorted = [assets[k] for k in sorted(assets)]
    save_json(MEDIA / "assets.json", {
        "_comment": "Generated by build/scripts/generate_media_inventory.py. One record per unique media asset; per-page placements live in build/data/media/placements/. Owner-confirmed facts enter via owner_facts_confirmed.json only.",
        "generated": INVENTORY_DATE,
        "image_assets": sum(1 for a in assets_sorted if a["media_type"] == "image"),
        "video_assets": sum(1 for a in assets_sorted if a["media_type"] == "video"),
        "channel_url": snapshot.get("channel_url"),
        "assets": assets_sorted,
    })
    for slug, data in per_page_placements.items():
        save_json(PLACEMENTS_DIR / (slug + ".json"), data)

    write_review_docs(assets, per_page_placements)

    total_p = sum(len(d["placements"]) for d in per_page_placements.values())
    print("assets: %d images, %d videos" % (
        sum(1 for a in assets.values() if a["media_type"] == "image"),
        sum(1 for a in assets.values() if a["media_type"] == "video")))
    print("placements: %d across %d pages" % (total_p, len(per_page_placements)))


# ---------------------------------------------------------------- review docs

def esc(s):
    return htmllib.escape(str(s if s is not None else ""), quote=True)


def write_review_docs(assets, per_page_placements):
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    for page_file, prefix, slug in PAGES:
        data = per_page_placements[slug]
        lines = []
        lines.append("# Media review — `%s`" % page_file)
        lines.append("")
        lines.append("_Generated %s by `build/scripts/generate_media_inventory.py` — do not hand-edit; "
                     "record owner facts in `build/data/media/placements/%s.json` (or tell the assistant "
                     "the placement ID and the facts)._" % (INVENTORY_DATE, slug))
        lines.append("")
        lines.append("%d image placement(s), %d video placement(s)."
                     % (data["image_placements"], data["video_placements"]))
        lines.append("")
        chrome = [p for p in data["placements"] if p.get("is_site_chrome")]
        content = [p for p in data["placements"] if not p.get("is_site_chrome")]
        if chrome:
            lines.append("Site-chrome branding images on this page (same on every page; reviewed once, "
                         "not per page): %s." % ", ".join("`%s` (%s)" % (p["placement_id"], assets[p["asset_id"]]["filename"]) for p in chrome))
            lines.append("")
        for p in content:
            a = assets.get(p["asset_id"], {})
            lines.append("---")
            lines.append("")
            lines.append("### %s" % p["placement_id"])
            lines.append("")
            if p["media_type"] == "image":
                lines.append("| | |")
                lines.append("|---|---|")
                lines.append("| Image | [%s](%s) |" % (a.get("filename"), a.get("full_size_url")))
                lines.append("| Page position | %s |" % (p.get("project_or_section") or "—"))
                lines.append("| Current heading | %s |" % (p.get("current_heading") or "—"))
                lines.append("| Current caption | %s |" % (p.get("current_caption") or "—"))
                lines.append("| Current alt text | %s |" % (p.get("current_alt") or "*(empty)*"))
                lines.append("| Full-size link | %s |" % (p.get("current_link_destination") or "—"))
                lines.append("| Verification | **%s** |" % p.get("verification_status"))
                lines.append("| Status | %s |" % p.get("status"))
                if a.get("is_duplicate"):
                    lines.append("| Also used at | %s |" % ", ".join(x for x in a["duplicate_placements"] if x != p["placement_id"]))
                if p.get("conflict_note"):
                    lines.append("| ⚠ Conflict | %s |" % p["conflict_note"])
                facts = {k: v for k, v in (p.get("owner_facts") or {}).items() if v}
                if facts:
                    lines.append("")
                    lines.append("Confirmed owner facts: " + "; ".join("**%s**: %s" % (k, v) for k, v in sorted(facts.items())))
                missing = [k for k, v in (p.get("owner_facts") or {}).items() if not v]
                lines.append("")
                lines.append("Owner facts still needed: %s." % (", ".join(missing) if missing else "none"))
            else:
                lines.append("| | |")
                lines.append("|---|---|")
                lines.append("| Video | [%s](%s) |" % (p.get("youtube_video_id"), a.get("source_url")))
                lines.append("| Visible title | %s |" % (p.get("current_visible_title") or "—"))
                lines.append("| Upload date / duration | %s / %s |" % (p.get("upload_date") or "?", p.get("duration_iso8601") or "?"))
                lines.append("| In page schema | %s |" % ("yes" if p.get("in_page_schema") else "no"))
                lines.append("| Verification | **%s** |" % p.get("verification_status"))
                if p.get("metadata_flags"):
                    lines.append("| ⚠ Metadata flags | %s |" % ", ".join(p["metadata_flags"]))
            lines.append("")
        if data.get("schema_only_video_ids"):
            lines.append("---")
            lines.append("")
            lines.append("⚠ VideoObject schema entries with no visible video placement on this page: %s"
                         % ", ".join(data["schema_only_video_ids"]))
            lines.append("")
        with open(REVIEW_DIR / (slug + ".md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines))

    # ------- static, read-only HTML index -------
    rows = []
    for page_file, prefix, slug in PAGES:
        data = per_page_placements[slug]
        content = [p for p in data["placements"] if not p.get("is_site_chrome")]
        cards = []
        for p in content:
            a = assets.get(p["asset_id"], {})
            if p["media_type"] == "image":
                thumb = a.get("thumbnail_url") or ""
                label = a.get("filename") or ""
            else:
                thumb = a.get("thumbnail_url") or ""
                label = "YouTube " + (p.get("youtube_video_id") or "")
            flags = []
            if p.get("conflict_note"):
                flags.append("CONFLICT")
            if p.get("metadata_flags"):
                flags.extend(p["metadata_flags"])
            if p.get("status") != "present":
                flags.append(p.get("status"))
            cards.append(
                '<div class="c"><a href="%s" target="_blank" rel="noopener"><img loading="lazy" src="%s" alt=""></a>'
                '<div class="m"><b>%s</b><br><span class="f">%s</span><br>'
                '<span class="s">%s</span>%s<br><span class="t">%s</span></div></div>'
                % (esc(a.get("source_url") or a.get("full_size_url") or "#"), esc(thumb),
                   esc(p["placement_id"]), esc(label),
                   esc(p.get("verification_status")),
                   (' <span class="w">%s</span>' % esc("; ".join(flags))) if flags else "",
                   esc(clean_ws(p.get("current_alt") or p.get("current_visible_title") or ""))))
        rows.append('<section><h2 id="%s">%s <small>(%d content placements)</small></h2><div class="grid">%s</div></section>'
                    % (esc(slug), esc(page_file), len(content), "".join(cards)))

    toc = " &bull; ".join('<a href="#%s">%s</a>' % (esc(slug), esc(prefix)) for _, prefix, slug in PAGES)
    html_doc = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>San Diego Hardwoods — media review index (local, read-only)</title>
<style>
body{font-family:Segoe UI,Arial,sans-serif;margin:24px;background:#faf7f2;color:#2b2115;}
h1{font-size:22px} h2{margin-top:38px;border-bottom:2px solid #c9b58f;padding-bottom:6px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;}
.c{background:#fff;border:1px solid #ddd0bb;border-radius:8px;overflow:hidden;}
.c img{width:100%%;height:150px;object-fit:cover;display:block;background:#eee;}
.m{padding:8px 10px;font-size:12.5px;line-height:1.45;}
.f{color:#6b5b41;} .s{color:#146414;font-weight:600;} .w{color:#a31414;font-weight:700;}
.t{color:#555;font-style:italic;}
.note{background:#fdf3dd;border:1px solid #e3cf9b;border-radius:8px;padding:10px 14px;max-width:900px;}
</style></head><body>
<h1>San Diego Hardwoods — media review index</h1>
<p class="note">Local, read-only review page generated %s by <code>build/scripts/generate_media_inventory.py</code>.
It is NOT part of the website and must never be deployed. Thumbnails load from the live image/YouTube hosts, so
open it with an internet connection. Identify any photo or video by its bold placement ID (e.g. HOME-IMG-001)
when dictating facts. Green status = owner-confirmed; red = flagged for review.</p>
<p>%s</p>
%s
</body></html>
""" % (esc(INVENTORY_DATE), toc, "\n".join(rows))
    with open(REVIEW_DIR / "index.html", "w", encoding="utf-8", newline="\n") as f:
        f.write(html_doc)


if __name__ == "__main__":
    main()
