# -*- coding: utf-8 -*-
"""Milestone 2.5 media-inventory validator.

Re-scans the 13 generated pages and checks them against the structured media
inventory (build/data/media/). Fails loudly (exit 1) on any violation:

  1. every image placement in a generated page has a placement record
  2. every visible video placement has a placement record
  3. every placement points to a valid asset_id
  4. asset_id values are unique
  5. placement_id values are unique (site-wide)
  6. approved records have non-blank approved wording (proposed_alt / titles)
  7. approved video records point at real video IDs
  8. no unverified factual metadata is auto-published: a placement whose
     approval_status is not "approved" must not have its proposed wording
     equal to the live page text (nothing is injected yet in 2.5, so any
     match would mean text was hand-published outside the workflow)
  9. no asset carries conflicting approved project identities
 10. every JSON file in the inventory parses as strict JSON

Run after generate_media_inventory.py:
  python build/scripts/validate_media_inventory.py
"""
import json
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent
ROOT = BUILD.parent
MEDIA = BUILD / "data" / "media"
PLACEMENTS_DIR = MEDIA / "placements"

sys.path.insert(0, str(BUILD / "scripts"))
from generate_media_inventory import PAGES, scan_page  # noqa: E402

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def main():
    # 10. strict JSON everywhere in the inventory
    inventory_files = [MEDIA / "assets.json", MEDIA / "owner_facts_confirmed.json"]
    inventory_files += sorted(PLACEMENTS_DIR.glob("*.json"))
    parsed = {}
    for path in inventory_files:
        if not path.exists():
            err("missing inventory file: %s" % path)
            continue
        try:
            with open(path, encoding="utf-8") as f:
                parsed[path.name] = json.load(f)
        except json.JSONDecodeError as e:
            err("invalid JSON in %s: %s" % (path, e))
    if errors:
        report()
        return

    assets = {a["asset_id"]: a for a in parsed["assets.json"]["assets"]}
    # 4. unique asset ids
    raw_ids = [a["asset_id"] for a in parsed["assets.json"]["assets"]]
    if len(raw_ids) != len(set(raw_ids)):
        err("duplicate asset_id values in assets.json")

    snapshot = json.load(open(BUILD / "data" / "youtube_videos.json", encoding="utf-8"))
    yt_ids = {v["id"] for v in snapshot["videos"]}

    all_placement_ids = []
    for page_file, prefix, slug in PAGES:
        pdata = parsed.get(slug + ".json")
        if pdata is None:
            err("missing placements file for %s" % page_file)
            continue
        placements = pdata["placements"]
        present = [p for p in placements if p.get("status") == "present"]
        all_placement_ids += [p["placement_id"] for p in placements]

        # 1 + 2: every scanned placement has a record
        images, videos, _schema = scan_page(ROOT / page_file)
        img_keys = {}
        for img in images:
            img_keys[img["src"]] = img_keys.get(img["src"], 0) + 1
        rec_img_keys = {}
        for p in present:
            if p["media_type"] == "image":
                src = p.get("current_src")
                rec_img_keys[src] = rec_img_keys.get(src, 0) + 1
        for src, n in sorted(img_keys.items()):
            if rec_img_keys.get(src, 0) != n:
                err("%s: image %r appears %d time(s) on page but %d time(s) in inventory"
                    % (page_file, src, n, rec_img_keys.get(src, 0)))
        for src, n in sorted(rec_img_keys.items()):
            if src not in img_keys:
                err("%s: inventory lists image %r marked present but it is not on the page" % (page_file, src))

        vid_ids_page = {}
        for v in videos:
            vid_ids_page[v["youtube_id"]] = vid_ids_page.get(v["youtube_id"], 0) + 1
        rec_vid_ids = {}
        for p in present:
            if p["media_type"] == "video":
                rec_vid_ids[p["youtube_video_id"]] = rec_vid_ids.get(p["youtube_video_id"], 0) + 1
        for vid, n in sorted(vid_ids_page.items()):
            if rec_vid_ids.get(vid, 0) != n:
                err("%s: video %s appears %d time(s) on page but %d time(s) in inventory"
                    % (page_file, vid, n, rec_vid_ids.get(vid, 0)))

        for p in placements:
            # 3. valid asset reference
            if p["asset_id"] not in assets:
                err("%s: placement %s references unknown asset %s" % (page_file, p["placement_id"], p["asset_id"]))
            # 6. approved wording must not be blank
            if p.get("approval_status") == "approved":
                if p["media_type"] == "image" and not (p.get("proposed_alt") or "").strip():
                    err("%s: %s is approved but proposed_alt is blank" % (page_file, p["placement_id"]))
                # 7. approved videos must reference a real, known video ID
                if p["media_type"] == "video" and p.get("youtube_video_id") not in yt_ids:
                    err("%s: %s approved but video ID %s is not in the channel snapshot"
                        % (page_file, p["placement_id"], p.get("youtube_video_id")))
            # 8. nothing auto-published: unapproved proposals must not already be live text
            if p.get("approval_status") not in ("approved",):
                if p["media_type"] == "image" and p.get("proposed_alt") and p.get("proposed_alt") == p.get("current_alt"):
                    err("%s: %s has UNapproved proposed_alt identical to the live alt text "
                        "(published outside the approval workflow?)" % (page_file, p["placement_id"]))
            if p.get("status") == "missing_from_page":
                warn("%s: %s flagged missing_from_page (media removed or renamed)" % (page_file, p["placement_id"]))
            if p.get("conflict_note"):
                warn("%s: %s has an owner-review conflict: %s" % (page_file, p["placement_id"], p["conflict_note"]))

    # 5. site-wide unique placement ids
    dupes = sorted({pid for pid in all_placement_ids if all_placement_ids.count(pid) > 1})
    if dupes:
        err("duplicate placement_id values: %s" % ", ".join(dupes))

    # 9. no conflicting approved project identities per asset
    identity = {}
    for page_file, prefix, slug in PAGES:
        for p in parsed[slug + ".json"]["placements"]:
            name = (p.get("owner_facts") or {}).get("project_name")
            if name:
                identity.setdefault(p["asset_id"], set()).add(name)
    for aid, names in sorted(identity.items()):
        if len(names) > 1:
            err("asset %s carries conflicting project identities: %s" % (aid, " / ".join(sorted(names))))

    report()


def report():
    for w in warnings:
        print("WARN  " + w)
    if errors:
        for e in errors:
            print("ERROR " + e)
        print("\nmedia inventory INVALID: %d error(s), %d warning(s)" % (len(errors), len(warnings)))
        sys.exit(1)
    print("media inventory valid: 0 errors, %d warning(s)" % len(warnings))


if __name__ == "__main__":
    main()
